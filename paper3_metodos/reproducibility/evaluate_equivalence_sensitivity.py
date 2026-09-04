#!/usr/bin/env python3
"""Sensitivity of Paper 3 agreement to comparison equivalence rules.

The script requires the authorized restricted baseline and closed validation
workbook, but writes aggregate outputs only. It never exports identifiers or
row-level values.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


N_BY_YEAR = {1910: 155, 1911: 182, 1912: 183, 1913: 246, 1914: 317, 1915: 355}
MONTHS = {
    "ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12,
}
NATIONALITY_EQUIVALENCES = {
    "arg": "argentina", "argent": "argentina", "argentino": "argentina",
    "argentina": "argentina", "esp": "espana", "espanol": "espana",
    "espanola": "espana", "espana": "espana", "ital": "italia",
    "italiano": "italia", "italiana": "italia", "italo": "italia",
    "italia": "italia", "frances": "francia", "francesa": "francia",
    "francia": "francia", "oriental": "uruguay", "uruguayo": "uruguay",
    "uruguaya": "uruguay", "uruguay": "uruguay", "paraguay": "paraguay",
    "paraguayo": "paraguay", "paraguaya": "paraguay", "ruso": "rusia",
    "rusa": "rusia", "rusia": "rusia", "boliviano": "bolivia",
    "boliviana": "bolivia", "bolivia": "bolivia", "brasileno": "brasil",
    "brasilena": "brasil", "brasil": "brasil", "aleman": "alemania",
    "alemana": "alemania", "alemania": "alemania", "suizo": "suiza",
    "suiza": "suiza", "ingles": "inglaterra", "inglesa": "inglaterra",
    "inglaterra": "inglaterra",
}
FIELD_MAP = {
    "nombre_alumno": "nombre_alumno",
    "edad": "edad",
    "domicilio": "domicilio_raw",
    "curso": "curso_ingreso_raw",
    "padre_tutor": "padre_tutor",
    "observaciones": "observaciones",
    "nacionalidad_alumno": "nacionalidad_alumno_raw",
    "procedencia": "procedencia",
    "profesion_tutor": "profesion_tutor",
    "nacionalidad_tutor": "nacionalidad_tutor_raw",
}
CONTEXTUAL_FIELDS = {
    "nacionalidad_alumno", "procedencia", "profesion_tutor", "nacionalidad_tutor"
}


def text(value: object) -> str:
    return "" if pd.isna(value) else str(value).strip()


def unaccent(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def canon_strict(value: object) -> str:
    return text(value)


def canon_case_space(value: object) -> str:
    return re.sub(r"\s+", " ", text(value).lower()).strip()


def canon_formal(value: object) -> str:
    normalized = unaccent(text(value).lower()).replace("º", "o").replace("°", "o")
    normalized = re.sub(r"[^\w]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def canon_age(value: object) -> str:
    raw = text(value)
    if not raw:
        return ""
    try:
        number = float(raw)
        return str(int(round(number))) if np.isclose(number, round(number)) else str(number)
    except (TypeError, ValueError):
        return canon_formal(value)


def canon_course(value: object) -> str:
    normalized = canon_formal(value)
    match = re.search(r"\b([1-9])(?:o|ro|do|to|er)?\b", normalized)
    number = match.group(1) if match else ""
    orientation = "letras" if "letra" in normalized else (
        "ciencias" if "cienc" in normalized else ""
    )
    return f"{number}|{orientation}" if number else normalized


def canon_nationality(value: object) -> str:
    normalized = canon_formal(value)
    if not normalized:
        return ""
    for source, target in NATIONALITY_EQUIVALENCES.items():
        if normalized == source or normalized.startswith(source + " "):
            return target
    return normalized


def is_idem(value: object) -> bool:
    normalized = text(value).upper()
    return bool(normalized) and ("IDEM" in normalized or normalized in {'"', "''"})


def effective_review_value(frame: pd.DataFrame, field: str) -> pd.Series:
    literal = frame[f"rev_{field}_literal"].map(text)
    resolved = frame[f"rev_{field}_resuelta"].map(text)
    return pd.Series(
        np.where(literal.map(is_idem), resolved, literal),
        index=frame.index,
        dtype="string",
    )


def comparison_matrix(
    frame: pd.DataFrame,
    general_comparator,
    nationality_comparator,
    course_comparator,
) -> pd.DataFrame:
    output = pd.DataFrame(index=frame.index)
    baseline_date = pd.to_datetime(frame["fecha_reconstruida"], errors="coerce")
    review_month = frame["rev_mes_resuelto"].astype(str).str.strip().str.upper().map(MONTHS)
    review_day = pd.to_numeric(frame["rev_dia_resuelto"], errors="coerce")
    output["fecha"] = review_month.eq(baseline_date.dt.month) & review_day.eq(baseline_date.dt.day)

    for field, baseline_column in FIELD_MAP.items():
        review = (
            effective_review_value(frame, field)
            if field in CONTEXTUAL_FIELDS
            else frame[f"rev_{field}"].map(text)
        )
        baseline = frame[baseline_column].map(text)
        if field == "edad":
            comparator = canon_age
        elif field == "curso":
            comparator = course_comparator
        elif field.startswith("nacionalidad"):
            comparator = nationality_comparator
        else:
            comparator = general_comparator
        output[field] = review.map(comparator).eq(baseline.map(comparator))
    return output


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit(
            "Uso: paper_methods_equivalence_sensitivity.py "
            "BASELINE.csv PLANILLA_CERRADA.xlsm RESUMEN.csv POR_CAMPO.csv"
        )
    baseline_path, workbook_path, summary_path, field_path = map(Path, sys.argv[1:])

    review = pd.read_excel(workbook_path, sheet_name="validacion_independiente", dtype=object)
    baseline = pd.read_csv(baseline_path, dtype=object).set_index("id_registro", drop=False)
    review["id_registro"] = review["id_registro"].astype(str)
    frame = review.join(baseline, on="id_registro", rsuffix="_pipeline")
    frame["_year"] = pd.to_numeric(frame["anio_libro"], errors="coerce").astype("Int64")

    if len(frame) != 180 or frame["id_registro"].nunique() != 180:
        raise RuntimeError("La auditoría cerrada no contiene los 180 registros únicos esperados")

    scenarios = [
        ("estricto_resuelto_tipado", canon_strict, canon_strict, canon_strict),
        ("minusculas_y_espacios", canon_case_space, canon_case_space, canon_case_space),
        ("normalizacion_formal", canon_formal, canon_formal, canon_formal),
        ("principal_sin_recodificacion_nacionalidad", canon_formal, canon_formal, canon_course),
        ("principal_sin_canonizacion_curso", canon_formal, canon_nationality, canon_formal),
        ("principal_reportado", canon_formal, canon_nationality, canon_course),
    ]

    matrices = {}
    for name, general, nationality, course in scenarios:
        matrices[name] = comparison_matrix(frame, general, nationality, course)

    primary_matches = int(matrices["principal_reportado"].to_numpy().sum())
    if primary_matches != 1867:
        raise RuntimeError(
            f"La especificación principal produjo {primary_matches} coincidencias; se esperaban 1867"
        )

    summary_rows = []
    field_rows = []
    for name, _, _, _ in scenarios:
        matrix = matrices[name]
        matches = int(matrix.to_numpy().sum())
        comparisons = int(matrix.size)
        weighted = sum(
            matrix.loc[frame.index[frame["_year"].eq(year)]].to_numpy().mean() * stratum_size
            for year, stratum_size in N_BY_YEAR.items()
        ) / sum(N_BY_YEAR.values())
        summary_rows.append({
            "escenario": name,
            "coincidencias": matches,
            "discrepancias": comparisons - matches,
            "comparaciones": comparisons,
            "concordancia_pct": round(100 * matches / comparisons, 4),
            "concordancia_ponderada_pct": round(100 * weighted, 4),
            "diferencia_coincidencias_vs_principal": matches - primary_matches,
            "diferencia_pp_vs_principal": round(100 * (matches - primary_matches) / comparisons, 4),
        })
        for field in matrix.columns:
            field_matches = int(matrix[field].sum())
            field_rows.append({
                "escenario": name,
                "campo": field,
                "coincidencias": field_matches,
                "discrepancias": len(matrix) - field_matches,
                "comparaciones": len(matrix),
                "concordancia_pct": round(100 * field_matches / len(matrix), 4),
            })

    pd.DataFrame(summary_rows).to_csv(summary_path, index=False, encoding="utf-8")
    pd.DataFrame(field_rows).to_csv(field_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()

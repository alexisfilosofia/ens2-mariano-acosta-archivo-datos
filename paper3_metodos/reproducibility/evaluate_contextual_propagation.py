#!/usr/bin/env python3
"""Regenerate the aggregate contextual-propagation audit without row output.

The script inventories adjacent equal values within the same source workbook
and folio for four contextual fields. It then classifies only the candidate
sites that belong to the assisted-audit sheet. No record identifier, value,
folio locator, or row-level classification is written or printed.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd


FIELDS = {
    "nacionalidad_alumno": "nacionalidad_alumno_raw",
    "procedencia": "procedencia",
    "profesion_tutor": "profesion_tutor",
    "nacionalidad_tutor": "nacionalidad_tutor_raw",
}

REVIEW_COLUMNS = {
    "nacionalidad_alumno": (
        "rev_nacionalidad_alumno_literal",
        "rev_nacionalidad_alumno_resuelta",
    ),
    "procedencia": ("rev_procedencia_literal", "rev_procedencia_resuelta"),
    "profesion_tutor": (
        "rev_profesion_tutor_literal",
        "rev_profesion_tutor_resuelta",
    ),
    "nacionalidad_tutor": (
        "rev_nacionalidad_tutor_literal",
        "rev_nacionalidad_tutor_resuelta",
    ),
}

NATIONALITIES = {
    "arg": "argentina",
    "argent": "argentina",
    "argentino": "argentina",
    "argentina": "argentina",
    "esp": "espana",
    "espanol": "espana",
    "espanola": "espana",
    "espana": "espana",
    "ital": "italia",
    "italiano": "italia",
    "italiana": "italia",
    "italo": "italia",
    "italia": "italia",
    "frances": "francia",
    "francesa": "francia",
    "francia": "francia",
    "oriental": "uruguay",
    "uruguayo": "uruguay",
    "uruguaya": "uruguay",
    "uruguay": "uruguay",
    "paraguay": "paraguay",
    "paraguayo": "paraguay",
    "paraguaya": "paraguay",
    "ruso": "rusia",
    "rusa": "rusia",
    "rusia": "rusia",
    "boliviano": "bolivia",
    "boliviana": "bolivia",
    "bolivia": "bolivia",
    "brasileno": "brasil",
    "brasilena": "brasil",
    "brasil": "brasil",
    "aleman": "alemania",
    "alemana": "alemania",
    "alemania": "alemania",
    "suizo": "suiza",
    "suiza": "suiza",
    "ingles": "inglaterra",
    "inglesa": "inglaterra",
    "inglaterra": "inglaterra",
}


def text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def canonical(value: object) -> str:
    value = text(value).lower().replace("º", "o").replace("°", "o")
    value = "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )
    return re.sub(r"[^\w]+", " ", value).strip()


def equivalent(field: str, baseline_value: object, reviewed_literal: object) -> bool:
    left = canonical(baseline_value)
    right = canonical(reviewed_literal)
    if field in {"nacionalidad_alumno", "nacionalidad_tutor"}:
        left = canonical_nationality(left)
        right = canonical_nationality(right)
    return left == right


def canonical_nationality(value: str) -> str:
    if not value:
        return ""
    for key, canonical_value in NATIONALITIES.items():
        if value == key or value.startswith(key + " "):
            return canonical_value
    return value


def candidate_sites(baseline: pd.DataFrame) -> pd.DataFrame:
    required = {
        "id_registro",
        "archivo_fuente",
        "numero_hoja",
        "fila_fuente_excel",
        *FIELDS.values(),
    }
    missing = sorted(required - set(baseline.columns))
    if missing:
        raise ValueError(f"baseline is missing required columns: {missing}")

    frame = baseline.copy()
    frame["_row"] = pd.to_numeric(frame["fila_fuente_excel"], errors="coerce")
    frame["_folio"] = frame["numero_hoja"].astype("string")
    frame = frame.sort_values(["archivo_fuente", "_folio", "_row"]).reset_index(drop=True)

    parts: list[pd.DataFrame] = []
    grouping = ["archivo_fuente", "_folio"]
    for field, column in FIELDS.items():
        previous = frame.groupby(grouping, dropna=False)[column].shift()
        current = frame[column]
        same = (
            current.notna()
            & previous.notna()
            & current.astype("string").str.strip().eq(
                previous.astype("string").str.strip()
            )
        )
        part = frame.loc[same, ["id_registro", column]].copy()
        part["field"] = field
        part["baseline_value"] = part[column]
        parts.append(part[["id_registro", "field", "baseline_value"]])
    return pd.concat(parts, ignore_index=True)


def classify(candidates: pd.DataFrame, review: pd.DataFrame) -> dict[str, int]:
    if review["id_registro"].astype(str).duplicated().any():
        raise ValueError("assisted-audit sheet contains duplicate id_registro values")
    indexed = review.assign(_id=review["id_registro"].astype(str)).set_index("_id")

    counts = {
        "confirmed_idem": 0,
        "explicit_repetition_matching": 0,
        "explicit_repetition_discrepant": 0,
        "absence": 0,
    }
    reviewed_sites = 0
    for row in candidates.itertuples(index=False):
        record_id = str(row.id_registro)
        if record_id not in indexed.index:
            continue
        reviewed_sites += 1
        literal_column, resolved_column = REVIEW_COLUMNS[row.field]
        reviewed = indexed.loc[record_id]
        literal = text(reviewed.get(literal_column))
        resolved = text(reviewed.get(resolved_column))
        if literal == "[[IDEM]]":
            counts["confirmed_idem"] += 1
        elif not literal and not resolved:
            counts["absence"] += 1
        elif equivalent(row.field, row.baseline_value, literal):
            counts["explicit_repetition_matching"] += 1
        else:
            counts["explicit_repetition_discrepant"] += 1
    counts["observed_contextual_sites"] = reviewed_sites
    return counts


def build_summary(baseline: pd.DataFrame, review: pd.DataFrame) -> pd.DataFrame:
    candidates = candidate_sites(baseline)
    counts = classify(candidates, review)
    explicit = (
        counts["explicit_repetition_matching"]
        + counts["explicit_repetition_discrepant"]
    )
    rows = [
        ("candidate_sites", len(candidates)),
        ("records_with_candidate_sites", candidates["id_registro"].astype(str).nunique()),
        ("observed_contextual_sites", counts["observed_contextual_sites"]),
        ("confirmed_idem", counts["confirmed_idem"]),
        ("explicit_repetition", explicit),
        ("explicit_repetition_matching", counts["explicit_repetition_matching"]),
        ("explicit_repetition_discrepant", counts["explicit_repetition_discrepant"]),
        ("absence", counts["absence"]),
        ("unreviewed_candidate_sites", len(candidates) - counts["observed_contextual_sites"]),
    ]
    return pd.DataFrame(rows, columns=["indicator", "value"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--closed-workbook", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--check-canonical",
        action="store_true",
        help="fail unless the frozen Paper 3 aggregate counts are reproduced",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    baseline = pd.read_csv(args.baseline, dtype=object)
    review = pd.read_excel(
        args.closed_workbook,
        sheet_name="validacion_independiente",
        dtype=object,
    )
    summary = build_summary(baseline, review)
    observed = dict(summary.itertuples(index=False, name=None))
    if args.check_canonical:
        expected = {
            "candidate_sites": 2222,
            "records_with_candidate_sites": 1280,
            "observed_contextual_sites": 293,
            "confirmed_idem": 226,
            "explicit_repetition": 59,
            "explicit_repetition_matching": 54,
            "explicit_repetition_discrepant": 5,
            "absence": 8,
            "unreviewed_candidate_sites": 1929,
        }
        if observed != expected:
            raise AssertionError({"expected": expected, "observed": observed})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    print(json.dumps({"status": "contextual_propagation_verified", "row_level_output": False}))


if __name__ == "__main__":
    main()

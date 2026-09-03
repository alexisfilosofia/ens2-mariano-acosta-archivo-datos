#!/usr/bin/env python3
"""Evalúa el tamiz automático frente a la auditoría humana sin publicar identificadores.

Uso:
    python paper_methods_qa_screening.py BASELINE.csv DISCREPANCIAS.csv SALIDA.csv

La salida contiene únicamente resultados agregados. Los dos insumos permanecen
en el circuito restringido porque contienen datos e identificadores individuales.
"""

from pathlib import Path
import sys

import pandas as pd


SEED = 20260822
N_POR_ANIO = 30


def as_bool(series: pd.Series) -> pd.Series:
    verdaderos = {"1", "true", "t", "yes", "y", "si", "sí"}
    return series.fillna(False).map(lambda x: str(x).strip().lower() in verdaderos)


def division(num: float, den: float) -> float:
    return float(num / den) if den else float("nan")


def metricas(celdas: dict[str, float]) -> dict[str, float]:
    tp, fp, fn, tn = (celdas[k] for k in ("tp", "fp", "fn", "tn"))
    total = tp + fp + fn + tn
    return {
        **celdas,
        "sensibilidad": division(tp, tp + fn),
        "especificidad": division(tn, tn + fp),
        "valor_predictivo_positivo": division(tp, tp + fp),
        "valor_predictivo_negativo": division(tn, tn + fn),
        "tasa_banderas": division(tp + fp, total),
        "tasa_registros_con_discrepancia": division(tp + fn, total),
    }


def main(base_path: str, discrepancias_path: str, salida_path: str) -> None:
    base = pd.read_csv(base_path, low_memory=False)
    discrepancias = pd.read_csv(discrepancias_path, low_memory=False)

    partes = []
    for anio, grupo in base.groupby("anio_libro"):
        partes.append(
            grupo.sample(
                n=min(N_POR_ANIO, len(grupo)),
                random_state=SEED + int(anio),
            )
        )
    muestra = pd.concat(partes, ignore_index=True)

    ids_discrepantes = set(discrepancias["id_registro"].dropna().astype(str))
    muestra["positivo_humano"] = (
        muestra["id_registro"].astype(str).isin(ids_discrepantes)
    )
    muestra["positivo_automatico"] = as_bool(muestra["requiere_revision"])

    automatico = muestra["positivo_automatico"]
    humano = muestra["positivo_humano"]
    mascaras = {
        "tp": automatico & humano,
        "fp": automatico & ~humano,
        "fn": ~automatico & humano,
        "tn": ~automatico & ~humano,
    }
    directas = {k: float(v.sum()) for k, v in mascaras.items()}

    tamanos = base.groupby("anio_libro").size().to_dict()
    muestra["peso"] = muestra["anio_libro"].map(tamanos) / N_POR_ANIO
    ponderadas = {
        k: float(muestra.loc[v, "peso"].sum()) for k, v in mascaras.items()
    }

    filas = [
        {
            "alcance": "muestra_180_no_ponderada",
            **metricas(directas),
            "nota": (
                "Unidad de clasificación: registro; positivo humano = al menos "
                "una discrepancia sustantiva en 11 dimensiones"
            ),
        },
        {
            "alcance": "estimacion_ponderada_composicion_anual",
            **metricas(ponderadas),
            "nota": (
                "Conteos expandidos descriptivos mediante pesos N_anio/30; "
                "no son observaciones enteras"
            ),
        },
    ]
    columnas = [
        "alcance", "tp", "fp", "fn", "tn", "sensibilidad",
        "especificidad", "valor_predictivo_positivo",
        "valor_predictivo_negativo", "tasa_banderas",
        "tasa_registros_con_discrepancia", "nota",
    ]
    pd.DataFrame(filas)[columnas].to_csv(
        Path(salida_path),
        index=False,
        encoding="utf-8",
        float_format="%.6f",
    )


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(
            "Uso: paper_methods_qa_screening.py BASELINE.csv DISCREPANCIAS.csv SALIDA.csv"
        )
    main(*sys.argv[1:])

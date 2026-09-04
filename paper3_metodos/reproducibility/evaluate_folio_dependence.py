#!/usr/bin/env python3
"""Sensitivity of Paper 3 uncertainty estimates to dependence within folios.

The authorized baseline and closed review workbook are required as inputs.
Only aggregate outputs are written; no record identifiers or row-level values
are exported.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from evaluate_equivalence_sensitivity import (
        N_BY_YEAR,
        canon_course,
        canon_formal,
        canon_nationality,
        comparison_matrix,
    )
except ImportError:  # Local development filename used before publication.
    from paper_methods_equivalence_sensitivity import (
        N_BY_YEAR,
        canon_course,
        canon_formal,
        canon_nationality,
        comparison_matrix,
    )


RECORD_BOOTSTRAP_SEED = 20260827
FOLIO_BOOTSTRAP_SEED = 20260904
N_REPLICATES = 5000


def weighted_mean(frame: pd.DataFrame, outcome: str) -> float:
    population_total = sum(N_BY_YEAR.values())
    return sum(
        frame.loc[frame["_year"].eq(year), outcome].mean() * stratum_size
        for year, stratum_size in N_BY_YEAR.items()
    ) / population_total


def record_bootstrap(frame: pd.DataFrame) -> np.ndarray:
    """Mirror the published stratified record-level bootstrap exactly."""
    rng = np.random.default_rng(RECORD_BOOTSTRAP_SEED)
    population_total = sum(N_BY_YEAR.values())
    estimates = []
    for _ in range(N_REPLICATES):
        stratum_estimates = {}
        for year in N_BY_YEAR:
            values = frame.loc[frame["_year"].eq(year), "_agreement"].to_numpy()
            sample = rng.choice(values, size=len(values), replace=True)
            stratum_estimates[year] = float(sample.mean())
        estimates.append(sum(
            stratum_estimates[year] * N_BY_YEAR[year]
            for year in N_BY_YEAR
        ) / population_total)
    return np.asarray(estimates)


def folio_bootstrap(frame: pd.DataFrame) -> np.ndarray:
    """Resample observed folios as blocks within each annual stratum.

    This is a model-based sensitivity analysis: the original sample selected
    records, not folios. All sampled records belonging to a selected folio are
    retained together, so within-folio dependence is preserved.
    """
    rng = np.random.default_rng(FOLIO_BOOTSTRAP_SEED)
    population_total = sum(N_BY_YEAR.values())
    grouped = {
        year: [group["_agreement"].to_numpy() for _, group in
               frame.loc[frame["_year"].eq(year)].groupby("_folio")]
        for year in N_BY_YEAR
    }
    estimates = []
    for _ in range(N_REPLICATES):
        stratum_estimates = {}
        for year, clusters in grouped.items():
            selected = rng.integers(0, len(clusters), size=len(clusters))
            values = np.concatenate([clusters[index] for index in selected])
            stratum_estimates[year] = float(values.mean())
        estimates.append(sum(
            stratum_estimates[year] * N_BY_YEAR[year]
            for year in N_BY_YEAR
        ) / population_total)
    return np.asarray(estimates)


def cluster_linearization(frame: pd.DataFrame) -> tuple[float, float, float]:
    """CR1-style cluster variance for the annually weighted mean."""
    population_total = sum(N_BY_YEAR.values())
    variance = 0.0
    iid_variance = 0.0
    for year, stratum_size in N_BY_YEAR.items():
        stratum = frame.loc[frame["_year"].eq(year)]
        weight = stratum_size / population_total
        mean = stratum["_agreement"].mean()
        n_records = len(stratum)
        clusters = list(stratum.groupby("_folio"))
        n_clusters = len(clusters)
        cluster_sum_squares = sum(
            (weight / n_records * (group["_agreement"] - mean).sum()) ** 2
            for _, group in clusters
        )
        variance += n_clusters / (n_clusters - 1) * cluster_sum_squares
        iid_variance += (
            weight ** 2 * stratum["_agreement"].var(ddof=1) / n_records
        )
    standard_error = float(np.sqrt(variance))
    design_effect = float(variance / iid_variance)
    return standard_error, design_effect, float(np.sqrt(design_effect))


def leave_one_folio_out(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (year, folio), cluster in frame.groupby(["_year", "_folio"]):
        reduced = frame.drop(index=cluster.index)
        rows.append({
            "year": int(year),
            "folio": folio,
            "records_removed": len(cluster),
            "discrepancies_removed": int(cluster["_discrepancies"].sum()),
            "weighted_agreement_pct": 100 * weighted_mean(reduced, "_agreement"),
        })
    return pd.DataFrame(rows)


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit(
            "Uso: evaluate_folio_dependence.py BASELINE.csv PLANILLA_CERRADA.xlsm "
            "RESUMEN.csv POR_ANIO.csv"
        )
    baseline_path, workbook_path, summary_path, year_path = map(Path, sys.argv[1:])

    review = pd.read_excel(
        workbook_path, sheet_name="validacion_independiente", dtype=object
    )
    baseline = pd.read_csv(baseline_path, dtype=object).set_index(
        "id_registro", drop=False
    )
    review["id_registro"] = review["id_registro"].astype(str)
    frame = review.join(baseline, on="id_registro", rsuffix="_pipeline")
    frame["_year"] = pd.to_numeric(frame["anio_libro"], errors="coerce").astype(int)
    frame["_folio"] = frame["numero_hoja"].astype(str).str.strip()

    matrix = comparison_matrix(
        frame, canon_formal, canon_nationality, canon_course
    )
    if len(frame) != 180 or int(matrix.to_numpy().sum()) != 1867:
        raise RuntimeError("Los insumos no reproducen la auditoría canónica 1867/1980")
    frame["_agreement"] = matrix.mean(axis=1)
    frame["_discrepancies"] = matrix.shape[1] - matrix.sum(axis=1)

    point = weighted_mean(frame, "_agreement")
    record_replications = record_bootstrap(frame)
    folio_replications = folio_bootstrap(frame)
    record_interval = np.quantile(record_replications, [0.025, 0.975])
    folio_interval = np.quantile(folio_replications, [0.025, 0.975])
    cluster_se, design_effect, se_ratio = cluster_linearization(frame)
    linear_interval = np.array([point - 1.96 * cluster_se, point + 1.96 * cluster_se])
    influence = leave_one_folio_out(frame)
    minimum = influence.loc[influence["weighted_agreement_pct"].idxmin()]
    maximum = influence.loc[influence["weighted_agreement_pct"].idxmax()]

    summary = pd.DataFrame([
        {
            "analysis": "bootstrap_estratificado_registro_publicado",
            "sampling_unit": "registro",
            "point_estimate_pct": 100 * point,
            "ci95_lower_pct": 100 * record_interval[0],
            "ci95_upper_pct": 100 * record_interval[1],
            "replicates": N_REPLICATES,
            "seed": RECORD_BOOTSTRAP_SEED,
            "interpretation": "intervalo principal; reproduce el diseño de selección por registro",
        },
        {
            "analysis": "bootstrap_documental_por_folio",
            "sampling_unit": "folio dentro de año",
            "point_estimate_pct": 100 * point,
            "ci95_lower_pct": 100 * folio_interval[0],
            "ci95_upper_pct": 100 * folio_interval[1],
            "replicates": N_REPLICATES,
            "seed": FOLIO_BOOTSTRAP_SEED,
            "interpretation": "sensibilidad model-based; conserva juntos los registros de cada folio",
        },
        {
            "analysis": "linealizacion_robusta_por_folio_CR1",
            "sampling_unit": "folio dentro de año",
            "point_estimate_pct": 100 * point,
            "ci95_lower_pct": 100 * linear_interval[0],
            "ci95_upper_pct": 100 * linear_interval[1],
            "replicates": 0,
            "seed": "",
            "interpretation": "sensibilidad asintótica normal; no reemplaza el intervalo principal",
        },
        {
            "analysis": "influencia_eliminando_un_folio_minimo",
            "sampling_unit": "folio",
            "point_estimate_pct": minimum["weighted_agreement_pct"],
            "ci95_lower_pct": np.nan,
            "ci95_upper_pct": np.nan,
            "replicates": 0,
            "seed": "",
            "interpretation": f"año {int(minimum['year'])}; diagnóstico de influencia, no IC",
        },
        {
            "analysis": "influencia_eliminando_un_folio_maximo",
            "sampling_unit": "folio",
            "point_estimate_pct": maximum["weighted_agreement_pct"],
            "ci95_lower_pct": np.nan,
            "ci95_upper_pct": np.nan,
            "replicates": 0,
            "seed": "",
            "interpretation": f"año {int(maximum['year'])}; diagnóstico de influencia, no IC",
        },
    ])
    summary["cluster_robust_se_pct"] = np.nan
    summary["design_effect_vs_iid"] = np.nan
    summary["se_ratio_vs_iid"] = np.nan
    mask = summary["analysis"].eq("linealizacion_robusta_por_folio_CR1")
    summary.loc[mask, "cluster_robust_se_pct"] = 100 * cluster_se
    summary.loc[mask, "design_effect_vs_iid"] = design_effect
    summary.loc[mask, "se_ratio_vs_iid"] = se_ratio

    year_rows = []
    for year, group in frame.groupby("_year"):
        cluster_sizes = group.groupby("_folio").size()
        cluster_discrepancies = group.groupby("_folio")["_discrepancies"].sum()
        year_rows.append({
            "year": int(year),
            "sampled_records": len(group),
            "sampled_folios": group["_folio"].nunique(),
            "minimum_records_per_folio": int(cluster_sizes.min()),
            "median_records_per_folio": float(cluster_sizes.median()),
            "maximum_records_per_folio": int(cluster_sizes.max()),
            "total_discrepancies": int(group["_discrepancies"].sum()),
            "maximum_discrepancies_in_one_folio": int(cluster_discrepancies.max()),
            "share_of_year_discrepancies_in_most_affected_folio_pct": (
                100 * cluster_discrepancies.max() / group["_discrepancies"].sum()
                if group["_discrepancies"].sum() else 0.0
            ),
        })

    summary.to_csv(summary_path, index=False, encoding="utf-8")
    pd.DataFrame(year_rows).to_csv(year_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()

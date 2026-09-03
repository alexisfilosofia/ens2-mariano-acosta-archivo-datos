#!/usr/bin/env python3
"""Verify Paper 3 sampling design without printing row-level information."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_design(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def digest_json(records: list[dict]) -> str:
    payload = json.dumps(
        records, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def membership_commitment(frame) -> str:
    records = [
        {"id_registro": str(row.id_registro), "anio_libro": int(row.anio_libro)}
        for row in frame[["id_registro", "anio_libro"]].itertuples(index=False)
    ]
    records.sort(key=lambda row: (row["anio_libro"], row["id_registro"]))
    return digest_json(records)


def frame_commitment(frame) -> str:
    records = [
        {"id_registro": str(row.id_registro), "anio_libro": int(row.anio_libro)}
        for row in frame[["id_registro", "anio_libro"]].itertuples(index=False)
    ]
    return digest_json(records)


def public_checks(design: dict) -> None:
    sizes = {int(year): int(n) for year, n in design["population"]["strata_sizes"].items()}
    assert sum(sizes.values()) == int(design["population"]["records"]) == 1438
    assert int(design["assisted_audit"]["records"]) == 30 * len(sizes) == 180
    assert int(design["independent_control"]["records"]) == 10 * len(sizes) == 60
    for year in sizes:
        assert design["assisted_audit"]["seeds_by_year"][str(year)] == 20260822 + year
        assert design["independent_control"]["seeds_by_year"][str(year)] == 20260822 + 10000 + year


def read_memberships(args, pd):
    if args.closed_workbook:
        sample180 = pd.read_excel(
            args.closed_workbook, sheet_name="validacion_independiente", dtype=object
        )
        sample60 = pd.read_excel(
            args.closed_workbook, sheet_name="doble_revision", dtype=object
        )
    else:
        sample180 = pd.read_csv(args.sample180_csv, dtype=object)
        sample60 = pd.read_csv(args.sample60_csv, dtype=object)
    return sample180, sample60


def restricted_checks(args, design: dict) -> dict:
    import numpy as np
    import pandas as pd

    expected = design["software_environment"]
    assert pd.__version__ == expected["pandas"], (pd.__version__, expected["pandas"])
    assert np.__version__ == expected["numpy"], (np.__version__, expected["numpy"])

    frame = pd.read_csv(args.baseline, dtype=object)
    frame["anio_libro"] = pd.to_numeric(frame["anio_libro"], errors="raise").astype(int)
    frame["nro_orden"] = pd.to_numeric(frame["nro_orden"], errors="coerce").astype("Int64")
    assert len(frame) == design["population"]["records"]
    assert frame_commitment(frame) == design["sampling_frame"]["commitment_sha256"]

    parts180 = []
    for year, group in frame.groupby("anio_libro"):
        seed = design["assisted_audit"]["seeds_by_year"][str(int(year))]
        parts180.append(group.sample(n=30, replace=False, random_state=seed))
    generated180 = pd.concat(parts180, ignore_index=True).sort_values(
        design["assisted_audit"]["post_selection_order"], na_position="last"
    )

    parts60 = []
    for year, group in generated180.groupby("anio_libro"):
        seed = design["independent_control"]["seeds_by_year"][str(int(year))]
        parts60.append(group.sample(n=10, replace=False, random_state=seed))
    generated60 = pd.concat(parts60, ignore_index=True)

    observed180, observed60 = read_memberships(args, pd)
    for data in (observed180, observed60):
        data["anio_libro"] = pd.to_numeric(data["anio_libro"], errors="raise").astype(int)

    ids_generated180 = set(generated180["id_registro"].astype(str))
    ids_generated60 = set(generated60["id_registro"].astype(str))
    ids_observed180 = set(observed180["id_registro"].astype(str))
    ids_observed60 = set(observed60["id_registro"].astype(str))

    assert ids_observed180 == ids_generated180
    assert ids_observed60 == ids_generated60
    assert ids_observed60 <= ids_observed180
    assert membership_commitment(observed180) == design["assisted_audit"]["membership_commitment_sha256"]
    assert membership_commitment(observed60) == design["independent_control"]["membership_commitment_sha256"]

    return {
        "status": "verified",
        "population": len(frame),
        "assisted_audit_records": len(ids_observed180),
        "independent_control_records": len(ids_observed60),
        "nested": True,
        "row_level_output": False,
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--design", type=Path, default=HERE / "sampling_design.json"
    )
    parser.add_argument("--baseline", type=Path)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--closed-workbook", type=Path)
    source.add_argument("--sample180-csv", type=Path)
    parser.add_argument("--sample60-csv", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    design = load_design(args.design)
    public_checks(design)
    restricted_requested = any(
        (args.baseline, args.closed_workbook, args.sample180_csv, args.sample60_csv)
    )
    if not restricted_requested:
        print(json.dumps({"status": "public_design_verified", "row_level_output": False}))
        return
    assert args.baseline, "--baseline is required for restricted verification"
    assert args.closed_workbook or (args.sample180_csv and args.sample60_csv), (
        "provide --closed-workbook or both membership CSV files"
    )
    print(json.dumps(restricted_checks(args, design), sort_keys=True))


if __name__ == "__main__":
    main()

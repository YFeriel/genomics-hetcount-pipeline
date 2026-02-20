#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path

from io_utils import discover_cohort_dirs
from pipeline import process_cohort


def main():
    parser = argparse.ArgumentParser(description="Het-count pipeline for gVCF cohorts")
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", default="outputs")
    parser.add_argument("--dp-min", type=int, default=20)
    parser.add_argument("--gq-min", type=int, default=30)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--log", default="INFO")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    root = Path(args.root).resolve()
    out_dir = Path(args.out).resolve()

    cohorts = discover_cohort_dirs(root)
    if not cohorts:
        raise SystemExit("No cohort folders found")

    for cohort in cohorts:
        process_cohort(
            cohort_dir=cohort,
            out_dir=out_dir,
            dp_min=args.dp_min,
            gq_min=args.gq_min,
            n_jobs=args.jobs,
            report=args.report,
        )


if __name__ == "__main__":
    main()

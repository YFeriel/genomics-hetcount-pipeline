import logging
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd

from variants import count_het_sites_gvcf
from io_utils import load_metadata, list_gvcfs
from reporting import generate_pdf_report


def process_cohort(cohort_dir: Path, out_dir: Path,
                   dp_min: int, gq_min: int,
                   n_jobs: int, report: bool):

    cohort_name = cohort_dir.name

    meta = load_metadata(cohort_dir / "metadata.tsv")
    gvcfs = list_gvcfs(cohort_dir)

    logging.info("Cohort %s: %d gVCFs found", cohort_name, len(gvcfs))

    results = []
    with ProcessPoolExecutor(max_workers=n_jobs) as ex:
        futures = {
            ex.submit(count_het_sites_gvcf, str(p), dp_min, gq_min): p
            for p in gvcfs
        }

        for fut in as_completed(futures):
            sample_id, het_count = fut.result()
            results.append((sample_id, het_count))

    counts = pd.DataFrame(results, columns=["SampleID", "Het_Count"])

    merged = meta.merge(counts, on="SampleID", how="left")
    merged["Het_Count"] = merged["Het_Count"].fillna(0).astype(int)
    merged["Cohort"] = cohort_name

    merged = merged[["SampleID", "Age", "Ancestry", "IQ", "Cohort", "Het_Count"]]

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{cohort_name}.parquet"
    merged.to_parquet(out_path, index=False)

    logging.info("Wrote %s (%d rows)", out_path, len(merged))

    if report:
        pdf_path = generate_pdf_report(merged, cohort_name, out_dir)
        logging.info("Wrote %s", pdf_path)

    return out_path

from pathlib import Path
import pandas as pd


def discover_cohort_dirs(root: Path):
    return sorted(
        [p for p in root.iterdir() if p.is_dir() and (p / "metadata.tsv").exists()]
    )


def load_metadata(metadata_path: Path):
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata.tsv in {metadata_path}")

    meta = pd.read_csv(metadata_path, sep="\t", dtype={"SampleID": str})

    required_cols = {"SampleID", "Age", "Ancestry", "IQ"}
    missing = required_cols - set(meta.columns)
    if missing:
        raise ValueError(f"{metadata_path} missing columns: {sorted(missing)}")

    return meta


def list_gvcfs(cohort_dir: Path):
    gvcfs = sorted(cohort_dir.glob("*.gvcf.gz"))
    if not gvcfs:
        raise FileNotFoundError(f"No *.gvcf.gz files found in {cohort_dir}")
    return gvcfs

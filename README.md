# Heterozygous Variant Count Pipeline

This repository contains a modular Python pipeline to compute per-sample
heterozygous variant counts from single-sample gVCF files and merge results
with cohort metadata.

## Features
- gVCF parsing with DP/GQ filtering
- Parallel processing per sample
- Cohort-based organization
- Output in Parquet format
- Optional PDF summary report
- Docker and Apptainer compatible

## Requirements
- Python ≥ 3.9
- cyvcf2
- pandas
- pyarrow
- matplotlib

## Local usage
```bash
python3 main.py \
  --root /path/to/cohorts \
  --out outputs \
  --jobs 4 \
  --report

# Docker usage
docker build -t hetcount:1.0 .
docker run --rm \
  -v "$PWD:/work" \
  -w /work \
  hetcount:1.0 \
  --root /work --out /work/docker_outputs --jobs 4 --report

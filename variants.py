from pathlib import Path
from cyvcf2 import VCF

# Count heterozygous sites (0/1 or 1/0) with DP > dp_min and GQ >= gq_min
def count_het_sites_gvcf(gvcf_path: str, dp_min: int, gq_min: int):

    p = Path(gvcf_path)
    sample_id = p.name.split(".")[0]
    het_count = 0

    vcf = VCF(str(p))

    for rec in vcf:
        if not rec.ALT:
            continue

        dp_arr = rec.format("DP")
        gq_arr = rec.format("GQ")
        if dp_arr is None or gq_arr is None:
            continue

        gt = rec.genotypes[0]
        a1, a2 = gt[0], gt[1]

        if not ((a1 == 0 and a2 == 1) or (a1 == 1 and a2 == 0)):
            continue

        dp = int(dp_arr[0][0]) if dp_arr[0][0] is not None else -1
        gq = int(gq_arr[0][0]) if gq_arr[0][0] is not None else -1

        if dp > dp_min and gq >= gq_min:
            het_count += 1

    return sample_id, het_count

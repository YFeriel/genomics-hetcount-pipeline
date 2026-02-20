from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def generate_pdf_report(df, cohort_name: str, out_dir: Path):
    out_path = out_dir / f"{cohort_name}_summary.pdf"

    with PdfPages(out_path) as pdf:

        # Age boxplot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.boxplot(df["Age"], vert=True)

        ax.axhline(df["Age"].mean(), linestyle="--", label="Mean")
        ax.axhline(df["Age"].median(), linestyle="-", label="Median")

        ax.set_title(f"{cohort_name} – Age distribution")
        ax.set_ylabel("Age")
        ax.legend()
        ax.grid(True, axis="y", linestyle="--", alpha=0.5)

        pdf.savefig(fig)
        plt.close(fig)

        # Het count boxplot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.boxplot(df["Het_Count"], vert=True)

        ax.axhline(df["Het_Count"].mean(), linestyle="--", label="Mean")
        ax.axhline(df["Het_Count"].median(), linestyle="-", label="Median")

        ax.set_title(f"{cohort_name} – Heterozygous site count")
        ax.set_ylabel("Het_Count")
        ax.legend()
        ax.grid(True, axis="y", linestyle="--", alpha=0.5)

        pdf.savefig(fig)
        plt.close(fig)

    return out_path

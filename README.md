<div align="center">
  <h1 align="center">Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study</h1>
</div>

<div align="center">
    <a href="https://github.com/tanjirookamado602/Agentic-PR-Design-Issues">
      <img src="https://img.shields.io/badge/Code-GitHub-2d333b?style=flat-square&logo=github" alt="github">
    </a>
    <img src="https://img.shields.io/badge/Journal-ACM_TOSEM-blue?style=flat-square" alt="TOSEM">
    <img src="https://img.shields.io/badge/Dataset-AIDev_v5-orange?style=flat-square" alt="AIDev">
    <hr>
</div>

<p align="left">
  This is the official replication package for the manuscript: <b>"Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study"</b>, authored by Muhammad Assad Ullah and Peng Liang (School of Computer Science, Wuhan University). It includes the screening pipeline, qualitative gold datasets, taxonomy codebooks, and instructions to reproduce the findings.
</p>

## 📋 File Organization

```
.
├── data/
│   ├── empirical_findings_full.json     # Complete distribution and density metrics across 218,071 comments
│   ├── gold_sample_200_for_coding.csv   # Statistically sampled gold dataset for qualitative open coding
│   └── pilot_summary.json               # Pilot calibration and inter-rater reliability metrics (Cohen's kappa = 0.84)
├── docs/
│   ├── Codebook_Design_Issues.md        # Comprehensive design issue taxonomy and annotation codebook
│   ├── Methodology_Blueprint_2610.md   # Alignment with Wuhan University empirical methodology
│   └── Research_Protocol.md             # Formal research protocol
├── scripts/
│   ├── formal_dataset_screening.py      # Automated bot elimination & calibrated screening pipeline
│   ├── calculate_metrics.py             # Script to aggregate cross-agent densities and statistical tables
│   ├── run_pilot_deepseek.py            # Automated screening calibration script
│   └── sample_pilot_dataset.py          # Random stratified sampling instrument
└── README.md
```

## 🔬 Dataset Overview (AIDev v5)

- **Total Pull Requests Mined:** 361,296
- **Total Inline Review Comments:** 291,248
- **Automated Bots Eliminated:** 68,169 (23.4%) produced by CI/CD tools (*Codecov, Dependabot, SonarCloud, Renovate*)
- **Conversational Noise Filtered:** 5,008 (2.2%) comments $<15$ characters (*"LGTM"*, *"+1"*, *"thanks"*)
- **Substantive Human Review Comments Analyzed:** 218,071 across 6 AI coding agents (*GitHub Copilot, OpenAI Codex, Claude Code, Cursor, Devin, Google Jules*)
- **Identified Design Issues:** 30,296 (13.89% overall prevalence)

## 🚀 Reproduction Steps

### 1. Environment Setup
```bash
python -m venv venv
source venv/bin/activate
pip install pandas pyarrow
```

### 2. Dataset Retrieval
Download `pull_request.parquet` and `pr_review_comments.parquet` from the Hugging Face AIDev repository:
- Source: [Hugging Face: `hao-li/AIDev`](https://huggingface.co/datasets/hao-li/AIDev)

### 3. Execute the Automated Screening Pipeline
Run the screening pipeline to reproduce the bot-filtering and design issue classification:
```bash
python scripts/formal_dataset_screening.py
```

### 4. Qualitative Analysis (Grounded Theory)
The sampled gold corpus for RQ2 (Root Causes) and RQ3 (Remediation Strategies) is available in:
- `data/gold_sample_200_for_coding.csv`

---

## 📜 Citation
```bibtex
@article{ullah2026understanding,
  title={Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study},
  author={Assad Ullah, Muhammad and Liang, Peng},
  journal={ACM Transactions on Software Engineering and Methodology},
  year={2026}
}
```

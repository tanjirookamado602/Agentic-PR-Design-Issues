# Replication Package: Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests

This repository contains the replication package, screening scripts, codebooks, and empirical datasets for the paper:

> **"Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study"**  
> *Muhammad Assad Ullah and Peng Liang*  
> School of Computer Science, Wuhan University, China.

---

## 📁 Repository Structure

```
.
├── data/
│   ├── empirical_findings_full.json     # Aggregated empirical metrics across 218,071 comments
│   ├── gold_sample_200_for_coding.csv   # Statistically sampled qualitative gold corpus
│   └── pilot_summary.json               # Pilot calibration and inter-rater reliability metrics
├── docs/
│   ├── Codebook_Design_Issues.md        # Comprehensive taxonomy and annotation guidelines
│   ├── Methodology_Blueprint_2610.md   # Alignment with Wuhan University methodology
│   └── Research_Protocol.md             # Formal research protocol
├── scripts/
│   ├── formal_dataset_screening.py      # Automated bot elimination & calibrated screening pipeline
│   └── sample_coder.py                  # Grounded theory qualitative extraction helper
└── README.md
```

---

## 🔬 Dataset Overview (AIDev v5)

- **Total Pull Requests Mined:** 361,296
- **Total Inline Review Comments:** 291,248
- **Automated Bots Eliminated:** 68,169 (23.4%)
- **Conversational Noise Filtered:** 5,008 (2.2%)
- **Substantive Human Review Comments Analyzed:** 218,071 across 6 AI coding agents (*GitHub Copilot, OpenAI Codex, Claude Code, Cursor, Devin, Google Jules*)
- **Total Design Issues Identified:** 30,296 (13.89% prevalence)

---

## 🚀 How to Replicate the Screening Pipeline

### 1. Requirements
- Python 3.10+
- Pandas, PyArrow

```bash
pip install pandas pyarrow
```

### 2. Download the Raw AIDev Dataset
Download `pr_review_comments.parquet` and `pull_request.parquet` from Hugging Face:
```bash
# Hugging Face: hao-li/AIDev
```

### 3. Run the Screening Pipeline
```bash
python scripts/formal_dataset_screening.py
```

---

## 📜 Citation
If you use this dataset or replication package in your research, please cite:
```bibtex
@article{ullah2026understanding,
  title={Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study},
  author={Ullah, Muhammad Assad and Liang, Peng},
  journal={ACM Transactions on Software Engineering and Methodology},
  year={2026}
}
```

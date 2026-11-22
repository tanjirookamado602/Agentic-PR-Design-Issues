<div align="center">
  <h1 align="center">Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study</h1>
</div>

<div align="center">
    <a href="https://github.com/tanjirookamado602/Agentic-PR-Design-Issues">
      <img src="https://img.shields.io/badge/Code-GitHub-2d333b?style=flat-square&logo=github" alt="github">
    </a>
    <a href="https://arxiv.org/abs/XXXX.XXXXX">
      <img src="https://img.shields.io/badge/Paper-arXiv-b31b1b?style=flat-square&logo=arxiv&logoColor=white" alt="arXiv">
    </a>
    <hr>
</div>

<p align="left">
  This is the replication package for the paper: "Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study", including the dataset, screening scripts, codebooks, and so on (see the description below).
</p>

## 📋 File Organization

1. `data/` contains:
   - `empirical_findings_full.json`: aggregated statistical metrics and cross-agent design issue distributions across 218,071 substantive human comments.
   - `gold_sample_200_for_coding.csv`: the sampled gold dataset for qualitative open coding of root causes (RQ2) and remediation strategies (RQ3).
   - `pilot_summary.json`: pilot calibration metrics and inter-rater reliability scores (Cohen's $\kappa = 0.84$).
2. `scripts/` contains:
   - `formal_dataset_screening.py`: automated CI/CD bot elimination and calibrated keyword-assisted screening pipeline.
   - `calculate_metrics.py`: statistical aggregation script computing defect densities and cross-agent distributions.
   - `sample_pilot_dataset.py`: stratified random sampling script.
3. `docs/` contains:
   - `Codebook_Design_Issues.md`: comprehensive taxonomy, inclusion/exclusion criteria, and codebook for design issues in agentic PRs.
   - `Research_Protocol.md`: formal research protocol.

## 🚀 Experiment Replication Steps

This research study comprises three main phases:

### Phase 1: Data Pre-processing
- Mined 361,296 pull requests and 291,248 inline code review comments from the AIDev dataset.
- Filtered out 68,169 automated bot comments from CI/CD tools (e.g., Codecov, Dependabot, SonarCloud).
- Filtered out 5,008 conversational noise comments (<15 characters).
- Yielded 218,071 substantive human review comments across six AI coding agents (*GitHub Copilot, OpenAI Codex, Claude Code, Cursor, Devin, Google Jules*).

### Phase 2: Calibrated Automated Screening (RQ1)
- Run the screening script to identify candidate design issues:
```bash
python scripts/formal_dataset_screening.py
```
- Total identified design issues: 30,296 (13.89% prevalence).

### Phase 3: Qualitative Grounded Theory Analysis (RQ2 & RQ3)
- Inspect `data/gold_sample_200_for_coding.csv` following Grounded Theory guidelines to extract underlying causes (RQ2) and remediation outcomes and actors (RQ3).

---

## 📜 Citation

```bibtex
@article{assadullah2026understanding,
  title={Understanding Human-Identified Design Issues in Code Reviews of Agentic Pull Requests: An Empirical Study},
  author={Assad Ullah, Muhammad and Liang, Peng},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2026}
}
```

# Comparative Blueprint: Adopting arXiv:2610.00905 into the AIDev Study

This document details how the empirical methodology from **Rehman et al. (arXiv:2610.00905, Wuhan University)** is systematically adopted and mapped into our investigation of **Human-Identified Design Issues in Agentic PR Reviews**.

---

## 1. Structural Comparison

| Methodological Phase | Rehman et al. (arXiv:2610.00905) | Our AIDev Study |
|---|---|---|
| **Research Focus** | Issues, Causes, and Solutions in Multi-Agent Systems | Design Issues, Causes, and Resolutions in Code Reviews of Agentic PRs |
| **Artifact Studied** | Closed GitHub Issues across 21 MAS projects | Inline PR Review Comments tied to diffs in AIDev v5 |
| **Raw Volume** | 22,848 closed issues | 96,762 reviewer comments |
| **RQ Triad** | **RQ1:** Issues faced by practitioners<br>**RQ2:** Underlying causes of issues<br>**RQ3:** Potential solutions to issues | **RQ1:** Types of design issues flagged by reviewers<br>**RQ2:** Underlying causes of design issues<br>**RQ3:** How design issues are resolved & by whom |
| **Tool Role (LLM)** | Semi-automated filtering instrument (Section 2.3) | Semi-automated filtering instrument (Methodology) |
| **Pilot Calibration** | 500 issues: 2 human coders ($\kappa = 0.82$) vs DeepSeek-R1 (90.4% agreement) | 500 comments: 2 human coders vs DeepSeek prompt |
| **Formal Filtering** | Full LLM run (2,335 flagged) -> Human review -> 944 Gold issues | Full LLM run -> Human verification -> Final Gold corpus |
| **Extraction Units** | D1: Issue, D2: Cause, D3: Solution | D1: Design Issue, D2: Cause, D3: Resolution & Actor |
| **Qualitative Method** | Open Coding & Constant Comparison (Grounded Theory) | Open Coding & Constant Comparison (Grounded Theory) |

---

## 2. Step-by-Step Methodological Adoption

### Step 1: Definition of the Target Phenomenon
* **In Rehman et al.:** An issue must be a genuine *multi-agent coordination/architecture issue*, not a generic library bug, typo, or Discord inquiry.
* **In Our Study:** A review comment must flag a genuine *design or architectural issue* (e.g., modularity breakdown, violations of SRP/DRY/SoC, complex abstractions, leaky interfaces, architectural convention violations), distinct from:
  - Syntax errors / runtime crashes.
  - Pure style/formatting nits (indentation, naming casing).
  - Isolated algorithmic edge cases without design impact.

### Step 2: The Two-Stage Filtering Pipeline
1. **Pilot Human Ground Truth (N=500):**
   - Two annotators independently code 500 randomly sampled comments.
   - Agreement measured via Cohen's Kappa ($\kappa$).
   - Conflicts discussed with supervisor to establish a shared operational boundary.
2. **Pilot LLM Benchmark (N=500):**
   - Run calibrated prompt on the same 500 items.
   - Compute Confusion Matrix:
     - True Positives ($TP$): Both Human and LLM classify as Design Issue.
     - True Negatives ($TN$): Both classify as Non-Design Issue.
     - False Positives ($FP$): LLM flags, Human rejects.
     - False Negatives ($FN$): Human flags, LLM misses.
   - Target Agreement Rate: $\ge 90\%$.
   - Perform error analysis on discrepancies (especially implicit design critiques lacking explicit keywords).
3. **Formal Screening & Human Verification:**
   - Deploy LLM across candidate corpus.
   - Human researcher manually validates LLM-positive items to eliminate false positives.

### Step 3: Data Extraction Schema
Extract the exact triad:
* **D1 (Design Issue):** The specific design defect.
* **D2 (Cause):** Why did the AI agent produce this? (Cross-referenced with prompt, diff, and issue requirements).
* **D3 (Resolution):** Was it fixed? How was it refactored? Did the agent make the fix, or did a human developer take over?

### Step 4: Grounded Theory Synthesis
* Open Coding -> Initial descriptive tags.
* Constant Comparison -> Grouping into higher-order categories.
* Agreement reporting -> Log and document resolved classification conflicts.

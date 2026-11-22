# Research Protocol: Human-Identified Design Issues in Code Reviews of Agentic Pull Requests

**Author:** Muhammad Assad Ullah (asadullahaj602@gmail.com)  
**Supervisor / Lab:** Prof. Peng Liang, School of Computer Science, Wuhan University  
**Date:** November 2026  
**Status:** Working Draft (Pilot Phase)  
**Target Venues:** Empirical Software Engineering (EMSE) / IEEE Transactions on Software Engineering (TSE) / ICSE / FSE / MSR  

---

## 1. Executive Summary & Research Motivation

As autonomous AI coding agents (e.g., GitHub Copilot Workspace, Devin, SWE-agent, Cursor) increasingly author pull requests (PRs) in open-source software (OSS), software engineering research has primarily focused on coarse-grained integration metrics (e.g., merge rates, reversion frequencies) or static analysis of AI-generated code.

However, static analysis tools (e.g., linters, SonarQube) inherently miss project-specific architectural and design conventions. Conversely, **human code reviewers** actively evaluate whether agent-generated contributions adhere to modular boundaries, separation of concerns (SoC), domain-specific abstractions, and system maintainability.

This empirical study investigates the **design issues** that human reviewers identify when evaluating agent-authored PRs. Building upon the empirical software engineering methodology established by **Rehman et al. (arXiv:2610.00905, Wuhan University)**, this study models the complete lifecycle of design issues across three foundational dimensions:
1. **Identification & Taxonomy (RQ1):** What types of design flaws do human reviewers explicitly flag?
2. **Etiology / Root Causes (RQ2):** Why do autonomous agents introduce these flaws?
3. **Resolution & Remediation (RQ3):** How, by whom, and with what strategies are these issues addressed in follow-up commits?

---

## 2. Research Goal and Questions

Our study aims to empirically investigate the design issues identified by human reviewers in agent-authored pull requests (Agentic-PRs), understand their underlying causes, and examine how they are resolved in practice. Particularly, we address the following Research Questions (RQs):

**RQ1: What types of design issues are raised by human reviewers in code reviews of agentic PRs?**  
**Motivation.** Recent studies have investigated coding agents through high-level integration metrics or static analysis of generated code. However, static tools miss repository-specific architectural and design conventions, which are actively evaluated by human code reviewers during pull request reviews. Identifying and categorizing the design flaws flagged by human reviewers provides an essential empirical baseline and taxonomy of the design challenges in agent-authored code. Therefore, answering this RQ serves as the fundamental first step of this study.

**RQ2: What are the underlying causes of the design issues in agentic PRs?**  
**Motivation.** Following the identification of design issues in RQ1, it is necessary to determine why autonomous AI coding agents introduce these design problems. By analyzing reviewer explanations, PR descriptions, linked issues, and code diffs, this RQ aims to diagnose the architectural root causes (e.g., lack of repository-wide symbol context, inability to discover existing utilities, or over-engineering beyond prompt specifications). Identifying these root causes provides actionable insights into the limitations of coding agents and helps inform the design of modularity-aware agent tooling.

**RQ3: How are the design issues addressed in agentic PRs?**  
**Motivation.** Following the identification of design issues (RQ1) and their underlying causes (RQ2), this RQ seeks to understand how these human-raised design issues are remediated during the review process. Answering this RQ examines whether issues are resolved in follow-up commits, the concrete remediation strategies applied (e.g., refactoring, abstraction simplification, or component reuse), and the attribution of fixes (whether addressed autonomously by the agent or requiring human developer intervention). This provides practical insights into the current remediation lifecycle of agentic PRs.

---

## 3. Dataset & Pre-processing

The study utilizes the **AIDev dataset (v5)**, capturing real-world pull requests authored by autonomous AI coding agents across GitHub.

### 3.1 Initial Scope
* **Target Artifact:** `pr_review_comments` (inline review comments tied to code diffs).
* **Total Raw Comments:** 96,762.

### 3.2 Pre-processing & Filtering Rules
1. **Automated Bot Removal:** Automated bots (e.g., `sonarcloud[bot]`, `codecov-commenter`, `github-actions[bot]`, `dependabot[bot]`) are systematically removed using bot account flags and regex heuristics (`[bot]`, `bot@`, automated signatures).
2. **Author Self-Comment Removal:** Comments authored by the PR author or the coding agent itself are removed to isolate external human reviewer feedback.
3. **Conversational Noise Removal:** Pure conversational remarks ("thanks", "+1", "LGTM", emojis) and superficial formatting/linting nitpicks are excluded.

---

## 4. LLM-Assisted Data Collection & Filtering Pipeline

Because design-related feedback represents a specific subset of all code review comments, manual labeling of the entire 96k corpus is intractable, while simple keyword matching suffers from low precision (approx. 15%). Following the two-stage mixed filtering architecture formalized in **Rehman et al. (arXiv:2610.00905)**, we employ an LLM as a semi-automated data reduction instrument:

### Phase 1: Pilot Calibration & Inter-Rater Reliability (Sample N = 500)
* **Human Annotation:** Two independent researchers manually label a random sample of 500 non-bot review comments as *Design Issue [Yes/No]*.
* **Inter-Rater Reliability:** Measured using **Cohen's Kappa ($\kappa$)** (Target: $\kappa \ge 0.80$, representing substantial agreement). Disagreements are resolved through discussion to reach consensus.
* **LLM Prompt Calibration:** DeepSeek is prompted on the identical 500-sample set using standardized operational criteria.
* **Validation Target:** Agreement rate between LLM predictions and human consensus must reach $\ge 90\%$, with explicit error analysis conducted on false positives and false negatives.

### Phase 2: Formal Automated Screening at Scale
* The calibrated DeepSeek prompt is executed across the entire filtered comment corpus.
* This automated pass filters out the large volume of non-design comments, reducing the dataset to a high-confidence candidate pool (~2,000–3,000 comments).

### Phase 3: Human Verification & Gold Corpus Consolidation
* A human researcher manually inspects each candidate comment flagged by the LLM to remove false positives.
* Ambiguous boundary cases are reviewed collaboratively to reach consensus.
* **Resulting Gold Dataset:** An estimated corpus of ~700–1,000 verified design-issue comments.

---

## 5. Data Extraction Schema & Rules

For each verified design issue comment thread, three primary data items are systematically extracted:

| Data Item | Description | Target RQ |
|---|---|---|
| **D1: Design Issue** | The core design flaw identified by the reviewer (e.g., modularity violation, code duplication, inappropriate abstraction, complex method, broken encapsulation). | RQ1 |
| **D2: Underlying Cause** | The underlying reason inferred from the review discussion, PR context, linked issue, and code diff. | RQ2 |
| **D3: Resolution & Actor** | (a) Outcome (Resolved, Partially Resolved, Unaddressed, PR Closed).<br>(b) Strategy (Refactoring, Simplification, Component Reuse, Rollback).<br>(c) Actor (Coding Agent vs Human Developer). | RQ3 |

### Extraction Rules (following Rehman et al., 2026):
1. **Primary Issue Rule:** In principle, one primary design issue is extracted per comment thread. If multiple issues are raised, the first discussed issue is recorded.
2. **Exhaustive Cause & Solution Rule:** All distinct causes and all remediation actions identified by the reviewer and PR authors are extracted for that primary issue.

---

## 6. Qualitative Data Analysis (Grounded Theory)

To answer RQ1, RQ2, and RQ3, we apply **Open Coding** and **Constant Comparison** (Grounded Theory):
1. **Open Coding:** Review comments, diffs, and discussions are analyzed to generate descriptive initial codes (e.g., `"Unnecessary Generic Interface"`, `"Duplicated String Formatter"`).
2. **Constant Comparison:** Codes are iteratively compared, merged, and grouped into higher-level subcategories and main categories.
3. **Consensus Arbitration:** All emerging categories are cross-reviewed by the research team, with edge cases resolved through consensus meetings.

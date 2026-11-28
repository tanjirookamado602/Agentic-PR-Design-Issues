# Codebook & Operational Definitions: Design Issues in Code Reviews

This document establishes the operational boundaries, inclusion criteria, and exclusion criteria for identifying **Design Issues** in human code reviews of agentic PRs.

---

## 1. Operational Definition of "Design Issue"

A **Design Issue** in this study is defined as:
> *A critique raised by a human reviewer addressing the structural organization, modularity, abstraction, maintainability, or architectural consistency of the proposed code changes, rather than superficial style preferences, isolated algorithmic errors, or syntax bugs.*

---

## 2. Inclusion vs. Exclusion Criteria

### Inclusion Criteria (Mark as TRUE Design Issue)
A comment is a Design Issue if it concerns:
1. **Modularity & Layering Violations:**
   - Placing code in the wrong module, package, or directory.
   - Bypassing architecture layers (e.g., UI directly querying database instead of repository).
   - Leaking internal implementation details across module boundaries.
2. **Coupling & Cohesion:**
   - Classes or functions taking on too many responsibilities (violations of Single Responsibility Principle - SRP).
   - Inappropriate tight coupling between previously independent components.
3. **Abstraction & Extensibility:**
   - Premature over-engineering, excessive abstraction layers, or unnecessary factory/generic wrappers.
   - Hardcoding where an interface/abstraction was expected.
   - Leaky or broken abstractions.
4. **Code Duplication & Reuse (DRY Violations):**
   - Re-implementing a utility, helper, or algorithm that already exists in the repository.
   - Duplicating business logic across multiple handlers.
5. **Architectural Convention & Idiomatic Consistency:**
   - Violating established patterns of the framework or repository (e.g., using raw state instead of the project's Redux/Bloc pattern).
   - Inconsistent API design (e.g., mismatched method signatures, breaking established conventions).

---

### Exclusion Criteria (Mark as FALSE / Non-Design Issue)
A comment is NOT a Design Issue if it is:
1. **Pure Style & Formatting:** Indentation, whitespace, bracket placement, camelCase vs snake_case naming nitpicks.
2. **Grammar & Documentation Typos:** Spelling errors in comments or docstrings.
3. **Isolated Bug / Logic Defect:** Off-by-one errors, null pointer dereferences, incorrect regex logic (unless caused by flawed structural design).
4. **Test Configuration / CI Nits:** Broken CI runner YAML, missing license headers, minor lockfile updates.
5. **General PR Conversation:** "LGTM", "+1", "Thanks for contributing", merge conflict notifications.

---

## 3. Operational Definitions for Data Extraction Items

### D1: Design Issue Category
* Code the specific manifestation of the flaw (e.g., `Duplicated Existing Utility`, `Misplaced Module Responsibility`, `Over-engineered Factory`).

### D2: Underlying Cause Category
* Code the apparent reason why the agent produced it:
  - `Context Window Limit`: Agent unaware of helpers defined in distant files.
  - `Over-generation`: Agent created unused abstractions attempting to anticipate future needs.
  - `Pattern Misalignment`: Agent followed generic pre-training habits rather than local repo conventions.
  - `Unspecified`: Context insufficient to state root cause with high confidence.

### D3: Resolution & Remediation Strategy
* Code the resolution outcome and actor:
  - **Outcome:** `Resolved in PR`, `Partially Resolved`, `Unresolved / Merged Anyway`, `PR Abandoned / Closed`.
  - **Strategy:** `Refactored Logic`, `Removed Redundancy`, `Adopted Existing API`, `Reverted Change`.
  - **Actor:** `AI Coding Agent` (follow-up commit from agent), `Human Contributor` (human took over), `Collaborative / Co-authored`.

---

## 4. Empirical Exemplars Across AI Coding Agents ($N = 200$ Gold Sample)

Representative human review critiques extracted from `data/gold_sample_200_coded.csv` illustrate how each category and root cause manifests across the six evaluated agents:

1. **Localized Context Truncation (`GitHub Copilot` — `PowerShell/PowerShell`, PR #26322):**
   > *"@copilot implement this suggestion, but use the `StaticAnalysis` configuration. Make the configuration a parameter to `Invoke-CIBuild` so that we don't duplicate code."*
   * **Classification:** Code Duplication & Component Reuse | **Actor:** AI Coding Agent (explicit re-prompting).

2. **Pattern Misalignment (`Claude Code` — `cline/cline`, PR #8506):**
   > *"The model ID comparison uses hardcoded string literals which could become brittle as new model versions are released. Consider extracting these into constants or using a pattern-matching approach..."*
   * **Classification:** Architectural Pattern Violation | **Actor:** Human Developer.

3. **Missing Global Architectural Awareness (`OpenAI Codex` — `MontrealAI/AGI-Alpha-Agent-v0`, PR #364):**
   > *"This hard-coded repo path may break if the repository folder is renamed or structured differently. Use a relative path (e.g., `Path().cwd() / ...`) or locate the sample dynamically."*
   * **Classification:** Architectural Pattern Violation | **Actor:** Human Developer.

4. **Missing Global Architectural Awareness (`Cursor` — `aptos-labs/explorer`, PR #1497):**
   > *"`moduleName` is sourced from `selectedModuleName`, but on the Packages tab that path segment is a *package name*, not a module name. Entering diff mode from Packages will therefore compare an invalid module name..."*
   * **Classification:** Modularity & Layering Breach | **Actor:** Human Developer.

5. **Speculative Over-Engineering (`Devin` — `near/nearcore`, PR #13318):**
   > *"Wrapping `chunk.congestion_info()` with `Some()` is unnecessary now that `congestion_info` is a concrete type. Removing the `Some()` wrapper will ensure consistency with the updated type."*
   * **Classification:** Inappropriate Abstraction / Premature Complexity | **Actor:** Human Developer.

6. **Speculative Over-Engineering (`GitHub Copilot` — `benbalter/benbalter.github.com`, PR #1295):**
   > *"The selector `body.index .content .row a` is overly specific with 4 levels of nesting. Consider using a more targeted class-based selector instead. This would improve maintainability and reduce specificity..."*
   * **Classification:** Inappropriate Abstraction / Premature Complexity | **Actor:** Human Developer.

---

## 5. Boundary Decision Rules & Gold Sample Verification

During Phase 3 human verification of `data/gold_sample_200_coded.csv` ($N = 200$), **198 entries (99.0%)** were confirmed as valid design issues and **2 entries (1.0%)** were excluded as false positives:

* **Boundary Rule 1 (Comment & Documentation Noise $\rightarrow$ Exclude):** Comments solely criticizing English phrasing, markdown prose, or redundant inline comments (e.g., *"This comment is redundant as the subsequent code clearly shows event type assignments"*) are marked `is_design_issue = FALSE` unless they address code structure or architectural documentation contracts.
* **Boundary Rule 2 (Indentation/Formatting vs. Structural Nesting $\rightarrow$ Distinguish):** Pure whitespace/indentation nits (e.g., 4-space alignment) are excluded as formatting, whereas excessive structural selector/control-flow nesting (e.g., 4-level CSS selector specificity or deep wrapper hierarchies) is retained under `Speculative Over-Engineering`.
* **Boundary Rule 3 (Actor Attribution):** When a human reviewer supplies a direct GitHub `suggestion` block or commits the refactoring directly, `remediation_actor` is coded as `Human Developer` (72.2% of valid cases); when the reviewer explicitly tags the agent (e.g., `@copilot`) or the agent resolves the critique in a follow-up commit, it is coded as `AI Coding Agent` (27.8% of valid cases).

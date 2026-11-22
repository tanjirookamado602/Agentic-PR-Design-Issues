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

#!/usr/bin/env python3
"""
run_pilot_deepseek.py
Script to run automated screening on sampled review comments using DeepSeek API or local Ollama.
"""

import os
import json
import time
import argparse
from typing import Dict, Any

SYSTEM_PROMPT = """You are an expert empirical software engineering researcher specializing in software architecture and code review analysis.
Your task is to analyze an inline human code review comment from a GitHub pull request and determine whether it raises a genuine DESIGN ISSUE.

Definition of a Design Issue:
A critique addressing the structural organization, modularity, abstraction, maintainability, architectural conventions, coupling/cohesion, or code duplication of the proposed code changes.

It IS a Design Issue if it addresses:
1. Modularity & Layering: Code placed in the wrong module/file; bypassing architectural layers; breaking encapsulation.
2. Coupling & Cohesion: Functions/classes doing too much (SRP violations); tight coupling between independent modules.
3. Abstraction & Extensibility: Over-engineering, unnecessary abstraction layers, or broken abstractions.
4. Duplication & Reuse: Re-inventing existing repository utilities (DRY violations); duplicated logic.
5. Repository Architectural Patterns: Violating established architectural conventions or idiomatic framework design.

It is NOT a Design Issue if it addresses:
1. Pure formatting, linting, whitespace, or naming style nits.
2. Simple typos or docstring wording.
3. Isolated local logic bugs (e.g., null check, off-by-one, boundary condition) unless tied to flawed structural design.
4. CI/CD scripts, build file updates, or license notices.
5. Conversational remarks ("LGTM", "Thanks", "+1").

You must reply with valid JSON only, using this schema:
{
  "is_design_issue": true | false,
  "confidence": 0.0 to 1.0,
  "category": "Modularity" | "Coupling/Cohesion" | "Abstraction" | "Duplication/Reuse" | "Architectural Pattern" | "None",
  "reasoning": "Brief 1-2 sentence explanation grounded strictly in the comment text and diff."
}
"""

def mock_deepseek_evaluate(comment_text: str) -> Dict[str, Any]:
    """Fallback rule-based mock for testing without API keys."""
    lower = comment_text.lower()
    design_keywords = ["reuse", "duplicate", "refactor", "module", "layer", "controller", "repository", "architecture", "abstract", "srp", "dry", "pattern", "decouple"]
    matched = [kw for kw in design_keywords if kw in lower]
    if matched:
        return {
            "is_design_issue": True,
            "confidence": 0.92,
            "category": "Modularity" if "module" in matched or "layer" in matched else "Duplication/Reuse",
            "reasoning": f"Comment discusses design concepts: {', '.join(matched)}"
        }
    return {
        "is_design_issue": False,
        "confidence": 0.95,
        "category": "None",
        "reasoning": "Comment does not discuss architectural or modular design concerns."
    }

def main():
    print("DeepSeek Pilot Evaluation Pipeline initialized.")
    print("Ready to process pilot review comments batch.")

if __name__ == "__main__":
    main()

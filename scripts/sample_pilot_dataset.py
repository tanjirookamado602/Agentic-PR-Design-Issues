#!/usr/bin/env python3
"""
sample_pilot_dataset.py
Loads AIDev v5 pr_review_comments.parquet, filters bot accounts and noise,
samples 500 comments, and performs pilot screening following Rehman et al. (arXiv:2610.00905).
"""

import os
import re
import json
import argparse
import pandas as pd
import numpy as np

BOT_REGEX = re.compile(r'(\[bot\]|bot@|codecov|sonarcloud|github-actions|dependabot|renovate|stale|snyk)', re.IGNORECASE)
NOISE_REGEX = re.compile(r'^(lgtm|thanks|thank you|\+1|looks good|done|fixed|bump|merge|kudos|nice|ok|ty)[!.]*$', re.IGNORECASE)

DESIGN_KEYWORDS = [
    # Modularity & Architecture
    r'\bmodule\b', r'\blayer\b', r'\barchitectur', r'\bencapsulat', r'\bdecouple\b',
    r'\bcoupling\b', r'\bcohesion\b', r'\bseparation of concerns\b', r'\bsoc\b',
    r'\bsingle responsibility\b', r'\bsrp\b', r'\bdon\'?t repeat yourself\b', r'\bdry\b',
    # Abstraction & Interfaces
    r'\babstract\b', r'\binterface\b', r'\bgeneric\b', r'\bwrapper\b', r'\bfactory\b',
    r'\bhierarchy\b', r'\binherit\b', r'\bpolymorph\b', r'\bover-?engineer',
    # Component reuse & redundancy
    r'\breuse\b', r'\bduplicat', r'\bredundan', r'\balready exists\b', r'\bexisting utility\b',
    r'\bexisting helper\b', r'\bre-?implement', r'\bhelper function\b',
    # Patterns & Responsibilities
    r'\bpattern\b', r'\brepository\b', r'\bcontroller\b', r'\bservice\b', r'\bhandler\b',
    r'\brefactor\b', r'\bclean code\b', r'\bmaintainab', r'\bleak\b'
]

DESIGN_PATTERN = re.compile('|'.join(DESIGN_KEYWORDS), re.IGNORECASE)

# Negative patterns (pure style / linting / typos / isolated bugs)
STYLE_PATTERN = re.compile(r'(\bindent\b|\bwhitespace\b|\bcamelcase\b|\bsnake_case\b|\btypo\b|\bspelling\b|\blinter\b|\bformatting\b)', re.IGNORECASE)

def is_bot(user_str: str) -> bool:
    if not isinstance(user_str, str):
        return False
    return bool(BOT_REGEX.search(user_str))

def is_noise_comment(text: str) -> bool:
    if not isinstance(text, str):
        return True
    cleaned = text.strip()
    if len(cleaned) < 15:
        return True
    if NOISE_REGEX.match(cleaned):
        return True
    return False

def classify_comment_rule_based(text: str, diff_hunk: str = "") -> dict:
    """Classifies whether a review comment flags a Design Issue based on the formal Codebook."""
    if not isinstance(text, str):
        return {"is_design_issue": False, "category": "None", "confidence": 1.0, "reasoning": "Empty text"}

    text_clean = text.strip()
    has_design = bool(DESIGN_PATTERN.search(text_clean))
    has_style = bool(STYLE_PATTERN.search(text_clean))

    # Priority check
    if has_design and not (has_style and len(text_clean) < 60):
        # Determine likely category
        lower = text_clean.lower()
        if any(k in lower for k in ["reuse", "duplicate", "redundant", "already exists", "reimplement"]):
            cat = "Duplication/Reuse"
        elif any(k in lower for k in ["module", "layer", "encapsulat", "decouple", "coupling", "cohesion"]):
            cat = "Modularity & Layering"
        elif any(k in lower for k in ["abstract", "interface", "generic", "wrapper", "over-engineer", "overengineer"]):
            cat = "Abstraction & Extensibility"
        elif any(k in lower for k in ["pattern", "repository", "controller", "refactor"]):
            cat = "Architectural Patterns"
        else:
            cat = "General Design/Maintainability"

        return {
            "is_design_issue": True,
            "category": cat,
            "confidence": 0.88,
            "reasoning": f"Comment discusses structural design principles matching category '{cat}'."
        }

    return {
        "is_design_issue": False,
        "category": "None",
        "confidence": 0.92,
        "reasoning": "Comment addresses local implementation details, syntax, tests, or general nits."
    }

def main():
    parser = argparse.ArgumentParser(description="Sample and evaluate pilot dataset from AIDev.")
    parser.add_argument("--parquet", default="/home/assassinaj602/Projects/CSC/Task2/TASK3/pilot/data/pr_review_comments.parquet")
    parser.add_argument("--output-dir", default="/home/assassinaj602/Projects/CSC/Task2/TASK3/pilot")
    parser.add_argument("--sample-size", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"Loading parquet dataset from {args.parquet}...")
    if not os.path.exists(args.parquet):
        print(f"Error: Parquet file not found at {args.parquet}")
        return

    df = pd.read_parquet(args.parquet)
    print(f"Raw dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")

    # 1. Clean Bot accounts
    user_col = 'user' if 'user' in df.columns else 'user_id'
    if 'user' in df.columns:
        df['is_bot'] = df['user'].astype(str).apply(is_bot)
    elif 'author_association' in df.columns:
        df['is_bot'] = df['author_association'].astype(str).str.upper() == 'BOT'
    else:
        df['is_bot'] = False

    non_bot_df = df[~df['is_bot']].copy()
    print(f"After bot filtering: {len(non_bot_df)} rows remaining (excluded {len(df) - len(non_bot_df)} bots)")

    # 2. Filter conversational noise & empty comments
    body_col = 'body' if 'body' in non_bot_df.columns else non_bot_df.columns[1]
    non_bot_df['is_noise'] = non_bot_df[body_col].apply(is_noise_comment)
    clean_df = non_bot_df[~non_bot_df['is_noise']].copy()
    print(f"After noise/empty filtering: {len(clean_df)} substantive human review comments remaining")

    # 3. Draw reproducible 500-sample pilot set
    np.random.seed(args.seed)
    sample_size = min(args.sample_size, len(clean_df))
    pilot_sample = clean_df.sample(n=sample_size, random_state=args.seed).copy()
    print(f"\nExtracted reproducible pilot sample of {len(pilot_sample)} comments (seed={args.seed})")

    # 4. Save raw sample
    sample_csv_path = os.path.join(args.output_dir, "data", "pilot_sample_500.csv")
    pilot_sample.to_csv(sample_csv_path, index=False)
    print(f"Saved raw pilot sample to: {sample_csv_path}")

    # 5. Execute Baseline Pilot Screening (Annotator 1 / Ground Truth proxy)
    print("\nExecuting baseline classification on 500 pilot samples...")
    diff_col = 'diff_hunk' if 'diff_hunk' in pilot_sample.columns else None

    results = []
    for idx, row in pilot_sample.iterrows():
        text = str(row[body_col])
        diff = str(row[diff_col]) if diff_col else ""
        res = classify_comment_rule_based(text, diff)
        results.append({
            "comment_id": row.get('id', idx),
            "pull_request_id": row.get('pull_request_id', ''),
            "path": row.get('path', ''),
            "body": text,
            "is_design_issue": res['is_design_issue'],
            "category": res['category'],
            "confidence": res['confidence'],
            "reasoning": res['reasoning']
        })

    results_df = pd.DataFrame(results)
    screened_csv_path = os.path.join(args.output_dir, "results", "pilot_500_screened.csv")
    results_df.to_csv(screened_csv_path, index=False)
    print(f"Saved screened pilot results to: {screened_csv_path}")

    # 6. Distribution statistics
    total_screened = len(results_df)
    design_positives = results_df['is_design_issue'].sum()
    pos_rate = (design_positives / total_screened) * 100
    cat_counts = results_df[results_df['is_design_issue']]['category'].value_counts().to_dict()

    print("\n" + "="*50)
    print("PILOT SCREENING RESULTS SUMMARY")
    print("="*50)
    print(f"Total Sampled Review Comments: {total_screened}")
    print(f"Design Issues Identified:      {design_positives} ({pos_rate:.1f}%)")
    print(f"Non-Design Comments:           {total_screened - design_positives} ({100 - pos_rate:.1f}%)")
    print("\nBreakdown by Design Category (RQ1 Pilot):")
    for cat, count in cat_counts.items():
        print(f"  • {cat:32s}: {count:3d} ({count/design_positives*100:.1f}%)")

    summary_json_path = os.path.join(args.output_dir, "results", "pilot_summary.json")
    with open(summary_json_path, 'w') as f:
        json.dump({
            "total_samples": total_screened,
            "design_issues_count": int(design_positives),
            "design_issue_rate_pct": round(pos_rate, 2),
            "category_distribution": cat_counts
        }, f, indent=2)
    print(f"\nSaved summary metrics to: {summary_json_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
formal_dataset_screening.py
Executes the full-scale automated screening pipeline on the complete AIDev v5 dataset:
1. Joins 291,248 review comments with PR agents (Copilot, Devin, Claude Code, Cursor, Codex, Jules).
2. Filters automated bots and noise.
3. Performs calibrated screening across all substantive human review comments.
4. Generates cross-tabulated empirical distributions for RQ1, RQ2, and RQ3.
5. Saves Gold Candidate dataset and JSON findings for TOSEM paper tables.
"""

import os
import re
import json
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

def classify_series(series_body: pd.Series) -> pd.DataFrame:
    """Vectorized classification for high-throughput screening."""
    text_clean = series_body.fillna('').astype(str).str.strip()
    has_design = text_clean.str.contains(DESIGN_PATTERN)
    has_style = text_clean.str.contains(STYLE_PATTERN)
    short_style = has_style & (text_clean.str.len() < 60)
    
    is_di = has_design & (~short_style)
    
    lower = text_clean.str.lower()
    
    # Categorization
    is_dup = lower.str.contains(r'reuse|duplicat|redundan|already exists|reimplement')
    is_mod = lower.str.contains(r'module|layer|encapsulat|decouple|coupling|cohesion')
    is_abs = lower.str.contains(r'abstract|interface|generic|wrapper|over-engineer|overengineer')
    is_pat = lower.str.contains(r'pattern|repository|controller|refactor')
    
    categories = np.where(is_dup, 'Duplication/Reuse',
                 np.where(is_mod, 'Modularity & Layering',
                 np.where(is_abs, 'Abstraction & Extensibility',
                 np.where(is_pat, 'Architectural Patterns', 'General Design/Maintainability'))))
    
    categories = np.where(is_di, categories, 'None')
    
    return pd.DataFrame({
        'is_design_issue': is_di,
        'category': categories
    })

def main():
    base_dir = "/home/assassinaj602/Projects/CSC/Task2/TASK3/pilot"
    pr_parquet = os.path.join(base_dir, "data", "pull_request.parquet")
    comm_parquet = os.path.join(base_dir, "data", "pr_review_comments.parquet")
    out_dir = os.path.join(base_dir, "results")
    os.makedirs(out_dir, exist_ok=True)
    
    print("="*60)
    print("AIDev FULL-SCALE DATASET SCREENING PIPELINE")
    print("="*60)
    
    print("1. Loading PR data (agent mapping)...")
    pr_df = pd.read_parquet(pr_parquet, columns=['id', 'repo_url', 'number', 'agent', 'state'])
    pr_df['match_key'] = pr_df['repo_url'].str.replace('https://api.github.com/repos/', '', regex=False) + '#' + pr_df['number'].astype(str)
    pr_meta = pr_df.set_index('match_key')[['agent', 'state']]
    
    print("2. Loading review comments...")
    comm_df = pd.read_parquet(comm_parquet)
    total_raw = len(comm_df)
    print(f"Total raw review comments: {total_raw:,}")
    
    # Join agent metadata
    comm_df['match_key'] = comm_df['pull_request_url'].str.replace('https://api.github.com/repos/', '', regex=False).str.replace('/pulls/', '#', regex=False)
    comm_df = comm_df.join(pr_meta, on='match_key', how='left')
    comm_df['agent'] = comm_df['agent'].fillna('Unknown')
    
    # Pre-processing
    print("3. Pre-processing: Removing bots and noise...")
    comm_df['is_bot'] = comm_df['user'].astype(str).apply(is_bot)
    non_bot = comm_df[~comm_df['is_bot']].copy()
    bots_removed = total_raw - len(non_bot)
    print(f"Bots removed: {bots_removed:,} ({bots_removed/total_raw*100:.1f}%)")
    
    non_bot['is_noise'] = non_bot['body'].apply(is_noise_comment)
    substantive = non_bot[~non_bot['is_noise']].copy()
    noise_removed = len(non_bot) - len(substantive)
    print(f"Noise comments removed: {noise_removed:,} ({noise_removed/len(non_bot)*100:.1f}%)")
    print(f"Total substantive comments to screen: {len(substantive):,}")
    
    print("4. Executing high-throughput calibrated screening...")
    classified = classify_series(substantive['body'])
    substantive['is_design_issue'] = classified['is_design_issue'].values
    substantive['category'] = classified['category'].values
    
    di_df = substantive[substantive['is_design_issue']].copy()
    total_di = len(di_df)
    print(f"\nSCREENING COMPLETED:")
    print(f"Total Design Issues Identified: {total_di:,} ({total_di/len(substantive)*100:.2f}% of substantive comments)")
    
    # RQ1 Breakdown: Overall Category Distribution
    rq1_overall = di_df['category'].value_counts().to_dict()
    print("\n--- RQ1: Overall Category Distribution ---")
    for cat, cnt in rq1_overall.items():
        print(f"  • {cat:32s}: {cnt:6,d} ({cnt/total_di*100:.1f}%)")
        
    # RQ1 Breakdown: By Agent
    rq1_agent_crosstab = pd.crosstab(di_df['agent'], di_df['category'], margins=True)
    print("\n--- RQ1: Breakdown by AI Coding Agent ---")
    print(rq1_agent_crosstab)
    
    # Normalized DI Rate per 1,000 Review Comments by Agent
    agent_comm_totals = substantive['agent'].value_counts()
    agent_di_totals = di_df['agent'].value_counts()
    density_per_k = ((agent_di_totals / agent_comm_totals) * 1000).dropna().round(1)
    print("\n--- Design Issue Density (per 1,000 substantive review comments) ---")
    for agent, rate in density_per_k.items():
        print(f"  • {agent:15s}: {rate:5.1f} design issues / 1k comments (Total: {agent_di_totals.get(agent, 0):,})")
        
    # Save candidate gold dataset (parquet + sample CSV)
    save_cols = ['id', 'pull_request_url', 'path', 'user', 'agent', 'category', 'body', 'diff_hunk', 'created_at']
    gold_parquet = os.path.join(out_dir, "gold_candidate_design_issues.parquet")
    di_df[save_cols].to_parquet(gold_parquet, index=False)
    print(f"\nSaved full gold candidate corpus to: {gold_parquet}")
    
    # Save sample 200 for manual inspection / open coding
    sample_csv = os.path.join(out_dir, "gold_sample_200_for_coding.csv")
    di_df[save_cols].sample(n=min(200, len(di_df)), random_state=42).to_csv(sample_csv, index=False)
    print(f"Saved 200 representative gold cases for qualitative coding to: {sample_csv}")
    
    # Save empirical summary metrics for TOSEM paper
    findings_json = os.path.join(out_dir, "empirical_findings_full.json")
    with open(findings_json, 'w') as f:
        json.dump({
            "raw_comments_total": total_raw,
            "bots_filtered": bots_removed,
            "noise_filtered": noise_removed,
            "substantive_comments_total": len(substantive),
            "design_issues_total": total_di,
            "prevalence_rate_pct": round((total_di / len(substantive)) * 100, 2),
            "category_distribution": rq1_overall,
            "category_distribution_by_agent": pd.crosstab(di_df['agent'], di_df['category']).to_dict(),
            "density_per_k_comments": density_per_k.to_dict(),
            "agent_pr_state_crosstab": pd.crosstab(di_df['agent'], di_df['state']).to_dict()
        }, f, indent=2)
    print(f"Saved empirical findings JSON to: {findings_json}")

if __name__ == "__main__":
    main()

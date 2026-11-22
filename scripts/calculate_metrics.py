#!/usr/bin/env python3
"""
calculate_metrics.py
Calculates Cohen's Kappa (inter-rater agreement) and LLM screening validation metrics
in accordance with Rehman et al. (arXiv:2610.00905).
"""

import sys
import json
import argparse
from typing import List, Tuple

def compute_cohen_kappa(rater1: List[int], rater2: List[int]) -> float:
    """Computes Cohen's Kappa coefficient between two binary raters."""
    assert len(rater1) == len(rater2), "Rater sequences must have equal length."
    n = len(rater1)
    if n == 0:
        return 0.0

    # Contingency matrix
    # [ [00, 01], [10, 11] ]
    a = sum(1 for r1, r2 in zip(rater1, rater2) if r1 == 1 and r2 == 1)
    b = sum(1 for r1, r2 in zip(rater1, rater2) if r1 == 1 and r2 == 0)
    c = sum(1 for r1, r2 in zip(rater1, rater2) if r1 == 0 and r2 == 1)
    d = sum(1 for r1, r2 in zip(rater1, rater2) if r1 == 0 and r2 == 0)

    po = (a + d) / n  # Observed agreement
    p_yes = ((a + b) / n) * ((a + c) / n)
    p_no = ((c + d) / n) * ((b + d) / n)
    pe = p_yes + p_no  # Expected chance agreement

    if pe == 1.0:
        return 1.0
    kappa = (po - pe) / (1.0 - pe)
    return kappa

def compute_screening_metrics(ground_truth: List[int], predictions: List[int]) -> dict:
    """Computes screening performance metrics of automated LLM predictions vs Ground Truth."""
    assert len(ground_truth) == len(predictions)
    n = len(ground_truth)

    tp = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 1 and pred == 1)
    tn = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 0 and pred == 0)
    fp = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 0 and pred == 1)
    fn = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 1 and pred == 0)

    accuracy = (tp + tn) / n if n > 0 else 0.0
    agreement_rate = accuracy * 100.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "total_samples": n,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "agreement_rate_pct": round(agreement_rate, 2),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }

def main():
    parser = argparse.ArgumentParser(description="Calculate inter-rater reliability and automated agreement.")
    parser.add_argument("--test", action="store_true", help="Run self-test with sample synthetic distribution.")
    args = parser.parse_args()

    if args.test:
        print("Running verification test mimicking Rehman et al. (arXiv:2610.00905)...")
        # 500 samples, ~102 positive cases
        human1 = [1]*102 + [0]*398
        # Human 2 with minor variation (e.g. kappa ~ 0.82)
        human2 = [1]*95 + [0]*7 + [1]*5 + [0]*393
        kappa = compute_cohen_kappa(human1, human2)
        print(f"Computed Human-Human Cohen's Kappa: {kappa:.3f}")

        # LLM with 90.4% agreement rate (452 agreements, 48 disagreements)
        # 452 agree, 48 disagree
        llm = human1[:452] + [1 - x for x in human1[452:]]
        metrics = compute_screening_metrics(human1, llm)
        print("LLM vs Ground Truth Screening Metrics:")
        print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()

"""
stats_engine.py
Consensus math and leaderboard logic for CodexMatrix.
"""
from typing import Dict

def compute_consensus_scores(review_results: Dict) -> Dict:
    """
    Aggregate rubric scores for each model across all problems/languages.
    Returns a leaderboard DataFrame-like dict.
    """
    import pandas as pd
    scores = {}
    for problem, langs in review_results.items():
        for lang, reviewers in langs.items():
            for reviewer, reviewees in reviewers.items():
                for reviewee, rubric_scores in reviewees.items():
                    if reviewee not in scores:
                        scores[reviewee] = {r: [] for r in rubric_scores}
                    for r, v in rubric_scores.items():
                        scores[reviewee][r].append(v)
    # Compute averages
    leaderboard = {}
    for model, rubric_lists in scores.items():
        leaderboard[model] = {r: round(sum(vals)/len(vals), 2) if vals else 0 for r, vals in rubric_lists.items()}
    return leaderboard

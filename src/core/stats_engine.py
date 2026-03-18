"""
stats_engine.py - Real-Time Calculator Module
Focuses entirely on the current session Matrix.
Builds heatmaps, bar charts, and winner determination for the Current Session.
"""
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


RUBRIC = [
    "Syntactic Correctness",
    "Algorithmic Efficiency",
    "Readability & Documentation",
    "Edge-Case Handling",
    "Security Vulnerabilities"
]


def build_review_matrix(review_results: Dict) -> pd.DataFrame:
    """
    Build a comprehensive M x M matrix showing which model reviewed which model
    and what scores they gave.
    
    Args:
        review_results: Dict from judge_matrix.py with structure:
            {problem: {language: {reviewer: {reviewee: rubric_scores}}}}
    
    Returns:
        DataFrame: M (models) x N (metrics) with aggregated scores
    """
    aggregated_scores = {}
    
    # Aggregate all scores for each model
    for problem, langs in review_results.items():
        for lang, reviewers in langs.items():
            for reviewer, reviewees in reviewers.items():
                for reviewee, rubric_scores in reviewees.items():
                    if reviewee not in aggregated_scores:
                        aggregated_scores[reviewee] = {r: [] for r in RUBRIC}
                    
                    for rubric, score in rubric_scores.items():
                        aggregated_scores[reviewee][rubric].append(score)
    
    # Calculate averages
    leaderboard = {}
    for model, rubric_lists in aggregated_scores.items():
        leaderboard[model] = {
            r: round(sum(vals) / len(vals), 2) if vals else 0 
            for r, vals in rubric_lists.items()
        }
    
    return pd.DataFrame(leaderboard).T


def get_overall_winner(leaderboard_df: pd.DataFrame) -> Tuple[str, float]:
    """
    Determine the session winner based on average score across all rubrics.
    
    Args:
        leaderboard_df: DataFrame from build_review_matrix()
    
    Returns:
        Tuple: (model_name, average_score)
    """
    if leaderboard_df.empty:
        return None, 0
    
    leaderboard_df['Overall'] = leaderboard_df.mean(axis=1)
    winner = leaderboard_df['Overall'].idxmax()
    score = round(leaderboard_df.loc[winner, 'Overall'], 2)
    
    return winner, score


def build_heatmap_data(review_results: Dict, metric: str = "Algorithmic Efficiency") -> np.ndarray:
    """
    Build a heatmap showing how each model (reviewer) scored each model (reviewee)
    on a specific metric.
    
    Args:
        review_results: Review results dict
        metric: The rubric criterion to visualize (e.g., "Algorithmic Efficiency")
    
    Returns:
        numpy array: M x M matrix where rows=reviewers, cols=reviewees
    """
    models_set = set()
    scores_by_pair = {}
    
    # Collect all models and build pair-wise scores
    for problem, langs in review_results.items():
        for lang, reviewers in langs.items():
            for reviewer, reviewees in reviewers.items():
                models_set.add(reviewer)
                for reviewee, rubric_scores in reviewees.items():
                    models_set.add(reviewee)
                    key = (reviewer, reviewee)
                    if key not in scores_by_pair:
                        scores_by_pair[key] = []
                    
                    if metric in rubric_scores:
                        scores_by_pair[key].append(rubric_scores[metric])
    
    models_list = sorted(list(models_set))
    n = len(models_list)
    
    # Build matrix
    matrix = np.zeros((n, n))
    for i, reviewer in enumerate(models_list):
        for j, reviewee in enumerate(models_list):
            key = (reviewer, reviewee)
            if key in scores_by_pair:
                scores = scores_by_pair[key]
                matrix[i, j] = round(sum(scores) / len(scores), 2)
    
    return matrix, models_list


def build_rubric_comparison(leaderboard_df: pd.DataFrame, top_n: int = 3) -> Dict:
    """
    Build detailed rubric comparison for top N models.
    
    Args:
        leaderboard_df: DataFrame from build_review_matrix()
        top_n: Number of top models to include
    
    Returns:
        Dict with top models and their scores per rubric
    """
    # Calculate overall scores
    leaderboard_df['Overall'] = leaderboard_df.mean(axis=1)
    top_models = leaderboard_df.nlargest(top_n, 'Overall')
    
    return top_models.drop('Overall', axis=1).to_dict('index')


def compute_consus_scores(review_results: Dict) -> Dict:
    """
    Aggregate rubric scores for each model across all problems/languages.
    Returns a leaderboard dict with all metrics.
    
    Args:
        review_results: Full review results from judge_matrix.py
    
    Returns:
        Dict: {model: {rubric1: score, rubric2: score, ...}}
    """
    scores = {}
    
    for problem, langs in review_results.items():
        for lang, reviewers in langs.items():
            for reviewer, reviewees in reviewers.items():
                for reviewee, rubric_scores in reviewees.items():
                    if reviewee not in scores:
                        scores[reviewee] = {r: [] for r in rubric_scores.keys()}
                    
                    for r, v in rubric_scores.items():
                        scores[reviewee][r].append(v)
    
    # Compute averages
    leaderboard = {}
    for model, rubric_lists in scores.items():
        leaderboard[model] = {
            r: round(sum(vals) / len(vals), 2) if vals else 0 
            for r, vals in rubric_lists.items()
        }
    
    return leaderboard


def generate_summary_stats(session_data: Dict, review_results: Dict) -> Dict:
    """
    Generate summary statistics for the entire session.
    
    Args:
        session_data: Session configuration
        review_results: All review results
    
    Returns:
        Dict with session summary stats
    """
    return {
        "total_problems": len(session_data.get("problems", [])),
        "total_models": len(session_data.get("models", [])),
        "total_languages": len(session_data.get("languages", [])),
        "total_reviews": sum(
            len(reviewees) 
            for problem in review_results.values()
            for lang in problem.values()
            for reviewees in lang.values()
            for _ in reviewees.values()
        ),
        "rubric_size": 5  # Number of criteria in rubric
    }


if __name__ == "__main__":
    # Test with mock data
    from src.judge_matrix import peer_review_matrix
    from src.requester import generate_code_parallel
    
    print("Stats Engine Ready")

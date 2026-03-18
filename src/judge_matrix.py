"""
judge_matrix.py
Peer-review matrix logic for CodexMatrix.
"""
from typing import Dict, List

RUBRIC = [
    "Syntactic Correctness",
    "Algorithmic Efficiency",
    "Readability & Documentation",
    "Edge-Case Handling",
    "Security Vulnerabilities"
]

def peer_review_matrix(gen_results: Dict, models: List[str]) -> Dict:
    """
    Simulate peer review: Each model reviews all others for each problem/language.
    Returns nested dict: {problem: {language: {reviewer: {reviewee: rubric_scores}}}}
    """
    import random
    reviews = {}
    for problem, langs in gen_results.items():
        reviews[problem] = {}
        for lang, model_codes in langs.items():
            reviews[problem][lang] = {}
            for reviewer in models:
                reviews[problem][lang][reviewer] = {}
                for reviewee in models:
                    scores = {r: random.randint(1, 5) for r in RUBRIC}
                    reviews[problem][lang][reviewer][reviewee] = scores
    return reviews

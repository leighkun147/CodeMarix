"""
data_sanitizer.py - Internal Cleanup Module
Converts raw JSON responses from AI APIs into clean Python dictionaries.
Handles errors, missing fields, and standardizes output format.
"""
import json
from typing import Dict, Any, List, Optional


def sanitize_code_generation(raw_response: str, model: str, problem: str, language: str) -> Dict[str, Any]:
    """
    Sanitize raw API response from code generation into a clean dict.
    
    Args:
        raw_response: Raw text or JSON from API
        model: Name of the model (e.g., "GPT-4o")
        problem: The coding problem asked
        language: Programming language requested
        
    Returns:
        Clean dict with keys: {code, model, problem, language, timestamp, valid}
    """
    import datetime
    
    result = {
        "code": "",
        "model": model,
        "problem": problem,
        "language": language,
        "timestamp": datetime.datetime.now().isoformat(),
        "valid": False,
        "error": None
    }
    
    if not raw_response or not isinstance(raw_response, str):
        result["error"] = "Invalid response format"
        return result
    
    try:
        # Try parsing as JSON first (for structured API responses)
        if raw_response.strip().startswith('{'):
            parsed = json.loads(raw_response)
            result["code"] = parsed.get("code", parsed.get("content", str(parsed)))
        else:
            # Plain text response
            result["code"] = raw_response
        
        # Validate the code
        if result["code"] and len(result["code"].strip()) > 0:
            result["valid"] = True
        else:
            result["error"] = "Empty code response"
            
    except json.JSONDecodeError:
        result["code"] = raw_response
        result["valid"] = True if len(raw_response.strip()) > 0 else False
        if not result["valid"]:
            result["error"] = "Empty response"
    except Exception as e:
        result["error"] = f"Parsing error: {str(e)}"
    
    return result


def sanitize_review_scores(raw_scores: Dict[str, Any], rubric: List[str]) -> Dict[str, int]:
    """
    Sanitize peer review scores into a clean dict.
    
    Args:
        raw_scores: Raw scores dict from API
        rubric: List of rubric criteria
        
    Returns:
        Clean dict with integer scores 1-5 for each rubric item
    """
    result = {}
    
    for criterion in rubric:
        score = raw_scores.get(criterion, 3)  # Default to 3/5 if missing
        
        # Ensure score is int between 1-5
        if isinstance(score, (int, float)):
            result[criterion] = max(1, min(5, int(score)))
        else:
            result[criterion] = 3
    
    return result


def sanitize_session_data(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean the entire session state before processing.
    
    Args:
        session_data: Full session state dict
        
    Returns:
        Validated and cleaned session data
    """
    cleaned = {
        "models": session_data.get("models", []),
        "languages": session_data.get("languages", []),
        "problems": session_data.get("problems", []),
        "api_keys": {},
        "errors": []
    }
    
    # Sanitize API keys (just ensure they're non-empty strings)
    for model, key in session_data.get("api_keys", {}).items():
        if isinstance(key, str) and key.strip():
            cleaned["api_keys"][model] = key.strip()
        else:
            cleaned["errors"].append(f"Invalid API key for {model}")
    
    # Sanitize problems (remove empty ones)
    cleaned["problems"] = [p.strip() for p in session_data.get("problems", []) if p.strip()]
    
    # Sanitize models and languages
    cleaned["models"] = [m for m in session_data.get("models", []) if m]
    cleaned["languages"] = [l for l in session_data.get("languages", []) if l]
    
    return cleaned


def format_code_for_display(code: str, language: str = "python") -> str:
    """
    Format code with basic syntax highlighting indicators for display.
    
    Args:
        code: Raw code string
        language: Programming language
        
    Returns:
        Formatted code (can be HTML or markdown)
    """
    # Add language hint for markdown code blocks
    return f"```{language}\n{code}\n```"


if __name__ == "__main__":
    # Test examples
    test_response = '{"code": "print(\'Hello\')"}'
    result = sanitize_code_generation(test_response, "GPT-4o", "Print hello world", "Python")
    print("Sanitized:", result)

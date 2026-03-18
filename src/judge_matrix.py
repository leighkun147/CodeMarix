"""
judge_matrix.py
Peer-review matrix with actual code grading logic for CodexMatrix.
Each model reviews every other model's code against a rubric.
"""
from typing import Dict, List, Optional
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


RUBRIC = [
    "Syntactic Correctness",
    "Algorithmic Efficiency",
    "Readability & Documentation",
    "Edge-Case Handling",
    "Security Vulnerabilities"
]

GRADING_PROMPT_TEMPLATE = """
You are an expert code reviewer. Grade the following {language} code solution for this problem:

PROBLEM: {problem}

CODE TO REVIEW:
```{language}
{code}
```

Rate the code on the following criteria (1-5 scale, where 1=Poor, 5=Excellent):

1. Syntactic Correctness - Does the code compile/run without syntax errors?
2. Algorithmic Efficiency - Is the algorithm optimal in terms of time and space complexity?
3. Readability & Documentation - Is the code well-written and documented?
4. Edge-Case Handling - Does it handle edge cases and boundary conditions?
5. Security Vulnerabilities - Are there any security issues or best practices violations?

IMPORTANT: You MUST respond with ONLY a valid JSON object, starting with {{ and ending with }}. Do not add any text before or after the JSON.

{{
    "Syntactic Correctness": 5,
    "Algorithmic Efficiency": 4,
    "Readability & Documentation": 4,
    "Edge-Case Handling": 3,
    "Security Vulnerabilities": 4
}}
"""

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    "openai": {"rpm": 3500, "min_delay": 0.3, "max_retries": 3},
    "anthropic": {"rpm": 50, "min_delay": 1.2, "max_retries": 3},
    "google": {"rpm": 15, "min_delay": 4.0, "max_retries": 5},  # Free tier: 15 RPM
    "deepseek": {"rpm": 60, "min_delay": 1.0, "max_retries": 3},
}


def _call_with_rate_limit_handling(api_func, prompt: str, api_key: str, model_name: str):
    """
    Call an API function with intelligent rate limit handling.
    Implements exponential backoff for 429 errors.
    
    Args:
        api_func: The API function to call (_grade_with_openai, etc.)
        prompt: The prompt to send
        api_key: The API key
        model_name: Name of the model (for rate limit config)
    
    Returns:
        Dict with grading scores
    
    Raises:
        RuntimeError: If all retries fail
    """
    # Determine which provider we're using
    if "claude" in model_name.lower():
        provider = "anthropic"
    elif "gemini" in model_name.lower():
        provider = "google"
    elif "deepseek" in model_name.lower():
        provider = "deepseek"
    else:
        provider = "openai"
    
    config = RATE_LIMIT_CONFIG.get(provider, RATE_LIMIT_CONFIG["openai"])
    min_delay = config["min_delay"]
    max_retries = config["max_retries"]
    
    # Initial delay before first attempt
    time.sleep(min_delay)
    
    last_error = None
    for attempt in range(max_retries):
        try:
            return api_func(prompt, api_key)
        except RuntimeError as e:
            error_str = str(e)
            last_error = e
            
            # Check if it's a rate limit error (429)
            if "429" in error_str or "rate limit" in error_str.lower() or "too many requests" in error_str.lower():
                if attempt < max_retries - 1:
                    # Exponential backoff: 4s, 8s, 16s, 32s
                    wait_time = min_delay * (2 ** attempt)
                    print(f"⏳ Rate limited (attempt {attempt + 1}/{max_retries}). Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError(f"Google free tier rate limit (15 RPM). Please wait a minute before retrying. Details: {error_str}")
            else:
                # Not a rate limit error, raise immediately
                raise
        except Exception as e:
            # Other errors, raise immediately
            raise
    
    # If we got here, raise the last error
    if last_error:
        raise last_error
    raise RuntimeError(f"Failed to grade with {model_name} after {max_retries} attempts")


def grade_code_with_api(code: str, problem: str, language: str, 
                       reviewer_model: str, api_key: str, use_mock: bool = False) -> Dict[str, int]:
    """
    Use an LLM API to grade code against the rubric.
    
    Args:
        code: The code to be graded
        problem: The coding problem description
        language: Programming language
        reviewer_model: Which model is doing the review
        api_key: API key for the reviewer model
        use_mock: If True, return mock grades
    
    Returns:
        Dict with scores for each rubric criterion
    
    Raises:
        ValueError: If API key is invalid or empty
        RuntimeError: If API call fails
    """
    if not api_key or not api_key.strip():
        raise ValueError(f"No API key provided for {reviewer_model}")
    
    if use_mock:
        # Mock grades for testing only
        import random
        return {r: random.randint(2, 5) for r in RUBRIC}
    
    prompt = GRADING_PROMPT_TEMPLATE.format(
        language=language,
        problem=problem,
        code=code
    )
    
    try:
        # Try OpenAI API first (Claude 3.5 Sonnet for grading, or GPT-4o)
        if "Claude" in reviewer_model or "claude" in reviewer_model:
            result = _call_with_rate_limit_handling(_grade_with_anthropic, prompt, api_key, reviewer_model)
        elif "Gemini" in reviewer_model or "gemini" in reviewer_model:
            result = _call_with_rate_limit_handling(_grade_with_google, prompt, api_key, reviewer_model)
        elif "DeepSeek" in reviewer_model or "deepseek" in reviewer_model:
            result = _call_with_rate_limit_handling(_grade_with_deepseek, prompt, api_key, reviewer_model)
        else:
            result = _call_with_rate_limit_handling(_grade_with_openai, prompt, api_key, reviewer_model)
        
        # Validate result
        if not result or not isinstance(result, dict):
            raise RuntimeError(f"Invalid response format from {reviewer_model}")
        
        return result
        
    except ValueError as e:
        raise RuntimeError(f"API Key Error ({reviewer_model}): {str(e)}")
    except requests.exceptions.Timeout:
        raise RuntimeError(f"API Timeout ({reviewer_model}): Request took too long")
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"Connection Error ({reviewer_model}): {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error grading with {reviewer_model}: {str(e)}")


def _extract_json_from_response(response_text: str, model_name: str) -> dict:
    """
    Robustly extract and parse JSON from LLM response.
    Handles various response formats with extra whitespace, text, etc.
    
    Args:
        response_text: Raw text from LLM API
        model_name: Name of model (for error messages)
    
    Returns:
        Parsed JSON dict
    
    Raises:
        RuntimeError: If JSON extraction/parsing fails
    """
    if not response_text or not isinstance(response_text, str):
        raise RuntimeError(f"{model_name}: Empty or invalid response")
    
    # Try to find and extract JSON
    response_text = response_text.strip()
    
    # Strategy 1: Find first { and last }
    json_start = response_text.find('{')
    json_end = response_text.rfind('}')
    
    if json_start == -1 or json_end == -1 or json_end <= json_start:
        raise RuntimeError(
            f"{model_name}: Could not find JSON in response\n"
            f"Response: {response_text[:200]}"
        )
    
    # Extract JSON substring and strip whitespace
    json_str = response_text[json_start:json_end + 1].strip()
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # Try removing leading/trailing whitespace more aggressively
        json_str_cleaned = json_str.replace('\n', ' ').replace('\r', ' ')
        try:
            return json.loads(json_str_cleaned)
        except json.JSONDecodeError:
            raise RuntimeError(
                f"{model_name}: Failed to parse JSON\n"
                f"Error: {str(e)}\n"
                f"Attempted: {json_str[:300]}"
            )


def _grade_with_google(prompt: str, api_key: str) -> Dict[str, int]:
    """Grade using Google Gemini API. Raises exception on invalid key."""
    if not api_key or not api_key.strip():
        raise ValueError("Google API key is empty")
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 401:
            raise ValueError("Google API key is invalid or expired (401 Unauthorized)")
        elif response.status_code == 403:
            raise ValueError("Google API key is forbidden (403 Forbidden)")
        elif response.status_code == 429:
            raise RuntimeError("Google API rate limit exceeded (429 - Too Many Requests)")
        elif response.status_code != 200:
            error_msg = response.json() if response.text else f"Status {response.status_code}"
            raise RuntimeError(f"Google API Error: {error_msg}")
        
        try:
            response_data = response.json()
            response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            raise RuntimeError(f"Unexpected Google API response format: {response.text[:200]}")
        
        # Extract and validate JSON
        scores_dict = _extract_json_from_response(response_text, "Google/Gemini")
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            if r not in scores_dict:
                raise RuntimeError(f"Google response missing criterion: {r}")
            score = int(scores_dict[r])
            result[r] = max(1, min(5, score))
        
        return result
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Google API request timed out (30s)")
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Google/Gemini API call failed: {str(e)}")


def _grade_with_deepseek(prompt: str, api_key: str) -> Dict[str, int]:
    """Grade using DeepSeek API (OpenAI-compatible). Raises exception on invalid key."""
    if not api_key or not api_key.strip():
        raise ValueError("DeepSeek API key is empty")
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-coder",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 500
        }
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers, json=payload, timeout=30
        )
        
        if response.status_code == 401:
            raise ValueError("DeepSeek API key is invalid or expired (401 Unauthorized)")
        elif response.status_code == 403:
            raise ValueError("DeepSeek API key is forbidden (403 Forbidden)")
        elif response.status_code == 429:
            raise RuntimeError("DeepSeek API rate limit exceeded (429 - Too Many Requests)")
        elif response.status_code != 200:
            error_msg = response.json().get("error", {}).get("message", f"Status {response.status_code}")
            raise RuntimeError(f"DeepSeek API Error: {error_msg}")
        
        response_text = response.json()["choices"][0]["message"]["content"]
        
        # Extract and validate JSON
        scores_dict = _extract_json_from_response(response_text, "DeepSeek")
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            if r not in scores_dict:
                raise RuntimeError(f"DeepSeek response missing criterion: {r}")
            score = int(scores_dict[r])
            result[r] = max(1, min(5, score))
        
        return result
        
    except requests.exceptions.Timeout:
        raise RuntimeError("DeepSeek API request timed out (30s)")
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"DeepSeek API call failed: {str(e)}")



def _grade_with_openai(prompt: str, api_key: str) -> Dict[str, int]:
    """Grade using OpenAI API. Raises exception on invalid key."""
    if not api_key or not api_key.strip():
        raise ValueError("OpenAI API key is empty")
    
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 500
        }
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                headers=headers, json=payload, timeout=30)
        
        if response.status_code == 401:
            raise ValueError("OpenAI API key is invalid or expired (401 Unauthorized)")
        elif response.status_code == 403:
            raise ValueError("OpenAI API key is forbidden (403 Forbidden)")
        elif response.status_code == 429:
            raise RuntimeError("OpenAI API rate limit exceeded (429 - Too Many Requests)")
        elif response.status_code != 200:
            error_msg = response.json().get("error", {}).get("message", f"Status {response.status_code}")
            raise RuntimeError(f"OpenAI API Error: {error_msg}")
        
        response_text = response.json()["choices"][0]["message"]["content"]
        
        # Extract and validate JSON using robust parsing
        scores_dict = _extract_json_from_response(response_text, "OpenAI")
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            if r not in scores_dict:
                raise RuntimeError(f"OpenAI response missing criterion: {r}")
            score = int(scores_dict[r])
            result[r] = max(1, min(5, score))
        
        return result
        
    except requests.exceptions.Timeout:
        raise RuntimeError("OpenAI API request timed out (30s)")
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {str(e)}")


def _grade_with_anthropic(prompt: str, api_key: str) -> Dict[str, int]:
    """Grade using Anthropic API. Raises exception on invalid key."""
    if not api_key or not api_key.strip():
        raise ValueError("Anthropic API key is empty")
    
    try:
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.anthropic.com/v1/messages",
                                headers=headers, json=payload, timeout=30)
        
        if response.status_code == 401:
            raise ValueError("Anthropic API key is invalid or expired (401 Unauthorized)")
        elif response.status_code == 403:
            raise ValueError("Anthropic API key is forbidden (403 Forbidden)")
        elif response.status_code == 429:
            raise RuntimeError("Anthropic API rate limit exceeded (429 - Too Many Requests)")
        elif response.status_code != 200:
            error_msg = response.json().get("error", {}).get("message", f"Status {response.status_code}")
            raise RuntimeError(f"Anthropic API Error: {error_msg}")
        
        response_text = response.json()["content"][0]["text"]
        
        # Extract and validate JSON using robust parsing
        scores_dict = _extract_json_from_response(response_text, "Anthropic")
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            if r not in scores_dict:
                raise RuntimeError(f"Anthropic response missing criterion: {r}")
            score = int(scores_dict[r])
            result[r] = max(1, min(5, score))
        
        return result
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Anthropic API request timed out (30s)")
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Anthropic API call failed: {str(e)}")


def peer_review_matrix(gen_results: Dict, models: List[str], api_keys: Dict[str, str] = None,
                      use_mock: bool = False) -> Dict:
    """
    Create peer review matrix: Each model reviews all others' code.
    Uses parallel execution for efficiency.
    
    IMPORTANT: For research purposes, this uses REAL API calls with provided keys.
    Invalid keys will raise clear error messages - no silent fallbacks!
    
    Args:
        gen_results: Output from requester.py with structure:
                    {problem: {language: {model: {code, model, problem, language, valid}}}}
        models: List of model names
        api_keys: Dict mapping models to API keys for grading
        use_mock: If True, use mock grades for testing (not recommended for research)
    
    Returns:
        Dict: {problem: {language: {reviewer: {reviewee: rubric_scores}}}}
    
    Raises:
        ValueError: If API keys are invalid or missing
        RuntimeError: If API calls fail
    """
    if api_keys is None:
        api_keys = {}
    
    # Validate API keys upfront only if not in mock mode
    if not use_mock:
        missing_keys = [m for m in models if not api_keys.get(m, "").strip()]
        if missing_keys:
            raise ValueError(f"Missing API keys for research mode: {', '.join(missing_keys)}")
    
    reviews = {}
    tasks = []
    
    # Prepare all review tasks
    for problem, langs in gen_results.items():
        reviews[problem] = {}
        for lang, model_codes in langs.items():
            reviews[problem][lang] = {}
            
            for reviewer in models:
                reviews[problem][lang][reviewer] = {}
                
                for reviewee in models:
                    # Get the code to review
                    code_entry = model_codes.get(reviewee, {})
                    code = code_entry.get("code", "")
                    
                    if not code or not code_entry.get("valid", False):
                        # Skip reviewing invalid code
                        reviews[problem][lang][reviewer][reviewee] = {r: 0 for r in RUBRIC}
                        continue
                    
                    # Add task for this code review
                    tasks.append((problem, lang, reviewer, reviewee, code))
    
    # Execute reviews in parallel
    errors = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for problem, lang, reviewer, reviewee, code in tasks:
            future = executor.submit(
                grade_code_with_api,
                code, problem, lang, reviewer, 
                api_keys.get(reviewer, ""), use_mock
            )
            futures[future] = (problem, lang, reviewer, reviewee)
        
        # Collect results
        for future in as_completed(futures):
            problem, lang, reviewer, reviewee = futures[future]
            try:
                scores = future.result()
                reviews[problem][lang][reviewer][reviewee] = scores
            except ValueError as e:
                error_msg = f"[RESEARCH ERROR] Invalid API key for {reviewer}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
            except RuntimeError as e:
                error_msg = f"[RESEARCH ERROR] {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
            except Exception as e:
                error_msg = f"[RESEARCH ERROR] Unexpected error: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
    
    # If we had errors, report them
    if errors:
        raise RuntimeError(
            f"Peer review failed with {len(errors)} error(s):\n" + 
            "\n".join(errors) + 
            "\n\nFor research purposes, all API keys must be valid and models must have sufficient quota."
        )
    
    return reviews

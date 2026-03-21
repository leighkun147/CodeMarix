"""
judge_matrix.py
Peer-review matrix with comprehensive code grading logic for CodexMatrix.
Each model reviews every other model's code against an advanced rubric.
"""
from typing import Dict, List, Optional
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# Comprehensive benchmarking rubric (1-5 scale)
RUBRIC = [
    "Correctness & Accuracy",       # Does it produce correct output?
    "Efficiency (Time)",             # Optimal time complexity?
    "Efficiency (Space)",            # Optimal space/memory usage?
    "Readability & Clear Code",      # Easy to understand & maintain?
    "Documentation & Comments",      # Well-documented?
    "Edge-Case Handling",            # Handles corner cases properly?
    "Error Handling & Robustness",   # Graceful error management?
    "Security & Safe Practices",     # Avoids vulnerabilities?
    "Code Simplicity",               # Avoids unnecessary complexity?
    "Best Practices & Standards"     # Follows language conventions?
]

GRADING_PROMPT_TEMPLATE = """
You are an expert code reviewer grading across 10 dimensions.
Grade the following {language} code solution STRICTLY on 1-5 scale.

PROBLEM: {problem}

CODE TO REVIEW:
```{language}
{code}
```

Rate the code on EACH criterion below (1=Poor, 5=Excellent). Respond with ONLY a valid JSON object with no additional text:

{{
  "1": 5,
  "2": 4,
  "3": 4,
  "4": 4,
  "5": 3,
  "6": 4,
  "7": 3,
  "8": 5,
  "9": 4,
  "10": 4
}}

WHERE:
1 = Correctness & Accuracy
2 = Efficiency (Time)
3 = Efficiency (Space)
4 = Readability & Clear Code
5 = Documentation & Comments
6 = Edge-Case Handling
7 = Error Handling & Robustness
8 = Security & Safe Practices
9 = Code Simplicity
10 = Best Practices & Standards
"""

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    "openai": {"rpm": 3500, "min_delay": 0.3, "max_retries": 3},
    "anthropic": {"rpm": 50, "min_delay": 1.2, "max_retries": 3},
    "google": {"rpm": 15, "min_delay": 4.0, "max_retries": 5},  # Free tier: 15 RPM
    "groq": {"rpm": 30, "min_delay": 0.5, "max_retries": 3},  # Groq free tier: generous
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
    elif "groq" in model_name.lower():
        provider = "groq"
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
        elif "Groq" in reviewer_model or "groq" in reviewer_model:
            result = _call_with_rate_limit_handling(_grade_with_groq, prompt, api_key, reviewer_model)
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


def _normalize_json_keys(scores_dict: dict) -> dict:
    """
    Normalize dictionary keys by mapping numeric indices to RUBRIC criteria.
    Also handles string keys with criterion names for backward compatibility.
    
    Args:
        scores_dict: Raw dictionary from JSON parse
    
    Returns:
        Normalized dictionary with RUBRIC keys
    
    Raises:
        RuntimeError: If keys cannot be mapped to RUBRIC
    """
    if not isinstance(scores_dict, dict):
        raise RuntimeError(f"Expected dict, got {type(scores_dict)}: {str(scores_dict)[:200]}")
    
    normalized = {}
    
    # Try numeric key mapping first (new format: "1", "2", etc.)
    numeric_indices = {}
    for key, value in scores_dict.items():
        try:
            # Try to convert key to integer
            idx = int(str(key).strip('"\''))
            if 1 <= idx <= len(RUBRIC):
                numeric_indices[idx] = value
        except (ValueError, TypeError):
            pass
    
    # If we got all 10 numeric keys, use them
    if len(numeric_indices) == 10:
        for idx in range(1, 11):
            normalized[RUBRIC[idx - 1]] = numeric_indices[idx]
        return normalized
    
    # Fallback: try string key matching (old format with criterion names)
    rubric_normalized = {r.strip().lower(): r for r in RUBRIC}
    
    for key, value in scores_dict.items():
        # Strip whitespace, newlines, and quotes from key
        clean_key = key.strip().lower() if isinstance(key, str) else str(key).strip().lower()
        # Remove any quotes that might be in the key
        clean_key = clean_key.strip('\'"').strip()
        
        # Find matching RUBRIC entry
        if clean_key in rubric_normalized:
            actual_key = rubric_normalized[clean_key]
            normalized[actual_key] = value
        else:
            # Try fuzzy matching for partial matches
            found = False
            for rubric_key in rubric_normalized.keys():
                if rubric_key in clean_key or clean_key in rubric_key:
                    actual_key = rubric_normalized[rubric_key]
                    normalized[actual_key] = value
                    found = True
                    break
    
    return normalized


def _extract_json_from_response(response_text: str, model_name: str) -> dict:
    """
    Robustly extract and parse JSON from LLM response.
    Handles various response formats with extra whitespace, text, etc.
    
    Args:
        response_text: Raw text from LLM API
        model_name: Name of model (for error messages)
    
    Returns:
        Parsed JSON dict with normalized keys
    
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
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        # Try removing leading/trailing whitespace more aggressively
        json_str_cleaned = json_str.replace('\n', ' ').replace('\r', ' ')
        try:
            parsed = json.loads(json_str_cleaned)
        except json.JSONDecodeError:
            # Last resort: try to repair common JSON issues
            try:
                # Replace newlines with spaces in keys
                json_str_repaired = json_str
                # Try to find and fix quoted strings with internal newlines
                import re
                json_str_repaired = re.sub(r'"\s*\n\s*"', '", "', json_str_repaired)
                parsed = json.loads(json_str_repaired)
            except Exception:
                raise RuntimeError(
                    f"{model_name}: Failed to parse JSON\n"
                    f"Error: {str(e)}\n"
                    f"Attempted: {json_str[:300]}"
                )
    
    if not isinstance(parsed, dict):
        raise RuntimeError(f"{model_name}: JSON parsed but is not a dict, got {type(parsed)}")
    
    # Normalize keys to match RUBRIC exactly
    try:
        normalized = _normalize_json_keys(parsed)
    except Exception as e:
        raise RuntimeError(
            f"{model_name}: Failed to normalize keys\n"
            f"Error: {str(e)}\n"
            f"Parsed keys: {list(parsed.keys())}"
        )
    
    return normalized


def _grade_with_google(prompt: str, api_key: str) -> Dict[str, int]:
    """Grade using Google Gemini API. Raises exception on invalid key."""
    if not api_key or not api_key.strip():
        raise ValueError("Google API key is empty")
    
    try:
        # Try gemini-2.0-flash first
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 500
            }
        }
        response = requests.post(url, json=payload, timeout=30)
        
        # If 400 or 404, try fallback to gemini-1.5-flash
        if response.status_code in [400, 404]:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
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
        
        # Validate all required criteria are present
        missing_keys = [r for r in RUBRIC if r not in scores_dict]
        if missing_keys:
            raise RuntimeError(
                f"Google response missing {len(missing_keys)} criteria: {', '.join(missing_keys)}\n"
                f"Found keys: {list(scores_dict.keys())}"
            )
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            try:
                score = int(scores_dict[r])
                result[r] = max(1, min(5, score))
            except (ValueError, TypeError) as e:
                raise RuntimeError(f"Invalid score for {r}: {scores_dict[r]} (expected 1-5 integer)")
        
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
        
        # Validate all required criteria are present
        missing_keys = [r for r in RUBRIC if r not in scores_dict]
        if missing_keys:
            raise RuntimeError(
                f"DeepSeek response missing {len(missing_keys)} criteria: {', '.join(missing_keys)}\n"
                f"Found keys: {list(scores_dict.keys())}"
            )
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            try:
                score = int(scores_dict[r])
                result[r] = max(1, min(5, score))
            except (ValueError, TypeError) as e:
                raise RuntimeError(f"Invalid score for {r}: {scores_dict[r]} (expected 1-5 integer)")
        
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
        
        # Validate all required criteria are present
        missing_keys = [r for r in RUBRIC if r not in scores_dict]
        if missing_keys:
            raise RuntimeError(
                f"OpenAI response missing {len(missing_keys)} criteria: {', '.join(missing_keys)}\n"
                f"Found keys: {list(scores_dict.keys())}"
            )
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            try:
                score = int(scores_dict[r])
                result[r] = max(1, min(5, score))
            except (ValueError, TypeError) as e:
                raise RuntimeError(f"Invalid score for {r}: {scores_dict[r]} (expected 1-5 integer)")
        
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
        
        # Validate all required criteria are present
        missing_keys = [r for r in RUBRIC if r not in scores_dict]
        if missing_keys:
            raise RuntimeError(
                f"Anthropic response missing {len(missing_keys)} criteria: {', '.join(missing_keys)}\n"
                f"Found keys: {list(scores_dict.keys())}"
            )
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            try:
                score = int(scores_dict[r])
                result[r] = max(1, min(5, score))
            except (ValueError, TypeError) as e:
                raise RuntimeError(f"Invalid score for {r}: {scores_dict[r]} (expected 1-5 integer)")
        
        return result
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Anthropic API request timed out (30s)")
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Anthropic API call failed: {str(e)}")


def _grade_with_groq(prompt: str, api_key: str) -> Dict[str, int]:
    """Grade using Groq API. Raises exception on invalid key."""
    if not api_key or not api_key.strip():
        raise ValueError("Groq API key is empty")
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 500
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                headers=headers, json=payload, timeout=30)
        
        if response.status_code == 401:
            raise ValueError("Groq API key is invalid or expired (401 Unauthorized)")
        elif response.status_code == 403:
            raise ValueError("Groq API key is forbidden (403 Forbidden)")
        elif response.status_code == 429:
            raise RuntimeError("Groq API rate limit exceeded (429 - Too Many Requests)")
        elif response.status_code == 400:
            error_detail = response.json() if response.text else "Bad Request"
            raise RuntimeError(f"Groq API Error 400 (Bad Request): {error_detail}")
        elif response.status_code != 200:
            error_msg = response.json().get("error", {}).get("message", f"Status {response.status_code}")
            raise RuntimeError(f"Groq API Error: {error_msg}")
        
        response_text = response.json()["choices"][0]["message"]["content"]
        
        # Extract and validate JSON using robust parsing
        scores_dict = _extract_json_from_response(response_text, "Groq")
        
        # Validate all required criteria are present
        missing_keys = [r for r in RUBRIC if r not in scores_dict]
        if missing_keys:
            raise RuntimeError(
                f"Groq response missing {len(missing_keys)} criteria: {', '.join(missing_keys)}\n"
                f"Found keys: {list(scores_dict.keys())}"
            )
        
        # Validate and normalize scores
        result = {}
        for r in RUBRIC:
            try:
                score = int(scores_dict[r])
                result[r] = max(1, min(5, score))
            except (ValueError, TypeError) as e:
                raise RuntimeError(f"Invalid score for {r}: {scores_dict[r]} (expected 1-5 integer)")
        
        return result
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Groq API request timed out (30s)")
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Groq API call failed: {str(e)}")


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

"""
requester.py
Parallel code generation with actual API calls for CodexMatrix.
Supports OpenAI, Anthropic, Google, and other LLM providers.
"""
from typing import List, Dict, Optional
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed



def call_openai_api(problem: str, language: str, api_key: str) -> str:
    """Call OpenAI API (GPT-4o, GPT-4 Turbo, etc.) for code generation."""
    try:

        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "gpt-4o",
            "messages": [{
                "role": "user",
                "content": f"Write a {language} solution for: {problem}\nReturn only the code, no explanations."
            }],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                                headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"# OpenAI API Error: {response.status_code}"
    except Exception as e:
        return f"# Error calling OpenAI: {str(e)}"


def call_anthropic_api(problem: str, language: str, api_key: str) -> str:
    """Call Anthropic API (Claude models) for code generation."""
    try:
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        payload = {
            "model": "claude-3-5-sonnet",
            "max_tokens": 1000,
            "messages": [{
                "role": "user",
                "content": f"Write a {language} solution for: {problem}\nReturn only the code, no explanations."
            }]
        }
        response = requests.post("https://api.anthropic.com/v1/messages",
                                headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            return f"# Anthropic API Error: {response.status_code}"
    except Exception as e:
        return f"# Error calling Anthropic: {str(e)}"


def call_google_api(problem: str, language: str, api_key: str) -> str:
    """Call Google API (Gemini models) for code generation."""
    try:
        # Try gemini-2.0-flash first, fall back to gemini-1.5-flash if needed
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Write a {language} solution for: {problem}\nReturn only the code, no explanations."
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        elif response.status_code == 400:
            # Try fallback to gemini-1.5-flash
            url_fallback = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            response_fallback = requests.post(url_fallback, json=payload, timeout=30)
            if response_fallback.status_code == 200:
                return response_fallback.json()["candidates"][0]["content"]["parts"][0]["text"]
            else:
                error_msg = response_fallback.json().get("error", {}).get("message", "Unknown error")
                return f"# Google API Error: {response_fallback.status_code} - {error_msg}"
        else:
            error_msg = response.json().get("error", {}).get("message", f"Status {response.status_code}") if response.text else f"Status {response.status_code}"
            return f"# Google API Error: {response.status_code} - {error_msg}"
    except Exception as e:
        return f"# Error calling Google: {str(e)}"


def call_deepseek_api(problem: str, language: str, api_key: str) -> str:
    """Call DeepSeek API (OpenAI-compatible) for code generation."""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-coder",
            "messages": [{
                "role": "user",
                "content": f"Write a {language} solution for: {problem}\nReturn only the code, no explanations."
            }],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        response = requests.post("https://api.deepseek.com/chat/completions",
                                headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"# DeepSeek API Error: {response.status_code}"
    except Exception as e:
        return f"# Error calling DeepSeek: {str(e)}"


def call_groq_api(problem: str, language: str, api_key: str, model: str = "llama-3.3-70b-versatile") -> str:
    """Call Groq API (LLaMA, Mixtral) for code generation."""
    try:
        # Map friendly names to Groq model IDs
        model_mapping = {
            "llama-3.1-70b": "llama-3.3-70b-versatile",
            "llama-3.1": "llama-3.3-70b-versatile",
            "mixtral": "mixtral-8x7b-32768",
            "llama-3-8b": "llama3-8b-8192",
        }
        
        # Extract model ID from the model name
        groq_model = "llama-3.3-70b-versatile"  # Default
        for key, value in model_mapping.items():
            if key in model.lower():
                groq_model = value
                break
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": groq_model,
            "messages": [{
                "role": "user",
                "content": f"Write a {language} solution for: {problem}\nReturn only the code, no explanations."
            }],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            # Return more detailed error info for debugging
            try:
                error_detail = response.json()
                return f"# Groq API Error: {response.status_code} - {error_detail}"
            except:
                return f"# Groq API Error: {response.status_code} - {response.text[:200]}"
    except Exception as e:
        return f"# Error calling Groq: {str(e)}"


def get_api_caller(model: str):
    """
    Return the appropriate API caller function for a given model.
    
    Args:
        model: Model name (e.g., "GPT-4o", "Claude 3.5 Sonnet", "Gemini 1.0 Pro", "Groq - Llama 3.1 70B")
    
    Returns:
        Function to call the appropriate API
    """
    if "GPT" in model or "gpt" in model:
        return call_openai_api
    elif "Claude" in model or "claude" in model:
        return call_anthropic_api
    elif "Gemini" in model or "gemini" in model:
        return call_google_api
    elif "Groq" in model or "groq" in model:
        return (lambda p, l, k: call_groq_api(p, l, k, model))
    elif "DeepSeek" in model or "deepseek" in model:
        return call_deepseek_api
    else:
        return None


def call_model_api(problem: str, language: str, model: str, api_key: str, use_mock: bool = False) -> str:
    """
    Call the appropriate API for a given model.
    
    Args:
        problem: Coding problem description
        language: Programming language
        model: Model name
        api_key: API authentication key
        use_mock: If True, return mock data instead of calling API
    
    Returns:
        Generated code string
    """
    if use_mock or not api_key:
        # Mock response for testing
        return f"# {language} solution for '{problem}' by {model}\n# Test code\nprint('Hello World')"
    
    caller = get_api_caller(model)
    if not caller:
        return f"# Unknown model: {model}"
    
    return caller(problem, language, api_key)


def generate_code_parallel(problems: List[str], languages: List[str], models: List[str], 
                          api_keys: Dict[str, str], use_mock: bool = False, max_workers: int = 5) -> Dict:
    """
    Generate code in parallel for each problem, language, and model.
    Uses ThreadPoolExecutor for concurrent API calls.
    
    Args:
        problems: List of coding problems
        languages: List of programming languages
        models: List of AI models to use
        api_keys: Dict mapping model names to API keys
        use_mock: If True, use mock data instead of actual API calls
        max_workers: Maximum concurrent threads
    
    Returns:
        Nested dict: {problem: {language: {model: {code, model, problem, language, valid}}}}
    """
    from src.utils.data_sanitizer import sanitize_code_generation
    
    results = {}
    
    # Define all tasks
    tasks = []
    for problem in problems:
        results[problem] = {}
        for lang in languages:
            results[problem][lang] = {}
            for model in models:
                tasks.append((problem, lang, model, api_keys.get(model, "")))
    
    # Execute in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for problem, lang, model, api_key in tasks:
            future = executor.submit(
                call_model_api, 
                problem, lang, model, api_key, use_mock
            )
            futures[future] = (problem, lang, model)
        
        # Collect results
        for future in as_completed(futures):
            problem, lang, model = futures[future]
            try:
                code = future.result()
                # Sanitize the response
                sanitized = sanitize_code_generation(code, model, problem, lang)
                results[problem][lang][model] = sanitized
            except Exception as e:
                results[problem][lang][model] = {
                    "code": "",
                    "model": model,
                    "problem": problem,
                    "language": lang,
                    "valid": False,
                    "error": str(e)
                }
    
    return results

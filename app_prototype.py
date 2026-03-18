"""
CodexMatrix Prototype - Streamlit App
A detailed, working prototype for decentralized AI benchmarking.
"""
import streamlit as st
from src.requester import generate_code_parallel
from src.judge_matrix import peer_review_matrix
from src.stats_engine import compute_consensus_scores
import os

st.set_page_config(page_title="CodexMatrix Benchmark", layout="wide")
st.title("⚔️ CodexMatrix: The $M^2$ Autonomous AI Benchmarking Engine")

st.sidebar.header("Session Setup")
st.sidebar.subheader("Enter up to 5 coding challenges:")
problem_inputs = []
for i in range(5):
    prob = st.sidebar.text_input(f"Problem {i+1}", "", key=f"problem_{i+1}")
    if prob.strip():
        problem_inputs.append(prob.strip())
problems = "\n".join(problem_inputs)
languages = st.sidebar.multiselect("Select Languages", ["Python", "C", "C++", "Rust", "Go", "Java", "JavaScript", "TypeScript", "Kotlin", "Swift", "Ruby", "PHP", "Scala", "Haskell", "Julia"])
models = st.sidebar.multiselect("Select Codex Models", ["GPT-4o", "Claude 3.5 Sonnet", "Gemini 1.5 Pro", "DeepSeek-Coder-V2", "Codestral", "Llama 3 / CodeLlama", "Qwen-Coder", "StarCoder2", "Grok-1", "GitHub Copilot API"])

# Initialize session state for API keys
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {}

# API Key Input Section
if models:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 API Keys (stored in RAM only)")
    for model in models:
        api_key = st.sidebar.text_input(f"{model} API Key", type="password", key=f"api_key_{model}")
        st.session_state.api_keys[model] = api_key
    st.sidebar.info("✓ Keys are stored in RAM and never saved to disk.")

if st.sidebar.button("Start Benchmark"):
    st.write("## Benchmark Results")
    problem_list = problem_inputs
    if not problem_list or not languages or not models:
        st.error("Please provide problems, languages, and models.")
    elif any(not st.session_state.api_keys.get(m, "").strip() for m in models):
        st.error("❌ Please provide an API key for all selected models.")
    else:
        with st.spinner("Generating code in parallel..."):
            gen_results = generate_code_parallel(problem_list, languages, models, st.session_state.api_keys)
        st.success("Code generation complete.")
        st.write("### Peer Review Matrix")
        review_results = peer_review_matrix(gen_results, models)
        st.write("### Consensus Scores & Leaderboard")
        scores = compute_consensus_scores(review_results)
        st.dataframe(scores)
        st.write("### Raw Generation & Reviews")
        st.json({"generation": gen_results, "reviews": review_results})

st.sidebar.markdown("---")
st.sidebar.info("API keys are stored in RAM only. No user prompts or code are uploaded.")

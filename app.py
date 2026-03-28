"""
app.py - CodexMatrix MVP: Session-Only Workflow
A complete Streamlit application implementing the $M^2$ autonomous AI benchmarking engine.
Uses Streamlit Session State as the "Temporary Vault" for all data.

Workflow:
  Input → Generation (requester.py) → Review (judge_matrix.py) 
  → Analysis (stats_engine.py) → Output (Streamlit UI)
  → Cleanup (browser closes → RAM cleared)
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
import json

from src.requester import generate_code_parallel
from src.judge_matrix import peer_review_matrix, RUBRIC
from src.core.stats_engine import (
    build_review_matrix, 
    get_overall_winner, 
    build_heatmap_data,
    build_rubric_comparison,
    compute_consus_scores,
    generate_summary_stats
)
from src.utils.data_sanitizer import sanitize_session_data
from src.new_ui_theme import (
    apply_creative_theme,
    create_stat_card,
    create_winner_banner,
    create_stat_grid,
    display_formatted_dataframe,
    create_metric_table,
    CREATIVE_PALETTE
)


# ============================================================================
# PERSISTENT PREFERENCES (Browser Form Memory)
# ============================================================================

PREFERENCES_FILE = os.path.expanduser("~/.codexmatrix_prefs.json")

def load_preferences():
    """Load saved form inputs (problems, models, languages, API keys)."""
    if os.path.exists(PREFERENCES_FILE):
        try:
            with open(PREFERENCES_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_preferences(prefs: dict):
    """Save form inputs to persistent storage."""
    try:
        with open(PREFERENCES_FILE, "w") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        st.warning(f"⚠️ Could not save preferences: {e}")


# ============================================================================
# PAGE CONFIGURATION & SESSION STATE INITIALIZATION
# ============================================================================

st.set_page_config(
    page_title="CodexMatrix MVP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply creative theme
apply_creative_theme()

# Load saved preferences from disk
saved_prefs = load_preferences()

# Initialize Session State as the "Temporary Vault"
if "session_initialized" not in st.session_state:
    st.session_state.session_initialized = True
    st.session_state.session_start = datetime.now()
    st.session_state.api_keys = saved_prefs.get("api_keys", {})
    st.session_state.models = saved_prefs.get("models", [])
    st.session_state.languages = saved_prefs.get("languages", ["Python"])
    st.session_state.problems = saved_prefs.get("problems", [])
    st.session_state.generation_results = None
    st.session_state.review_results = None
    st.session_state.stats_complete = False
    st.session_state.benchmark_running = False
    st.session_state.error_messages = []

# ============================================================================
# UI STYLING & CONSTANTS - Using Military Command Center Theme
# ============================================================================
# Military theme is applied globally via apply_military_theme()
# Theme colors defined in src/ui_components.py

AVAILABLE_MODELS = [
    # OpenAI
    "GPT-4o",
    "GPT-4o Mini",

    # Anthropic
    "Claude 3.5 Sonnet",
    "Claude 3.5 Haiku",

    # Google Gemini
    "Gemini 2.0 Flash",
    "Gemini 1.5 Flash",

    # Groq hosted models
    "Groq - Llama 3.1 70B",
    "Groq - LLaMA 3 8B",
    "Groq - Mixtral 8x7B",

    # DeepSeek
    "DeepSeek Coder V2",
]

AVAILABLE_LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", 
    "C", "Rust", "Go", "Ruby", "PHP", "Kotlin", "Swift"
]


# ============================================================================
# MAIN UI: HEADER & INSTRUCTIONS
# ============================================================================

st.title("⚔️ CodexMatrix: The Session-Only AI Code Benchmarking Engine")
st.markdown("""
**CodexMatrix** evaluates code-generating AI models using a peer-review matrix ($M^2$).
- 🚀 **Single-Session Workflow**: No database, no persistence
- 🔐 **Privacy First**: API keys stay in RAM, cleared when browser closes
- ⚡ **Real-Time Analysis**: Live heatmaps and winner determination
- 📊 **Peer Review**: Each model reviews every other model's code
- 💾 **Form Memory**: Your problems, models, languages, and API keys are saved locally and restored on your next visit

""")

# ============================================================================
# SIDEBAR: INPUT COLLECTION
# ============================================================================

with st.sidebar:
    st.header("🛠️ CodexMatrix Control Panel")
    st.divider()
    st.subheader("Step 1: Enter Coding Problems")
    st.caption("Add up to 5 coding challenges (saved automatically)")
    
    problem_inputs = []
    for i in range(5):
        default_problem = saved_prefs.get("problems", [])[i] if i < len(saved_prefs.get("problems", [])) else ""
        prob = st.text_area(
            f"Problem {i+1}",
            value=default_problem,
            height=70,
            key=f"problem_input_{i}",
            placeholder=f"E.g., 'Implement quicksort for a list of integers'"
        )
        if prob.strip():
            problem_inputs.append(prob.strip())
    
    st.session_state.problems = problem_inputs
    
    st.divider()
    
    # Step 2: Model Selection
    st.subheader("Step 2: Select Models to Benchmark")
    st.info("""
    **Model Availability:**
    - ✅ **Gemini 2.0 Flash**: Free tier at [aistudio.google.com](https://aistudio.google.com)
      - Latest Gemini model (faster & more capable)
      - Rate limit: 15 requests/minute on free tier
      - No credit card required
    - ✅ **Groq - Llama 3.1 70B**: Free tier at [console.groq.com](https://console.groq.com)
      - Generous free tier with no hard limits
      - Fastest inference speed
    - ✅ **Groq - Mixtral 8x7B**: Free tier, excellent for code
    - ✅ **Groq - LLaMA 3 8B**: Free tier, lightweight model
    
    **Best for Learning:** Use **Groq** (truly unlimited free tier!)
    **Can't get API keys?** Try "Use Mock Data" toggle to test the system!
    """)

    
    st.session_state.models = st.multiselect(
        "Choose AI models",
        AVAILABLE_MODELS,
        default=saved_prefs.get("models", []),
        help="Select at least 1 model to benchmark"
    )
    
    st.divider()
    
    # Step 3: Language Selection
    st.subheader("Step 3: Select Programming Languages")
    st.session_state.languages = st.multiselect(
        "Choose programming languages",
        AVAILABLE_LANGUAGES,
        default=saved_prefs.get("languages", ["Python"])
    )
    
    st.divider()
    
    # Step 4: API Keys
    if st.session_state.models:
        st.subheader("Step 4: Enter API Keys (🔐 Saved for Next Time)")
        
        st.warning(
            "⚠️ **RESEARCH NOTICE**\n\n"
            "For research purposes, you MUST use real, valid API keys. "
            "If you use fake keys with mock data unchecked, you'll get an error. "
            "This ensures data integrity for your research."
        )
        
        for model in st.session_state.models:
            saved_key = saved_prefs.get("api_keys", {}).get(model, "")
            api_key = st.text_input(
                f"{model} API Key",
                value=saved_key,
                type="password",
                key=f"api_key_{model}",
                placeholder=f"Paste your real {model} API key here (40+ characters)"
            )
            if api_key:
                st.session_state.api_keys[model] = api_key
        
        st.info(
            "✅ **Form Memory**: API keys are saved locally and restored on your next visit. "
            "They are also cleared when you clear your browser cache."
        )
    
    st.divider()
    
    # Step 5: Launch Benchmark
    cols = st.columns(2)
    
    with cols[0]:
        if "use_mock" not in st.session_state:
            st.session_state.use_mock = False
        st.session_state.use_mock = st.checkbox(
            "🎭 Use Mock Data (Testing Only)",
            value=st.session_state.use_mock,
            help="⚠️ TESTING ONLY: Use fake data without API costs. "
                 "NOT suitable for research papers - results are simulated, not real LLM grading."
        )
    
    launch_benchmark = st.button(
        "🚀 Start Benchmark",
        key="launch_btn",
        width='stretch'
    )
    
    with cols[1]:
        if st.button("🗑️ Clear Saved Data", width='stretch', key="clear_btn"):
            save_preferences({})
            st.success("✅ All saved data cleared!")
            st.rerun()


# ============================================================================
# VALIDATION & ERROR HANDLING
# ============================================================================

def validate_session_inputs() -> tuple[bool, list]:
    """Validate all session inputs. Returns (is_valid, error_messages)."""
    errors = []
    
    if not st.session_state.problems:
        errors.append("❌ Please enter at least 1 coding problem")
    
    if len(st.session_state.models) < 1:
        errors.append("❌ Please select at least 1 model")
    
    if not st.session_state.languages:
        errors.append("❌ Please select at least 1 programming language")
    
    if not st.session_state.use_mock:
        missing_keys = [m for m in st.session_state.models 
                       if not st.session_state.api_keys.get(m, "").strip()]
        if missing_keys:
            errors.append(f"❌ Missing API keys for: {', '.join(missing_keys)}")
    
    return len(errors) == 0, errors


# ============================================================================
# MAIN WORKFLOW: GENERATION → REVIEW → ANALYSIS → DISPLAY
# ============================================================================

if launch_benchmark:
    # Validate inputs
    is_valid, errors = validate_session_inputs()
    
    if not is_valid:
        st.error("\n".join(errors))
    else:
        # Save preferences for next time user visits
        prefs_to_save = {
            "problems": st.session_state.problems,
            "models": st.session_state.models,
            "languages": st.session_state.languages,
            "api_keys": st.session_state.api_keys
        }
        save_preferences(prefs_to_save)
        st.success("✅ Form inputs saved! They will appear next time you visit.")
        
        st.session_state.benchmark_running = True
        
        # ====== STEP A: CODE GENERATION ======
        st.header("📝 Step A: Code Generation")
        gen_placeholder = st.empty()
        
        with gen_placeholder.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.write("🔄 Generating code for all models and languages...")
            
            try:
                st.session_state.generation_results = generate_code_parallel(
                    problems=st.session_state.problems,
                    languages=st.session_state.languages,
                    models=st.session_state.models,
                    api_keys=st.session_state.api_keys,
                    use_mock=st.session_state.use_mock
                )
                
                progress_bar.progress(100)
                status_text.success("✅ Code generation complete!")
                
                # Display generation summary
                num_tasks = (len(st.session_state.problems) * 
                            len(st.session_state.languages) * 
                            len(st.session_state.models))
                st.info(f"Generated **{num_tasks}** code samples ({len(st.session_state.problems)} problems × "
                       f"{len(st.session_state.languages)} languages × {len(st.session_state.models)} models)")
                
                # Display actual generated code
                st.subheader("🔎 Generated Code Details")
                
                for problem in st.session_state.problems:
                    # Use native st.expander to avoid state loss issues
                    with st.expander(f"📌 Problem: {problem[:60]}..."):
                        for language in st.session_state.languages:
                            st.write(f"**Language: {language}**")
                            
                            # Create columns for each model
                            model_cols = st.columns(len(st.session_state.models))
                            
                            for idx, model in enumerate(st.session_state.models):
                                with model_cols[idx]:
                                    code_data = st.session_state.generation_results.get(problem, {}).get(language, {}).get(model, {})
                                    
                                    if code_data.get("valid"):
                                        st.write(f"✅ **{model}**")
                                        st.code(code_data.get("code", ""), language=language.lower())
                                    else:
                                        error_msg = code_data.get("error", "Unknown error")
                                        st.write(f"❌ **{model}**")
                                        st.error(error_msg)
                            
                            st.divider()
                
            except Exception as e:
                progress_bar.progress(0)
                status_text.error(f"❌ Error during generation: {str(e)}")
                st.stop()
        
        # ====== STEP B: PEER REVIEW ======
        st.header("🔍 Step B: Peer Review Matrix")
        review_placeholder = st.empty()
        
        with review_placeholder.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.write("🔄 Performing peer reviews (each model reviewing every other)...")
            
            try:
                st.session_state.review_results = peer_review_matrix(
                    gen_results=st.session_state.generation_results,
                    models=st.session_state.models,
                    api_keys=st.session_state.api_keys,
                    use_mock=st.session_state.use_mock
                )
                
                progress_bar.progress(100)
                status_text.success("✅ Peer review complete!")
                
                num_reviews = len(st.session_state.models) ** 2 * len(st.session_state.problems) * len(st.session_state.languages)
                st.info(f"Completed **{num_reviews}** peer reviews using actual LLM grading (not random)")
                
            except ValueError as e:
                progress_bar.progress(0)
                status_text.error(f"❌ API Key Validation Error:\n\n{str(e)}")
                st.error(
                    "### 🔑 API Key Issue\n\n"
                    "The API keys you provided are invalid or incomplete.\n\n"
                    "**For Research Purposes:**\n"
                    "- ✅ Use REAL API keys from OpenAI, Anthropic, or Google\n"
                    "- ✅ Get keys from: https://platform.openai.com/api-keys\n"
                    "- ❌ Do NOT use fake or test keys\n"
                    "- ❌ Do NOT use partially entered keys\n\n"
                    "**For Testing Without Costs:**\n"
                    "- ✅ Check '🎭 Use Mock Data' checkbox\n"
                    "- ✅ Run with mock mode (shows realistic workflow)\n"
                    "- ❌ But mock mode is NOT suitable for research papers"
                )
                st.stop()
            except RuntimeError as e:
                progress_bar.progress(0)
                status_text.error(f"❌ API Call Failed:\n\n{str(e)}")
                st.error(
                    "### 🚨 API Error During Grading\n\n"
                    f"**Details:** {str(e)}\n\n"
                    "**Possible Causes:**\n"
                    "1. Invalid or expired API key\n"
                    "2. API provider down or rate limited\n"
                    "3. Insufficient API quota/credits\n"
                    "4. Internet connection issue\n\n"
                    "**Next Steps:**\n"
                    "- Verify your API keys are correct\n"
                    "- Check API provider status page\n"
                    "- Ensure you have sufficient credits\n"
                    "- Try again with fewer models/problems\n"
                )
                st.stop()
            except Exception as e:
                progress_bar.progress(0)
                status_text.error(f"❌ Unexpected Error:\n\n{str(e)}")
                st.error(f"An unexpected error occurred: {str(e)}")
                st.stop()
        
        # ====== STEP C: ANALYSIS ======
        st.header("📊 Step C: Real-Time Analysis")
        
        try:
            # Build matrices
            leaderboard_df = build_review_matrix(st.session_state.review_results)
            overall_winner, winner_score = get_overall_winner(leaderboard_df)
            consensus_scores = compute_consus_scores(st.session_state.review_results)
            summary_stats = generate_summary_stats(
                {
                    "problems": st.session_state.problems,
                    "models": st.session_state.models,
                    "languages": st.session_state.languages
                },
                st.session_state.review_results
            )
            
            st.session_state.stats_complete = True
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.stop()
        
        # ====== STEP D: DISPLAY RESULTS (TABBED ORGANIZATION) ======
        st.header("🏆 Session Results & Analysis")
        
        # Main result tabs organized by category
        main_tab1, main_tab2, main_tab3 = st.tabs([
            "📊 OVERVIEW & RANKINGS",
            "📈 VISUALIZATIONS & INSIGHTS",
            "💾 DATA & EXPORT"
        ])
        
        # ========== TAB 1: OVERVIEW & RANKINGS ==========
        with main_tab1:
            st.subheader("🎯 Winner & Summary")
            
            # Winner Announcement
            if overall_winner:
                st.markdown(create_winner_banner(overall_winner, winner_score), unsafe_allow_html=True)
            
            st.divider()
            
            # Session Statistics with creative cards
            col_stats = st.columns(4)
            stats_data = [
                ("Problems", str(summary_stats["total_problems"]), "📝"),
                ("Models", str(summary_stats["total_models"]), "🤖"),
                ("Languages", str(summary_stats["total_languages"]), "💻"),
                ("Reviews", str(summary_stats["total_reviews"]), "📋"),
            ]
            
            for col, (label, value, icon) in zip(col_stats, stats_data):
                with col:
                    st.markdown(create_stat_card(label, value, icon), unsafe_allow_html=True)
            
            st.divider()
            
            # Leaderboard Table
            st.subheader("📋 Overall Leaderboard")
            leaderboard_display = leaderboard_df.copy()
            leaderboard_display['Overall'] = leaderboard_display.mean(axis=1)
            leaderboard_display = leaderboard_display.sort_values('Overall', ascending=False)
            
            st.dataframe(
                leaderboard_display.round(2),
                use_container_width=True,
                height=400
            )
            
            # Additional summary info
            st.divider()
            st.subheader("📌 Consensus Scores Summary")
            
            # Format consensus scores and display as beautiful chart
            if isinstance(consensus_scores, dict) and consensus_scores:
                # Aggregate consensus scores across all models for each rubric dimension
                rubric_scores = {}
                
                # Flatten the nested structure: {model: {rubric: score}} -> {rubric: [scores]}
                for model, rubrics in consensus_scores.items():
                    if isinstance(rubrics, dict):
                        for rubric, score in rubrics.items():
                            if rubric not in rubric_scores:
                                rubric_scores[rubric] = []
                            if isinstance(score, (int, float)):
                                rubric_scores[rubric].append(score)
                
                # Calculate consensus (average) for each rubric dimension
                consensus_data = {
                    rubric: round(sum(scores) / len(scores), 2)
                    for rubric, scores in rubric_scores.items()
                    if scores
                }
                
                # Create dataframe from consensus scores
                consensus_df = pd.DataFrame(
                    list(consensus_data.items()),
                    columns=['Dimension', 'Score']
                ).sort_values('Score', ascending=False)
                
                # Create beautiful bar chart
                fig = px.bar(
                    consensus_df,
                    x='Score',
                    y='Dimension',
                    orientation='h',
                    title='Consensus Scores Across All Rubric Dimensions',
                    labels={'Score': 'Average Score (1-5)', 'Dimension': 'Rubric Dimension'},
                    color='Score',
                    color_continuous_scale=['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e'],
                    height=500
                )
                
                fig.update_layout(
                    xaxis_range=[0, 5],
                    hovermode='closest',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    showlegend=False,
                    margin=dict(l=200, r=50, t=50, b=50)
                )
                
                fig.update_traces(
                    text=consensus_df['Score'].round(2),
                    textposition='outside',
                    hovertemplate='<b>%{y}</b><br>Score: %{x:.2f}/5.0<extra></extra>'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Also show as sortable table
                with st.expander("📊 View as Data Table"):
                    st.dataframe(
                        consensus_df.round(2),
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Dimension": st.column_config.TextColumn("📋 Rubric Dimension"),
                            "Score": st.column_config.ProgressColumn(
                                "⭐ Score",
                                min_value=0,
                                max_value=5
                            )
                        }
                    )
            else:
                st.warning("Unable to display consensus scores in expected format")
        
        # ========== TAB 2: VISUALIZATIONS & INSIGHTS ==========
        with main_tab2:
            # Sub-tabs for different visualization types
            viz_tab1, viz_tab2, viz_tab3 = st.tabs([
                "🔥 Peer Review Heatmap",
                "📊 Performance by Criteria",
                "🏅 Top Models Comparison"
            ])
            
            with viz_tab1:
                st.subheader("Peer Review Heatmap - Model Grades")
                st.write("**How each model scored others** (Correctness & Accuracy)")
                
                try:
                    matrix, models_list = build_heatmap_data(
                        st.session_state.review_results,
                        metric="Correctness & Accuracy"
                    )
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=matrix,
                        x=models_list,
                        y=models_list,
                        colorscale='Viridis',
                        text=matrix,
                        texttemplate='%{text:.2f}',
                        textfont={"size": 10}
                    ))
                    fig.update_layout(
                        height=600,
                        xaxis_title="Model Being Reviewed",
                        yaxis_title="Reviewing Model",
                        hovermode='closest'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("💡 **Interpretation**: Each row shows how one model rated others. Higher values = better reviews given.")
                    
                except Exception as e:
                    st.error(f"Could not generate heatmap: {e}")
            
            with viz_tab2:
                st.subheader("Performance Breakdown by Rubric Criteria")
                st.write("**How each model scores across different dimensions**")
                
                # Create bar chart for each criterion
                rubric_comparison = build_rubric_comparison(leaderboard_df.copy(), top_n=len(st.session_state.models))
                
                # Show all criteria in organized view
                criteria_per_row = 2
                rubric_list = list(RUBRIC)
                
                for i in range(0, len(rubric_list), criteria_per_row):
                    cols = st.columns(criteria_per_row)
                    
                    for col_idx, rubric in enumerate(rubric_list[i:i+criteria_per_row]):
                        with cols[col_idx]:
                            scores = [rubric_comparison[model].get(rubric, 0) for model in rubric_comparison.keys()]
                            
                            fig = px.bar(
                                x=list(rubric_comparison.keys()),
                                y=scores,
                                title=rubric,
                                labels={"x": "", "y": "Score (1-5)"},
                                color=scores,
                                color_continuous_scale='Viridis',
                                height=350
                            )
                            fig.update_layout(
                                showlegend=False,
                                hovermode='x unified',
                                margin=dict(l=0, r=0, t=40, b=0)
                            )
                            st.plotly_chart(fig, use_container_width=True)
            
            with viz_tab3:
                st.subheader("Top Models Side-by-Side Comparison")
                st.write("**Performance comparison of leading models**")
                
                top_n = min(3, len(st.session_state.models))
                rubric_comp = build_rubric_comparison(leaderboard_df.copy(), top_n=top_n)
                
                comparison_df = pd.DataFrame(rubric_comp).T
                comparison_df = comparison_df[RUBRIC]
                
                fig = px.bar(
                    comparison_df,
                    barmode='group',
                    title=f"Top {top_n} Models Performance",
                    labels={"index": "Model", "value": "Score"},
                    height=500,
                    color_discrete_sequence=['#3b82f6', '#a855f7', '#ec4899']
                )
                fig.update_layout(
                    hovermode='x unified',
                    xaxis_title="Rubric Criteria",
                    yaxis_title="Score (1-5)"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # ========== TAB 3: DATA & EXPORT ==========
        with main_tab3:
            data_tab1, data_tab2 = st.tabs([
                "📋 Raw Data",
                "📥 Download Report"
            ])
            
            with data_tab1:
                st.subheader("Detailed Raw Data")
                
                raw_col1, raw_col2 = st.columns(2)
                
                with raw_col1:
                    st.write("**Generation Results**")
                    with st.expander("View generated code details"):
                        st.json(st.session_state.generation_results, expanded=False)
                
                with raw_col2:
                    st.write("**Review Results**")
                    with st.expander("View peer review matrix"):
                        st.json(st.session_state.review_results, expanded=False)
            
            with data_tab2:
                st.subheader("Export Session Report")
                
                # Prepare downloadable data
                export_data = {
                    "session_info": {
                        "start_time": st.session_state.session_start.isoformat(),
                        "models": st.session_state.models,
                        "languages": st.session_state.languages,
                        "problems_count": len(st.session_state.problems),
                        "winner": overall_winner,
                        "winner_score": float(winner_score)
                    },
                    "leaderboard": leaderboard_df.to_dict(),
                    "consensus_scores": consensus_scores,
                    "summary_stats": summary_stats
                }
                
                json_str = json.dumps(export_data, indent=2)
                
                st.download_button(
                    "📥 Download Session Report (JSON)",
                    json_str,
                    f"codexmatrix_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json"
                )
                
                st.write("---")
                st.write("**📊 Export as CSV Tables**")
                
                col_csv1, col_csv2, col_csv3 = st.columns(3)
                
                with col_csv1:
                    leaderboard_csv = leaderboard_display.to_csv()
                    st.download_button(
                        "📊 Download Leaderboard (CSV)",
                        leaderboard_csv,
                        f"leaderboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
                
                with col_csv2:
                    # Handle consensus scores CSV export
                    if isinstance(consensus_scores, dict):
                        consensus_df = pd.DataFrame(
                            list(consensus_scores.items()),
                            columns=['Category', 'Score']
                        ).sort_values('Score', ascending=False)
                        consensus_csv = consensus_df.to_csv(index=False)
                    else:
                        consensus_csv = str(consensus_scores)
                    
                    st.download_button(
                        "📊 Download Consensus Scores (CSV)",
                        consensus_csv,
                        f"consensus_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
                
                with col_csv3:
                    # Summary stats CSV
                    summary_df = pd.DataFrame(
                        list(summary_stats.items()),
                        columns=['Metric', 'Value']
                    )
                    summary_csv = summary_df.to_csv(index=False)
                    
                    st.download_button(
                        "📊 Download Summary Stats (CSV)",
                        summary_csv,
                        f"summary_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
        
        st.divider()
        
        # Privacy Reminder
        st.info(
            "🔐 **Privacy & Cleanup Notice**\n\n"
            "This benchmark is completely ephemeral:\n"
            "- ✅ All API keys are stored only in RAM (this browser session)\n"
            "- ✅ No data is saved to disk or cloud\n"
            "- ✅ Code, problems, and reviews are never uploaded\n"
            "- ✅ When you close the browser, everything is automatically cleared\n\n"
            "**Start a new benchmark session to run another test→**"
        )


# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
<div style="text-align: center; color: #888; margin-top: 50px;">
    <p>CodexMatrix MVP • Session-Only Architecture • No Database • Privacy First</p>
    <p><small>Built with Streamlit • Powered by LLM Peer Review</small></p>
</div>
""", unsafe_allow_html=True)

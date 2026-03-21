"""
ui_components.py - Military Monitoring Platform UI Components
Radar chart visualization with overlay mode and military aesthetic styling
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import Dict, List, Tuple, Optional


# ============================================================================
# MILITARY MONITORING PLATFORM THEME
# ============================================================================

MILITARY_THEME = {
    "name": "Military Command Center",
    "bg_main": "#0a0e1a",  # Deep dark navy
    "bg_secondary": "#0f1419",  # Slightly lighter navy
    "bg_tertiary": "#141820",  # Grid background
    "accent_primary": "#00ff41",  # Military neon green
    "accent_secondary": "#00d9ff",  # Cyan/targeting color
    "accent_warning": "#ff6b35",  # Alert orange/red
    "accent_success": "#00ff41",  # Green for success
    "text_primary": "#f0f0f0",  # Bright white
    "text_secondary": "#a0a0a0",  # Gray for secondary
    "border": "#1a2332",  # Border color
    "grid": "rgba(0, 255, 65, 0.05)",  # Subtle grid overlay
    "glow": "0 0 20px rgba(0, 255, 65, 0.5)",  # Neon glow
    "scan_color": "rgba(0, 255, 65, 0.1)"  # Scan line effect
}


def apply_military_theme():
    """Apply the military command center theme with CSS styling."""
    theme = MILITARY_THEME
    
    # Custom CSS for military aesthetic
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
        
        * {{
            font-family: 'JetBrains Mono', 'Roboto Mono', monospace !important;
        }}
        
        body {{
            background-color: {theme['bg_main']};
            color: {theme['text_primary']};
            background-image: 
                repeating-linear-gradient(
                    0deg,
                    {theme['scan_color']} 0px,
                    {theme['scan_color']} 1px,
                    transparent 1px,
                    transparent 2px
                ),
                repeating-linear-gradient(
                    90deg,
                    {theme['grid']} 0px,
                    {theme['grid']} 1px,
                    transparent 1px,
                    transparent 40px
                );
        }}
        
        .main {{
            background-color: {theme['bg_main']};
        }}
        
        /* Command center header style */
        .military-header {{
            background: linear-gradient(135deg, {theme['accent_primary']}, {theme['accent_secondary']});
            color: {theme['bg_main']};
            padding: 20px 25px;
            border-radius: 0px;
            border: 2px solid {theme['accent_primary']};
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3), inset 0 0 30px rgba(0, 255, 65, 0.1);
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }}
        
        .military-header::before {{
            content: '█ ';
            animation: blink 1s infinite;
        }}
        
        @keyframes blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}
        
        /* Radar container with glow */
        .radar-container {{
            background-color: {theme['bg_secondary']};
            border: 3px solid {theme['accent_primary']};
            border-radius: 4px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 
                0 0 20px {theme['accent_primary']},
                inset 0 0 20px rgba(0, 255, 65, 0.05),
                0 0 40px rgba(0, 255, 65, 0.2);
            position: relative;
        }}
        
        .radar-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 255, 65, 0.03) 0px,
                rgba(0, 255, 65, 0.03) 1px,
                transparent 1px,
                transparent 2px
            );
            pointer-events: none;
            border-radius: 4px;
        }}
        
        /* Model selector style */
        .model-selector {{
            background-color: {theme['bg_secondary']};
            border: 2px solid {theme['accent_secondary']};
            border-radius: 4px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 0 15px rgba(0, 217, 255, 0.2);
        }}
        
        /* Metric card military style */
        .metric-card-military {{
            background-color: {theme['bg_secondary']};
            border-left: 4px solid {theme['accent_primary']};
            border-top: 2px solid {theme['accent_secondary']};
            border-radius: 0px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 
                0 0 20px rgba(0, 255, 65, 0.15),
                inset 0 0 20px rgba(0, 255, 65, 0.05);
            position: relative;
        }}
        
        .metric-card-military::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, {theme['accent_primary']}, transparent);
        }}
        
        /* Button styling */
        .stButton>button {{
            background: linear-gradient(135deg, {theme['accent_primary']} 0%, {theme['accent_secondary']} 100%);
            color: {theme['bg_main']};
            font-weight: 700;
            border-radius: 0px;
            border: 2px solid {theme['accent_primary']};
            padding: 12px 24px;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
            letter-spacing: 1px;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .stButton>button:hover {{
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.6), 0 0 50px rgba(0, 217, 255, 0.3);
            transform: translateY(-2px);
        }}
        
        .stButton>button:active {{
            transform: translateY(0px);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.4), inset 0 0 20px rgba(0, 255, 65, 0.1);
        }}
        
        /* Tab styling */
        .stTabs [role="tablist"] {{
            background: transparent;
            border-bottom: 2px solid {theme['accent_primary']};
        }}
        
        .stTabs [role="tablist"] button {{
            background-color: {theme['bg_secondary']};
            border: 1px solid {theme['border']};
            color: {theme['text_secondary']};
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }}
        
        .stTabs [role="tablist"] button:hover {{
            background-color: {theme['bg_tertiary']};
            color: {theme['accent_primary']};
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
        }}
        
        .stTabs [role="tablist"] button[aria-selected="true"] {{
            background-color: {theme['accent_primary']};
            color: {theme['bg_main']};
            border: 2px solid {theme['accent_primary']};
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }}
        
        /* Divider styling */
        hr {{
            border: 0;
            height: 2px;
            background: repeating-linear-gradient(
                90deg,
                {theme['accent_primary']},
                {theme['accent_primary']} 10px,
                transparent 10px,
                transparent 20px
            );
            margin: 30px 0;
        }}
        
        /* Text styling */
        h1, h2, h3 {{
            color: {theme['accent_primary']};
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
        }}
        
        /* Winner announcement */
        .winner-announcement {{
            background: linear-gradient(135deg, {theme['accent_primary']}, {theme['accent_secondary']});
            border: 3px solid {theme['accent_primary']};
            padding: 40px;
            border-radius: 0px;
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            color: {theme['bg_main']};
            box-shadow: 
                0 0 50px rgba(0, 255, 65, 0.5),
                0 0 100px rgba(0, 217, 255, 0.3),
                inset 0 0 30px rgba(255, 255, 255, 0.1);
            text-transform: uppercase;
            letter-spacing: 3px;
            margin: 30px 0;
            position: relative;
            overflow: hidden;
        }}
        
        .winner-announcement::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: sweep 2s infinite;
        }}
        
        @keyframes sweep {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        
        /* Data display styling */
        .dataframe {{
            background-color: {theme['bg_secondary']} !important;
            border: 2px solid {theme['accent_primary']} !important;
            border-radius: 0px;
        }}
        
        /* Expander styling */
        .streamlit-expanderHeader {{
            background-color: {theme['bg_secondary']};
            border: 1px solid {theme['accent_secondary']};
        }}
        
        .streamlit-expanderHeader:hover {{
            background-color: {theme['bg_tertiary']};
            box-shadow: 0 0 15px rgba(0, 217, 255, 0.3);
        }}
        
        /* Hide keyboard navigation hints and placeholder text */
        [aria-label*="keyboard"],
        [aria-label*="arrow"],
        [title*="keyboard"],
        [title*="arrow"],
        .keyboard-hint,
        .nav-hint {{
            display: none !important;
        }}
        
        /* Hide browser accessibility overlays */
        [role="tooltip"],
        .browser-nav-hint {{
            display: none !important;
        }}
        
        /* Hide broken expander icons - Streamlit expander arrows */
        [class*="expanderButton"],
        [data-testid*="expander"],
        button[aria-expanded] svg {{
            display: none !important;
        }}
        
        /* Replace expander icon with emoji */
        [class*="expanderButton"]::before {{
            content: "▶ ";
            display: inline;
        }}
        
        [class*="expanderButton"][aria-expanded="true"]::before {{
            content: "▼ ";
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# RUBRIC DEFINITIONS
# ============================================================================

RUBRIC_FULL = [
    "Correctness & Accuracy",
    "Efficiency (Time)",
    "Efficiency (Space)",
    "Readability & Clear Code",
    "Documentation & Comments",
    "Edge-Case Handling",
    "Error Handling & Robustness",
    "Security & Safe Practices",
    "Code Simplicity",
    "Best Practices & Standards"
]

# Group into 5 categories for cleaner radar chart
RUBRIC_GROUPED = {
    "Correctness": ["Correctness & Accuracy", "Edge-Case Handling"],
    "Efficiency": ["Efficiency (Time)", "Efficiency (Space)"],
    "Readability": ["Readability & Clear Code", "Code Simplicity"],
    "Documentation": ["Documentation & Comments"],
    "Security": ["Error Handling & Robustness", "Security & Safe Practices", "Best Practices & Standards"]
}


def aggregate_scores(scores_dict: Dict[str, float], rubric_mapping: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Aggregate detailed scores into grouped categories.
    
    Args:
        scores_dict: Dictionary with rubric item as key, score as value
        rubric_mapping: Mapping of category to list of rubric items
    
    Returns:
        Dictionary with category as key, average score as value
    """
    aggregated = {}
    for category, items in rubric_mapping.items():
        scores = []
        for item in items:
            # Try to find the item in scores_dict
            for key, value in scores_dict.items():
                if item.lower() in key.lower() or key.lower() in item.lower():
                    scores.append(value)
                    break
        if scores:
            aggregated[category] = np.mean(scores)
    return aggregated


# ============================================================================
# RADAR CHART CREATION
# ============================================================================

def create_single_model_radar(
    model_name: str,
    scores: Dict[str, float],
    use_grouped: bool = True,
    theme: Dict = None
) -> go.Figure:
    """
    Create a single model radar chart.
    
    Args:
        model_name: Name of the model
        scores: Dictionary of rubric scores
        use_grouped: Whether to use grouped rubric (5 categories) or full (10 items)
        theme: Theme dictionary for colors
    
    Returns:
        Plotly Figure object
    """
    if theme is None:
        theme = MILITARY_THEME
    
    if use_grouped:
        data = aggregate_scores(scores, RUBRIC_GROUPED)
        categories = list(data.keys())
        values = list(data.values())
    else:
        # Map numeric indices to rubric items
        values = []
        categories = []
        for i, rubric in enumerate(RUBRIC_FULL):
            # Try to find the score for this rubric
            for key, val in scores.items():
                if str(i+1) in str(key) or rubric.lower() in str(key).lower():
                    values.append(val)
                    categories.append(rubric[:20] + "..." if len(rubric) > 20 else rubric)
                    break
        
        if not values:
            values = list(scores.values())[:10]
            categories = RUBRIC_FULL[:len(values)]
    
    # Ensure 5-point scale
    values = [min(max(v, 0), 5) for v in values]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=model_name,
        opacity=0.7,
        line=dict(
            color=theme['accent_primary'],
            width=3
        ),
        marker=dict(
            size=10,
            color=theme['accent_primary'],
            symbol='diamond'
        ),
        fillcolor='rgba(0, 255, 65, 0.2)',
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.2f}/5<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(
                    size=11,
                    color=theme['text_secondary'],
                    family='JetBrains Mono'
                ),
                gridcolor='rgba(0, 255, 65, 0.2)',
                gridwidth=2,
                tickcolor=theme['accent_primary']
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=12,
                    color=theme['accent_primary'],
                    family='JetBrains Mono'
                ),
                gridcolor='rgba(0, 255, 65, 0.15)',
                linecolor=theme['accent_primary'],
                linewidth=2
            ),
            bgcolor='rgba(15, 20, 25, 0.5)'
        ),
        title=dict(
            text=f"🎯 TACTICAL ANALYSIS: {model_name.upper()}",
            font=dict(
                size=20,
                color=theme['accent_primary'],
                family='JetBrains Mono'
            ),
            x=0.5,
            xanchor='center'
        ),
        hovermode='closest',
        showlegend=False,
        height=600,
        paper_bgcolor=theme['bg_secondary'],
        plot_bgcolor='rgba(0, 0, 0, 0.5)',
        margin=dict(l=80, r=80, t=100, b=80),
        font=dict(
            family='JetBrains Mono',
            color=theme['text_primary']
        )
    )
    
    return fig


def create_overlay_radar(
    model_1: str,
    scores_1: Dict[str, float],
    model_2: str,
    scores_2: Dict[str, float],
    use_grouped: bool = True,
    theme: Dict = None
) -> go.Figure:
    """
    Create an overlay radar chart comparing two models.
    
    Args:
        model_1: First model name
        scores_1: First model scores
        model_2: Second model name
        scores_2: Second model scores
        use_grouped: Whether to use grouped rubric
        theme: Theme dictionary
    
    Returns:
        Plotly Figure object with both models overlaid
    """
    if theme is None:
        theme = MILITARY_THEME
    
    if use_grouped:
        data_1 = aggregate_scores(scores_1, RUBRIC_GROUPED)
        data_2 = aggregate_scores(scores_2, RUBRIC_GROUPED)
        categories = list(data_1.keys())
        values_1 = list(data_1.values())
        values_2 = list(data_2.values())
    else:
        # Use full rubric
        values_1 = list(scores_1.values())[:10]
        values_2 = list(scores_2.values())[:10]
        categories = RUBRIC_FULL[:len(values_1)]
    
    values_1 = [min(max(v, 0), 5) for v in values_1]
    values_2 = [min(max(v, 0), 5) for v in values_2]
    
    fig = go.Figure()
    
    # Model 1 trace (green)
    fig.add_trace(go.Scatterpolar(
        r=values_1,
        theta=categories,
        fill='toself',
        name=model_1,
        opacity=0.7,
        line=dict(
            color=theme['accent_primary'],
            width=3
        ),
        marker=dict(
            size=10,
            color=theme['accent_primary'],
            symbol='diamond'
        ),
        fillcolor='rgba(0, 255, 65, 0.2)',
        hovertemplate=f'<b>{model_1}</b><br>%{{theta}}<br>Score: %{{r:.2f}}/5<extra></extra>'
    ))
    
    # Model 2 trace (cyan)
    fig.add_trace(go.Scatterpolar(
        r=values_2,
        theta=categories,
        fill='toself',
        name=model_2,
        opacity=0.7,
        line=dict(
            color=theme['accent_secondary'],
            width=3,
            dash='dash'
        ),
        marker=dict(
            size=10,
            color=theme['accent_secondary'],
            symbol='square'
        ),
        fillcolor='rgba(0, 217, 255, 0.15)',
        hovertemplate=f'<b>{model_2}</b><br>%{{theta}}<br>Score: %{{r:.2f}}/5<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(
                    size=11,
                    color=theme['text_secondary'],
                    family='JetBrains Mono'
                ),
                gridcolor='rgba(0, 255, 65, 0.2)',
                gridwidth=2
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=12,
                    color=theme['accent_primary'],
                    family='JetBrains Mono'
                ),
                gridcolor='rgba(0, 255, 65, 0.15)'
            ),
            bgcolor='rgba(15, 20, 25, 0.5)'
        ),
        title=dict(
            text=f"⚔️ TACTICAL OVERLAY: {model_1.upper()} vs {model_2.upper()}",
            font=dict(
                size=20,
                color=theme['accent_primary'],
                family='JetBrains Mono'
            ),
            x=0.5,
            xanchor='center'
        ),
        hovermode='closest',
        showlegend=True,
        height=600,
        paper_bgcolor=theme['bg_secondary'],
        plot_bgcolor='rgba(0, 0, 0, 0.5)',
        margin=dict(l=80, r=80, t=120, b=80),
        font=dict(
            family='JetBrains Mono',
            color=theme['text_primary']
        ),
        legend=dict(
            x=1.1,
            y=1,
            bgcolor='rgba(20, 24, 32, 0.8)',
            bordercolor=theme['accent_primary'],
            borderwidth=2,
            font=dict(size=12, color=theme['accent_primary'])
        )
    )
    
    return fig


# ============================================================================
# UI COMPONENTS
# ============================================================================

def display_military_header(title: str):
    """Display a military-style header."""
    st.markdown(f"""
    <div class="military-header">
        {title}
    </div>
    """, unsafe_allow_html=True)


def display_metric_card(label: str, value: str, icon: str = "📊"):
    """Display a metric card with military styling."""
    st.markdown(f"""
    <div class="metric-card-military">
        <b>{icon} {label}</b><br>
        <span style="font-size: 20px; color: #00ff41;">{value}</span>
    </div>
    """, unsafe_allow_html=True)


def radar_analysis_section(review_results: Dict, models: List[str]):
    """
    Main section for radar chart analysis.
    
    Args:
        review_results: Review results dictionary from peer_review_matrix
        models: List of model names
    """
    display_military_header("🎯 TACTICAL RADAR ANALYSIS SYSTEM")
    
    st.write("📡 **Enhanced multi-dimensional performance visualization**")
    st.write("- **Single Radar**: Analyze one model's strengths and weaknesses")
    st.write("- **Overlay Comparison**: Compare two models head-to-head")
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="model-selector">
            <b>🎮 ANALYSIS MODE</b>
        </div>
        """, unsafe_allow_html=True)
        
        analysis_mode = st.radio(
            "Select analysis mode",
            ["📊 Single Model", "⚔️ Model Overlay"],
            label_visibility="collapsed"
        )
    
    with col2:
        if analysis_mode == "📊 Single Model":
            st.markdown("""
            <div style="color: #00ff41; font-size: 14px; padding: 10px; border-left: 3px solid #00ff41;">
                🔍 View detailed tactical assessment of a single model across all performance dimensions
            </div>
            """, unsafe_allow_html=True)
            
            selected_model = st.selectbox(
                "Select model for analysis",
                models,
                label_visibility="collapsed"
            )
            
            # Extract scores for selected model
            model_scores = extract_model_scores(review_results, selected_model)
            
            if model_scores:
                fig = create_single_model_radar(
                    selected_model,
                    model_scores,
                    use_grouped=True,
                    theme=MILITARY_THEME
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Display detailed breakdown
                with st.expander("📋 DETAILED METRICS BREAKDOWN"):
                    display_score_breakdown(model_scores, RUBRIC_GROUPED)
            else:
                st.error("❌ No scoring data available for this model")
        
        else:  # Overlay mode
            st.markdown("""
            <div style="color: #00d9ff; font-size: 14px; padding: 10px; border-left: 3px solid #00d9ff;">
                ⚔️ Tactical head-to-head comparison - Identify competitive advantages and vulnerabilities
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                model_1 = st.selectbox(
                    "Model 1 (Green Outline)",
                    models,
                    key="model_overlay_1",
                    label_visibility="collapsed"
                )
            
            with col_b:
                model_2 = st.selectbox(
                    "Model 2 (Cyan Dashed Outline)",
                    [m for m in models if m != model_1],
                    key="model_overlay_2",
                    label_visibility="collapsed"
                )
            
            scores_1 = extract_model_scores(review_results, model_1)
            scores_2 = extract_model_scores(review_results, model_2)
            
            if scores_1 and scores_2:
                fig = create_overlay_radar(
                    model_1,
                    scores_1,
                    model_2,
                    scores_2,
                    use_grouped=True,
                    theme=MILITARY_THEME
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Tactical comparison summary
                with st.expander("🎯 TACTICAL COMPARISON SUMMARY"):
                    display_comparison_analysis(model_1, scores_1, model_2, scores_2)
            else:
                st.error("❌ Unable to retrieve scoring data")


def extract_model_scores(review_results: Dict, model_name: str) -> Dict[str, float]:
    """
    Extract averaged scores for a model from review results.
    
    Args:
        review_results: Dictionary from peer_review_matrix
        model_name: Model to extract scores for
    
    Returns:
        Dictionary with rubric dimension as key, average score as value
    """
    if not review_results:
        return {}
    
    # Initialize tracking
    scores_by_rubric = {rubric: [] for rubric in RUBRIC_FULL}
    
    # Extract scores where this model was reviewed
    for reviewer, reviewees in review_results.items():
        if model_name in reviewees:
            grades = reviewees[model_name].get("grades", {})
            for rubric, score in grades.items():
                # Try to map the rubric index to our RUBRIC_FULL list
                try:
                    idx = int(rubric) - 1
                    if 0 <= idx < len(RUBRIC_FULL):
                        scores_by_rubric[RUBRIC_FULL[idx]].append(float(score))
                except (ValueError, IndexError):
                    pass
    
    # Average the scores
    averaged_scores = {}
    for rubric, scores in scores_by_rubric.items():
        if scores:
            averaged_scores[rubric] = np.mean(scores)
        else:
            averaged_scores[rubric] = 0.0
    
    return {k: v for k, v in averaged_scores.items() if v > 0}


def display_score_breakdown(scores: Dict[str, float], rubric_mapping: Dict[str, List[str]]):
    """Display detailed breakdown of scores in a table."""
    breakdown_data = []
    
    for category, items in rubric_mapping.items():
        category_scores = []
        for item in items:
            for key, value in scores.items():
                if item.lower() in key.lower() or key.lower() in item.lower():
                    category_scores.append(value)
                    breakdown_data.append({
                        "Category": category,
                        "Dimension": item,
                        "Score": f"{value:.2f}/5"
                    })
                    break
    
    if breakdown_data:
        st.dataframe(
            breakdown_data,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No detailed breakdown available")


def display_comparison_analysis(model_1: str, scores_1: Dict, model_2: str, scores_2: Dict):
    """Display tactical comparison analysis."""
    
    col1, col2, col3 = st.columns(3)
    
    avg_1 = np.mean(list(scores_1.values())) if scores_1 else 0
    avg_2 = np.mean(list(scores_2.values())) if scores_2 else 0
    
    with col1:
        st.metric(f"🔴 {model_1}", f"{avg_1:.2f}/5")
    
    with col2:
        diff = avg_1 - avg_2
        st.metric("⚔️ Advantage", f"{abs(diff):.2f}", delta=f"Winner: {model_1 if diff > 0 else model_2}")
    
    with col3:
        st.metric(f"🔵 {model_2}", f"{avg_2:.2f}/5")
    
    st.divider()
    
    # Identify strengths and weaknesses
    st.write("### Strengths & Weaknesses")
    
    agg_1 = aggregate_scores(scores_1, RUBRIC_GROUPED)
    agg_2 = aggregate_scores(scores_2, RUBRIC_GROUPED)
    
    comparison_data = []
    for dimension in agg_1.keys():
        score_1 = agg_1.get(dimension, 0)
        score_2 = agg_2.get(dimension, 0)
        winner = "🔴 " + model_1 if score_1 > score_2 else "🔵 " + model_2
        diff = abs(score_1 - score_2)
        
        comparison_data.append({
            "Dimension": dimension,
            model_1: f"{score_1:.2f}",
            model_2: f"{score_2:.2f}",
            "Advantage": winner,
            "Gap": f"{diff:.2f}"
        })
    
    st.dataframe(comparison_data, use_container_width=True, hide_index=True)

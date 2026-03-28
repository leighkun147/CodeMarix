"""
new_ui_theme.py - Creative & Experimental UI Design System
Modern, vibrant Blue & Purple theme with animations and interactive elements
"""
import streamlit as st
from typing import Dict, Optional
import json

# ============================================================================
# CREATIVE COLOR PALETTE (Blue & Purple)
# ============================================================================

CREATIVE_PALETTE = {
    # Primary Blues
    "blue_dark": "#0f172a",      # Deep navy background
    "blue_mid": "#1e3a8a",       # Mid blue
    "blue_bright": "#3b82f6",    # Vibrant blue
    "blue_accent": "#60a5fa",    # Lighter blue accent
    
    # Purple & Violet
    "purple_dark": "#2e1065",    # Deep purple
    "purple_mid": "#6b21a8",     # Rich purple
    "purple_bright": "#a855f7",  # Vibrant purple
    "purple_accent": "#d8b4fe",  # Light purple accent
    
    # Accents
    "cyan_accent": "#06b6d4",    # Cyan pop
    "pink_accent": "#ec4899",    # Pink highlight
    "indigo_accent": "#6366f1",  # Indigo accent
    
    # Neutrals
    "white": "#ffffff",
    "text_primary": "#f8fafc",   # Almost white
    "text_secondary": "#cbd5e1", # Light gray
    "text_muted": "#94a3b8",     # Muted gray
    "bg_dark": "#0f172a",
    "bg_darker": "#0c0e27",
    "border": "#334155",         # Slate border
}


def apply_creative_theme():
    """Apply the creative/experimental UI theme with CSS styling"""
    
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        
        body {{
            background: linear-gradient(135deg, {CREATIVE_PALETTE['bg_dark']} 0%, {CREATIVE_PALETTE['blue_dark']} 100%);
            color: {CREATIVE_PALETTE['text_primary']};
        }}
        
        /* Main container */
        .main {{
            background: linear-gradient(135deg, {CREATIVE_PALETTE['bg_dark']} 0%, {CREATIVE_PALETTE['purple_dark']} 100%);
            padding: 2rem;
        }}
        
        /* Page title styling */
        h1 {{
            background: linear-gradient(135deg, {CREATIVE_PALETTE['blue_bright']} 0%, {CREATIVE_PALETTE['purple_bright']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
        }}
        
        h2 {{
            color: {CREATIVE_PALETTE['text_primary']};
            font-size: 1.75rem;
            font-weight: 700;
            margin: 2rem 0 1rem 0;
        }}
        
        h3 {{
            color: {CREATIVE_PALETTE['blue_accent']};
            font-size: 1.25rem;
            font-weight: 600;
            margin: 1.5rem 0 0.75rem 0;
        }}
        
        /* Metadata/description text */
        .metadata {{
            color: {CREATIVE_PALETTE['text_secondary']};
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }}
        
        /* Creative card styling */
        .creative-card {{
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.3) 0%, rgba(107, 33, 168, 0.2) 100%);
            border: 1px solid rgba({CREATIVE_PALETTE['blue_bright']}, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }}
        
        .creative-card:hover {{
            border-color: rgba({CREATIVE_PALETTE['purple_bright']}, 0.6);
            box-shadow: 0 12px 24px rgba({CREATIVE_PALETTE['purple_bright']}, 0.15),
                        0 0 40px rgba({CREATIVE_PALETTE['cyan_accent']}, 0.1);
            transform: translateY(-4px);
        }}
        
        /* Winner banner */
        .winner-banner {{
            background: linear-gradient(135deg, {CREATIVE_PALETTE['blue_bright']} 0%, {CREATIVE_PALETTE['purple_bright']} 50%, {CREATIVE_PALETTE['pink_accent']} 100%);
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
            color: white;
            font-size: 1.5rem;
            font-weight: 700;
            box-shadow: 0 20px 40px rgba({CREATIVE_PALETTE['purple_bright']}, 0.3),
                        0 0 60px rgba({CREATIVE_PALETTE['blue_bright']}, 0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .winner-banner::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translate(0, 0); }}
            50% {{ transform: translate(30px, 30px); }}
            100% {{ transform: translate(0, 0); }}
        }}
        
        /* Stat box styling */
        .stat-box {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
            border: 1px solid rgba({CREATIVE_PALETTE['blue_accent']}, 0.3);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .stat-box:hover {{
            border-color: rgba({CREATIVE_PALETTE['purple_bright']}, 0.6);
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(168, 85, 247, 0.15) 100%);
            box-shadow: 0 0 20px rgba({CREATIVE_PALETTE['purple_bright']}, 0.2);
        }}
        
        .stat-value {{
            font-size: 1.875rem;
            font-weight: 800;
            background: linear-gradient(135deg, {CREATIVE_PALETTE['blue_bright']} 0%, {CREATIVE_PALETTE['purple_bright']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0.5rem 0;
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: {CREATIVE_PALETTE['text_secondary']};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* Button styling */
        .stButton > button {{
            background: linear-gradient(135deg, {CREATIVE_PALETTE['blue_bright']} 0%, {CREATIVE_PALETTE['purple_bright']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 4px 15px rgba({CREATIVE_PALETTE['purple_bright']}, 0.3);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 8px 25px rgba({CREATIVE_PALETTE['purple_bright']}, 0.5),
                        0 0 40px rgba({CREATIVE_PALETTE['cyan_accent']}, 0.2);
            transform: translateY(-2px);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
            box-shadow: 0 4px 15px rgba({CREATIVE_PALETTE['purple_bright']}, 0.3);
        }}
        
        /* Tab styling */
        .stTabs [role="tablist"] {{
            background: transparent;
            border-bottom: 2px solid rgba({CREATIVE_PALETTE['blue_accent']}, 0.3);
            gap: 0;
        }}
        
        .stTabs [role="tablist"] button {{
            background: transparent;
            color: {CREATIVE_PALETTE['text_secondary']};
            border: none;
            border-bottom: 2px solid transparent;
            padding: 1rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .stTabs [role="tablist"] button:hover {{
            color: {CREATIVE_PALETTE['blue_accent']};
        }}
        
        .stTabs [role="tablist"] button[aria-selected="true"] {{
            color: {CREATIVE_PALETTE['text_primary']};
            border-bottom: 2px solid;
            border-bottom-color: {CREATIVE_PALETTE['purple_bright']};
        }}
        
        .stTabs [role="tablist"] button[aria-selected="true"]::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, {CREATIVE_PALETTE['blue_bright']} 0%, {CREATIVE_PALETTE['purple_bright']} 100%);
        }}
        
        /* Input styling */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stMultiSelect > div > div > div {{
            background: rgba({CREATIVE_PALETTE['blue_mid']}, 0.1) !important;
            border: 1px solid rgba({CREATIVE_PALETTE['blue_accent']}, 0.3) !important;
            border-radius: 8px !important;
            color: {CREATIVE_PALETTE['text_primary']} !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {CREATIVE_PALETTE['purple_bright']} !important;
            box-shadow: 0 0 0 3px rgba({CREATIVE_PALETTE['purple_bright']}, 0.1) !important;
            background: rgba({CREATIVE_PALETTE['blue_mid']}, 0.15) !important;
        }}
        
        /* Dataframe styling */
        .stDataFrame {{
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.2) 0%, rgba(107, 33, 168, 0.1) 100%);
            border-radius: 8px;
            border: 1px solid rgba({CREATIVE_PALETTE['blue_accent']}, 0.2);
        }}
        
        /* Metric containers */
        .metric-container {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(168, 85, 247, 0.05) 100%);
            border: 1px solid rgba({CREATIVE_PALETTE['indigo_accent']}, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }}
        
        .metric-container:hover {{
            border-color: {CREATIVE_PALETTE['purple_bright']};
            box-shadow: 0 8px 16px rgba({CREATIVE_PALETTE['purple_bright']}, 0.1);
        }}
        
        /* Progress bar */
        .streamlit-progressBar > div > div > div {{
            background: linear-gradient(90deg, {CREATIVE_PALETTE['blue_bright']} 0%, {CREATIVE_PALETTE['purple_bright']} 100%);
            border-radius: 10px;
        }}
        
        /* Status messages */
        .stSuccess {{
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(49, 145, 117, 0.08) 100%);
            border-left: 4px solid #22c55e;
            border-radius: 8px;
        }}
        
        .stError {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.08) 100%);
            border-left: 4px solid #ef4444;
            border-radius: 8px;
        }}
        
        .stWarning {{
            background: linear-gradient(135deg, rgba(234, 179, 8, 0.1) 0%, rgba(202, 138, 4, 0.08) 100%);
            border-left: 4px solid #eab308;
            border-radius: 8px;
        }}
        
        .stInfo {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(168, 85, 247, 0.08) 100%);
            border-left: 4px solid {CREATIVE_PALETTE['blue_bright']};
            border-radius: 8px;
        }}
        
        /* Divider */
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, {CREATIVE_PALETTE['border']} 50%, transparent);
            margin: 2rem 0;
        }}
        
        /* Sidebar */
        .sidebar .sidebar-content {{
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.5) 0%, rgba(30, 58, 138, 0.3) 100%);
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {CREATIVE_PALETTE['bg_darker']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {CREATIVE_PALETTE['blue_bright']} 0%, {CREATIVE_PALETTE['purple_bright']} 100%);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, {CREATIVE_PALETTE['blue_accent']} 0%, {CREATIVE_PALETTE['purple_accent']} 100%);
        }}
        
        /* Animation for cards */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .creative-card {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        /* Counter animation */
        @keyframes countUp {{
            from {{
                opacity: 0.5;
            }}
            to {{
                opacity: 1;
            }}
        }}
        
        .stat-value {{
            animation: countUp 0.3s ease-out;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# UI COMPONENTS
# ============================================================================

def create_stat_card(label: str, value: str, icon: str = "📊") -> str:
    """Create a beautiful stat card HTML"""
    return f"""
    <div class="stat-box">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
    </div>
    """


def create_winner_banner(winner: str, score: float) -> str:
    """Create an eye-catching winner announcement banner"""
    return f"""
    <div class="winner-banner">
        🏆 <b>{winner.upper()}</b> 🏆<br>
        <span style="font-size: 1.1rem; opacity: 0.95;">Consensus Score: {score:.2f}/5.0</span>
    </div>
    """


def create_creative_card(title: str, content: str) -> str:
    """Create a creative card with gradient background"""
    return f"""
    <div class="creative-card">
        <h3 style="margin-top: 0;">{title}</h3>
        <p style="color: #cbd5e1; margin: 0;">{content}</p>
    </div>
    """


def render_progress_section(step_name: str, status: str, progress: float = 0):
    """Render a progress section with animation"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(step_name)
    with col2:
        st.write(status)
    st.progress(progress, text=f"{int(progress*100)}%")


# ============================================================================
# HELPER: Display formatted metadata
# ============================================================================

def display_metadata(text: str):
    """Display descriptive metadata text"""
    st.markdown(f'<p class="metadata">{text}</p>', unsafe_allow_html=True)


# ============================================================================
# GRID LAYOUT HELPERS
# ============================================================================

def create_stat_grid(stats: list):
    """Create a responsive grid of stat cards"""
    cols = st.columns(len(stats))
    for col, (label, value, icon) in zip(cols, stats):
        with col:
            st.markdown(create_stat_card(label, value, icon), unsafe_allow_html=True)


# ============================================================================
# TABLE & DATA DISPLAY HELPERS
# ============================================================================

def display_formatted_dataframe(df, title: str = None, height: int = 400, 
                                hide_index: bool = False, column_config: dict = None):
    """Display a beautifully formatted dataframe with custom styling"""
    if title:
        st.subheader(title)
    
    st.dataframe(
        df,
        use_container_width=True,
        height=height,
        hide_index=hide_index,
        column_config=column_config
    )


def create_metric_table(data_dict: dict, title: str = None, sort_value: bool = True):
    """Convert a dictionary into a formatted metric table"""
    import pandas as pd
    
    df = pd.DataFrame(
        list(data_dict.items()),
        columns=['Metric', 'Value']
    )
    
    if sort_value and df['Value'].dtype in ['float64', 'int64']:
        df = df.sort_values('Value', ascending=False)
    
    if title:
        st.subheader(title)
    
    return st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Metric": st.column_config.TextColumn("📊 Metric", width="medium"),
            "Value": st.column_config.NumberColumn("📈 Value", format="%.2f")
        }
    )

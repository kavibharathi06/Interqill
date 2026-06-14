import streamlit as st
from utils.helpers import navigate_to
from components.chart_section import render_charts

def render_dashboard_page():
    """Renders the interactive analytics and skill-gap metrics dashboard."""
    report = st.session_state.report_data
    profile = st.session_state.candidate_profile

    # 1. Redirect if no practice results exist
    if report is None:
        st.warning("No practice data available for analytics. Please complete an interview practice first.")
        if st.button("⬅️ Return to Home", key="dash_home_btn"):
            navigate_to("home")
        return

    # Header section
    st.markdown("""
    <div style="margin-bottom: 25px; text-align: center;">
        <span style="font-size: 11px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.1em; color: #8B5CF6;">Analytics Center</span>
        <h1 style="font-size: 38px; margin-top: 5px; margin-bottom: 5px; letter-spacing: -0.02em;">Interactive <span class="gradient-text">Performance Charts</span></h1>
        <p style="color: #94A3B8; font-size: 14px; margin: 0;">Multi-dimensional diagnostic views mapping verified tech capacities and recommended training paths.</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. KPI Cards Grid
    total_q = len(report["responses"])
    weak_count = len(report["weak_areas"])
    strong_count = len(report["strong_areas"])
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 30px;">
        <div class="glass-card" style="margin-bottom: 0; padding: 22px !important; border-color: rgba(99, 102, 241, 0.25);">
            <small style="color: #94A3B8; display: block; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px;">Overall Rating</small>
            <span class="metric-value">{report['overall_score']}%</span>
            <div style="font-size: 12px; color: #10B981; margin-top: 4px; font-weight: 500;">Practice Complete</div>
        </div>
        <div class="glass-card" style="margin-bottom: 0; padding: 22px !important; border-color: rgba(16, 185, 129, 0.25);">
            <small style="color: #94A3B8; display: block; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px;">Strong Skills</small>
            <span class="metric-value" style="background: linear-gradient(135deg, #10B981, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{strong_count} Skills</span>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">Score &ge; 70%</div>
        </div>
        <div class="glass-card" style="margin-bottom: 0; padding: 22px !important; border-color: rgba(239, 68, 68, 0.25);">
            <small style="color: #94A3B8; display: block; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px;">Focus Gaps</small>
            <span class="metric-value" style="background: linear-gradient(135deg, #EF4444, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{weak_count} Areas</span>
            <div style="font-size: 12px; color: #EF4444; margin-top: 4px; font-weight: 500;">Revision recommended</div>
        </div>
        <div class="glass-card" style="margin-bottom: 0; padding: 22px !important; border-color: rgba(6, 182, 212, 0.25);">
            <small style="color: #94A3B8; display: block; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px;">Question Coverage</small>
            <span class="metric-value" style="background: linear-gradient(135deg, #8B5CF6, #6366F1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{total_q} Qs</span>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">Practice complete</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Render Visual Charts & Heatmaps
    render_charts(report, profile)

    # Bottom Actions
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    cols = st.columns([1, 1])
    with cols[0]:
        if st.button("⬅️ Back to Practice Report", key="dash_report_btn"):
            navigate_to("result")
    with cols[1]:
        if st.button("🔄 Start New Practice", key="dash_reset_btn"):
            st.session_state.candidate_profile = None
            st.session_state.active_questions = []
            st.session_state.current_question_idx = 0
            st.session_state.responses = []
            st.session_state.report_data = None
            navigate_to("home")

import streamlit as st
from utils.helpers import navigate_to, get_html_download_link
from components.score_card import render_score_card
from components.chart_section import render_charts

def render_result_page():
    """Renders the comprehensive single-page summary and feedback dashboard."""
    report = st.session_state.report_data
    profile = st.session_state.candidate_profile

    # 1. Redirect if no report exists
    if report is None:
        st.warning("No practice report available. Please complete an interview practice first.")
        if st.button("⬅️ Return to Home"):
            navigate_to("home")
        return

    # Summary Page Title
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <span style="font-size: 11px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.1em; color: #6366F1;">Practice Feedback Dashboard</span>
        <h1 style="font-size: 44px; margin-top: 5px; margin-bottom: 8px; letter-spacing: -0.03em;">Your Performance <span class="gradient-text">Summary</span></h1>
        <p style="color: #94A3B8; font-size: 14.5px; margin: 0 auto; max-width: 600px;">Review your overall ratings, unlocked achievements, skill diagnostics, and tech recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Score Card Component (top layout)
    render_score_card(
        score=report["overall_score"],
        tech_score=report["technical_score"],
        comm_score=report["communication_score"],
        label=f"Verified profile report for {profile['name']}"
    )

    # 3. Achievements & Strengths Grid
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("<h4 style='color: #6366F1; font-size: 17px; margin-bottom: 15px;'>🏆 Unlocked Badges</h4>", unsafe_allow_html=True)
        # Custom achievements display
        for ach in report["achievements"]:
            st.markdown(f"""
            <div class="glass-card" style="display: flex; align-items: center; gap: 18px; padding: 16px 20px; border-color: rgba(99, 102, 241, 0.25); margin-bottom: 12px !important;">
                <span style="font-size: 30px; line-height: 1;">{ach['icon']}</span>
                <div>
                    <strong style="color: #F8FAFC; font-size: 14.5px; display: block; font-family: 'Poppins', sans-serif;">{ach['title']}</strong>
                    <span style="color: #94A3B8; font-size: 12px; display: block; line-height: 1.4; margin-top: 2px;">{ach['desc']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_right:
        st.markdown("<h4 style='color: #06B6D4; font-size: 17px; margin-bottom: 15px;'>📈 Strategic Recommendations</h4>", unsafe_allow_html=True)
        recs_html = "".join([f"<li style='margin-bottom: 12px; font-size: 13.5px; color: #E2E8F0; line-height: 1.5;'>{rec}</li>" for rec in report["recommendations"]])
        st.markdown(f"""
        <div class="glass-card" style="height: calc(100% - 32px); padding: 24px !important;">
            <ul style="padding-left: 20px; margin: 0;">
                {recs_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 4. Strengths vs Weaknesses side-by-side lists
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    col_str, col_weak = st.columns(2)
    
    with col_str:
        st.markdown("<h4 style='color: #10B981; font-size: 17px; margin-bottom: 15px;'>✓ Core Strengths</h4>", unsafe_allow_html=True)
        if report["strong_areas"]:
            for item in report["strong_areas"]:
                st.markdown(f"""
                <div class="glass-card" style="padding: 12px 18px !important; margin-bottom: 8px !important; border-color: rgba(16, 185, 129, 0.25); background: rgba(16, 185, 129, 0.02) !important;">
                    <span style="font-size: 13.5px; font-weight: 600; color: #A7F3D0;">✓ {item}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No strong skills verified (score >= 70%). Keep practicing to build confidence!")

    with col_weak:
        st.markdown("<h4 style='color: #EF4444; font-size: 17px; margin-bottom: 15px;'>⚠ Focus Areas</h4>", unsafe_allow_html=True)
        if report["weak_areas"]:
            for item in report["weak_areas"]:
                st.markdown(f"""
                <div class="glass-card" style="padding: 12px 18px !important; margin-bottom: 8px !important; border-color: rgba(239, 68, 68, 0.25); background: rgba(239, 68, 68, 0.02) !important;">
                    <span style="font-size: 13.5px; font-weight: 600; color: #FCA5A5;">⚠ {item}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Zero weakness categories logged! You met all technical expectations.")

    # 5. Visual Diagnostics & Charts
    render_charts(report, profile)

    # 6. Collapsible transcript review fold
    st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)
    with st.expander("🔍 View Detailed Question-by-Question Transcript"):
        st.markdown("<h4 style='color: #C084FC; font-size: 18px; margin-bottom: 15px;'>Detailed Response Evaluations</h4>", unsafe_allow_html=True)
        for idx, resp in enumerate(report["responses"]):
            eval_res = resp["evaluation"]
            color = "#10B981" if eval_res["final_score"] >= 70.0 else ("#8B5CF6" if eval_res["final_score"] >= 50.0 else "#EF4444")
            
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {color}; padding: 22px !important; margin-bottom: 16px !important;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <strong style="color: #F8FAFC; font-size: 14.5px;">Question {idx + 1} ({resp['skill']})</strong>
                    <span style="font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 12px; background: rgba(255, 255, 255, 0.05); color: #94A3B8;">
                        Score: {eval_res['final_score']}%
                    </span>
                </div>
                <p style="margin: 0 0 10px 0; font-size: 14px; color: #E2E8F0; line-height: 1.5; font-weight: 500;">
                    {resp['question']}
                </p>
                <div style="margin-bottom: 12px;">
                    <small style="color: #94A3B8; display: block; font-size: 11px; text-transform: uppercase;">Your Response</small>
                    <p style="margin: 4px 0 0 0; font-size: 13px; color: #E2E8F0; line-height: 1.5; font-style: italic;">
                        "{resp['answer']}"
                    </p>
                </div>
                <div style="padding: 10px 12px; background: rgba(99, 102, 241, 0.03); border-radius: 8px; border: 1px dashed rgba(99, 102, 241, 0.1); margin-bottom: 10px;">
                    <small style="color: #818CF8; display: block; font-size: 11px; text-transform: uppercase;">Expected Reference Keywords</small>
                    <p style="margin: 4px 0 0 0; font-size: 13px; color: #E2E8F0; line-height: 1.4;">
                        {resp['expected_answer']}
                    </p>
                </div>
                <div style="font-size: 12.5px; color: #94A3B8; line-height: 1.4;">
                    <strong>Coach Review:</strong> "{eval_res['feedback']}"
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 7. Download & Export
    st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="border-color: rgba(6, 182, 212, 0.25); background: rgba(6, 182, 212, 0.02) !important;">
        <h4 style="margin-top: 0; color: #06B6D4; font-size: 16px; margin-bottom: 8px;">📄 Export Report Dashboard</h4>
        <p style="font-size: 13px; color: #94A3B8; margin-bottom: 20px; line-height: 1.5;">
            Generate and download a print-friendly HTML portfolio of your practice transcript. Open it in your browser to print to PDF.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Download link HTML anchor
    download_link = get_html_download_link(report, profile)
    st.markdown(download_link, unsafe_allow_html=True)

    # Re-run button
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Start New Practice Session", key="result_start_new_btn"):
        st.session_state.active_questions = []
        st.session_state.current_question_idx = 0
        st.session_state.responses = []
        st.session_state.report_data = None
        navigate_to("interview")

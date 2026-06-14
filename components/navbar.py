import streamlit as st
from utils.helpers import navigate_to

def render_navbar():
    """Renders the sticky, glassmorphic navigation bar."""
    # Sticky Navigation Header
    st.markdown("""
    <div class="sticky-nav" style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #6366F1, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Poppins', sans-serif; letter-spacing: -0.03em;">InterQill</span>
            <span style="font-size: 11px; padding: 2px 10px; background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 20px; color: #A5B4FC; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">AI Platform</span>
        </div>
        <div style="font-size: 13.5px; color: #94A3B8; font-weight: 500; letter-spacing: -0.01em;">
            Practice. Evaluate. Improve.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if reset options should show below header (if candidate profile is loaded)
    if st.session_state.candidate_profile is not None:
        cols = st.columns([7, 1])
        with cols[1]:
            # Reset button to reload the application
            if st.button("🔄 Reset Profile", key="reset_profile_btn", use_container_width=True):
                # Clear session state objects
                st.session_state.candidate_profile = None
                st.session_state.active_questions = []
                st.session_state.current_question_idx = 0
                st.session_state.responses = []
                st.session_state.report_data = None
                navigate_to("home")

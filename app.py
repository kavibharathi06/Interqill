import streamlit as st
from utils.helpers import init_session_state, inject_premium_css
from components.navbar import render_navbar
from pages.home import render_home_page
from pages.interview import render_interview_page
from pages.result import render_result_page
from pages.dashboard import render_dashboard_page

# 1. Page Configuration Setup (must be the first Streamlit command called)
st.set_page_config(
    page_title="InterQill - Premium AI Interview Practice Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # 2. Session State Initialization
    init_session_state()

    # 3. Premium CSS Injection
    inject_premium_css()

    # 4. Display Navigation Header
    render_navbar()

    # 5. Routing Controller
    current_page = st.session_state.page

    try:
        if current_page == "home":
            render_home_page()
        elif current_page == "interview":
            render_interview_page()
        elif current_page == "result":
            render_result_page()
        elif current_page == "dashboard":
            render_dashboard_page()
        else:
            st.error(f"Routing Error: Page '{current_page}' not found.")
            if st.button("Return to Home"):
                st.session_state.page = "home"
                st.rerun()
    except Exception as e:
        st.error(f"An unexpected error occurred during execution: {e}")
        st.info("Try restarting the session or resetting the application from the toolbar.")

if __name__ == "__main__":
    main()

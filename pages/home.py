import streamlit as st
from utils.helpers import navigate_to
from services.resume_service import ResumeService

# A standard sample resume text for candidates testing the app
SAMPLE_RESUME_TEXT = """
Alex Morgan
alex.morgan@techmail.io
+1-415-555-2671
Full-Stack Data Engineer

Professional Summary:
Dynamic developer specializing in backend architectures, data engineering pipelines, and machine learning models.

Technical Skills:
- Programming Languages: Python, Java, JavaScript
- Frameworks & Web: React, NodeJS, Django, Flask, HTML, CSS
- Databases & Storage: SQL, MySQL, MongoDB
- Data Science & ML: Machine Learning, Deep Learning, NumPy, Pandas, NLP, TensorFlow, PyTorch
- Analytics & Reporting: Streamlit, Data Science, Data Analysis
"""

def render_home_page():
    """Renders the minimal, Stripe-inspired landing page with one primary upload CTA."""
    # 1. Hero Title & Tagline
    st.markdown("""
    <div style="text-align: center; padding: 60px 10px 40px 10px;">
        <div style="display: inline-flex; align-items: center; justify-content: center; margin-bottom: 20px; background: rgba(99, 102, 241, 0.08); padding: 8px 18px; border-radius: 30px; border: 1px solid rgba(99, 102, 241, 0.15);">
            <span style="font-size: 13px; font-weight: 700; color: #A5B4FC; letter-spacing: 0.08em; text-transform: uppercase;">Introducing InterQill</span>
        </div>
        <h1 style="font-size: 58px; line-height: 1.1; margin-bottom: 15px; font-weight: 800; letter-spacing: -0.03em;">
            Practice. Evaluate. <span class="gradient-text">Improve.</span>
        </h1>
        <p style="font-size: 19px; color: #94A3B8; max-width: 600px; margin: 0 auto; line-height: 1.6; font-weight: 400; letter-spacing: -0.01em;">
            Guided technical interview practice and explainable skill-gap analysis powered by classical NLP.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Main Upload Column
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    
    with col_mid:
        st.markdown("""
        <div class="glass-card" style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 48px; margin-bottom: 16px; color: #6366F1;">📄</div>
            <h3 style="margin-top: 0; margin-bottom: 8px; font-size: 20px; color: #F8FAFC;">Resume Upload</h3>
            <p style="font-size: 13px; color: #94A3B8; margin-bottom: 24px; line-height: 1.5;">
                Drag and drop your resume in PDF format. We will parse it to identify your technical skills and customize a tailored interview.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Primary Uploader Widget
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            label_visibility="collapsed",
            key="resume_uploader_main"
        )
        
        if uploaded_file is not None:
            # Render a skeleton loader/upload animation for premium visual experience
            with st.spinner("Extracting profile & validating skills..."):
                try:
                    resume_service = ResumeService()
                    pdf_bytes = uploaded_file.read()
                    profile = resume_service.process_resume(pdf_bytes)
                    
                    if not profile["skills"]:
                        # Fallback default stack
                        profile["skills"] = ["Python", "SQL", "JavaScript"]
                        
                    st.session_state.candidate_profile = profile
                    st.success("Resume parsed successfully!")
                    
                    # CTA button to start setup
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    if st.button("Continue to Interview Configuration ➡️", use_container_width=True):
                        navigate_to("interview")
                except Exception as e:
                    st.error(f"Failed to process resume: {e}")
                    
        # 3. Secondary Sample Profile Onboarding (styled subtly at the bottom)
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        with st.expander("💡 Don't have a resume handy? Try a demo profile"):
            st.markdown("""
            <p style="font-size: 13px; color: #94A3B8; margin-bottom: 15px; line-height: 1.5; text-align: center;">
                Load our pre-configured technical profile to immediately test the interview practice session and view analytical dashboards.
            </p>
            """, unsafe_allow_html=True)
            if st.button("Load Mock Candidate Profile ✨", use_container_width=True):
                resume_service = ResumeService()
                profile = resume_service.process_resume(SAMPLE_RESUME_TEXT.strip())
                st.session_state.candidate_profile = profile
                navigate_to("interview")

import streamlit as st
import base64
from typing import Dict, Any, List

def init_session_state():
    """Initializes all necessary session state variables for InterQill."""
    if "page" not in st.session_state:
        st.session_state.page = "home"
        
    if "candidate_profile" not in st.session_state:
        st.session_state.candidate_profile = None
        
    if "active_questions" not in st.session_state:
        st.session_state.active_questions = []
        
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
        
    if "responses" not in st.session_state:
        st.session_state.responses = []
        
    if "report_data" not in st.session_state:
        st.session_state.report_data = None

def navigate_to(page_name: str):
    """Safely updates the page variable and triggers a re-run."""
    st.session_state.page = page_name
    st.rerun()

def inject_premium_css():
    """Injects Apple/Stripe-inspired premium Glassmorphic CSS matching the exact design requirements."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Set dark theme variables */
    :root {
        --bg-color: #0B1120;
        --card-bg: rgba(255, 255, 255, 0.06);
        --primary-color: #6366F1;
        --secondary-color: #8B5CF6;
        --accent-color: #06B6D4;
        --success-color: #10B981;
        --text-color: #F8FAFC;
        --text-secondary: #94A3B8;
        --border-color: rgba(255, 255, 255, 0.08);
    }
    
    /* Global Overrides */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        letter-spacing: -0.02em;
    }
    
    /* Hide default Streamlit headers and footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth page fade-in transition */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stApp {
        animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Sticky Header wrapper */
    .sticky-nav {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(11, 17, 32, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border-color);
        padding: 15px 30px;
        margin-bottom: 30px;
        border-radius: 0 0 16px 16px;
    }
    
    /* Premium Glassmorphic Card (Apple + Stripe style) */
    .glass-card {
        background: var(--card-bg) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 20px !important;
        padding: 28px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.25), inset 0 1px 0 0 rgba(255, 255, 255, 0.08) !important;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s ease !important;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 50px 0 rgba(99, 102, 241, 0.15), inset 0 1px 0 0 rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(99, 102, 241, 0.35) !important;
    }
    
    /* Visual Skills Chips */
    .skill-chip {
        display: inline-block;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #A5B4FC;
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 13.5px;
        font-weight: 500;
        margin: 6px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        text-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
    }
    
    .skill-chip:hover {
        transform: scale(1.06) translateY(-2px);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
        border-color: rgba(99, 102, 241, 0.6);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
    }
    
    .other-chip {
        display: inline-block;
        background: rgba(6, 182, 212, 0.08);
        border: 1px solid rgba(6, 182, 212, 0.25);
        color: #67E8F9;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 12.5px;
        margin: 4px;
        transition: all 0.3s ease;
    }
    
    .other-chip:hover {
        transform: translateY(-1px);
        background: rgba(6, 182, 212, 0.15);
        border-color: rgba(6, 182, 212, 0.5);
    }
    
    /* Gradient Action Buttons (Apple/Stripe inspired) */
    div.stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: var(--text-color) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 12px 28px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        box-shadow: 0 4px 16px 0 rgba(99, 102, 241, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px 0 rgba(99, 102, 241, 0.45), 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%) !important;
    }
    
    /* Secondary/Reset style buttons override */
    div.stButton > button[key*="reset"], div.stButton > button[key*="back"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: none !important;
    }
    
    div.stButton > button[key*="reset"]:hover, div.stButton > button[key*="back"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Text inputs and Textareas */
    textarea, input {
        background-color: rgba(11, 17, 32, 0.6) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 14px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    textarea:focus, input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Gradient Text Header styling */
    .gradient-text {
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 50%, #22D3EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    .metric-value {
        font-size: 44px;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #22D3EE 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
    }
    
    /* Progress Bars container overrides */
    .progress-bar-container {
        width: 100%;
        height: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .tech-fill {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
    }
    
    .comm-fill {
        background: linear-gradient(90deg, var(--accent-color), var(--success-color));
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
    }
    
    /* Loading skeletons */
    @keyframes skeleton-glow {
        0% { background-color: rgba(255, 255, 255, 0.03); }
        50% { background-color: rgba(255, 255, 255, 0.08); }
        100% { background-color: rgba(255, 255, 255, 0.03); }
    }
    
    .skeleton-loader {
        animation: skeleton-glow 1.5s infinite ease-in-out;
        border-radius: 12px;
        height: 24px;
        margin-bottom: 12px;
    }
    
    /* Custom styling for file uploader zone */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 2px dashed rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 40px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--primary-color) !important;
        background: rgba(99, 102, 241, 0.04) !important;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Responsive margins */
    @media (max-width: 768px) {
        .glass-card {
            padding: 20px !important;
        }
        h1 {
            font-size: 32px !important;
        }
        .metric-value {
            font-size: 36px !important;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def generate_html_report(report_data: Dict[str, Any], candidate_info: Dict[str, Any]) -> str:
    """Generates a complete, beautiful self-contained HTML file of the candidate report for download."""
    skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in candidate_info['skills']])
    other_skills_html = "".join([f'<span class="other-tag">{s}</span>' for s in candidate_info['other_skills']])
    
    recommendations_html = "".join([f'<li>{rec}</li>' for rec in report_data['recommendations']])
    achievements_html = "".join([
        f'<div class="achievement-card"><span>{a["icon"]}</span> <div><strong>{a["title"]}</strong><br><small>{a["desc"]}</small></div></div>'
        for a in report_data['achievements']
    ])
    
    q_breakdown_html = ""
    for idx, resp in enumerate(report_data['responses']):
        eval_res = resp['evaluation']
        q_breakdown_html += f"""
        <div class="q-row">
            <h4>Q{idx+1}: {resp['question']} ({resp['skill']})</h4>
            <p><strong>Your Answer:</strong> <em>{resp['answer']}</em></p>
            <p><strong>Expected Concept:</strong> <em>{resp['expected_answer']}</em></p>
            <div class="score-row">
                <span>Technical: <strong>{eval_res['technical_score']}%</strong></span>
                <span>Communication: <strong>{eval_res['communication_score']}%</strong></span>
                <span>Combined: <strong>{eval_res['final_score']}%</strong></span>
            </div>
            <p><small style="color: #64748B;">{eval_res['feedback']}</small></p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>InterQill Performance Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #0B1120;
                color: #F8FAFC;
                margin: 0;
                padding: 40px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: #1E293B;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 40px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            }}
            .header {{
                border-bottom: 2px solid #334155;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            h1 {{ color: #6366F1; margin: 0; font-size: 32px; }}
            .score-circle {{
                float: right;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: linear-gradient(135deg, #6366F1, #8B5CF6);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(99,102,241,0.4);
            }}
            .meta {{ color: #94A3B8; margin-top: 10px; }}
            .section {{ margin-bottom: 30px; }}
            h3 {{ color: #06B6D4; border-left: 4px solid #6366F1; padding-left: 10px; }}
            .skill-tag {{
                display: inline-block;
                background: rgba(99, 102, 241, 0.2);
                border: 1px solid rgba(99, 102, 241, 0.4);
                color: #818CF8;
                padding: 4px 10px;
                border-radius: 12px;
                margin: 4px;
                font-size: 14px;
            }}
            .other-tag {{
                display: inline-block;
                background: rgba(6, 182, 212, 0.1);
                border: 1px solid rgba(6, 182, 212, 0.3);
                color: #22D3EE;
                padding: 4px 10px;
                border-radius: 12px;
                margin: 4px;
                font-size: 14px;
            }}
            .achievement-card {{
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.05);
                padding: 12px 20px;
                border-radius: 10px;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 15px;
            }}
            .q-row {{
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.05);
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 15px;
            }}
            .score-row {{
                margin: 15px 0;
                display: flex;
                gap: 20px;
                font-size: 14px;
                color: #94A3B8;
            }}
            .score-row strong {{ color: #F8FAFC; }}
            ul {{ padding-left: 20px; line-height: 1.6; }}
            @media print {{
                body {{ background: white; color: black; padding: 20px; }}
                .container {{ background: white; border: none; box-shadow: none; padding: 0; }}
                h1, h3 {{ color: #1E1B4B; }}
                .skill-tag, .other-tag {{ border: 1px solid #94A3B8; color: black; background: #F1F5F9; }}
                .achievement-card, .q-row {{ border: 1px solid #E2E8F0; background: #F8FAFC; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="score-circle">{report_data['overall_score']}%</div>
                <h1>InterQill Performance Report</h1>
                <div class="meta">
                    <strong>Candidate:</strong> {candidate_info['name']}<br>
                    <strong>Email:</strong> {candidate_info['email']} | <strong>Phone:</strong> {candidate_info['phone']}<br>
                    <strong>Technical Score:</strong> {report_data['technical_score']}% | <strong>Communication Score:</strong> {report_data['communication_score']}%
                </div>
            </div>
            
            <div class="section">
                <h3>Extracted Tech Profile</h3>
                <div>{skills_html}</div>
                <div style="margin-top: 10px;">{other_skills_html}</div>
            </div>

            <div class="section">
                <h3>Key Achievements</h3>
                {achievements_html}
            </div>

            <div class="section">
                <h3>Improvement Recommendations</h3>
                <ul>{recommendations_html}</ul>
            </div>

            <div class="section">
                <h3>Detailed Answers Breakdown</h3>
                {q_breakdown_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html

def get_html_download_link(report_data: Dict[str, Any], candidate_info: Dict[str, Any]) -> str:
    """Creates a clickable Streamlit download link for the report."""
    html_content = generate_html_report(report_data, candidate_info)
    b64 = base64.b64encode(html_content.encode()).decode()
    filename = f"interqill_report_{candidate_info['name'].replace(' ', '_').lower()}.html"
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="display:inline-block; background:linear-gradient(135deg, #06B6D4 0%, #10B981 100%); color:white; padding:12px 28px; border-radius:12px; text-decoration:none; font-weight:600; box-shadow:0 8px 20px rgba(6,182,212,0.25); font-family:\'Poppins\',sans-serif; transition: all 0.3s ease;">📥 Export Detailed Report (HTML/PDF)</a>'

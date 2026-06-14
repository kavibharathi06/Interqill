import streamlit as st
from typing import Dict, Any

def render_resume_card(profile: Dict[str, Any]):
    """Renders candidate parsed summary with glowing skill chips."""
    if not profile:
        return
        
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.03) !important;">
        <div style="width: 56px; height: 56px; border-radius: 50%; background: rgba(16, 185, 129, 0.15); display: flex; align-items: center; justify-content: center; margin: 0 auto 16px auto; border: 1px solid rgba(16, 185, 129, 0.35); box-shadow: 0 0 16px rgba(16, 185, 129, 0.2);">
            <span style="color: #10B981; font-size: 24px; font-weight: bold;">✓</span>
        </div>
        <h3 style="margin-top: 0; color: #10B981; font-size: 22px;">Resume Extracted & Profile Created</h3>
        <p style="color: #94A3B8; font-size: 13.5px; margin: 0 auto max-width: 500px;">
            Your credentials have been parsed. Key contact information and skill tags are listed below. Raw text processing logs are hidden for a clean candidate experience.
        </p>
    </div>
    
    <div class="glass-card">
        <h4 style="margin-top: 0; color: #6366F1; font-size: 18px; margin-bottom: 20px;">👤 Profile Overview</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
            <div>
                <small style="color: #94A3B8; display: block; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px;">Candidate Name</small>
                <strong style="font-size: 15px; color: #F8FAFC;">{profile['name']}</strong>
            </div>
            <div>
                <small style="color: #94A3B8; display: block; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px;">Email Address</small>
                <strong style="font-size: 15px; color: #F8FAFC;">{profile['email']}</strong>
            </div>
            <div>
                <small style="color: #94A3B8; display: block; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px;">Contact Number</small>
                <strong style="font-size: 15px; color: #F8FAFC;">{profile['phone']}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Skills section with rounded cards and glow effect
    st.markdown("<h4 style='color: #8B5CF6; margin-top: 25px;'>🛠️ Detected Core Technologies</h4>", unsafe_allow_html=True)
    if profile['skills']:
        chips = "".join([f'<div class="skill-chip">{skill}</div>' for skill in profile['skills']])
        st.markdown(f'<div style="margin-bottom: 25px; padding: 10px 0; display: flex; flex-wrap: wrap;">{chips}</div>', unsafe_allow_html=True)
    else:
        st.info("No matching core skills were detected in the uploaded PDF. A default development stack (Python, SQL, JavaScript) will be used for your practice.")

    # Other auxiliary skills
    if profile['other_skills']:
        st.markdown("<h4 style='color: #06B6D4; margin-top: 15px;'>🔍 Associated Skill tags (Skill2Vec)</h4>", unsafe_allow_html=True)
        other_chips = "".join([f'<div class="other-chip">{skill}</div>' for skill in profile['other_skills']])
        st.markdown(f'<div style="margin-bottom: 25px; padding: 10px 0; display: flex; flex-wrap: wrap;">{other_chips}</div>', unsafe_allow_html=True)

import streamlit as st
from utils.helpers import navigate_to
from services.question_service import QuestionService
from services.evaluation_service import EvaluationService
from components.question_card import render_question_card
from components.score_card import render_score_card

def render_interview_page():
    """Renders the setup dashboard or the active interview sequence."""
    profile = st.session_state.candidate_profile
    
    # 1. Redirect if no profile exists
    if profile is None:
        st.warning("Please upload a resume or select a sample profile first.")
        if st.button("⬅️ Return to Home"):
            navigate_to("home")
        return

    # 2. Setup screen: Interview has not started yet
    if not st.session_state.active_questions:
        render_interview_setup(profile)
        return

    # 3. Active Interview Loop
    idx = st.session_state.current_question_idx
    questions = st.session_state.active_questions
    
    # Check if category breakdown page is active (skill complete transition)
    if st.session_state.get("category_breakdown_active", False):
        render_category_breakdown()
        return

    # Get active question details
    active_q = questions[idx]
    
    # Check if feedback has already been generated for this step
    feedback = st.session_state.get("current_feedback", None)

    # Callback: when user clicks Submit Answer
    def handle_submit(answer: str):
        with st.spinner("Analyzing response..."):
            eval_service = EvaluationService()
            res = eval_service.evaluate_response(answer, active_q["expected_answer"])
            
            # Save evaluation feedback
            st.session_state.current_feedback = res
            
            # Add to response record
            st.session_state.responses.append({
                "skill": active_q["skill"],
                "question": active_q["question"],
                "expected_answer": active_q["expected_answer"],
                "answer": answer,
                "evaluation": res
            })
            st.rerun()

    # Callback: when user clicks Next Question / Finish
    def handle_next():
        current_skill = active_q["skill"]
        next_idx = idx + 1
        
        # Reset current feedback state
        st.session_state.current_feedback = None
        
        # Check if we have completed all questions in the active interview
        if next_idx >= len(questions):
            with st.spinner("Compiling final transcript..."):
                eval_service = EvaluationService()
                report = eval_service.aggregate_results(st.session_state.responses)
                st.session_state.report_data = report
                
                # Navigate directly to final report page
                st.session_state.current_question_idx = next_idx
                navigate_to("result")
        else:
            # Check if the next question belongs to a different skill category
            next_skill = questions[next_idx]["skill"]
            
            if current_skill != next_skill:
                # Store the index we want to jump to after checkpoint page
                st.session_state.next_question_idx_holder = next_idx
                st.session_state.category_breakdown_active = True
                st.session_state.category_breakdown_skill = current_skill
                st.rerun()
            else:
                st.session_state.current_question_idx = next_idx
                st.rerun()

    # Render the active question card (displays question, input area, and progress)
    render_question_card(
        question_data=active_q,
        current_idx=idx,
        total_questions=len(questions),
        on_submit=handle_submit,
        on_next=handle_next,
        feedback_data=feedback
    )

def render_interview_setup(profile):
    """Renders customization controls (which skills to test, count)."""
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top: 0; color: #6366F1; font-size: 24px; letter-spacing: -0.02em;">Practice Setup</h2>
        <p style="font-size: 13.5px; color: #94A3B8; margin-bottom: 0; line-height: 1.5;">
            Configure your self-guided practice session. Choose which of your extracted skills you wish to practice, and specify the number of test questions per skill.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Columns layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Selected Technologies to Practice:")
        selected_skills = []
        
        # Render a checkbox list of detected core skills
        cols_skills = st.columns(2)
        for i, skill in enumerate(profile["skills"]):
            col_target = cols_skills[i % 2]
            with col_target:
                if st.checkbox(skill, value=True, key=f"setup_check_{skill}"):
                    selected_skills.append(skill)
                    
        if not selected_skills:
            st.warning("Please select at least one technology to practice.")
            
    with col2:
        st.markdown("#### Practice Settings:")
        q_count = st.slider(
            "Questions per technology:",
            min_value=1,
            max_value=3,
            value=2,
            help="Select the depth of testing. Standard practice uses 2 questions per skill."
        )

    # Trigger action button
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    if st.button("Start Practice Session 🚀", use_container_width=True):
        if not selected_skills:
            st.error("Select at least one skill to start.")
        else:
            with st.spinner("Generating practice bank..."):
                q_service = QuestionService()
                active_qs = q_service.prepare_interview_questions(
                    skills=selected_skills,
                    resume_text=profile.get("raw_text", ""),
                    questions_per_skill=q_count
                )
                
                if not active_qs:
                    st.error("Error creating practice questions. Verify your skill selections.")
                else:
                    st.session_state.active_questions = active_qs
                    st.session_state.current_question_idx = 0
                    st.session_state.responses = []
                    st.session_state.category_breakdown_active = False
                    st.rerun()

def render_category_breakdown():
    """Renders the intermediate category completion stats and coach review."""
    skill = st.session_state.get("category_breakdown_skill", "")
    responses = st.session_state.responses
    
    # Filter responses matching this specific skill
    skill_res = [r for r in responses if r["skill"] == skill]
    
    if not skill_res:
        st.session_state.category_breakdown_active = False
        st.rerun()
        return

    # Calculate average scores for this skill category
    avg_tech = sum(r["evaluation"]["technical_score"] for r in skill_res) / len(skill_res)
    avg_comm = sum(r["evaluation"]["communication_score"] for r in skill_res) / len(skill_res)
    avg_final = sum(r["evaluation"]["final_score"] for r in skill_res) / len(skill_res)
    
    # Formulate performance summary
    if avg_final >= 80:
        summary = f"Excellent proficiency! You demonstrated a strong understanding of **{skill}** concepts, utilizing precise technical terminology."
    elif avg_final >= 60:
        summary = f"Capable performance. You answered the core concepts of **{skill}** correctly, though adding more background context and technical terms would improve your score."
    else:
        summary = f"Significant skill gaps detected in **{skill}**. Consider revising fundamental syntax, debugging protocols, and operational definitions."

    # Render intermediate scoreboard
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 25px;">
        <span style="font-size: 11px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.1em; color: #10B981;">Checkpoint Reached</span>
        <h2 style="font-size: 32px; margin-top: 5px; letter-spacing: -0.02em;">Category Completed: <span class="gradient-text">{skill}</span></h2>
    </div>
    """, unsafe_allow_html=True)
    
    render_score_card(
        score=round(avg_final, 1),
        tech_score=round(avg_tech, 1),
        comm_score=round(avg_comm, 1),
        label=f"{skill} Performance Checkpoint"
    )
    
    st.markdown(f"""
    <div class="glass-card">
        <h4 style="margin-top: 0; color: #8B5CF6; font-size: 16px;">Performance Summary</h4>
        <p style="margin: 0; font-size: 14px; color: #E2E8F0; line-height: 1.6;">
            {summary}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Continue button to trigger next question
    if st.button("Proceed to Next Category ➡️", use_container_width=True):
        st.session_state.current_question_idx = st.session_state.next_question_idx_holder
        st.session_state.category_breakdown_active = False
        st.rerun()

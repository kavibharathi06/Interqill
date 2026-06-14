import streamlit as st


def render_question_card(
    question_data,
    current_idx,
    total_questions,
    on_submit,
    on_next,
    feedback_data=None
):

    diff = {
        "Easy": "#10B981",
        "Medium": "#8B5CF6",
        "Hard": "#EF4444"
    }

    color = diff.get(
        question_data.get(
            "difficulty",
            "Medium"
        ),
        "#6366F1"
    )

    progress = int(
        (
            current_idx
            /
            total_questions
        )
        *
        100
    )


    st.progress(progress)


    st.markdown(
    f"""
<div style="margin-bottom:18px;">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:12px;
">

<div>

<h1 style="
margin:0;
font-size:48px;
font-weight:700;
color:#F8FAFC;
">
{question_data['skill']}
</h1>

<div style="
color:#94A3B8;
font-size:15px;
">

Question {current_idx+1} / {total_questions}

</div>

</div>

</div>


<div
style="
padding:34px;
border-radius:22px;
background:rgba(255,255,255,.04);
border:1px solid rgba(255,255,255,.08);
"
>

<div
style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:18px;
"
>

<div
style="
color:#94A3B8;
font-size:14px;
font-weight:600;
text-transform:uppercase;
letter-spacing:.08em;
"
>

{question_data.get("domain","Frontend")}

</div>


<div
style="
background:{color};
padding:7px 16px;
border-radius:999px;
color:white;
font-size:13px;
font-weight:700;
"
>

{question_data["difficulty"]}

</div>

</div>


<h2
style="
margin:0;
font-size:28px;
line-height:1.6;
color:#F8FAFC;
"
>

{question_data["question"]}

</h2>

</div>

</div>
""",
    unsafe_allow_html=True
)
    if feedback_data is None:

        answer = st.text_area(
            "",
            key=f"answer_{current_idx}",
            placeholder="Explain clearly...\nMention technical concepts..."
        )

        _, c = st.columns([5, 1])

        with c:

            if st.button(
                "Submit",
                use_container_width=True
            ):

                if answer.strip():

                    on_submit(answer)

                else:

                    st.warning(
                        "Enter answer"
                    )

        return


    st.markdown(
        "## 📊 Question Evaluation Report"
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Technical",
            f"{feedback_data.get('technical_score',0)}%"
        )

    with c2:

        st.metric(
            "Communication",
            f"{feedback_data.get('communication_score',0)}%"
        )

    with c3:

        st.metric(
            "Final Score",
            f"{feedback_data.get('final_score',0)}%"
        )


    st.info(
        question_data.get(
            "expected_answer",
            "No reference answer"
        )
    )


    st.success(
        feedback_data.get(
            "feedback",
            "No feedback"
        )
    )


    _, c = st.columns([5, 1])

    with c:

        label = (
            "Finish"
            if current_idx + 1 >= total_questions
            else
            "Next"
        )

        if st.button(
            label,
            use_container_width=True
        ):

            on_next()
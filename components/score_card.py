import streamlit as st


def render_score_card(
    score: float,
    tech_score: float,
    comm_score: float,
    label="Overall Score Breakdown"
):

    st.markdown(
        f"""
<style>

.metric-card {{
padding:20px;
border-radius:18px;
background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.08);
}}

.progress {{
height:10px;
background:rgba(255,255,255,.06);
border-radius:999px;
overflow:hidden;
}}

.fill {{
height:100%;
border-radius:999px;
}}

.tech {{
background:linear-gradient(
90deg,
#6366F1,
#8B5CF6
);
}}

.comm {{
background:linear-gradient(
90deg,
#06B6D4,
#10B981
);
}}

</style>

<div class="glass-card">

<h3 style="
margin-top:0;
color:#6366F1;
margin-bottom:25px;
">

{label}

</h3>

<div
style="
display:grid;
grid-template-columns:1fr 1.5fr;
gap:40px;
align-items:center;
"
>

<div
style="
text-align:center;
padding:20px;
"
>

<div
style="
font-size:12px;
color:#94A3B8;
text-transform:uppercase;
margin-bottom:10px;
"
>

Final Rating

<div
style="
font-size:72px;
font-weight:800;
font-family:Poppins,sans-serif;
background:linear-gradient(135deg,#6366F1,#8B5CF6,#06B6D4);
background-clip:text;
-webkit-background-clip:text;
color:transparent;
-webkit-text-fill-color:transparent;
line-height:1;
"
>
{score}%

</div>

</div>


<div>

<div style="margin-bottom:25px;">

<div
style="
display:flex;
justify-content:space-between;
margin-bottom:8px;
"
>

<span>
Technical Accuracy
</span>

<span>
{tech_score}%
</span>

</div>

<div class="progress">

<div
class="fill tech"
style="
width:{tech_score}%;
"
></div>

</div>

</div>


<div>

<div
style="
display:flex;
justify-content:space-between;
margin-bottom:8px;
"
>

<span>
Communication
</span>

<span>
{comm_score}%
</span>

</div>

<div class="progress">

<div
class="fill comm"
style="
width:{comm_score}%;
"
></div>

</div>

</div>

</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )
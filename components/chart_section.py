import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def render_charts(
    report_data,
    candidate_info
):

    st.markdown(
        """
<h3 style="
margin-top:30px;
font-size:22px;
color:#8B5CF6;
">
📊 Visual Performance Diagnostics
</h3>
""",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        render_radar_chart(
            report_data[
                "skill_scores"
            ]
        )

    with col2:

        render_progress_chart(
            report_data[
                "responses"
            ]
        )

    render_gap_heatmap(
        report_data,
        candidate_info
    )


def render_radar_chart(
    skill_scores
):

    if not skill_scores:

        st.info(
            "No skill scores available"
        )

        return


    skills = list(
        skill_scores.keys()
    )

    scores = list(
        skill_scores.values()
    )


    count = len(
        skills
    )


    angles = np.linspace(

        0,

        2
        *
        np.pi,

        count,

        endpoint=False

    ).tolist()


    scores += scores[:1]

    angles += angles[:1]


    fig, ax = plt.subplots(

        figsize=(5, 5),

        subplot_kw={
            "polar": True
        }

    )


    fig.patch.set_facecolor(
        "#0B1120"
    )


    ax.set_facecolor(
        "#111827"
    )


    ax.plot(

        angles,

        scores,

        color="#8B5CF6",

        linewidth=3

    )


    ax.fill(

        angles,

        scores,

        color="#8B5CF6",

        alpha=0.30

    )


    ax.set_ylim(
        0,
        100
    )


    ax.grid(

        color="#334155",

        alpha=0.3

    )


    ax.spines[
        "polar"
    ].set_color(
        "#334155"
    )


    plt.xticks(

        angles[:-1],

        skills,

        color="#CBD5E1",

        fontsize=9

    )


    plt.yticks(

        [20, 40, 60, 80],

        color="#64748B"

    )


    st.markdown(
        """
<div class="glass-card">

<h4 style="
color:#8B5CF6;
">

Skill Profile

</h4>

</div>
""",
        unsafe_allow_html=True
    )


    st.pyplot(
        fig,
        clear_figure=True
    )

    plt.close(fig)


def render_progress_chart(
    responses
):

    if not responses:

        return


    final = []

    tech = []

    comm = []


    for r in responses:

        e = r[
            "evaluation"
        ]

        final.append(
            e[
                "final_score"
            ]
        )

        tech.append(
            e[
                "technical_score"
            ]
        )

        comm.append(
            e[
                "communication_score"
            ]
        )


    x = list(

        range(

            1,

            len(
                responses
            )

            + 1

        )

    )


    fig, ax = plt.subplots(
        figsize=(5, 5)
    )


    fig.patch.set_facecolor(
        "#0B1120"
    )


    ax.set_facecolor(
        "#111827"
    )


    ax.plot(

        x,

        final,

        marker="o",

        linewidth=3,

        color="#8B5CF6",

        label="Overall"

    )


    ax.plot(

        x,

        tech,

        linestyle="--",

        color="#6366F1",

        label="Technical"

    )


    ax.plot(

        x,

        comm,

        linestyle=":",

        color="#06B6D4",

        label="Communication"

    )


    ax.set_ylim(
        0,
        100
    )


    ax.set_xlabel(

        "Questions",

        color="#CBD5E1"

    )


    ax.set_ylabel(

        "Score",

        color="#CBD5E1"

    )


    ax.tick_params(

        colors="#94A3B8"

    )


    ax.grid(

        color="#334155",

        alpha=0.2

    )


    for spine in ax.spines.values():

        spine.set_color(
            "#334155"
        )


    ax.legend(

        facecolor="#111827",

        edgecolor="#334155"

    )


    st.markdown(
        """
<div class="glass-card">

<h4 style="
color:#06B6D4;
">

Performance Timeline

</h4>

</div>
""",
        unsafe_allow_html=True
    )


    st.pyplot(
        fig,
        clear_figure=True
    )

    plt.close(fig)


def render_gap_heatmap(
    report_data,
    candidate_info
):

    scores = report_data[
        "skill_scores"
    ]


    st.markdown(
        """
### 🔥 Skill Gap Analysis
""",
        unsafe_allow_html=True
    )


    for skill, score in scores.items():

        if score >= 70:

            st.success(
                f"{skill} • {score}%"
            )

        elif score >= 50:

            st.warning(
                f"{skill} • {score}%"
            )

        else:

            st.error(
                f"{skill} • {score}%"
            )

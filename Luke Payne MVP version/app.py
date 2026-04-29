from __future__ import annotations

import streamlit as st

from src.planner import build_workout_plan, next_step_for_effort_and_pain


st.set_page_config(
    page_title="AI Workout Assistant MVP",
    page_icon="🏋️",
    layout="centered",
)

st.title("AI Workout Assistant MVP")
st.write(
    "A small rule-based workout assistant for busy students and beginner lifters. "
    "Enter your situation and the app builds a simple, safe workout plan."
)

with st.sidebar:
    st.header("User Inputs")

    focus = st.selectbox(
        "Workout focus",
        ["arms", "back", "legs", "core", "full_body"],
        format_func=lambda value: "full body" if value == "full_body" else value,
    )

    equipment_choice = st.selectbox(
        "Available equipment",
        [
            "no equipment",
            "dumbbells only",
            "chair only",
            "no equipment and chair",
            "dumbbells and chair",
        ],
    )

    equipment_map = {
        "no equipment": ["none"],
        "dumbbells only": ["dumbbells"],
        "chair only": ["chair"],
        "no equipment and chair": ["none", "chair"],
        "dumbbells and chair": ["dumbbells", "chair"],
    }

    minutes_available = st.slider(
        "Minutes available",
        min_value=5,
        max_value=60,
        value=20,
        step=5,
    )

    experience_level = st.selectbox(
        "Experience level",
        ["beginner", "intermediate", "advanced"],
    )

    busy_student = st.checkbox(
        "Prefer dorm-friendly options",
        value=True,
    )

    pain_status = st.radio(
        "Any pain right now?",
        ["no", "yes"],
        horizontal=True,
    )

    pain_area = None
    if pain_status == "yes":
        pain_area = st.selectbox(
            "Pain area",
            ["knee", "shoulder", "arm", "back", "upper_body"],
            format_func=lambda value: "upper body" if value == "upper_body" else value,
        )

    effort_level = st.slider(
        "Current effort level",
        min_value=1,
        max_value=10,
        value=6,
    )

    notes = st.text_area(
        "Extra notes",
        placeholder="Example: small dorm room, tired today, knee pain, no gym access",
    )

if st.button("Build My Workout", type="primary"):
    result = build_workout_plan(
        experience_level=experience_level,
        focus=focus,
        minutes_available=minutes_available,
        equipment=equipment_map[equipment_choice],
        busy_student=busy_student,
        pain_area=pain_area,
    )

    st.subheader("Recommended Plan")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total time", f"{result['total_minutes']} min")
    col2.metric("Time left", f"{result['time_left']} min")
    col3.metric("Exercises", len(result["plan"]))

    if result["plan"]:
        for index, item in enumerate(result["plan"], start=1):
            with st.expander(f"{index}. {item['name']}", expanded=True):
                st.write(f"**Body part:** {item['body_part']}")
                st.write(f"**Time:** {item['minutes']} minutes")
                st.write(f"**Prescription:** {item['prescription']}")
                st.write(f"**Rest:** {item['rest_seconds']} seconds")
                st.write(f"**Form cue:** {item['form_cue']}")
                st.write(f"**Equipment:** {item['equipment']}")
    else:
        st.warning("No safe plan was found with the current inputs.")

    st.subheader("Why This Plan")
    st.write(result["rationale"])

    if result.get("safety_note"):
        st.subheader("Safety Note")
        st.warning(result["safety_note"])

    st.subheader("In-the-Moment Coaching Check")
    follow_up = next_step_for_effort_and_pain(
        high_effort=effort_level >= 8,
        pain_reported=pain_status == "yes",
    )
    st.write(follow_up["message"])
    st.caption(follow_up["safety_note"])

    if notes:
        st.subheader("User Notes")
        st.write(notes)
else:
    st.info("Use the sidebar inputs, then click **Build My Workout**.")

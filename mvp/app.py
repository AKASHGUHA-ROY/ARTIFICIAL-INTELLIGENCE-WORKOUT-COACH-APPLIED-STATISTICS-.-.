import streamlit as st

from src.workout_logic import recommend_workout


st.title("AI Workout Assistant MVP")

st.write(
    "Enter your workout situation, and the assistant will recommend a safe next step."
)

muscle_group = st.selectbox(
    "Target muscle group",
    ["arms", "back", "legs", "full body", "chest", "core"],
)

equipment = st.selectbox(
    "Available equipment",
    ["no equipment", "dumbbells only", "gym equipment", "resistance band"],
)

duration_minutes = st.slider(
    "Workout duration in minutes",
    min_value=5,
    max_value=60,
    value=20,
)

experience_level = st.selectbox(
    "Experience level",
    ["beginner", "intermediate", "advanced"],
)

effort_level = st.slider(
    "Current effort level",
    min_value=1,
    max_value=10,
    value=6,
)

pain_status = st.selectbox(
    "Are you feeling pain?",
    ["no", "yes"],
)

notes = st.text_area(
    "Extra notes",
    placeholder="Example: knee pain, busy student, small dorm room, missed workout, etc.",
)

if st.button("Get Recommendation"):
    result = recommend_workout(
        muscle_group=muscle_group,
        equipment=equipment,
        duration_minutes=duration_minutes,
        experience_level=experience_level,
        effort_level=effort_level,
        pain_status=pain_status,
        notes=notes,
    )

    st.subheader("Recommended Next Step")
    st.write(result["recommended_next_step"])

    st.subheader("Reason")
    st.write(result["reason"])

    st.subheader("Safety Adjustment")
    st.write(result["safety_adjustment"])

    st.subheader("Alternative Easier Option")
    st.write(result["alternative_easier_option"])

    st.subheader("Progression / Replan Note")
    st.write(result["progression_note"])

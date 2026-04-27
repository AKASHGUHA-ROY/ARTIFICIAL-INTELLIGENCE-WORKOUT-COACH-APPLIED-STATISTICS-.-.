


st.set_page_config(page_title="AI Workout Assistant MVP", page_icon="🏋️")

st.title("AI Workout Assistant MVP")

st.write(
    "Enter your workout situation, and the assistant will recommend a safe next step "
    "using a small rule-based workout planner."
)

st.divider()

focus = st.selectbox(
    "Target workout focus",
    ["arms", "back", "legs", "core", "full_body"],
    format_func=lambda x: "full body" if x == "full_body" else x,
)

equipment_choice = st.selectbox(
    "Available equipment",
    [
        "no equipment",
        "dumbbells only",
        "chair only",
        "no equipment + chair",
        "dumbbells + chair",
    ],
)

equipment_map = {
    "no equipment": ["none"],
    "dumbbells only": ["dumbbells"],
    "chair only": ["chair"],
    "no equipment + chair": ["none", "chair"],
    "dumbbells + chair": ["dumbbells", "chair"],
}

equipment = equipment_map[equipment_choice]

minutes_available = st.slider(
    "Workout duration in minutes",
    min_value=5,
    max_value=60,
    value=20,
)

experience_level = st.selectbox(
    "Experience level",
    ["beginner", "intermediate", "advanced"],
)

busy_student = st.checkbox(
    "I am a busy student / need dorm-friendly options",
    value=True,
)

pain_reported = st.selectbox(
    "Are you feeling pain?",
    ["no", "yes"],
)

pain_area = None
if pain_reported == "yes":
    pain_area = st.selectbox(
        "Where is the pain?",
        ["knee", "upper_body", "arm", "shoulder", "back"],
        format_func=lambda x: "upper body" if x == "upper_body" else x,
    )

effort_level = st.slider(
    "Current effort level",
    min_value=1,
    max_value=10,
    value=6,
)

notes = st.text_area(
    "Extra notes",
    placeholder="Example: small dorm room, knee pain, tired today, missed yesterday's workout, etc.",
)

st.divider()

if st.button("Get Recommendation"):
    result = build_workout_plan(
        experience_level=experience_level,
        focus=focus,
        minutes_available=minutes_available,
        equipment=equipment,
        busy_student=busy_student,
        pain_area=pain_area,
    )

    st.subheader("Recommended Workout Plan")

    if result["plan"]:
        for index, item in enumerate(result["plan"], start=1):
            equipment_text = ", ".join(item["equipment"])
            rounds_text = (
                f"{item['rounds']} rounds"
                if item["rounds"] > 1
                else "1 round"
            )

            st.write(
                f"**{index}. {item['name']}** — "
                f"{item['total_minutes']} minutes total, "
                f"{rounds_text}, equipment: {equipment_text}"
            )
    else:
        st.warning("No safe workout was found with the current constraints.")

    st.subheader("Total Time")
    st.write(f"{result['total_minutes']} minutes")

    st.subheader("Why This Plan")
    st.write(result["rationale"])

    if result.get("safety_note"):
        st.subheader("Safety Note")
        st.warning(result["safety_note"])

    st.subheader("In-the-Moment Coaching Check")

    follow_up = next_step_for_effort_and_pain(
        high_effort=effort_level >= 8,
        pain_reported=pain_reported == "yes",
    )

    st.write(follow_up["message"])
    st.caption(follow_up["safety_note"])

    if notes:
        st.subheader("User Notes Considered")
        st.write(notes)

       

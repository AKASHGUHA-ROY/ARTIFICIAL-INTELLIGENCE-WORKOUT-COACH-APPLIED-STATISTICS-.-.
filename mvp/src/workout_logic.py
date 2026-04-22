def recommend_workout(
    muscle_group,
    equipment,
    duration_minutes,
    experience_level,
    effort_level,
    pain_status,
    notes,
):
    muscle_group = muscle_group.lower()
    equipment = equipment.lower()
    experience_level = experience_level.lower()
    pain_status = pain_status.lower()
    notes = notes.lower()

    if pain_status == "yes":
        return {
            "recommended_next_step": "Stop the painful movement for now and switch to a pain-free option.",
            "reason": "Pain is a safety signal, so the assistant should not recommend pushing through it.",
            "safety_adjustment": "Avoid sharp, worsening, or unstable pain. If pain continues, stop the session and consider getting help from a qualified professional.",
            "alternative_easier_option": "Do light mobility, walking, or an upper-body/core movement that does not trigger pain.",
            "progression_note": "Return to normal training only after the movement feels pain-free and controlled.",
        }

    if duration_minutes <= 15:
        time_note = "Keep the session short and simple with 2 rounds."
    elif duration_minutes <= 25:
        time_note = "Use a compact workout with 2 to 3 main exercises."
    else:
        time_note = "Use a fuller workout with 3 to 5 exercises."

    if experience_level == "beginner":
        level_note = "Use beginner-friendly movements and moderate intensity."
    else:
        level_note = "Use moderate to challenging movements while keeping form controlled."

    if "no equipment" in equipment:
        equipment_note = "Use bodyweight, wall-based, or floor-based movements."
    elif "dumbbell" in equipment:
        equipment_note = "Use dumbbell-based exercises and avoid assuming machines or a bench."
    else:
        equipment_note = "Use only the equipment listed by the user."

    if effort_level >= 8:
        effort_note = "Because effort is high, reduce intensity slightly or take a longer rest."
    else:
        effort_note = "Effort is manageable, so continue with controlled progression."

    if "arm" in muscle_group:
        workout = "wall push-ups, controlled tricep dips, arm circles, and isometric bicep squeezes"
    elif "back" in muscle_group:
        workout = "dumbbell rows, bent-over reverse flys, Romanian deadlifts, and controlled shrugs"
    elif "leg" in muscle_group:
        workout = "bodyweight squats to a chair, glute bridges, calf raises, and light mobility"
    elif "full" in muscle_group:
        workout = "bodyweight squats, wall push-ups, glute bridges, and plank holds"
    else:
        workout = "simple full-body movements based on the user’s available equipment"

    return {
        "recommended_next_step": f"Do a {duration_minutes}-minute {muscle_group} session using {workout}.",
        "reason": f"{time_note} {level_note} {equipment_note}",
        "safety_adjustment": "Move with control and stop if pain appears.",
        "alternative_easier_option": "Use fewer reps, shorter sets, or an easier bodyweight variation.",
        "progression_note": effort_note,
    }

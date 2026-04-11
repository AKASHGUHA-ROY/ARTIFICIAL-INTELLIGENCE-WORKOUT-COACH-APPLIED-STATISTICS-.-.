def recommend_next_step(user):
    muscle = user["muscle_group"].lower()
    duration = user["duration_minutes"]
    experience = user["experience_level"].lower()
    effort = user["effort_level"]
    pain = user["pain_flag"]

    if pain:
        return {
            "target_muscle_group": muscle,
            "recommended_next_step": "Stop the current exercise and switch to a lower-intensity or pain-free variation.",
            "reason": "Pain was reported, so safety comes first.",
            "safety_adjustment": "Reduce load or stop the session if pain continues.",
            "alternative_easier_option": "Light mobility work or pain-free bodyweight movement."
        }

    if muscle in ["arm", "arms"]:
        return {
            "target_muscle_group": "arms",
            "recommended_next_step": "Do a short beginner arm session with wall push-ups, controlled tricep dips, and isometric bicep squeezes.",
            "reason": "This matches arm day, beginner level, no-equipment limits, and a short 20-minute workout.",
            "safety_adjustment": "Stop if pain appears and reduce range of motion if elbows or shoulders feel uncomfortable.",
            "alternative_easier_option": "Use wall push-ups, arm circles, and isometric arm squeezes only."
        }

    if muscle == "chest":
        return {
            "target_muscle_group": "chest",
            "recommended_next_step": "Do a short beginner chest session with wall push-ups or knee push-ups for 2 to 3 sets.",
            "reason": "This fits a 20-minute no-equipment chest workout for a beginner.",
            "safety_adjustment": "Stop if wrist, shoulder, or chest pain appears.",
            "alternative_easier_option": "Use wall push-ups only."
        }

    if duration <= 20:
        volume_note = "Keep the session short with 2 to 3 exercises."
    else:
        volume_note = "Use a fuller session with 3 to 5 exercises."

    if experience == "beginner":
        intensity_note = "Use simple movements and moderate volume."
    else:
        intensity_note = "Use moderate to challenging movements."

    if effort >= 8:
        next_step = "Take a longer rest and reduce intensity slightly for the next set."
    else:
        next_step = "Continue with the planned workout and progress carefully."

    return {
        "target_muscle_group": muscle,
        "recommended_next_step": next_step,
        "reason": f"{volume_note} {intensity_note}",
        "safety_adjustment": "Stop if pain appears.",
        "alternative_easier_option": "Use fewer reps or an easier bodyweight version."
    }


if __name__ == "__main__":
    sample_user = {
        "muscle_group": "arms",
        "duration_minutes": 20,
        "experience_level": "beginner",
        "effort_level": 6,
        "pain_flag": False
    }

    result = recommend_next_step(sample_user)

    print("=== Workout Assistant Demo ===")
    for key, value in result.items():
        print(f"{key}: {value}")
results for the code 
=== Workout Assistant Demo ===
target_muscle_group: arms
recommended_next_step: Do a short beginner arm session with wall push-ups, controlled tricep dips, and isometric bicep squeezes.
reason: This matches arm day, beginner level, no-equipment limits, and a short 20-minute workout.
safety_adjustment: Stop if pain appears and reduce range of motion if elbows or shoulders feel uncomfortable.
alternative_easier_option: Use wall push-ups, arm circles, and isometric arm squeezes only.


** Process exited - Return Code: 0 **

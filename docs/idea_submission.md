# Project Title
AI Workout Trainer for Personalized Live Exercise Guidance

# Team Members
- [Your Name] — [your email]
- [Teammate Name] — [teammate email]
- [Teammate Name] — [teammate email]

# Problem Statement

## Who is the user?
The main users are beginners, busy students, working professionals, and people who want to exercise at home without paying for expensive gym memberships or personal trainers. It is also useful for users who live far from gyms and depend mostly on remote workouts.

## What problem or pain point do they experience today?
Many workout apps available today provide generic workout plans that may not be suitable for every user’s fitness level, goals, or available equipment. People often depend on workout videos or tutorials, but these do not adjust to what the user is doing during the session. As a result, users may not know whether they are training safely, using the right difficulty level, or making mistakes while performing exercises. This can lead to a surface-level understanding of workouts instead of a deeper and more effective training experience.

# Why Now?

## Why does this problem matter in the next 3–5 years?
In the next few years, more people are expected to rely on flexible and affordable fitness options because of rising costs, busy schedules, and the continued growth of home-based health and wellness habits. Users will increasingly want personalized guidance rather than one-size-fits-all workout plans.

## What changed that makes this possible now?
Recent improvements in artificial intelligence, language models, and recommendation systems make it possible to build systems that respond to user input in real time. At the same time, people are more comfortable than before using digital tools for fitness, self-improvement, and remote coaching. This creates a strong opportunity for an AI-powered workout assistant.

# Proposed AI-Powered Solution

## What does your product do for the user?
Our product is an AI workout trainer that gives live guidance during exercise sessions. The user enters information such as target muscle group, available equipment, workout duration, and experience level. During the workout, the user logs each set using text-based inputs such as reps, weight, effort level, and a pain flag. Based on this information, the system immediately suggests the next step, such as continuing, adjusting weight, changing reps, resting longer, switching to an easier variation, substituting an exercise, or stopping if there is injury risk.

## Where does AI/ML add unique value vs simple rules / heuristics?
AI adds unique value by making recommendations based on each user’s individual ability and workout progress instead of giving every person the same fixed routine. A simple rule-based system may be too rigid, but AI can better adapt to different user situations and generate more personalized coaching-style guidance. This makes the experience feel closer to a live trainer than a standard workout app.

# Initial Technical Concept

## What data would you need (or already have)?
We would need user profile data such as fitness level, target muscle groups, available equipment, and workout duration. We would also need workout session data such as reps completed, weight used, effort level, rest time, and pain indicators. In the beginning, we may rely on manually created examples, public exercise datasets, and synthetic workout logs if real user data is limited.

## What model(s) might you use?
The MVP could use a recommendation model or decision-support model to provide next-step workout suggestions. A GPT-style text model could generate natural-language coaching feedback and explain recommendations clearly. A vision-based model for camera tracking may be explored later, but the MVP will mainly focus on text-based inputs.

## How could your nanoGPT work feed into this?
Our nanoGPT-style work could support the text generation part of the project by helping the system produce short coaching responses, workout explanations, and safer exercise guidance. It could also be used to generate sample outputs and evaluate how clearly and usefully the system communicates with users.

# Scope for MVP

## What can you realistically build in ~6 weeks?
In about six weeks, we can realistically build a text-based MVP where users enter their workout goals, available equipment, experience level, and workout time, and receive a basic personalized workout plan. During the session, users can log each set, and the system can return live next-step suggestions based on those logs. Full camera-based form correction is outside the scope of the MVP and will be treated as future work.

## Define a very concrete v1 feature
A user can enter their target muscle group, available equipment, workout duration, and experience level, then log each set with reps, weight, effort, and pain status, and our system returns an immediate personalized recommendation for the next step.

# Risks and Open Questions

## Top 3 unknowns
1. **Recommendation accuracy:** The system may misinterpret user logs and provide suggestions that are too hard, too easy, or not fully appropriate.
2. **Exercise matching:** The app may recommend exercises that do not perfectly match the target muscle groups or user needs.
3. **Data and evaluation:** Limited real-world workout data may make it difficult to test whether the system’s recommendations are truly safe, useful, and effective.

# Planned Data Sources
- Public fitness and exercise datasets from Kaggle
- Hugging Face datasets related to health, exercise, or recommendation tasks
- Synthetic workout logs created by the team
- Public exercise libraries or workout databases
- Small-scale user feedback collected during MVP testing

# Project Title
AI Workout Trainer for Personalized Live Exercise Guidance

# Team Members
- [Akash Guha Roy] — [akashguharoy651@gmail.com]
- [Jacob] — [jacobstone2317@gmail.com]
- [lukee] — [lukeedogan@icloud.com]
- Payne - payneluke4@gmail.com

# Problem Statement

## Who is the user?
The main users are beginners in exercise, busy students, working professionals, and people who want to exercise at home without paying for expensive gym memberships or personal trainers. It is also useful for users who live far away from gyms and depend mostly on  online workouts.

## What problem or pain point do they experience today?
Many workout apps and videos available today provide generic workout plans that may not be suitable for every user’s fitness level, goals, or available equipment. While workout videos or tutorials are helpful, but these do not adjust to what the user is doing during the session. As a result, users may not know whether they are training safely, using the right difficulty level, or making mistakes while performing exercises. This can lead to a surface-level understanding of workouts instead of a deeper and more effective training experience.

# Why Now?

## Why does this problem matter in the next 3–5 years?
In the next few years, more people are expected to rely on flexible and affordable fitness options because of rising prices , busy schedules , and lack of transportation opportunities to go to the gym. Users will increasingly want personalized guidance rather than standard workout plans that may not be helpful to everyone . .

## What changed that makes this possible now?
Recent improvements in artificial intelligence apps , language models etc. make it possible to build systems that respond to user input and provide suggestions based on it .

# Proposed AI-Powered Solution

## What does your product do for the user?
Our product is an AI workout trainer that gives live guidance during exercise sessions. The user enters information such as target muscle group, available equipment, workout duration, and experience level. During the workout, the user logs each set using text-based inputs such as reps, weight, effort level, and a pain flag. Based on this information, the system immediately suggests the next step, such as continuing, adjusting weight, changing reps, resting longer, suggesting exercises of different difficulty levels, substituting an exercise, or stopping if there is injury risk.

## Where does AI/ML add unique value vs simple rules / heuristics?
AI adds unique value by making recommendations based on each user’s individual ability and workout progress instead of giving every person the same fixed routine. A simple rule-based system may be too rigid, but AI can better adapt to different user situations and generate more personalized coaching-style guidance. This makes the experience feel closer to a live trainer who helps you every minute than a standard workout app.

# Initial Technical Concept

## What data would you need (or already have)?
We would need user profile data such as fitness level, target muscle groups, available equipment, and workout duration. We would also need workout session data such as reps completed, weight used, effort level, rest time, and pain indicators. 

## What model(s) might you use?
The MVP could use a recommendation model or decision-support model to provide next-step workout suggestions. A GPT-style text model could generate natural-language coaching feedback and explain recommendations clearly. Gemini can be sued as well . A vision-based model for camera tracking will be wroked on afterwards, but the MVP will mainly focus on text-based inputs .

## How could your nanoGPT work feed into this?
Our nanoGPT-style work could support the text generation part of the project by helping the system understand the user's demand , produce workout explanations for different muscle types, and safer exercise guidance. It could also be used to generate sample outputs and evaluate how clearly and usefully the system communicates with users .

# Scope for MVP

## What can you realistically build in ~6 weeks?
In about six weeks, we can realistically build a text-based MVP where users enter their workout goals, available equipment, experience level, and available time, and receive a basic personalized workout plan. During the session, users can log each set, and the system can return live next-step suggestions based on those logs. 

## Define a very concrete v1 feature
A user can enter their target muscle group, available equipment, workout duration, and experience level, then log each set with reps, weight, effort, and pain status, and our system returns an immediate personalized recommendation for the next course of action .

# Risks and Open Questions

## Top 3 unknowns
1.  The system may misinterpret user logs due to technical glitches where it misreads the exercises done by the users and provdes incorrect suggestions .
2.  The app may recommend exercises that do not perfectly match the target muscle groups or user needs.
3. Whether the information given by the app is accurate and safe to follow .

# Planned Data Sources
- Base log
- Information regarding workouts given by users
- Public API'S
- Public exercise libraries or workout databases
- Small-scale user feedback collected during MVP testing

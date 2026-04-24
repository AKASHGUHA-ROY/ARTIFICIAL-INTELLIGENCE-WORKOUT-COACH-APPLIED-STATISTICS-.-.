# MVP Report

## 1. Executive Summary
This project builds a simple AI Workout Assistant MVP for busy students. The MVP is a Streamlit-based app that lets a user enter workout context such as target muscle group, available equipment, time, experience level, effort, pain status, and notes. The system then gives a safe personalized next-step workout recommendation.

## 2. User & Use Case
The main target user is a busy student who needs quick workout guidance that fits real-life constraints. The MVP is meant for users who may have limited time, limited equipment, small spaces, or mild pain concerns during exercise.

## 3. System Design
The MVP uses a simple Streamlit interface for user input and a rule-based workout logic file to generate recommendations. The app collects workout details and returns:
- recommended next step
- reason
- safety adjustment
- alternative easier option
- progression / replan note
- The recommendation logic is designed to answer the immediate next step first, while respecting safety signals and user constraints such as time, equipment, and pain status.

## 4. Data
The MVP uses a small exercise reference library stored in `mvp/data/exercise_library.json`. It also uses the test cases and design ideas developed in Phase 2 as guidance for what kinds of recommendations the system should produce.

## 5. Models / AI System
This MVP does not rely on a trained generative model. Instead, it uses a structured rule-based recommendation system based on the Phase 2 workout-assistant framework. The system focuses on safe next-step guidance, constraint handling, and simple fallback logic.

## 6. Evaluation
The MVP was tested through live demo cases in GitHub Codespaces using Streamlit. At least two demo scenarios were run:
- a normal workout recommendation case
- a pain-aware safety case
  

The outputs were recorded in `mvp/artifacts/demo_outputs.md`.

## 7. Limitations & Risks
The MVP is still limited. It is not a medical tool and cannot diagnose injuries. The recommendation logic is simple and does not yet adapt deeply to all user situations. The exercise library is small, and the app does not yet use a live LLM or long-term memory.

## 8. Next Steps
Future improvements include:
- expanding the exercise library
- improving pain-specific follow-up logic
- adding better substitution rules
- improving personalization
- adding a cleaner user interface
- supporting missed-workout replanning

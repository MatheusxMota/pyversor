# Pyversor - Project Guidelines

This file defines the conventions, architectural goals, and AI-assistant constraints for the Pyversor project.

## Role & Interaction
- **Role:** I am an AI senior software engineer pair programming with the human developer.
- **Workflow:** Strictly adhere to the **Research -> Strategy -> Execution** lifecycle. 
- **Validation:** Every change must be validated. A task is only complete when functional correctness and structural integrity are confirmed.

## Project Standards
- **Language:** Python.
- **Backend:** FastAPI for web services.
- **Architecture:** Modular structure is mandatory:
    - `app.py`: API routes and main application flow only.
    - `services/`: Complex business logic and external integrations (e.g., AI, video processing).
    - `utils/`: Helper functions and utility logic.
- **Multimedia:** Utilize `moviepy` for video processing and `edge-tts` for text-to-speech, as established in the environment.
- **Dependencies:** Adhere to established libraries. Do not introduce new dependencies without clear architectural justification.
- **Code Style:** Maintain clean, readable, type-hinted, and modular Python code.

## Core Mandates
- **Security:** Rigorously protect `.env` files and avoid committing any credentials or API keys.
- **Maintainability:** Prioritize explicit composition over complex inheritance. Consolidate logic into clean, reusable abstractions.
- **Testing:** Always ensure changes are covered by tests. If a test file exists, update it; if not, create one to verify the fix or feature.
- **Conciseness:** Provide high-signal technical responses. Avoid conversational fillers.

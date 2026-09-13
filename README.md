# Real Estate AI POC

AI-powered real estate research chatbot using publicly available
property/project data from DarGlobal and Wasalt.

## Architecture

- React + TypeScript
- FastAPI
- SQLite
- ChromaDB
- OpenRouter
- Playwright
- Docker

## Current Phase

Phase 1 - application foundation.

## Run

Copy:

.env.example

to:

.env

Then configure:

OPENROUTER_API_KEY=your_key

Start:

docker compose up --build

Frontend:

http://localhost:5173

Backend:

http://localhost:8000

Health:

http://localhost:8000/health

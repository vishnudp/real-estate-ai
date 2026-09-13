# Real Estate AI Intelligence POC

AI-powered real-estate intelligence platform for property discovery, search, analysis and conversational investment insights.

The POC combines public property data ingestion, structured/semantic search, deterministic real-estate intelligence engines and a local Ollama LLM behind a React + FastAPI application.

> **POC status:** All planned functional stages are completed for the current 3-day POC scope.

---

## 1. POC Objective

The system is designed to answer questions such as:

- Is this property a good investment?
- Why is this property a good or weak deal?
- What are the main risks?
- Is the asking price reasonable?
- How does the property compare with similar properties?
- What infrastructure supports this location?
- What is the property's growth potential?
- Which properties should I investigate right now?
- Why was a particular property ranked as an opportunity?

The LLM is used primarily for conversational understanding and explanation. Scores, valuation and deal decisions come from deterministic intelligence engines.

---

## 2. Completed Pipeline

```text
DarGlobal / Wasalt
        |
        v
Data Ingestion
        |
        v
Normalization
        |
        +--------------------+
        |                    |
        v                    v
     SQLite              ChromaDB
        |                    |
        +---------+----------+
                  |
                  v
           Query Understanding
                  |
                  v
          Structured Search
                  |
                  v
            Hybrid Search
                  |
                  v
              Chat API
                  |
                  v
           Advanced Search
                  |
                  v
            Location Data
                  |
                  v
        Location Intelligence
                  |
                  v
     Infrastructure Intelligence
                  |
                  v
        Comparable Engine
                  |
                  v
         Valuation Engine
                  |
                  v
          Growth Score Engine
                  |
                  v
             Risk Engine
                  |
                  v
        Investment Profile
                  |
                  v
          Personalization
                  |
                  v
             Deal Engine
                  |
                  v
          AI Orchestration
                  |
                  v
             Guardrails
                  |
                  v
             React UI
                  |
                  v
          Docker Deployment
```

### Completion checklist

- [x] DarGlobal ingestion
- [x] Wasalt ingestion
- [x] Normalization
- [x] SQLite persistence
- [x] ChromaDB vector storage
- [x] Query understanding
- [x] Structured search
- [x] Hybrid search
- [x] Chat API
- [x] Advanced search
- [x] Location data
- [x] Location Intelligence Engine
- [x] Infrastructure Intelligence
- [x] Comparable Engine
- [x] Valuation Engine
- [x] Growth Score Engine
- [x] Risk Engine
- [x] Investment Profile
- [x] Hyper-personalization
- [x] Deal Engine
- [x] AI Orchestration
- [x] Guardrails
- [x] React UI
- [x] Docker packaging

---

## 3. Architecture

```text
                           PUBLIC DATA
          +-------------------------------------------+
          |                                           |
          |  DarGlobal       Wasalt                  |
          |  Location / POI / Public infrastructure  |
          |                                           |
          +---------------------+---------------------+
                                |
                                v
                    +-----------------------+
                    |   INGESTION LAYER     |
                    |                       |
                    | HTTP / Playwright     |
                    | Scrapers / collectors |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | NORMALIZATION         |
                    |                       |
                    | Cleaning              |
                    | Deduplication         |
                    | Entity extraction     |
                    | Price/location fields |
                    +-----------+-----------+
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
        +------------------+          +------------------+
        | SQLite           |          | ChromaDB         |
        |                  |          |                  |
        | Properties       |          | Property vectors |
        | Projects         |          | Project vectors  |
        | Locations        |          | Descriptions     |
        | Comparables      |          | Amenities        |
        | Infrastructure  |          | Market knowledge |
        | Scores           |          |                  |
        | Valuations       |          | Persistent volume|
        +--------+---------+          +--------+---------+
                 |                             |
                 +--------------+--------------+
                                |
                                v
                    +-----------------------+
                    | INTELLIGENCE ENGINES  |
                    |                       |
                    | Location              |
                    | Infrastructure        |
                    | Comparable             |
                    | Valuation              |
                    | Growth                 |
                    | Risk                  |
                    | Investment Profile     |
                    | Personalization        |
                    | Deal                  |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | AI ORCHESTRATION      |
                    |                       |
                    | Intent                |
                    | Query decomposition   |
                    | Context assembly      |
                    | Hybrid retrieval      |
                    | Prompt construction   |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | GUARDRAILS            |
                    |                       |
                    | Evidence validation  |
                    | Numeric consistency  |
                    | Output validation    |
                    | Disclaimer handling  |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | Ollama                |
                    |                       |
                    | Qwen3 / local LLM     |
                    | Embedding model       |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | FastAPI               |
                    | REST / Chat APIs      |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | React                 |
                    | Conversational UI     |
                    +-----------------------+
```

---

# 4. Intelligence Layer

## Location Intelligence

Produces location-level information used by downstream engines.

Typical inputs:

- city
- area
- coordinates
- nearby POIs
- location metadata

---

## Infrastructure Intelligence

Evaluates relevant infrastructure around the property.

Examples:

- transport
- roads
- schools
- hospitals
- retail
- airports
- public infrastructure

---

## Comparable Engine

Identifies similar properties and calculates comparable-market metrics.

Typical factors:

- property type
- location
- bedrooms
- area
- price
- price per square unit
- similarity

---

## Valuation Engine

Provides an indicative property valuation from available comparable evidence.

Example output:

```json
{
  "estimated_value": 1008988.1,
  "fair_value_low": 908089.29,
  "fair_value_high": 1109886.9,
  "upside_percent": -8.27
}
```

The LLM must not independently recalculate this value.

---

## Growth Score Engine

Produces a deterministic growth assessment from available location/infrastructure/market evidence.

Example:

```text
Growth Score: 32
Assessment: negative
```

---

## Risk Engine

Provides an investment-risk assessment.

Example:

```text
Risk Score: 49.75
Risk Level: low_moderate
```

---

## Investment Profile

Represents the user's investment preferences.

Examples:

- budget
- investment vs self-use
- target property type
- preferred location
- expected return
- risk tolerance
- time horizon

---

## Personalization

Uses the investment profile and property intelligence to make recommendations relevant to the user.

---

## Deal Engine

Combines deterministic intelligence into an opportunity assessment.

Example:

```text
Deal Score: 40.42
Decision: weak
```

The Deal Engine is authoritative for the final deal assessment when a deal decision is available.

---

# 5. AI Orchestration

The AI Orchestration layer is deliberately separated from deterministic intelligence.

```text
User Query
    |
    v
Intent Classification
    |
    v
Query Decomposition
    |
    v
Property / Search Context
    |
    +---------------------+
    |                     |
    v                     v
SQLite               ChromaDB
    |                     |
    +----------+----------+
               |
               v
     Intelligence Engines
               |
               v
        Evidence Packet
               |
               v
            Ollama
               |
               v
          Guardrails
               |
               v
        Final Response
```

The LLM should explain verified intelligence rather than inventing or recalculating scores.

---

# 6. Example AI Response

For a question such as:

> Is this property a good investment and what are the main concerns?

A target response is:

```text
Assessment:
This property appears to be a weak investment opportunity based on
the current intelligence. Deal Score: 40.42/100.

Why:
- Investment risk is moderate.
- Two priced comparable properties are available.

Main concerns:
- Investment attractiveness is limited.
- The property is priced above its estimated value.
- Growth evidence is weak.

Valuation:
Estimated value is approximately $1.01M versus an asking price
of $1.10M, indicating the property is approximately 8.27% above
estimated value.

Confidence:
The assessment is based on the available property and market
intelligence.

This is an indicative analysis based on available property data
and POC-generated intelligence. It is not financial advice or a
professional property valuation.
```

---

# 7. Self-Contained Docker Architecture

The recommended deployment keeps the complete runtime in Docker.

```text
                           PUBLIC INTERNET
                                  |
                                  v
                         +----------------+
                         | Caddy / HTTPS  |
                         | 80 / 443       |
                         +-------+--------+
                                 |
                    +------------+------------+
                    |                         |
                    v                         v
             +-------------+           +-------------+
             | React       |           | FastAPI     |
             | Container   |---------->| Container   |
             +-------------+           +------+------+
                                             |
                          +------------------+------------------+
                          |                  |                  |
                          v                  v                  v
                    +-----------+      +-----------+      +-----------+
                    | SQLite    |      | ChromaDB  |      | Ollama    |
                    | Volume    |      | Volume    |      | Container |
                    +-----------+      +-----------+      |           |
                                                          | Qwen3     |
                                                          | Embeddings|
                                                          +-----------+

```

### Runtime components

| Component | Runtime |
|---|---|
| React | Docker container |
| FastAPI | Docker container |
| SQLite | Persistent Docker volume |
| ChromaDB | Persistent Docker volume |
| Ollama | Docker container |
| Caddy | Docker container / HTTPS reverse proxy |
| Networking | Docker Compose network |

Docker Compose is intended for defining and running multi-container applications and supports persistent named volumes. See the official Docker documentation: https://docs.docker.com/compose/

---

# 8. Environment Variables

Create:

```text
.env
```

Example:

```env
APP_ENV=production

BACKEND_PORT=8000
FRONTEND_PORT=80

OLLAMA_BASE_URL=http://ollama:11434

OLLAMA_CHAT_MODEL=qwen3:4b
OLLAMA_EMBED_MODEL=nomic-embed-text:latest

SQLITE_PATH=/data/app.db
CHROMA_PATH=/data/chroma

CORS_ORIGINS=*
```

Use the exact model names already configured in the project if they differ.

Do not commit secrets or production credentials to Git.

---

# 9. Local Docker Run

From the project root:

```bash
docker compose build
docker compose up -d
```

Check:

```bash
docker compose ps
```

Logs:

```bash
docker compose logs -f
```

Backend only:

```bash
docker compose logs -f backend
```

Ollama:

```bash
docker compose logs -f ollama
```

Frontend:

```bash
docker compose logs -f frontend
```

Stop:

```bash
docker compose down
```

Restart after code changes:

```bash
docker compose up -d --build
```

Verify the final resolved Compose configuration:

```bash
docker compose config
```

---

# 10. Ollama Model Initialization

If the Ollama container starts without the required models, pull them inside the container.

Example:

```bash
docker compose exec ollama ollama pull qwen3:4b
docker compose exec ollama ollama pull nomic-embed-text:latest
```

Verify:

```bash
docker compose exec ollama ollama list
```

The model directory should be persisted with an Ollama Docker volume so models do not have to be downloaded after every container recreation.

---

# 11. FREE PUBLIC DEPLOYMENT — RENDER

For the public 3-day POC, the recommended approach is **Render Free + OpenRouter Free Models**.

This does **not** require:

- a VPS
- a purchased domain
- Firebase
- Heroku
- Caddy
- Nginx

Render gives the deployed web service its own public `onrender.com` URL. Render's free web services are intended for testing, hobby projects and previews. They spin down after 15 minutes without inbound traffic and may take about a minute to start again.

### Important architecture decision

The local development environment remains fully self-contained with Ollama:

```text
LOCAL / HANDOVER

React
  |
FastAPI
  |
SQLite + ChromaDB
  |
Ollama
  +-- Qwen3
  +-- nomic-embed-text
```

The **free public deployment must not run Ollama** on Render Free. Render's free web service is currently only `0.1 CPU / 512 MB RAM`, which is not an appropriate runtime for Ollama + Qwen3.

For the public demo, use:

```text
PUBLIC DEMO

React
  |
FastAPI
  |
SQLite + ChromaDB
  |
OpenRouter
  |
openrouter/free
```

OpenRouter currently provides the `openrouter/free` router for zero-cost inference and dynamically selects an available free model. Free models have lower rate limits and availability can change.

### Public URL

After deployment Render will provide a URL similar to:

```text
https://real-estate-ai-poc.onrender.com
```

You do **not** need to own a domain for this URL. Every Render web service receives an `onrender.com` subdomain.

---

# 12. EXACT FREE DEPLOYMENT STEPS

Follow these steps in order. Do not create a VPS or configure DNS.

## Step 1 — Put the project in GitHub

Create a GitHub repository and push the complete project.

Example:

```bash
git init
git add .
git commit -m "Real Estate AI POC"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Before pushing, make sure `.env` and API keys are ignored:

```gitignore
.env
.env.*
!.env.example
__pycache__/
node_modules/
*.pyc
.venv/
data/runtime/
```

**Never commit `OPENROUTER_API_KEY`.**

---

## Step 2 — Add the cloud deployment profile

The repository needs a cloud Dockerfile that starts **FastAPI** and serves the built React application from the same service.

The target public architecture is:

```text
Browser
   |
   v
Render URL
   |
   v
FastAPI
   |
   +--> React static build
   |
   +--> /api/properties
   +--> /api/search
   +--> /api/chat
   +--> /api/properties/{id}/ai
   |
   +--> SQLite
   +--> ChromaDB
   +--> Intelligence Engines
   +--> Guardrails
   +--> OpenRouter
```

Do not expose FastAPI separately. Render only needs one public web service.

> **Repository-specific note:** the exact `Dockerfile.cloud` contents depend on the actual `frontend/` and `backend/` paths in the repository. The next implementation step should create this file against the real project tree rather than guessing paths.

---

## Step 3 — Change React API calls to same-origin URLs

Do not hard-code:

```text
http://localhost:8000
```

in the production React build.

Use:

```text
/api/properties
/api/search
/api/chat
/api/properties/{id}/ai
```

For example:

```typescript
const API_URL = import.meta.env.VITE_API_URL || "";

fetch(`${API_URL}/api/properties`);
```

For the Render deployment:

```env
VITE_API_URL=
```

This keeps React and FastAPI under the same public URL.

---

## Step 4 — Add an OpenRouter cloud provider

Keep the existing Ollama provider for local execution.

Use an environment switch:

```env
# Local
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_CHAT_MODEL=qwen3:4b
```

For Render:

```env
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=openrouter/free
```

OpenRouter's Free Models Router is specifically intended for zero-cost inference and automatically chooses from currently available free models.

You still need an OpenRouter account/API key for API access. Put the key in Render's Environment Variables section; do not put it in GitHub.

---

## Step 5 — Create an OpenRouter API key

Open OpenRouter, create an API key, and copy it once.

You will eventually enter it in Render as:

```text
OPENROUTER_API_KEY=YOUR_SECRET_KEY
```

Do not add it to:

```text
.env committed to GitHub
README.md
React code
Dockerfile
```

---

## Step 6 — Create the Render service

Open the Render dashboard.

Choose:

```text
New
  -> Web Service
```

Connect your GitHub account and select the repository.

Render officially supports Git-backed web services and Docker-based web services.

Use these values:

```text
Name:
real-estate-ai-poc

Branch:
main

Language:
Docker

Dockerfile Path:
./Dockerfile.cloud

Plan:
Free
```

Render's Docker runtime builds the service from the Dockerfile in the repository.

---

## Step 7 — Configure the Render environment variables

In:

```text
Render
  -> Your Service
  -> Environment
  -> Environment Variables
```

add the values required by the application.

Minimum cloud configuration:

```env
APP_ENV=production

LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=YOUR_SECRET_KEY
OPENROUTER_MODEL=openrouter/free

DATABASE_URL=sqlite:////app/data/app.db
SQLITE_PATH=/app/data/app.db
CHROMA_PATH=/app/data/chroma

CORS_ORIGINS=*
```

If the current project uses different variable names, use the names already consumed by the application.

Do **not** add:

```env
OLLAMA_BASE_URL=http://localhost:11434
```

for the Render profile.

---

## Step 8 — Configure the Render port

FastAPI must listen on:

```text
0.0.0.0
```

and the Render `PORT` environment variable.

Recommended command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
```

Render documents `10000` as the default expected port, although the application should use the `PORT` environment variable.

---

## Step 9 — Deploy

Click:

```text
Create Web Service
```

Render will:

```text
GitHub
   |
   v
Docker build
   |
   v
Docker image
   |
   v
FastAPI + React
   |
   v
Public Render URL
```

Wait for the first deployment to finish.

---

## Step 10 — Open the generated URL

Render will show something similar to:

```text
https://real-estate-ai-poc.onrender.com
```

Click that URL.

That is the URL you can send to the evaluator.

No purchased domain is required.

---

# 13. RENDER FREE LIMITATIONS — IMPORTANT

Render Free is suitable for this **3-day demonstration POC**, not production.

### 1. Service sleeps

After 15 minutes without inbound traffic, the free web service spins down.

The next request starts it again and may take about one minute.

Therefore, tell the evaluator:

> The first request may take around a minute if the demo has been idle.

### 2. Local files are ephemeral

This is the most important limitation.

Render Free does **not** provide persistent disks. Changes to local files, including SQLite databases, are lost when the service redeploys, restarts, or spins down.

Therefore the public POC must **not depend on runtime-created SQLite/Chroma data surviving a restart**.

Use this approach instead:

```text
Git repository / Docker image
             |
             v
      Seed / sample data
             |
             v
      Container startup
             |
       +-----+-----+
       |           |
       v           v
    SQLite      ChromaDB
       |           |
       +-----+-----+
             |
             v
       FastAPI starts
```

For the 3-day demo, rebuild the local runtime data from the committed/packaged POC dataset when the container starts.

### 3. Ollama is not deployed on Render Free

The local deployment remains:

```text
Ollama
  +-- qwen3:4b
  +-- nomic-embed-text
```

The public deployment uses OpenRouter for LLM inference because the Render Free compute allocation is too small for Ollama/Qwen3. Render's current Free web service plan is `0.1 CPU / 512 MB RAM`.

### 4. OpenRouter free models have rate limits

The `openrouter/free` router is free, but free models have lower rate limits and their availability can change.

This is acceptable for an evaluator/demo with a small number of requests.

---

# 14. Cloud Data / ChromaDB Strategy

The local application uses:

```text
SQLite
ChromaDB
Ollama embeddings
```

For the public free deployment, do not assume Ollama is available.

There are two possible cloud strategies:

### Strategy A — Recommended for the 3-day demo

Package the already-generated POC dataset and Chroma index into the deployment artifact and use structured retrieval as the primary path.

```text
Committed POC dataset
        |
        +--> SQLite seed
        |
        +--> Chroma seed
        |
        v
     FastAPI
```

### Strategy B — Cloud embedding adapter

If semantic search must be regenerated at runtime, add a cloud embedding adapter.

OpenRouter exposes an embeddings API, but the embedding endpoint is not automatically free; the selected embedding model has its own pricing.

Therefore **do not assume that OpenRouter embeddings are free just because the chat model is free**.

For this POC, Strategy A is preferred.

---

# 15. Deployment Verification

After Render reports the deployment as live:

### Test 1 — Homepage

Open:

```text
https://YOUR-SERVICE.onrender.com
```

Expected:

```text
Property Intelligence
Real Estate Assistant
```

### Test 2 — Property list

Select a property.

### Test 3 — Investment analysis

Ask:

```text
Is this property a good investment?
```

### Test 4 — Follow-up

Ask:

```text
Why?
```

### Test 5 — Risk

Ask:

```text
What are the main concerns?
```

### Test 6 — Valuation

Ask:

```text
How does the valuation compare with the asking price?
```

### Test 7 — Comparable analysis

Ask:

```text
How does this property compare with similar properties?
```

### Test 8 — Infrastructure

Ask:

```text
What infrastructure supports this location?
```

### Test 9 — Opportunity ranking

Ask:

```text
Give me the 10 opportunities I should investigate right now based on my investment strategy.
```

---

# 16. If Render Deployment Fails

Open:

```text
Render
  -> Service
  -> Logs
```

Look for the first Python/Docker error rather than the final generic deployment message.

Common issues:

### Port error

Make sure FastAPI uses:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
```

### React API error

Make sure production React calls:

```text
/api/...
```

not:

```text
http://localhost:8000/api/...
```

### OpenRouter error

Check:

```text
OPENROUTER_API_KEY
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=openrouter/free
```

### SQLite/Chroma missing after restart

This is expected on Render Free if the application writes runtime data to the local filesystem. Rebuild/seed the POC data at startup instead of treating the local filesystem as persistent.

---

# 17. LOCAL vs PUBLIC Deployment

The repository supports two deployment profiles.

## Local / self-contained

```text
Docker Compose
     |
     +-- React
     +-- FastAPI
     +-- SQLite
     +-- ChromaDB
     +-- Ollama
           +-- Qwen3
           +-- nomic-embed-text
```

Run:

```bash
docker compose up -d --build
```

This is the **handover/self-contained** environment.

## Public / free demo

```text
Render Free
     |
     +-- React
     +-- FastAPI
     +-- SQLite / seeded POC data
     +-- ChromaDB / seeded POC data
     +-- Intelligence Engines
     +-- Guardrails
     +-- OpenRouter Free Model
```

This is the **evaluator URL** environment.

The intelligence engines remain the same.

Only the runtime LLM provider changes:

```text
LOCAL:
Ollama -> Qwen3

PUBLIC:
OpenRouter -> openrouter/free
```

---

# 18. Local Docker Quick Start

From the project root:

```bash
docker compose build
docker compose up -d
```

Check:

```bash
docker compose ps
```

Logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

Open:

```text
http://localhost
```

---

# 19. Public Deployment Quick Start

The complete free deployment sequence is:

```text
1. Create GitHub repository
        |
        v
2. Push the project
        |
        v
3. Add Dockerfile.cloud
        |
        v
4. Configure React for /api/*
        |
        v
5. Add OpenRouter provider
        |
        v
6. Create OpenRouter API key
        |
        v
7. Create Render Web Service
        |
        v
8. Select Docker runtime
        |
        v
9. Select Free plan
        |
        v
10. Add environment variables
        |
        v
11. Deploy
        |
        v
12. Open generated .onrender.com URL
        |
        v
13. Test chatbot
```

### Final result

```text
https://YOUR-SERVICE.onrender.com
```

No VPS.

No purchased domain.

No DNS configuration.

No Caddy.

No Nginx.

No separate frontend hosting.

---

# 20. POC Demo Flow

Recommended evaluator flow:

```text
1. Open Render URL
          |
2. Select DarGlobal / Wasalt property
          |
3. Ask:
   "Is this property a good investment?"
          |
4. Show:
   Deal Score
   Investment assessment
   Valuation
   Growth
   Risk
          |
5. Ask:
   "Why?"
          |
6. Ask:
   "What are the main concerns?"
          |
7. Ask:
   "How does it compare with similar properties?"
          |
8. Ask:
   "What infrastructure supports this location?"
          |
9. Ask:
   "Give me the top opportunities I should investigate."
```

This demonstrates that the application is an intelligence system rather than a generic LLM chatbot.

---

# 21. What the LLM Does vs What the Engines Do

```text
+--------------------------------+----------------------------+
| Deterministic Engines          | AI / LLM                   |
+--------------------------------+----------------------------+
| Comparable calculation         | Query understanding        |
| Valuation calculation          | Explanation                |
| Growth score                   | Conversational response    |
| Risk score                     | Ranking explanation        |
| Deal score                     | Evidence summarization     |
| Investment profile             | Natural language           |
| Infrastructure metrics         | Follow-up conversation     |
| Evidence                       | User-facing answer         |
+--------------------------------+----------------------------+
```

This separation is important because investment scores and valuations should not be hallucinated by the LLM.

---

# 22. Data Persistence

### Local Docker

The following are persisted using Docker volumes:

```text
SQLite
ChromaDB
Ollama models
```

Recommended volumes:

```text
sqlite_data
chroma_data
ollama_data
```

### Render Free

Do **not** treat the Render filesystem as persistent. Render Free web services use ephemeral filesystems and do not support persistent disks.

Therefore the public POC uses seeded/rebuildable data.

For production, move SQLite/Chroma to proper persistent storage and use a production database/vector store.

---

# 23. Troubleshooting

### Backend cannot connect to Ollama locally

Check:

```bash
docker compose logs ollama
```

Verify:

```text
OLLAMA_BASE_URL=http://ollama:11434
```

Do not use `localhost:11434` from inside the backend container.

### Model not found locally

```bash
docker compose exec ollama ollama list
docker compose exec ollama ollama pull qwen3:4b
docker compose exec ollama ollama pull nomic-embed-text:latest
```

### Render application does not start

Check Render logs and verify:

```text
host = 0.0.0.0
port = $PORT
```

### React API errors on Render

Use same-origin paths:

```text
/api/...
```

not:

```text
http://localhost:8000/...
```

### OpenRouter errors

Check:

```text
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openrouter/free
```

### First request is slow

This can happen after Render Free has spun down the service after inactivity. Wait for the service to start.

---

# 24. Scope / POC Limitations

This is a demonstration POC, not a production investment platform.

Potential production enhancements:

- authentication / authorization
- user accounts
- persistent conversation history
- production PostgreSQL
- production vector database
- background ingestion jobs
- scheduled scraping
- queue-based processing
- distributed workers
- observability
- rate limiting
- advanced security
- data freshness monitoring
- source reliability scoring
- model evaluation
- GPU inference
- automated deployment pipeline
- persistent cloud storage

These are intentionally outside the current 3-day POC scope.

---

# 25. Disclaimer

All property intelligence, valuation estimates, growth scores, risk scores and deal scores are indicative outputs based on available data and the implemented POC algorithms.

They should not be considered financial advice, investment advice, a guaranteed return, or a professional property valuation.

---

# 26. Final Deployment Architecture

## Local self-contained architecture

```text
                         LOCAL MACHINE
                              |
                              v
                    +-------------------+
                    |  Docker Compose   |
                    +---------+---------+
                              |
        +---------------------+---------------------+
        |                     |                     |
        v                     v                     v
    +--------+           +---------+          +-----------+
    | React  |           | FastAPI |          |  Ollama   |
    +--------+           +----+----+          |   Qwen3   |
                                 |             +-----------+
                       +---------+---------+
                       |                   |
                       v                   v
                   +--------+         +----------+
                   | SQLite |         | ChromaDB |
                   +--------+         +----------+
```

## Public free POC architecture

```text
                         INTERNET
                            |
                            v
             https://YOUR-SERVICE.onrender.com
                            |
                            v
                  +--------------------+
                  |    Render Free     |
                  |    Web Service     |
                  +---------+----------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
        +-------------+             +-------------+
        | React Build |             |   FastAPI   |
        | Static UI   |             |   Backend   |
        +-------------+             +------+------+
                                           |
                  +------------------------+----------------------+
                  |             |             |          |         |
                  v             v             v          v         v
               SQLite       ChromaDB     Location   Valuation   Deal
               /seeded       /seeded      Engine     Engine      Engine
               data          data            |          |          |
                  |             |             +----------+----------+
                  +-------------+                        |
                                                         v
                                                    Guardrails
                                                         |
                                                         v
                                                  OpenRouter Free
```

### Public URL

```text
https://YOUR-SERVICE.onrender.com
```

### Local URL

```text
http://localhost
```

---

# 27. Official Deployment References

- Render Free services: https://render.com/docs/free
- Render Web Services: https://render.com/docs/web-services
- Render Docker deployment: https://render.com/docs/docker
- OpenRouter Free Models Router: https://openrouter.ai/docs/guides/routing/routers/free-router
- OpenRouter Embeddings: https://openrouter.ai/docs/api/api-reference/embeddings/create-embeddings


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

Docker Compose is intended for defining and running multi-container applications and supports persistent named volumes. See the official Docker documentation: https://docs.docker.com/compose/ citeturn0search5turn0search4

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

# 11. Deploy to a Public URL

For this 3-day POC, the simplest reliable deployment is:

```text
Git repository
      |
      v
Ubuntu VPS / Cloud VM
      |
      v
Docker
      |
      v
docker compose up -d --build
      |
      v
Caddy
      |
      v
HTTPS
      |
      v
https://your-domain.com
```

This avoids introducing Kubernetes or a managed database and keeps the architecture aligned with the self-contained POC requirement.

## Recommended server

Use one Linux VM with:

- Ubuntu 22.04/24.04
- at least 8 GB RAM recommended
- 4+ vCPU recommended
- 30–50 GB SSD minimum
- public IPv4
- ports 80 and 443 available

Ollama/model inference is the main reason not to use a very small web-service instance.

---

# 12. VPS Deployment

After creating an Ubuntu VPS:

```bash
ssh ubuntu@YOUR_SERVER_IP
```

Install Docker using the official Docker instructions.

Then verify:

```bash
docker --version
docker compose version
```

Docker Compose is available as part of Docker Desktop or as the Compose plugin on Linux. citeturn0search8

Clone the project:

```bash
git clone YOUR_GIT_REPOSITORY
cd YOUR_PROJECT_DIRECTORY
```

Create `.env`:

```bash
nano .env
```

Add the production configuration.

Build and start:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
```

At this point, if the frontend is exposed directly on port 80, the temporary URL is:

```text
http://YOUR_SERVER_IP
```

For the final HTTPS URL, use a domain.

---

# 13. Domain + HTTPS

Example:

```text
poc.example.com
```

Create a DNS A record:

```text
poc.example.com  ->  YOUR_SERVER_PUBLIC_IP
```

Then configure Caddy:

```text
poc.example.com {
    reverse_proxy frontend:80
}
```

If React and FastAPI need separate routing, use:

```text
poc.example.com {
    reverse_proxy /api/* backend:8000
    reverse_proxy frontend:80
}
```

Caddy automatically manages publicly trusted HTTPS certificates when the hostname resolves to the server and ports 80/443 are reachable. citeturn0search1turn0search3

Then:

```bash
docker compose up -d
```

Your application becomes:

```text
https://poc.example.com
```

Caddy is particularly suitable for this POC because it can act as the public reverse proxy and automatically provision/renew HTTPS certificates. citeturn0search0turn0search3

---

# 14. Recommended Production Compose Topology

A deployment-oriented Compose file should have approximately these services:

```yaml
services:

  frontend:
    build:
      context: ./frontend
    restart: unless-stopped
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
    restart: unless-stopped
    environment:
      OLLAMA_BASE_URL: http://ollama:11434
      SQLITE_PATH: /data/app.db
      CHROMA_PATH: /data/chroma
    volumes:
      - sqlite_data:/data
      - chroma_data:/data/chroma
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    restart: unless-stopped
    volumes:
      - ollama_data:/root/.ollama

  caddy:
    image: caddy:latest
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - frontend
      - backend

volumes:
  sqlite_data:
  chroma_data:
  ollama_data:
  caddy_data:
  caddy_config:
```

Adapt paths and service names to the actual repository before using this exact file.

---

# 15. Important: React API Configuration

For public deployment, do not hard-code:

```text
http://localhost:8000
```

inside the React application.

Prefer same-origin API calls:

```text
/api/properties
/api/search
/api/chat
/api/properties/{id}/ai
```

Then Caddy routes:

```text
/api/*  -> backend:8000
/*      -> frontend:80
```

This means the browser only sees:

```text
https://poc.example.com
```

and the backend remains private inside the Docker network.

---

# 16. Ports

Only expose:

```text
Internet
   |
   +--> 80  Caddy
   |
   +--> 443 Caddy
```

Do **not** publicly expose:

```text
8000  FastAPI
11434 Ollama
ChromaDB port
SQLite
```

The internal services communicate through Docker's private network.

---

# 17. Deployment Verification

After deployment:

### 1. Check containers

```bash
docker compose ps
```

All required services should be running.

### 2. Check backend

```bash
docker compose exec backend \
  curl http://localhost:8000/health
```

### 3. Check Ollama

```bash
docker compose exec ollama ollama list
```

### 4. Check frontend

Open:

```text
https://YOUR_DOMAIN
```

### 5. Test property search

```text
Search Dubai properties
```

### 6. Test property intelligence

Select a property and ask:

```text
Is this property a good investment?
```

### 7. Test conversational follow-up

```text
Why?
```

```text
What are the main risks?
```

```text
How does the valuation compare with the asking price?
```

### 8. Test opportunity query

```text
Give me the 10 opportunities I should investigate
right now based on my investment strategy.
```

---

# 18. POC Demo Flow

The recommended demo should be:

```text
1. Open public URL
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

This demonstrates that the system is more than a generic LLM chatbot.

---

# 19. What the LLM Does vs What the Engines Do

```text
+--------------------------------+----------------------------+
| Deterministic Engines          | Ollama / AI                |
+--------------------------------+----------------------------+
| Comparable calculation         | Query understanding       |
| Valuation calculation          | Explanation               |
| Growth score                   | Conversational response   |
| Risk score                     | Ranking explanation       |
| Deal score                     | Evidence summarization    |
| Investment profile             | Natural language          |
| Infrastructure metrics        | Follow-up conversation    |
| Evidence                       | User-facing answer        |
+--------------------------------+----------------------------+
```

This separation is important because investment scores and valuations should not be hallucinated by the LLM.

---

# 20. Data Persistence

The following must be persistent:

```text
SQLite
ChromaDB
Ollama models
```

Do not store these only inside ephemeral containers.

Recommended:

```text
sqlite_data
chroma_data
ollama_data
```

as Docker named volumes.

---

# 21. Backup

For the POC, periodically back up:

```text
SQLite database
ChromaDB data
application configuration
.env configuration template
```

Never commit real secrets.

Example:

```bash
docker compose down

docker run --rm \
  -v project_sqlite_data:/data \
  -v $(pwd)/backup:/backup \
  alpine \
  tar czf /backup/sqlite-backup.tar.gz /data
```

Use the actual Docker volume name shown by:

```bash
docker volume ls
```

---

# 22. Troubleshooting

### Backend cannot connect to Ollama

Check:

```bash
docker compose logs ollama
```

Verify:

```text
OLLAMA_BASE_URL=http://ollama:11434
```

Do not use:

```text
localhost:11434
```

from inside the backend container.

---

### Model not found

Run:

```bash
docker compose exec ollama ollama list
```

Then:

```bash
docker compose exec ollama ollama pull qwen3:4b
```

---

### SQLite data disappeared

Verify the SQLite directory is mounted to a persistent volume.

---

### Chroma data disappeared

Verify Chroma's persistence directory is mounted to a persistent Docker volume.

---

### Frontend shows API errors

Check:

```bash
docker compose logs backend
```

and verify React calls:

```text
/api/...
```

rather than:

```text
http://localhost:8000/...
```

---

### HTTPS certificate not issued

Verify:

```text
DNS A record -> VPS public IP
```

and that ports:

```text
80
443
```

are open.

Caddy requires the public hostname to resolve to the server and external access to ports 80/443 for the normal publicly trusted certificate flow. citeturn0search1turn0search3

---

# 23. Scope / POC Limitations

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

These are intentionally outside the current 3-day POC scope.

---

# 24. Disclaimer

All property intelligence, valuation estimates, growth scores, risk scores and deal scores are indicative outputs based on available data and the implemented POC algorithms.

They should not be considered financial advice, investment advice, a guaranteed return, or a professional property valuation.

---

# 25. Quick Start

### Local

```bash
git clone YOUR_REPOSITORY
cd YOUR_PROJECT

docker compose up -d --build

docker compose ps
```

Open:

```text
http://localhost
```

### Public deployment

```text
1. Create Ubuntu VPS
2. Install Docker
3. Clone repository
4. Configure .env
5. Configure domain DNS
6. Configure Caddy
7. Run docker compose up -d --build
8. Verify containers
9. Open https://your-domain.com
```

---

## Final Deployment Architecture

```text
                         USERS
                           |
                           v
                 https://poc.example.com
                           |
                           v
                    +-------------+
                    |    Caddy    |
                    | HTTPS / TLS |
                    +------+------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
      +-------------+              +-------------+
      |   React     |              |  FastAPI    |
      | Container   |              | Container   |
      +-------------+              +------+------+
                                         |
                     +-------------------+-------------------+
                     |                   |                   |
                     v                   v                   v
               +-----------+       +-----------+       +-----------+
               | SQLite    |       | ChromaDB  |       |  Ollama   |
               | Volume    |       | Volume    |       | Container |
               +-----------+       +-----------+       |           |
                                                       | Qwen3     |
                                                       | Embedding |
                                                       +-----------+

                  Everything runs under Docker Compose
```

**Target public endpoint:**

```text
https://poc.example.com
```

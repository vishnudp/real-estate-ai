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

# 4. Complete Architecture

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              PUBLIC DATA & KNOWLEDGE SOURCES                                   │
│                                                                                              │
│   ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐                    │
│   │    DarGlobal     │     │      Wasalt      │     │ Public Location  │                    │
│   │                  │     │                  │     │ & Infrastructure │                    │
│   │ Properties       │     │ Properties       │     │ Data             │                    │
│   │ Projects         │     │ Listings         │     │                  │                    │
│   │ Prices           │     │ Prices           │     │ OSM / POIs       │                    │
│   │ Amenities        │     │ Amenities        │     │ Roads            │                    │
│   │ Locations        │     │ Locations        │     │ Metro / Transit  │                    │
│   └────────┬─────────┘     └────────┬─────────┘     │ Hospitals        │                    │
│            │                        │               │ Schools          │                    │
│            │                        │               │ Airports         │                    │
│            │                        │               └────────┬─────────┘                    │
└────────────┼────────────────────────┼────────────────────────┼───────────────────────────────┘
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  DATA INGESTION LAYER                                         │
│                                                                                              │
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────────────────┐    │
│  │ DarGlobal Scraper   │   │ Wasalt Scraper      │   │ Location / Infrastructure      │    │
│  │                     │   │                     │   │ Collector                      │    │
│  │ Playwright / HTTP   │   │ Playwright / HTTP   │   │                               │    │
│  │ Rate limiting       │   │ Rate limiting       │   │ Geospatial / Public data      │    │
│  │ Retry               │   │ Retry               │   │ POI / transport / amenities   │    │
│  └──────────┬──────────┘   └──────────┬──────────┘   └───────────────┬─────────────────┘    │
│             │                         │                              │                      │
│             └─────────────────────────┼──────────────────────────────┘                      │
│                                       ▼                                                     │
│                           ┌────────────────────────┐                                         │
│                           │  INGESTION CONTROLLER  │                                         │
│                           │                        │                                         │
│                           │ Source validation      │                                         │
│                           │ Deduplication          │                                         │
│                           │ Crawl metadata         │                                         │
│                           │ Error / retry handling │                                         │
│                           └────────────┬───────────┘                                         │
└────────────────────────────────────────┼─────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              RAW DATA / DOCUMENT STORE                                        │
│                                                                                              │
│  Raw HTML     Raw JSON     Property descriptions     Project information                    │
│  Images/URLs  Source URL   Amenities                Infrastructure information              │
│  Timestamp    Source       Location data            Market/context documents               │
│                                                                                              │
└────────────────────────────────────────┬─────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                NORMALIZATION & ENRICHMENT                                     │
│                                                                                              │
│  Cleaning              Deduplication            Entity Extraction                            │
│  Price normalization   Location normalization   Property normalization                      │
│  Project normalization Amenity extraction       Geo-coordinate normalization                │
│  Source attribution    Data freshness            Data quality scoring                        │
│                                                                                              │
└────────────────────────────────────────┬─────────────────────────────────────────────────────┘
                                         │
                         ┌───────────────┴────────────────┐
                         │                                │
                         ▼                                ▼
┌──────────────────────────────────┐       ┌──────────────────────────────────┐
│          LOCAL SQLITE            │       │           LOCAL CHROMADB         │
│                                  │       │                                  │
│ Structured / transactional data  │       │ Semantic knowledge              │
│                                  │       │                                  │
│ • Properties                     │       │ • Property descriptions         │
│ • Projects                       │       │ • Project descriptions          │
│ • Prices                         │       │ • Amenities                      │
│ • Locations                      │       │ • Infrastructure knowledge      │
│ • Amenities                      │       │ • Location knowledge             │
│ • Comparables                    │       │ • Market documents              │
│ • Infrastructure                 │       │ • Public source content         │
│ • Scores                         │       │ • Scraped textual content       │
│ • Valuations                     │       │                                  │
│ • Investment Profiles            │       │ Ollama Embeddings                │
│ • Evidence                       │       │ nomic-embed-text                 │
│ • Risks                          │       │                                  │
│ • Source metadata                │       │                                  │
└───────────────┬──────────────────┘       └────────────────┬─────────────────┘
                │                                           │
                └─────────────────────┬─────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                         REAL ESTATE INTELLIGENCE ENGINE LAYER                                │
│                                                                                              │
│   ┌──────────────────────────┐        ┌─────────────────────────────┐                       │
│   │ Location Intelligence    │        │ Infrastructure Intelligence │                       │
│   │ Engine                   │        │ Engine                      │                       │
│   │                          │        │                             │                       │
│   │ Accessibility            │        │ Roads                       │                       │
│   │ POI proximity            │        │ Metro                       │                       │
│   │ Schools                  │        │ Airports                    │                       │
│   │ Hospitals               │        │ Hospitals                   │                       │
│   │ Lifestyle                │        │ Schools                     │                       │
│   │ Location Score           │        │ Future infrastructure       │                       │
│   └────────────┬─────────────┘        │ Infrastructure Score        │                       │
│                │                      └──────────────┬──────────────┘                       │
│                │                                     │                                      │
│                └──────────────────┬──────────────────┘                                      │
│                                   │                                                         │
│   ┌───────────────────────────────┴─────────────────────────────┐                           │
│   │                                                             │                           │
│   ▼                                                             ▼                           │
│ ┌──────────────────────────┐                    ┌─────────────────────────────┐             │
│ │ Comparable Engine        │                    │ Growth Score Engine         │             │
│ │                          │                    │                             │             │
│ │ Property matching        │                    │ Location growth             │             │
│ │ Size matching            │                    │ Infrastructure growth       │             │
│ │ Bedroom matching         │                    │ Development signals          │             │
│ │ Location matching        │                    │ Market indicators            │             │
│ │ Price/sqft comparison    │                    │ Growth potential             │             │
│ │ Comparable Score          │                    │ Growth Score                 │             │
│ └────────────┬─────────────┘                    └──────────────┬──────────────┘             │
│              │                                                 │                            │
│              └──────────────────────┬──────────────────────────┘                            │
│                                     │                                                       │
│                                     ▼                                                       │
│                         ┌──────────────────────────┐                                        │
│                         │     VALUATION ENGINE     │                                        │
│                         │                          │                                        │
│                         │ Comparable-based value   │                                        │
│                         │ Price/sqft analysis      │                                        │
│                         │ Estimated value           │                                        │
│                         │ Fair value range          │                                        │
│                         │ Upside / downside         │                                        │
│                         │ Valuation Score           │                                        │
│                         └────────────┬─────────────┘                                        │
│                                      │                                                      │
│                                      ▼                                                      │
│                         ┌──────────────────────────┐                                        │
│                         │     RISK ENGINE          │                                        │
│                         │                          │                                        │
│                         │ Data quality risk        │                                        │
│                         │ Valuation uncertainty    │                                        │
│                         │ Market risk              │                                        │
│                         │ Infrastructure risk      │                                        │
│                         │ Comparable confidence    │                                        │
│                         │ Overall Risk             │                                        │
│                         └────────────┬─────────────┘                                        │
└──────────────────────────────────────┼───────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                           HYPER-PERSONALIZATION LAYER                                        │
│                                                                                              │
│  ┌──────────────────────────────┐      ┌────────────────────────────────┐                   │
│  │ Investment Profile           │      │ Personalization Engine         │                   │
│  │                              │      │                                │                   │
│  │ Budget                       │─────►│ Dynamic scoring weights        │                   │
│  │ Preferred locations          │      │ Personalized ranking           │                   │
│  │ Property type                │      │ Risk adjustment                │                   │
│  │ Risk tolerance               │      │ Investment objective           │                   │
│  │ Investment horizon           │      │ Query context                  │                   │
│  │ Capital appreciation         │      │ User preferences               │                   │
│  │ Rental income                │      │ Personalized explanations      │                   │
│  │ Growth preference            │      │                                │                   │
│  └──────────────────────────────┘      └────────────────┬───────────────┘                   │
│                                                         │                                   │
└─────────────────────────────────────────────────────────┼───────────────────────────────────┘
                                                          │
                                                          ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DEAL INTELLIGENCE ENGINE                                     │
│                                                                                              │
│                         ┌─────────────────────────────┐                                      │
│                         │        DEAL ENGINE          │                                      │
│                         │                             │                                      │
│                         │ Location Score              │                                      │
│                         │ Infrastructure Score        │                                      │
│                         │ Growth Score                │                                      │
│                         │ Comparable Score            │                                      │
│                         │ Valuation Score             │                                      │
│                         │ Risk Score                  │                                      │
│                         │ User Preference Weight      │                                      │
│                         └──────────────┬──────────────┘                                      │
│                                        │                                                     │
│                                        ▼                                                     │
│                              ┌─────────────────────┐                                         │
│                              │  PERSONALIZED DEAL  │                                         │
│                              │       SCORE         │                                         │
│                              │                     │                                         │
│                              │      0 ─── 100      │                                         │
│                              └──────────┬──────────┘                                         │
│                                         │                                                    │
│                         ┌───────────────┼────────────────┐                                   │
│                         ▼               ▼                ▼                                   │
│                      Evidence          Risks          Confidence                            │
│                                                                                              │
└─────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AI ORCHESTRATION LAYER                                     │
│                                                                                              │
│  Query Understanding                                                                         │
│       │                                                                                      │
│       ├── Intent Detection                                                                   │
│       ├── Property / Project Entity Extraction                                               │
│       ├── Location Extraction                                                                │
│       ├── Investment Criteria Extraction                                                     │
│       └── Query Decomposition                                                                │
│                                                                                              │
│  Context Manager                                                                             │
│       │                                                                                      │
│       ├── User Investment Profile                                                            │
│       ├── Conversation History                                                               │
│       ├── Current Property                                                                    │
│       └── Previous Analysis                                                                  │
│                                                                                              │
│  Tool / Engine Router                                                                        │
│       │                                                                                      │
│       ├── Location Engine                                                                    │
│       ├── Infrastructure Engine                                                              │
│       ├── Comparable Engine                                                                   │
│       ├── Valuation Engine                                                                    │
│       ├── Growth Engine                                                                       │
│       ├── Risk Engine                                                                         │
│       └── Deal Engine                                                                         │
│                                                                                              │
│  Hybrid Retrieval                                                                            │
│       │                                                                                      │
│       ├── SQLite structured filtering                                                         │
│       └── Chroma semantic retrieval                                                          │
│                                                                                              │
│  Evidence Context Builder                                                                     │
│       │                                                                                      │
│       └── Source + Metric + Score + Evidence + Confidence                                    │
│                                                                                              │
└─────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  PRE-LLM GUARDRAILS                                          │
│                                                                                              │
│  Input Validation       Prompt Injection Detection       PII Protection                     │
│  Query Safety           Scope Validation                Source Validation                   │
│  Context Validation     Data Freshness Check             Evidence Requirement                │
│                                                                                              │
│                          ONLY TRUSTED CONTEXT                                                │
│                                  │                                                           │
└──────────────────────────────────┼───────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  LOCAL AI / LLM LAYER                                       │
│                                                                                              │
│                                  ┌───────────────────┐                                       │
│                                  │      OLLAMA       │                                       │
│                                  │                   │                                       │
│                                  │ Qwen3:4b          │                                       │
│                                  │ Qwen3:8b          │                                       │
│                                  │                   │                                       │
│                                  │ Reasoning         │                                       │
│                                  │ Explanation       │                                       │
│                                  │ Ranking rationale │                                       │
│                                  │ Conversation      │                                       │
│                                  └─────────┬─────────┘                                       │
│                                            │                                                 │
└────────────────────────────────────────────┼─────────────────────────────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 POST-LLM GUARDRAILS                                           │
│                                                                                              │
│  ┌──────────────────────┐   ┌──────────────────────┐   ┌────────────────────────────────┐  │
│  │ Schema Validation    │   │ Numeric Validation   │   │ Evidence Validation            │  │
│  │                      │   │                      │   │                                │  │
│  │ Valid JSON           │   │ Price consistency    │   │ Every claim supported          │  │
│  │ Required fields      │   │ Score consistency   │   │ Source verification            │  │
│  │ Response structure   │   │ Valuation check     │   │ No unsupported claims          │  │
│  └──────────────────────┘   └──────────────────────┘   └────────────────────────────────┘  │
│                                                                                              │
│  ┌──────────────────────┐   ┌──────────────────────┐   ┌────────────────────────────────┐  │
│  │ Hallucination Check  │   │ Risk Disclosure      │   │ Financial Boundary             │  │
│  │                      │   │                      │   │                                │  │
│  │ Unsupported claims   │   │ Risk explanation     │   │ No guaranteed returns          │  │
│  │ Evidence mismatch    │   │ Confidence level     │   │ No direct buy/sell advice      │  │
│  │ Regeneration         │   │ Data limitations     │   │ Indicative analysis only       │  │
│  └──────────────────────┘   └──────────────────────┘   └────────────────────────────────┘  │
│                                                                                              │
└─────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      FASTAPI BFF                                             │
│                                                                                              │
│  /api/chat                 /api/properties              /api/search                          │
│  /api/opportunities        /api/valuation               /api/comparables                      │
│  /api/location             /api/infrastructure          /api/growth                          │
│  /api/intelligence         /api/profile                 /api/deal                            │
│  /api/health                                                                                 │
│                                                                                              │
└─────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                          │
                                          │ REST / JSON
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       REACT UI                                               │
│                                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌───────────────────────────┐  │
│  │ AI CHAT        │  │ PROPERTY       │  │ OPPORTUNITY    │  │ INVESTMENT PROFILE       │  │
│  │                │  │ SEARCH         │  │ DASHBOARD      │  │                           │  │
│  │ Ask anything   │  │ Search/filter  │  │ Top 10 Deals   │  │ Budget                    │  │
│  │ Follow-ups     │  │ Properties     │  │ Deal Score     │  │ Risk                      │  │
│  │ Why?           │  │ Projects       │  │ Ranking        │  │ Horizon                   │  │
│  └────────────────┘  └────────────────┘  └────────────────┘  │ Objective                 │  │
│                                                               │ Preferences               │  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  └───────────────────────────┘  │
│  │ LOCATION       │  │ INFRASTRUCTURE │  │ VALUATION      │                                 │
│  │ INTELLIGENCE   │  │ INTELLIGENCE   │  │ ANALYSIS       │                                 │
│  │                │  │                │  │                │                                 │
│  │ Location Score │  │ Infra Score    │  │ Fair Value     │                                 │
│  │ POIs           │  │ Transport      │  │ Asking Price   │                                 │
│  │ Accessibility  │  │ Roads          │  │ Upside         │                                 │
│  └────────────────┘  └────────────────┘  └────────────────┘                                 │
│                                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                         PROPERTY INTELLIGENCE                                           │  │
│  │                                                                                         │  │
│  │ Deal Score │ Growth │ Location │ Infrastructure │ Valuation │ Risk │ Confidence        │  │
│  │                                                                                         │  │
│  │ WHY IS THIS A GOOD DEAL?                                                                │  │
│  │                                                                                         │  │
│  │ Evidence → Explanation → Risks → Confidence → Sources                                  │  │
│  └────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  SELF-CONTAINED DOCKER                                       │
│                                                                                              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌──────────────┐                   │
│  │   React    │    │  FastAPI   │    │  SQLite    │    │   ChromaDB   │                   │
│  │ Container  │    │ Container  │    │   Volume   │    │    Volume    │                   │
│  └────────────┘    └─────┬──────┘    └────────────┘    └──────────────┘                   │
│                           │                                                                  │
│                           ▼                                                                  │
│                    ┌────────────┐                                                            │
│                    │   Ollama   │                                                            │
│                    │ Container  │                                                            │
│                    │            │                                                            │
│                    │ Qwen3      │                                                            │
│                    │ Embeddings │                                                            │
│                    └────────────┘                                                            │
│                                                                                              │
│                    docker compose up --build                                                 │
└──────────────────────────────────────────────────────────────────────────────────────────────┘


# 5. Intelligence Layer

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

# 6. AI Orchestration

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

# 7. Example AI Response

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

# 8. Self-Contained Docker Architecture

The application is packaged as a Docker-based runtime. In local development, the FastAPI backend can use a local Ollama container for LLM inference. In production on Render, the backend uses OpenRouter over HTTPS, while application data is stored on a persistent Render disk.

                              PUBLIC INTERNET
                                     |
                                     v
                         +------------------------+
                         | Render HTTPS / Proxy   |
                         | TLS / Public URL       |
                         +-----------+------------+
                                     |
                                     v
                         +------------------------+
                         | Real Estate AI         |
                         | Docker Web Service     |
                         |                        |
                         | React Frontend         |
                         |        |               |
                         |        v               |
                         | FastAPI Backend        |
                         +-----------+------------+
                                     |
                   +-----------------+------------------+
                   |                 |                  |
                   v                 v                  v
            +-------------+   +-------------+   +----------------+
            | SQLite      |   | ChromaDB    |   | OpenRouter     |
            | Database    |   | Vector Store|   | HTTPS API      |
            |             |   |             |   |                |
            | /app/data/  |   | /app/data/  |   | External LLM   |
            +------+------+   +------+------+   +-------+--------+
                   |                 |                  |
                   +--------+--------+                  |
                            |                           |
                            v                           v
                    +---------------+          +----------------+
                    | Render        |          | Selected       |
                    | Persistent    |          | LLM Model      |
                    | Disk          |          | via OpenRouter |
                    | /app/data     |          +----------------+
                    +---------------+


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

Local Development Architecture

For local development and testing, the same Docker application can connect to Ollama running locally.

                         LOCAL MACHINE
                              |
                              v
                    +-------------------+
                    | Docker Container   |
                    |                    |
                    | React + FastAPI    |
                    +---------+---------+
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          +-------------+          +---------------+
          | /app/data   |          | Ollama        |
          |             |          |               |
          | SQLite      |          | Qwen3         |
          | ChromaDB    |          | Embeddings    |
          +-------------+          +---------------+


The local LLM configuration uses:

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=qwen3:4b


Production Architecture

In production, Ollama is not required inside the Render container. The FastAPI backend communicates with OpenRouter using HTTPS

Browser
   |
   | HTTPS
   v
Render
   |
   v
Docker Web Service
   |
   +---- React Frontend
   |
   +---- FastAPI Backend
           |
           +---- SQLite
           |
           +---- ChromaDB
           |
           +---- HTTPS
                  |
                  v
             OpenRouter
                  |
                  v
              LLM Model

The production LLM configuration uses:

LLM_PROVIDER=openrouter
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=<secret>
OPENROUTER_MODEL=<model>

The API key is stored as a Render environment variable and is not included in the Docker image or source code.

Persistent Application Data

The application stores its database and vector store under /app/data:

/app/data/
├── realestate.db
└── chroma/


On Render, /app/data is mounted to a persistent disk so that SQLite and ChromaDB data survive application restarts and redeployments.

Render Web Service
        |
        +---- Docker Container
        |          |
        |          +---- /app/data
        |
        +---- Persistent Disk
                   |
                   +---- realestate.db
                   +---- chroma/



LLM Provider Strategy

The application supports separate LLM providers for local development and production:

Environment	Provider	LLM Runtime
Local Docker	Ollama	Local Qwen3
Render Production	OpenRouter	Remote LLM via HTTPS

This allows the application to be developed and tested locally without depending on an external LLM service, while production can use OpenRouter without requiring GPU infrastructure on Render.

Production Request Flow

A typical AI request follows this path:

User
 |
 | HTTPS
 v
Render
 |
 v
React Frontend
 |
 | POST /api/properties/{id}/ai
 v
FastAPI
 |
 +---- Search / Retrieval
 |       |
 |       +---- SQLite
 |       |
 |       +---- ChromaDB
 |
 +---- LLM Request
          |
          | HTTPS
          v
      OpenRouter
          |
          v
       LLM Model
          |
          v
      FastAPI
          |
          v
      React UI
          |
          v
         User

Key Deployment Principle

The Docker container contains the complete application runtime:

    React frontend
    FastAPI backend
    Python dependencies
    Application code
    Database and vector-store configuration

However, LLM inference is externalized in production to OpenRouter. This keeps the Render deployment lightweight and avoids requiring Ollama, GPU resources, or locally hosted LLM models in the production environment.

The architecture therefore provides:

Local:
Docker + Ollama + SQLite + ChromaDB

Production:
Docker + OpenRouter + Persistent SQLite + Persistent ChromaDB


# 9. Environment Variables

Create:

```text
.env
```

Example:

```env
APP_ENV=development

LLM_PROVIDER=ollama

OLLAMA_BASE_URL=http://localhost:11434

OPENROUTER_API_KEY = <ap_key>
OPENROUTER_MODEL=openrouter/free

SQLITE_PATH=
CHROMA_PATH= /app/data/chroma

CORS_ORIGINS=*

FRONTEND_URL=http://localhost:5173

DATABASE_URL=sqlite:////app/data/realestate.db

OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

```

Use the exact model names already configured in the project if they differ.

Do not commit secrets or production credentials to Git.

---

# 10. Local Docker Run

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

# 11. Ollama Model Initialization

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

12. FREE PUBLIC DEPLOYMENT — RENDER + OPENROUTER

For the public 3-day POC, the recommended deployment is:

Render Free + OpenRouter Free Models

This provides a public HTTPS URL without requiring:

    VPS
    Purchased domain
    Firebase
    Heroku
    Caddy
    Nginx
    Separate frontend hosting
    Ollama on the public server

Render provides the application with its own public onrender.com URL.

    Important: Render Free is suitable for this short POC/demo deployment. It is not intended to be the final production infrastructure for a persistent real-estate intelligence platform.

12.1 Deployment Architecture

The project uses two runtime profiles.
Local / Handover

The local environment remains fully self-contained:

LOCAL DEVELOPMENT / HANDOVER

                    Docker Compose
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
      +-------+       +--------+      +---------+
      | React |       |FastAPI |      | Ollama  |
      +-------+       +---+----+      |  Qwen3  |
                          |            +---------+
                    +-----+-----+
                    |           |
                    v           v
                 SQLite      ChromaDB

Local LLM:

Ollama
 ├── qwen3:4b
 └── nomic-embed-text

Public POC

The public deployment does not run Ollama.

                         PUBLIC INTERNET
                                |
                                v
                +-------------------------------+
                | Render HTTPS / Public URL     |
                |                               |
                | https://real-estate-ai-jnxg.onrender.com/   |
                +---------------+---------------+
                                |
                                v
                +-------------------------------+
                | Render Web Service            |
                | Docker                        |
                |                               |
                | React + FastAPI               |
                +---------------+---------------+
                                |
              +-----------------+-----------------+
              |                 |                 |
              v                 v                 v
          +---------+       +---------+      +------------+
          | SQLite  |       | ChromaDB |      | OpenRouter |
          | POC Data|       | POC Data |      | HTTPS API  |
          +---------+       +---------+      +------+-----+
                                                    |
                                                    v
                                             +-------------+
                                             | Free LLM    |
                                             | Model       |
                                             +-------------+

The key difference is:

LOCAL:
FastAPI -> Ollama -> Qwen3

PUBLIC:
FastAPI -> OpenRouter -> Free LLM

12.2 Why Ollama Is Not Deployed to Render Free

The local application uses Ollama because it provides a self-contained LLM runtime.

That is appropriate for:

    local development
    offline testing
    handover
    controlled demonstrations

It is not appropriate for the Render Free public POC because the available compute and memory are too limited for running an Ollama-based LLM runtime reliably.

Therefore:

                         LOCAL                  PUBLIC
                         -----                  ------

LLM Runtime              Ollama                 OpenRouter
Model                    Qwen3                  Free routed model
GPU                      Local hardware         Not required
LLM hosting              Self-hosted            External API

This keeps the Render service lightweight.
12.3 OpenRouter Configuration

The public POC uses OpenRouter as the LLM provider.

Configure:

LLM_PROVIDER=openrouter

OPENROUTER_API_KEY=YOUR_SECRET_KEY

OPENROUTER_MODEL=openrouter/free

OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

The openrouter/free router selects an available free model.

Free-model availability and rate limits can change, so the public POC should not depend on a specific free model remaining available indefinitely.

For a production deployment, use a deliberately selected model and appropriate paid API limits instead of relying on the free router.
12.4 Local Ollama Configuration

The local profile continues to use Ollama.

Example:

LLM_PROVIDER=ollama

OLLAMA_BASE_URL=http://ollama:11434

OLLAMA_MODEL=qwen3:4b

If the existing local Docker configuration uses:

host.docker.internal

that is also acceptable for the current local Docker test.

The important rule is:

Render:
DO NOT use host.docker.internal for Ollama.

Render cannot access an Ollama instance running on the developer's laptop.
12.5 Running the Cloud Docker Image Locally

Before deploying to Render, the cloud Docker image can be tested locally.

Build:

docker build -f Dockerfile.cloud -t real-estate-ai-cloud .

Local Ollama test

The current working test is:

docker run --rm \
  -p 10000:10000 \
  -e APP_ENV=production \
  -e LLM_PROVIDER=ollama \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e OLLAMA_MODEL=qwen3:4b \
  -e CORS_ORIGINS=http://localhost:10000 \
  -e DATABASE_URL=sqlite:////app/data/realestate.db \
  -e CHROMA_PATH=/app/data/chroma \
  --add-host=host.docker.internal:host-gateway \
  real-estate-ai-cloud

Expected startup:

Uvicorn running on http://0.0.0.0:10000

The successful API tests should include:

GET  /api/search
POST /api/properties/{id}/ai

OpenRouter test

The same image should also be tested with the OpenRouter configuration before deploying:

docker run --rm \
  -p 10000:10000 \
  -e APP_ENV=production \
  -e LLM_PROVIDER=openrouter \
  -e OPENROUTER_BASE_URL=https://openrouter.ai/api/v1 \
  -e OPENROUTER_API_KEY=YOUR_SECRET_KEY \
  -e OPENROUTER_MODEL=openrouter/free \
  -e CORS_ORIGINS=http://localhost:10000 \
  -e DATABASE_URL=sqlite:////app/data/realestate.db \
  -e CHROMA_PATH=/app/data/chroma \
  real-estate-ai-cloud

Do not commit the API key to GitHub or place it inside the Dockerfile.
12.6 GitHub Repository

Create a GitHub repository and push the complete project.

Example:

git init
git add .
git commit -m "Real Estate AI POC"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main

Before pushing, ensure secrets and generated runtime files are ignored:

.env
.env.*
!.env.example

__pycache__/
*.pyc
.venv/
node_modules/

data/runtime/
*.db

chroma/

Never commit:

OPENROUTER_API_KEY

12.7 Cloud Dockerfile

The repository should contain:

Dockerfile.cloud

The cloud image should:

    Build the React frontend.
    Install the FastAPI/Python dependencies.
    Package the application.
    Serve the React application through FastAPI.
    Expose the API endpoints.
    Listen on 0.0.0.0.
    Use the Render PORT environment variable.

Target architecture:

Browser
   |
   v
Render
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

There is only one public Render Web Service.

Do not expose a separate FastAPI service and React service for this POC.
12.8 React API Configuration

The React application must not hard-code:

http://localhost:8000

for the public build.

Prefer same-origin API requests:

/api/properties
/api/search
/api/chat
/api/properties/{id}/ai

For example:

const API_URL = import.meta.env.VITE_API_URL || "";

fetch(`${API_URL}/api/properties`);

For Render:

VITE_API_URL=

This produces:

https://YOUR-SERVICE.onrender.com
        |
        +-- /
        +-- /api/properties
        +-- /api/search
        +-- /api/chat
        +-- /api/properties/{id}/ai

No separate frontend domain is required.
12.9 Create the Render Web Service

Open the Render Dashboard.

Select:

New
  -> Web Service

Connect GitHub and select the project repository.

Use:

Name:
real-estate-ai-poc

Branch:
main

Runtime:
Docker

Dockerfile:
./Dockerfile.cloud

Plan:
Free

Render will build the Docker image from the repository and start the resulting web service.
12.10 Render Environment Variables

In:

Render
  -> Service
  -> Environment
  -> Environment Variables

configure:

APP_ENV=production

LLM_PROVIDER=openrouter

OPENROUTER_API_KEY=YOUR_SECRET_KEY
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free

DATABASE_URL=sqlite:////app/data/realestate.db
CHROMA_PATH=/app/data/chroma

CORS_ORIGINS=*

Use the exact variable names expected by the application.

If the application has a different SQLite variable, preserve the existing application configuration rather than introducing duplicate variables.
12.11 Render Port

FastAPI must listen on:

0.0.0.0

and should use the Render PORT variable.

Recommended:

uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}

Replace:

app.main:app

with the actual FastAPI application entry point used by the project.

Do not bind the production application to:

127.0.0.1
localhost

It must be reachable from Render's network.
12.12 Deploy

Click:

Create Web Service

Render will perform:

GitHub
   |
   v
Docker Build
   |
   v
Docker Image
   |
   v
Render Web Service
   |
   +--> React
   +--> FastAPI
   +--> SQLite
   +--> ChromaDB
   +--> Intelligence Engines
   +--> OpenRouter

Once the service becomes live, Render will provide a public HTTPS URL.
12.13 Public URL

The public POC will receive a URL similar to:

https://real-estate-ai-jnxg.onrender.com/

The exact hostname is generated by Render.

No purchased domain is required.

No DNS configuration is required.

No Caddy or Nginx configuration is required.

The evaluator can simply open the Render URL.
12.14 Render Free Storage Limitation

This is an important limitation of the free POC.

Render Free does not provide a persistent disk for the service.

Therefore files written to the container filesystem should be treated as ephemeral.

That includes:

SQLite
ChromaDB
uploaded/generated runtime files

Do not design the 3-day POC around the assumption that:

/app/data/realestate.db

will survive every restart/redeploy.
12.15 POC Data Strategy

For the short public demonstration, use a rebuildable/seeded dataset.

Recommended:

Repository
    |
    +--> POC property data
    |
    +--> SQLite seed
    |
    +--> Chroma seed/index
    |
    v
Docker image / startup
    |
    v
/app/data
    |
    +--> realestate.db
    +--> chroma/

If the application needs to recreate these files, make the startup process idempotent:

Container starts
      |
      v
Does database exist?
      |
   +--+--+
   |     |
  YES    NO
   |     |
   |     v
   |   Seed DB
   |     |
   +-----+
      |
      v
Does Chroma index exist?
      |
   +--+--+
   |     |
  YES    NO
   |     |
   |     v
   |   Build/restore index
   |     |
   +-----+
      |
      v
FastAPI starts

This makes the POC recoverable after a restart.
12.16 ChromaDB and Embeddings

The local architecture can use:

Ollama
  |
  +-- nomic-embed-text

For the public free POC, do not assume that an Ollama embedding model is available on Render.

The preferred approach for the short POC is to ship/rebuild the prepared Chroma index rather than dynamically embedding the entire dataset on every startup.

If runtime embeddings are required, implement a separate cloud embedding provider.

Do not assume that an OpenRouter chat model being free means that embedding requests are also free.
12.17 Public AI Request Flow

A typical request will follow:

User
 |
 | HTTPS
 v
Render
 |
 v
React
 |
 | POST /api/properties/10/ai
 v
FastAPI
 |
 +---- Retrieval
 |       |
 |       +---- SQLite
 |       |
 |       +---- ChromaDB
 |
 +---- Intelligence Engines
 |       |
 |       +---- Valuation
 |       +---- Growth
 |       +---- Risk
 |       +---- Deal Score
 |
 +---- Guardrails
 |
 +---- OpenRouter
          |
          v
       Free LLM
          |
          v
       FastAPI
          |
          v
        React
          |
          v
         User

The LLM should explain and summarize the deterministic intelligence produced by the application rather than independently inventing valuation or investment scores.
12.18 Local vs Public Configuration
Component	Local / Handover	Public POC
Frontend	React	React
Backend	FastAPI	FastAPI
Packaging	Docker	Docker
Database	SQLite	SQLite / seeded
Vector DB	ChromaDB	ChromaDB / seeded
LLM	Ollama	OpenRouter
Chat Model	Qwen3	openrouter/free
Embeddings	Ollama	Prepared/seeded index
HTTPS	Local HTTP / optional	Render HTTPS
Reverse Proxy	Not required	Render
Caddy	No	No
Nginx	No	No
VPS	No	No
Persistent Disk	Docker volume	Not available on Free
Public URL	No	*.onrender.com
12.19 Render Free Limitations

The free service is suitable for this 3-day POC but has important limitations.
Service spin-down

The free web service can spin down after a period of inactivity.

The first request after inactivity may therefore be slower while the service starts.

Tell the evaluator:

    If the demo has been idle, the first request may take some time while the Render service wakes up.

Ephemeral filesystem

Runtime-written files are not guaranteed to persist.

Therefore:

SQLite
ChromaDB
runtime-generated files

must be treated as rebuildable for this POC.
Limited compute

Do not run:

Ollama
Qwen3
large local models

inside the Render Free web service.
OpenRouter free-model limits

openrouter/free is appropriate for a small evaluator/demo workload, but free model availability and rate limits can change.

For production, use a deliberately selected model with an appropriate API budget and limits.
12.20 Deployment Verification

After the Render deployment reports Live, test the application in this order.
1. Homepage

https://YOUR-SERVICE.onrender.com/

Expected:

Real Estate AI

2. Property search

Test:

Please share me the property in Oman

Expected:

GET /api/search

3. Property AI

Select a property and ask:

Is this property a good investment?

Expected:

POST /api/properties/{id}/ai

4. Follow-up

Ask:

Why?

5. Risk

Ask:

What are the main concerns?

6. Valuation

Ask:

How does the valuation compare with the asking price?

7. Comparables

Ask:

How does this property compare with similar properties?

8. Infrastructure

Ask:

What infrastructure supports this location?

9. Opportunity ranking

Ask:

Give me the top opportunities I should investigate.

12.21 Troubleshooting
Render container does not start

Check the Render logs.

Verify:

0.0.0.0
$PORT

The application must not listen only on localhost.
OpenRouter authentication error

Verify:

LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free

Never expose the API key in React.

The key must only be used by FastAPI/server-side code.
React cannot reach the API

Check that production requests use:

/api/...

rather than:

http://localhost:8000/api/...

Ollama connection error on Render

If you see an error involving:

localhost:11434
host.docker.internal:11434

the Render configuration is incorrectly using the local Ollama provider.

Render must use:

LLM_PROVIDER=openrouter

SQLite/Chroma data disappears

This is expected if the service restarts and the data was written only to the ephemeral filesystem.

Use the seeded/rebuildable POC data strategy.

For a real production deployment, move persistent data to appropriate managed storage/database/vector infrastructure.
12.22 Final Deployment Architecture
Local

                    LOCAL MACHINE

                 Docker Compose
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
    React           FastAPI          Ollama
                       |               |
              +--------+--------+      +-- Qwen3
              |                 |      +-- Embeddings
              v                 v
           SQLite           ChromaDB

Public POC

                    PUBLIC INTERNET
                           |
                           v
                Render HTTPS Endpoint
                           |
                           v
                +---------------------+
                | Render Web Service  |
                |                     |
                | Docker              |
                |                     |
                | React + FastAPI     |
                +----------+----------+
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
       SQLite          ChromaDB        OpenRouter
       POC Data        POC Index           |
                                            v
                                       Free LLM

Final public URL

https://real-estate-ai-jnxg.onrender.com/

No VPS.

No purchased domain.

No DNS.

No Caddy.

No Nginx.

No Firebase.

No separate frontend hosting.

No Ollama on Render.

The only external AI dependency for the public POC is:

Fast
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




✅ DarGlobal ingestion
✅ Normalization
✅ SQLite
✅ ChromaDB
✅ Query understanding
✅ Structured search
✅ Hybrid search
✅ Chat API
        │
        ▼
👉 NEXT: Advanced Search
        │
        ▼
   Location Data
        │
        ▼
   Location Engine
        │
        ▼
   Infrastructure
        │
        ▼
   Comparable Engine
        │
        ▼
   Valuation Engine
        │
        ▼
   Growth Engine
        │
        ▼
   Risk Engine
        │
        ▼
   Investment Profile
        │
        ▼
   Personalization
        │
        ▼
   Deal Engine
        │
        ▼
   AI Orchestration
        │
        ▼
   Guardrails
        │
        ▼
   React UI
        │
        ▼
   Docker

# AstroForge
AstroForge is a backend-focused system designed to ingest real NASA data, process it through a high-performance Rust computation engine, and expose the results through a clean Python API and a minimal Textual dashboard.

This project follows a backend-first philosophy and aims to build a complete Level 1 foundation before expanding to more advanced features.

## Overview
AstroForge consists of three main services:

1. **Python API (Flask)**  
   Handles NASA data ingestion, orchestration, communication with Rust, and exposes endpoints consumed by the dashboard.

2. **Rust Engine**  
   A dedicated microservice for scientific calculations such as simplified orbital metrics, velocity estimation, impact energy, and heuristic risk scoring.

3. **Dashboard (Textual)**  
   A minimal UI for viewing NASA data, analysis results, and system logs.

An infrastructure layer using Docker Compose ties everything together.

## Project Goals (Level 1 Scope)
- Fetch and normalize NASA NEOWS and APOD data.
- Send normalized data to the Rust computation engine.
- Return computed metrics to the Python API.
- Display data, analysis, and logs via the Textual dashboard.
- Keep the structure minimal until real code justifies expansion.
- Produce a complete, finished, and maintainable baseline system.

## Architecture
### Python API (Flask)
Orchestrates data ingestion, MongoDB persistence, and Rust engine integration.

**Responsibilities:**
- NASA NEO data retrieval and normalization
- MongoDB operations (raw asteroids, analysis results)
- Rust engine communication
- RESTful API endpoints
- Structured logging

**Key modules:**
- `core/` — NASA client, Rust client, MongoDB, configuration, pipeline orchestration
- `routes/` — NASA endpoints, analysis orchestration
- `models/` — Domain models (Asteroid, Orbit, AnalysisResult)
- `utils/` — Logging, validation

---

### Rust Engine
High-performance computation service for asteroid risk analysis.

**Responsibilities:**
- Impact energy calculations
- Risk scoring algorithms
- Domain validation
- HTTP API (Axum)

**Key modules:**
- `domain/` — Asteroid, RiskResult, error types
- `logic/` — Impact physics, orbital calculations
- `dto/` — Data transfer objects with validation
- `api/` — HTTP endpoints

### Dashboard (Textual)
Minimal UI for data visualization and system monitoring.

**Status:** Planned (not yet implemented)

## Project Structure
services/
├── python-api/
│   ├── app/
│   │   ├── core/          # Pipeline, clients, configuration
│   │   ├── routes/        # API endpoints
│   │   ├── models/        # Domain models
│   │   └── utils/         # Logger, validators
│   ├── requirements.txt
│   └── Dockerfile
│
├── rust-engine/
│   ├── src/
│   │   ├── domain/        # Core business logic
│   │   ├── logic/         # Physics calculations
│   │   ├── dto/           # API contracts
│   │   └── api/           # HTTP handlers
│   ├── Cargo.toml
│   └── Dockerfile
│
└── dashboard/
    ├── Textual/
    └── requirements.txt

infra/
├── docker-compose.yml
├── scripts/
└── env/

docs/
├── architecture.md
├── roadmap-levels.md
├── api-spec-python.md
└── api-spec-rust.md
```

---

## Data Flow

```
NASA API → Python API → MongoDB (asteroids_raw)
                ↓
        Pipeline Orchestrator
                ↓
          Rust Engine (risk analysis)
                ↓
        MongoDB (asteroid_analyses)
```

---

## API Endpoints

### Python API (Port 5001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/nasa/neo/feed` | GET | Fetch NASA NEO data |
| `/nasa/neo/save` | POST | Persist NASA data to MongoDB |
| `/pipeline/neo/analyze` | POST | Analyze unprocessed asteroids |
| `/pipeline/neo/analyze/<id>` | POST | Analyze single asteroid |
| `/pipeline/status` | GET | System health check |

### Rust Engine (Port 8080)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/process/asteroid` | POST | Process asteroid risk analysis |

---

## Technology Stack

- **Python 3.x** — Flask, PyMongo, Requests
- **Rust** — Axum, Tokio, Serde
- **MongoDB** — Document storage
- **Docker** — Containerization
- **Textual** — Dashboard (planned)

---

## Development Philosophy

- Backend-first development
- Minimal structure, grow organically
- Clear service boundaries
- Maintainability over premature optimization
- Environment-based configuration (12-factor)

---

## Current Status

See `PROJECT_STATUS.md` for detailed implementation status and next steps.

**Operational:**
- Python API with NASA integration
- Rust computation engine
- MongoDB persistence
- End-to-end analysis pipeline

**Pending:**
- Textual dashboard
- Docker Compose deployment
- Production configuration

---
## License
This project currently has no license.
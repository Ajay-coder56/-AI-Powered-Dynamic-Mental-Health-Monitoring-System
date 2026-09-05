# MindSafe — AI-Powered Dynamic Mental Health Monitoring System

> **Smart India Hackathon 2026 · Problem Statement ID: 26094**
> Ministry of Women and Child Development · Govt. of India

---

## Overview

MindSafe is an AI Mental Health Monitoring System designed to track, assess, and support victims. It currently features a completed Phase-1 UI prototype (Victim App & Counsellor Dashboard) and the foundational Phase-2 backend infrastructure (Gateway, FastAPI, PostgreSQL).

**Current Status:** Phase-2 architecture scaffolding is complete. The UI has been preserved and placed inside `apps/web`. Backend and Gateway logic are ready for the initial integration of Authentication and Case Management endpoints.

## Architecture

```
┌─────────────────────┐
│   React Frontend    │  (Vite · Port 8443)
│   apps/web/         │
└─────────┬───────────┘
          │ HTTP
┌─────────▼───────────┐
│  Node.js Gateway    │  (Express · Port 3001)
│  services/api-gateway
└─────────┬───────────┘
          │ HTTP Proxy
┌─────────▼───────────┐
│  Python FastAPI     │  (Uvicorn · Port 8000)
│  services/backend/  │  REST API · SQLAlchemy
└─────────┬───────────┘
          │ asyncpg
┌─────────▼───────────┐
│  PostgreSQL 16      │  (Docker · Port 5432)
│  database/          │
└─────────────────────┘
```

## Repository Structure

A monorepo structure designed for scalability and clear separation of concerns:

```
SIH 2026/
├── apps/
│   └── web/                   ← React 19 Frontend (Phase 1 prototype)
├── services/
│   ├── api-gateway/           ← Node.js Express Gateway
│   └── backend/               ← Python FastAPI Backend
├── database/                  ← PostgreSQL migrations & seeds
├── ai/                        ← [Placeholder] Future AI modules (nlp, speech, distress, explainability)
├── design/                    ← [Placeholder] Design assets & system documentation
├── docs/                      ← [Placeholder] Technical documentation
├── scripts/                   ← [Placeholder] Utility scripts
├── tests/                     ← [Placeholder] Integration/E2E tests
├── docker-compose.yml         ← PostgreSQL + pgAdmin infrastructure
├── .env.example               ← Environment configuration template
└── README.md                  ← Project documentation
```

## Prerequisites

| Tool | Version |
|------|---------|
| Node.js | 20+ |
| Python | 3.11+ |
| Docker & Docker Compose | Latest |

## Setup Instructions & Development Commands

### 1. Environment Setup
```bash
copy .env.example .env
```
Update configuration parameters within `.env` as needed.

### 2. Start the Database
```bash
docker compose up -d
# Schema & seed data load automatically on first run
# pgAdmin available at http://localhost:5050 (admin@mindsafe.dev / admin)
```

### 3. Start FastAPI Backend
```bash
cd services/backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API Documentation (Swagger): http://localhost:8000/docs

### 4. Start API Gateway
```bash
cd services/api-gateway
npm install
npm run dev
```

### 5. Start Frontend
```bash
cd apps/web
npm install
npm run dev
```

## Future Components

The `ai/` folder contains structural placeholders for future intelligence modules:
- `nlp/`: For analyzing text inputs and notes.
- `speech/`: For processing voice-based check-ins.
- `distress/`: Predictive modeling for alerting.
- `explainability/`: XAI logic for transparent AI decision-making.

*(Note: Advanced AI, Kafka, Redis, and external notification hooks like WhatsApp/IVRS are deferred to later phases).*

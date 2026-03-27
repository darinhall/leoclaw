# LeoClaw

A distributed browser-automation agent system built on the **infrastructure-first** principle.

```
Oracle VM (always-on)          Lume VM (macOS GUI)
┌──────────────────────┐       ┌──────────────────────┐
│   orchestrator       │◄─────►│   lume-client        │
│   ├── planner        │  HTTP │   ├── actions/        │
│   ├── executor       │       │   ├── capture/        │
│   └── agents/        │       │   └── transport/      │
└──────────────────────┘       └──────────────────────┘
```

The orchestrator is the **brain**. The lume-client is the **hands + eyes**.

---

## Quick Start (local, no Docker)

```bash
# 1. Copy env
make env

# 2. Terminal A — start orchestrator
make orchestrator

# 3. Terminal B — start lume-client (mock mode)
make client

# 4. Terminal C — send your first task
make smoke-test
```

## Quick Start (Docker)

```bash
make env
make up
make smoke-test
make logs
```

---

## Repo Structure

```
leoclaw/
├── services/
│   ├── orchestrator/      # FastAPI control plane
│   ├── lume-client/       # runs inside Lume VM
│   └── worker/            # async background tasks
├── shared/
│   ├── schemas/           # Pydantic models (Task, Action, Observation)
│   ├── utils/             # logging
│   └── constants/
├── infra/
│   ├── docker/            # docker-compose
│   ├── oracle/            # Oracle VM setup script
│   └── lume/              # Lume VM setup guide
├── memory/
│   └── logs/
├── scripts/
├── Makefile
└── .env.example
```

---

## Build Order (do NOT skip)

| Step | What | Status |
|------|------|--------|
| 1 | Orchestrator skeleton (local) | Done |
| 2 | Define schemas | Done |
| 3 | Lume client (mock) | Done |
| 4 | Connect real Lume VM | Next |
| 5 | Real browser actions | |
| 6 | Screenshot loop | |
| 7 | Basic planner | Done (rule-based) |
| 8 | Add Ollama | |
| 9 | Deploy to Oracle Cloud | |
| 10 | Logging to Postgres | |

---

## Minimal Working Loop

You are done with Step 3 when this works end-to-end:

1. `POST /task {"goal": "Open Google and search cats"}`
2. Orchestrator plans steps
3. Lume-client polls, executes, captures screenshots
4. Observations flow back to orchestrator
5. `GET /task/{id}` shows observations

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ORCHESTRATOR_URL` | `http://localhost:8000` | Where lume-client connects |
| `MOCK_ACTIONS` | `true` | Set `false` inside real Lume VM |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama endpoint (Step 8) |
| `DATABASE_URL` | — | Postgres DSN (Step 10) |

---

## API

### `POST /task`
Submit a goal.
```json
{"goal": "Open Google and search cats"}
```
Response:
```json
{"status": "received", "task_id": "...", "steps": ["navigate:...", "..."]}
```

### `GET /task/{id}`
Retrieve observations for a task.

### `GET /client/poll`
Used by lume-client to fetch the next pending task.

### `POST /client/observe`
Used by lume-client to return a screenshot + metadata.

### `GET /health`
Orchestrator liveness check.

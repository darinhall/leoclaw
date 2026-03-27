.PHONY: up down restart logs orchestrator client test lint

COMPOSE = docker compose -f infra/docker/docker-compose.yml

# ── Docker ─────────────────────────────────────────────────────────────────

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

# ── Local dev (no Docker) ──────────────────────────────────────────────────

orchestrator:
	bash scripts/start_orchestrator.sh

client:
	bash scripts/start_lume_client.sh

# ── Test the minimal working loop ──────────────────────────────────────────
# Prerequisites: orchestrator must be running on localhost:8000

smoke-test:
	@echo "Sending smoke-test task..."
	curl -s -X POST http://localhost:8000/task \
	  -H "Content-Type: application/json" \
	  -d '{"goal": "Open Google and search cats"}' | python3 -m json.tool

# ── Lint / format ──────────────────────────────────────────────────────────

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .

# ── Misc ───────────────────────────────────────────────────────────────────

reset:
	bash scripts/reset_vm.sh

env:
	cp -n .env.example .env && echo ".env created — fill in your values"

venv:
	python3 -m venv .venv
	.venv/bin/pip install -q -r services/orchestrator/requirements.txt
	.venv/bin/pip install -q -r services/lume-client/requirements.txt
	@echo "==> .venv ready"

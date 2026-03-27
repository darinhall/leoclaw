#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Create venv if it doesn't exist
if [ ! -f ".venv/bin/python" ]; then
  echo "==> Creating .venv..."
  python3 -m venv .venv
fi

echo "==> Installing orchestrator dependencies..."
.venv/bin/pip install -q -r services/orchestrator/requirements.txt

export PYTHONPATH="$REPO_ROOT"

.venv/bin/uvicorn app.main:app \
  --app-dir services/orchestrator \
  --host 0.0.0.0 \
  --port 8000 \
  --reload

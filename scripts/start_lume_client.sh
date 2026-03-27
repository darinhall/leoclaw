#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -f ".venv/bin/python" ]; then
  echo "==> Creating .venv..."
  python3 -m venv .venv
fi

echo "==> Installing lume-client dependencies..."
.venv/bin/pip install -q -r services/lume-client/requirements.txt

export PYTHONPATH="$REPO_ROOT"
export MOCK_ACTIONS="${MOCK_ACTIONS:-true}"
export ORCHESTRATOR_URL="${ORCHESTRATOR_URL:-http://localhost:8000}"

.venv/bin/python services/lume-client/client.py

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Stopping containers..."
docker compose -f "$REPO_ROOT/infra/docker/docker-compose.yml" down -v 2>/dev/null || true

echo "==> Clearing logs and screenshots..."
rm -rf "$REPO_ROOT/memory/logs"/*
rm -rf /tmp/leoclaw

echo "==> Done."

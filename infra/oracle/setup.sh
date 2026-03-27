#!/usr/bin/env bash
# Oracle VM setup — run once after provisioning
set -euo pipefail

echo "==> Installing Docker"
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"

echo "==> Installing Docker Compose plugin"
sudo apt-get install -y docker-compose-plugin

echo "==> Opening firewall port 8000 (orchestrator)"
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT

echo "==> Installing Ollama (Step 8)"
curl -fsSL https://ollama.com/install.sh | sh

echo "==> Done. Re-login for docker group to take effect."
echo "    Then: cd /opt/leoclaw && make up"

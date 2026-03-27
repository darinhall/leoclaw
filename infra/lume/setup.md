# Lume VM Setup

## What goes here

The `lume-client` service runs **inside** a [Lume](https://github.com/lume-dev/lume) macOS VM so it has access to a real GUI (browser, screen, etc.).

## Steps

1. **Create a Lume VM** — use the Lume CLI or app to spin up a macOS guest.

2. **Install Python 3.11** inside the VM:
   ```bash
   brew install python@3.11
   ```

3. **Clone the repo** (or just copy `services/lume-client/` + `shared/`) into the VM:
   ```bash
   git clone https://github.com/YOUR_ORG/leoclaw /opt/leoclaw
   ```

4. **Install dependencies**:
   ```bash
   cd /opt/leoclaw/services/lume-client
   pip3.11 install -r requirements.txt
   ```

5. **Set the orchestrator URL**:
   ```bash
   export ORCHESTRATOR_URL=http://<oracle-vm-ip>:8000
   export MOCK_ACTIONS=false   # flip when you're ready for real actions
   ```

6. **Run the client**:
   ```bash
   python3.11 client.py
   ```

## Real Actions (Step 5+)

Uncomment in `requirements.txt`:
```
pyautogui>=0.9.54
playwright>=1.44.0
```

Then install playwright browsers:
```bash
playwright install chromium
```

Update `actions/browser.py` to use playwright instead of raising `NotImplementedError`.

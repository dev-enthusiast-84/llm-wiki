---
name: stop-wiki-ui
description: 'Stop the running LLM Wiki Query UI (Streamlit). Checks if the process is running, kills it, and confirms it is stopped.'
argument-hint: 'No argument needed'
---

# Stop Wiki UI

Stop the Streamlit wiki query UI that was started by `/launch-wiki-ui`.

## Procedure

### 1. Check if the UI is running

```bash
pgrep -fl "streamlit run wiki_query.py"
```

- **If no output**: the UI is not running — report "Wiki UI is not running." and stop.
- **If output**: proceed to stop it.

### 2. Stop the process

```bash
pkill -f "streamlit run wiki_query.py"
```

### 3. Confirm it is stopped

```bash
pgrep -fl "streamlit run wiki_query.py"
```

- **If no output**: stopped successfully.
- **If still running**: report the PID and ask the user to run `kill -9 <PID>` manually.

## Output

Emit one of these result lines:

```
✅ Wiki UI stopped — 2026-04-25
```

```
ℹ️  Wiki UI was not running — nothing to stop.
```

```
❌ Wiki UI still running (PID <n>) — run `kill -9 <n>` to force-stop.
```

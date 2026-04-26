---
mode: agent
description: Stop the running LLM Wiki Query UI (Streamlit process). Checks if it is running, kills it, and confirms it is stopped.
---

## Step 1: Check if the UI is running

Run:
```bash
pgrep -fl "streamlit run wiki_query.py"
```

- If no output: the UI is not running — report "Wiki UI is not running." and stop.
- If output: proceed to stop it.

## Step 2: Stop the process

Run:
```bash
pkill -f "streamlit run wiki_query.py"
```

## Step 3: Confirm it is stopped

Run:
```bash
pgrep -fl "streamlit run wiki_query.py"
```

- No output → stopped successfully.
- Still running → report the PID and instruct the user to run `kill -9 <PID>`.

## Output

Emit exactly one of these result lines:

```
✅ Wiki UI stopped — YYYY-MM-DD
```

```
ℹ️  Wiki UI was not running — nothing to stop.
```

```
❌ Wiki UI still running (PID <n>) — run `kill -9 <n>` to force-stop.
```

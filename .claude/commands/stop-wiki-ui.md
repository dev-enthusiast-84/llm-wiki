---
description: Stop the running LLM Wiki Query UI (Streamlit process).
---

## Step 1: Check if the UI is running

```bash
pgrep -fl "streamlit run wiki_query.py"
```

- If no output: report "Wiki UI is not running." and stop.
- If output: proceed.

## Step 2: Stop the process

```bash
pkill -f "streamlit run wiki_query.py"
```

## Step 3: Confirm it is stopped

```bash
pgrep -fl "streamlit run wiki_query.py"
```

- No output → stopped successfully.
- Still running → report the PID and ask the user to run `kill -9 <PID>`.

## Output

Emit exactly one of:

```
✅ Wiki UI stopped — YYYY-MM-DD
```

```
ℹ️  Wiki UI was not running — nothing to stop.
```

```
❌ Wiki UI still running (PID <n>) — run `kill -9 <n>` to force-stop.
```

$ARGUMENTS

---
description: Launch the LLM Wiki Query UI. Checks dependencies, reports wiki data availability, then starts the Streamlit app and guides the user to configure model and API key.
---

## Usage

**Invoke:** type `/launch-wiki-ui` in the Claude Code CLI  
**When to run:** any time you want to query the wiki through a browser interface  
**Prerequisites:**
- Python 3 available (`python3 --version`)
- `wiki_query.py` present in the project root
- An API key from any major LLM provider (Anthropic, OpenAI, Google, Mistral, Cohere, etc.)

**Arguments:** none required  
**Note:** you will be asked to enter your model ID and API key inside the browser UI — they are never stored to disk or git.

---

## Step 1: Check dependencies

Run:
```bash
python3 -c "import streamlit, litellm" 2>&1
```

- If the import fails, install: `pip3 install streamlit litellm` and confirm success before continuing.
- If it succeeds, proceed.

## Step 2: Report wiki data availability

List all `.md` files in `wiki/` excluding `index.md` and `log.md`.

- **If entity pages exist**: report them — e.g. "Wiki contains 12 pages: transformer.md, attention.md, …"
- **If wiki is empty**: warn the user:
  > The wiki has no entity pages yet. The UI will launch but all queries will return "No information found."
  > To populate the wiki: add source files (PDF, PPTX, DOCX, TXT, HTML) to `raw/` then run `/compile-papers`.

## Step 3: Launch the UI

Run:
```bash
streamlit run wiki_query.py
```

The app will open at **http://localhost:8501**.

---

## Verification Steps

After the UI launches, confirm it is working correctly by:

1. **Browser opens**: navigate to http://localhost:8501 — the Settings screen should appear with two text fields (Model ID and API Key)
2. **Security notice visible**: confirm the `🔒 Security notice` banner is shown before any input field
3. **Model field validated**: type `INVALID MODEL` and click "Validate & continue" — an error should appear rejecting non-lowercase/special characters
4. **API key field masked**: confirm the API Key field shows `•••` when typing (password masking active)
5. **Wiki confirmation screen**: after entering valid credentials, the next screen should list the entity pages found (or show an empty-state warning if wiki is empty)
6. **Chat disabled when empty**: if wiki has no pages, the chat input should be disabled with a message explaining why

---

## Results Summary

Once the UI is running, output this exact block:

```
✅ Wiki UI launched — http://localhost:8501  YYYY-MM-DD

📋 Wiki status:
   Entity pages available: N  (list filenames, or "none — queries will return no results")

🔒 Security controls active:
   • Model ID validated against allowlist regex (OWASP A03)
   • API key format validated before network call (OWASP A07)
   • Key stored in browser session memory only — never written to disk or git

🖥️  Settings screen requires before first query:
   1. Model ID  — enter the model ID for your chosen provider, e.g.:
      • Anthropic: claude-opus-4-7 / claude-sonnet-4-6 / claude-haiku-4-5
      • OpenAI:    gpt-4o / gpt-4o-mini / o3
      • Google:    gemini/gemini-2.0-flash / gemini/gemini-1.5-pro
      • Mistral:   mistral/mistral-large-latest
      • Cohere:    cohere/command-r-plus
   2. API key   — obtain from your provider's developer console
   → Click "Validate & continue", then review the Wiki Data Availability screen

🔍 Verification: open http://localhost:8501 and confirm the Settings screen appears.
➡️  Next step: enter model ID and API key; if wiki is empty, run /compile-papers first.
```

$ARGUMENTS

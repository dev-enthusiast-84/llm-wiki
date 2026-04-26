---
mode: agent
description: Launch the LLM Wiki Query UI. Checks dependencies, reports wiki data availability, then starts the Streamlit app and guides the user to configure model and API key.
---

## Step 1: Check dependencies

Run:
```bash
python3 -c "import streamlit, litellm" 2>&1
```

- If the import fails, run `pip3 install streamlit litellm` and confirm success before continuing.
- If it succeeds, proceed.

## Step 2: Report wiki data availability

List all `.md` files in `wiki/` excluding `index.md` and `log.md`.

- **If entity pages exist**: Report them — e.g. "Wiki contains 12 pages: transformer.md, attention.md, …"
- **If wiki is empty**: Warn the user:
  > The wiki has no entity pages yet. The UI will launch but queries will return no results.
  > To populate the wiki: add source files (PDF, PPTX, DOCX, TXT, HTML) to `raw/` then run `Compile Papers to Wiki`.

## Step 3: Launch the UI

Run:
```bash
streamlit run wiki_query.py
```

The app will open at **http://localhost:8501**.

Inform the user:
> The wiki query UI is running at http://localhost:8501
>
> **Before querying — Settings screen:**
> 1. **Model ID** — enter the model ID for your chosen provider:
>    - Anthropic: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`
>    - OpenAI: `gpt-4o`, `gpt-4o-mini`, `o3`
>    - Google: `gemini/gemini-2.0-flash`, `gemini/gemini-1.5-pro`
>    - Mistral: `mistral/mistral-large-latest`
>    - Cohere: `cohere/command-r-plus`
>    Input is validated against an allowlist pattern; special characters are rejected (OWASP A03).
> 2. **API key** — obtain from your provider's developer console.
>    The key is held in browser session memory only — never written to disk or git (OWASP A02 / A04).
> 3. Click **Validate & continue** — the key is verified with your provider before you proceed.
> 4. **Wiki confirmation screen** — review which topics are available before the chat opens.
>
> Queries run **strictly against the wiki**. If the wiki does not contain an answer the UI returns
> an explicit "No information found" message with instructions on which files to add to `raw/`
> and which command (`Sync Wiki from Raw`) to run.

## Output

After the UI launches, emit this results block:

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

➡️  Next step: enter model ID and API key; if wiki is empty, run Compile Papers to Wiki first.
```

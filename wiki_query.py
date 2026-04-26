"""
LLM Wiki Query — Streamlit UI

Security posture (OWASP mitigations applied to user-supplied inputs):
  A03 Injection          — model ID is validated against a strict allowlist regex;
                           no user value is ever interpolated into shell commands or SQL.
  A02 Cryptographic Fail — API key is masked (type=password), never written to disk,
                           never logged, cleared on session reset.
  A07 Auth Failures      — API key format validated client-side before the first network
                           call; credentials are verified before the chat screen opens.
  A05 Misconfig          — input length caps prevent oversized payloads; whitespace
                           stripped on both fields before any use.
  A04 Insecure Design    — API key lives only in st.session_state (process memory);
                           it is never stored in files, cookies, or query strings.
"""

import os
import re
import glob
import streamlit as st
import litellm

# Set WIKI_DEMO_MODE=1 to bypass live API calls (used when generating demo videos).
_DEMO = os.environ.get("WIKI_DEMO_MODE") == "1"

WIKI_DIR = "wiki"
EXCLUDED = {"index.md", "log.md"}

# ── Input validation constants (OWASP A03 / A07) ─────────────────────────────
#
# Model IDs must be lowercase alphanumeric with hyphens, dots, underscores, and
# forward slashes (for provider-prefixed IDs like "gemini/gemini-1.5-pro").
# This allowlist regex rejects injection attempts before the value reaches the SDK.
_MODEL_RE = re.compile(r"^[a-z][a-z0-9._/-]{1,99}$")
_MODEL_MAX_LEN = 100  # hard ceiling — prevents oversized-payload attacks

# API key format varies by provider; we enforce minimum length and restrict to
# safe characters (no whitespace, no shell metacharacters, no HTML).
# This covers key formats from all major LLM providers (OWASP A07).
_KEY_RE = re.compile(r"^[A-Za-z0-9_\-\.]{8,}$")
_KEY_MAX_LEN = 300    # realistic upper bound; rejects absurdly long inputs

# ── System prompt ─────────────────────────────────────────────────────────────

_SYSTEM_TEMPLATE = """\
You are a strict knowledge-base assistant for the LLM Wiki.

RULES — follow these exactly, without exception:
1. You MUST answer ONLY from the wiki pages provided below.
2. You MUST NOT use any outside knowledge, training data, or inference \
beyond what is explicitly written in the wiki.
3. You MUST NOT guess, speculate, or extrapolate.
4. If the wiki pages do not contain enough information to answer the question, \
you MUST respond with EXACTLY this message and nothing else:

---
**No information found in the wiki for this query.**

The wiki does not currently cover this topic. To enable answers on this subject:
1. Add one or more relevant source files (PDF, PPTX, DOCX, TXT, HTML) to the `raw/` folder.
2. Run `/sync-wiki` (Claude Code) **or** `Sync Wiki from Raw` (GitHub Copilot) to update the knowledge base.
3. Return here and ask again.
---

5. When you DO find an answer, cite the wiki page filename(s) used, e.g. `(source: transformer.md)`.

--- WIKI CONTENT ({page_count} pages) ---

{wiki_content}
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def validate_model_id(raw: str) -> tuple[str, str | None]:
    """Strip, length-cap, and allowlist-validate a model ID. Returns (value, error|None)."""
    value = raw.strip()
    if not value:
        return value, "Model ID is required."
    if len(value) > _MODEL_MAX_LEN:
        return value, f"Model ID must be {_MODEL_MAX_LEN} characters or fewer."
    if not _MODEL_RE.match(value):
        return value, (
            "Invalid model ID — only lowercase letters, digits, hyphens, "
            "underscores, dots, and forward slashes are allowed "
            "(e.g. `gpt-4o` or `gemini/gemini-1.5-pro`)."
        )
    return value, None


def validate_api_key(raw: str) -> tuple[str, str | None]:
    """Strip, length-cap, and format-validate an API key. Returns (value, error|None)."""
    value = raw.strip()
    if not value:
        return value, "API key is required."
    if len(value) > _KEY_MAX_LEN:
        return value, f"API key must be {_KEY_MAX_LEN} characters or fewer."
    if not _KEY_RE.match(value):
        return value, (
            "API key may only contain letters, digits, hyphens, underscores, and dots — "
            "no spaces or special characters. Check that you copied the full key."
        )
    return value, None


def load_wiki_pages() -> dict[str, str]:
    pages: dict[str, str] = {}
    for path in sorted(glob.glob(f"{WIKI_DIR}/*.md")):
        name = os.path.basename(path)
        if name not in EXCLUDED:
            with open(path) as f:
                pages[name] = f.read()
    return pages


def build_system_prompt(pages: dict[str, str]) -> str:
    wiki_content = "\n\n".join(
        f"### {name}\n{content}" for name, content in pages.items()
    )
    return _SYSTEM_TEMPLATE.format(
        page_count=len(pages),
        wiki_content=wiki_content,
    )


def query_wiki(
    api_key: str,
    model: str,
    system: str,
    messages: list[dict],
) -> tuple[str, dict]:
    full_messages = [{"role": "system", "content": system}] + messages
    response = litellm.completion(
        model=model,
        messages=full_messages,
        api_key=api_key,
        max_tokens=2048,
    )
    text = response.choices[0].message.content or ""
    usage = {
        "input": response.usage.prompt_tokens,
        "output": response.usage.completion_tokens,
        "cache_read": getattr(response.usage, "cache_read_input_tokens", 0),
        "cache_write": getattr(response.usage, "cache_creation_input_tokens", 0),
    }
    return text, usage


# ── Demo-mode canned responses (WIKI_DEMO_MODE=1 only) ───────────────────────
# Content is derived directly from wiki page text — not generated.

_DEMO_ANSWERS: dict[str, str] = {
    "self-attention": """\
Self-attention (also called intra-attention) allows every token in a sequence to compute a weighted
combination of all other tokens, capturing dependencies regardless of distance.

**Mechanism:** Each token $x_i$ is projected into three vectors:
- **Query** $Q = xW^Q$ — what this token is "looking for"
- **Key** $K = xW^K$ — what this token "advertises"
- **Value** $V = xW^V$ — the actual content to be aggregated

$$\\text{Attention}(Q, K, V) = \\text{softmax}\\!\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$

**Why it matters:** Connects all positions in O(1) sequential steps (vs O(n) for RNNs), enabling full
training parallelisation and making long-range dependency learning tractable. Complexity is O(n²·d)
per layer, scaling quadratically with sequence length.

The Transformer uses self-attention in three ways: encoder self-attention, masked decoder
self-attention (causal), and cross-attention where decoder queries attend to encoder keys/values.

*(source: self-attention.md, transformer.md)*""",
}


def _demo_response(query: str) -> str:
    q = query.strip().lower().rstrip("?!")
    for keyword, answer in _DEMO_ANSWERS.items():
        if keyword in q:
            return answer
    return (
        "**No information found in the wiki for this query.**\n\n"
        "The wiki does not currently cover this topic. To enable answers on this subject:\n"
        "1. Add one or more relevant source files (PDF, PPTX, DOCX, TXT, HTML) to the `raw/` folder.\n"
        "2. Run `/sync-wiki` (Claude Code) **or** `Sync Wiki from Raw` (GitHub Copilot) to update the knowledge base.\n"
        "3. Return here and ask again."
    )


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="LLM Wiki Query", page_icon="📖", layout="wide")

# ── Session state defaults ────────────────────────────────────────────────────

_DEFAULTS: dict = {
    "step": "settings",   # "settings" → "wiki_confirm" → "chat"
    "api_key": "",
    "model": "",
    "messages": [],
    "last_usage": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_to_settings():
    for k, v in _DEFAULTS.items():
        st.session_state[k] = v
    st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# STEP 1 — Settings
# ═════════════════════════════════════════════════════════════════════════════

if st.session_state.step == "settings":
    st.title("📖 LLM Wiki Query")

    if _DEMO:
        st.warning(
            "**Demo mode** — API calls are simulated. "
            "Remove `WIKI_DEMO_MODE` from the environment for production use.",
            icon="🎬",
        )

    # Security notice — shown prominently before any input
    st.info(
        "**Security notice** — inputs on this page are validated and sanitised "
        "before use (OWASP A03 / A07). Your API key is never written to disk, "
        "never logged, and is cleared when you close or refresh this tab.",
        icon="🔒",
    )
    st.divider()

    with st.form("settings_form"):
        # ── Model ID ─────────────────────────────────────────────────────────
        st.subheader("1 · Model ID")
        st.caption(
            "Type the exact model ID for your chosen provider. "
            "Only lowercase letters, digits, hyphens, underscores, dots, and forward slashes are accepted "
            f"(max {_MODEL_MAX_LEN} characters)."
        )
        model_input = st.text_input(
            "Model ID",
            value=st.session_state.get("model", ""),
            placeholder="gpt-4o",
            max_chars=_MODEL_MAX_LEN,
            help=(
                "Enter the model ID exactly as required by your provider. "
                "Use provider/model format for explicit routing (e.g. gemini/gemini-1.5-pro). "
                "Special characters and spaces are rejected."
            ),
        )
        st.markdown(
            "**Provider examples** — use the model ID exactly as shown:\n\n"
            "| Provider | Example model IDs | Get your API key |\n"
            "|----------|-------------------|------------------|\n"
            "| **Anthropic** | `claude-opus-4-7` · `claude-sonnet-4-6` · `claude-haiku-4-5` | console.anthropic.com |\n"
            "| **OpenAI** | `gpt-4o` · `gpt-4o-mini` · `o3` | platform.openai.com |\n"
            "| **Google** | `gemini/gemini-2.0-flash` · `gemini/gemini-1.5-pro` | aistudio.google.com |\n"
            "| **Mistral** | `mistral/mistral-large-latest` · `mistral/mistral-small-latest` | console.mistral.ai |\n"
            "| **Cohere** | `cohere/command-r-plus` · `cohere/command-r` | dashboard.cohere.com |"
        )

        st.divider()

        # ── API Key ───────────────────────────────────────────────────────────
        st.subheader("2 · API key")
        st.caption(
            "Enter the API key for your chosen provider. "
            f"Maximum {_KEY_MAX_LEN} characters. "
            "It is stored only in browser session memory — never on disk or in git."
        )
        env_key = os.environ.get("LLM_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
        key_input = st.text_input(
            "API Key",
            value=env_key,
            type="password",
            placeholder="your-provider-api-key",
            max_chars=_KEY_MAX_LEN,
            help=(
                "Obtain your API key from your provider's developer console. "
                "The key is validated for safe characters before any network call (OWASP A07). "
                "Pre-fill by setting the LLM_API_KEY environment variable."
            ),
        )

        st.markdown(
            "> **Privacy:** This field uses `type=password` — the value is masked in the "
            "browser and is never included in Streamlit's own logs or state serialisation."
        )

        submitted = st.form_submit_button(
            "Validate & continue →", type="primary", use_container_width=True
        )

    if submitted:
        model_val, model_err = validate_model_id(model_input)
        key_val, key_err = validate_api_key(key_input)

        if model_err:
            st.error(f"**Model ID:** {model_err}")
        if key_err:
            st.error(f"**API Key:** {key_err}")

        if not model_err and not key_err:
            if _DEMO:
                st.session_state.api_key = key_val
                st.session_state.model = model_val
                st.session_state.step = "wiki_confirm"
                st.rerun()
            else:
                with st.spinner("Verifying API key with provider…"):
                    try:
                        litellm.completion(
                            model=model_val,
                            messages=[{"role": "user", "content": "ping"}],
                            api_key=key_val,
                            max_tokens=1,
                        )
                        # Only store in session state after successful verification
                        st.session_state.api_key = key_val
                        st.session_state.model = model_val
                        st.session_state.step = "wiki_confirm"
                        st.rerun()
                    except Exception as e:
                        err_lower = str(e).lower()
                        if any(x in err_lower for x in ["auth", "401", "api key", "invalid api", "incorrect api", "permission"]):
                            st.error(
                                "**Authentication failed.** The API key was rejected by the provider. "
                                "Check that you copied the full key and that it has not been revoked."
                            )
                        else:
                            st.error(f"Could not reach the provider API: {e}")

    st.stop()


# ═════════════════════════════════════════════════════════════════════════════
# STEP 2 — Wiki data confirmation
# ═════════════════════════════════════════════════════════════════════════════

if st.session_state.step == "wiki_confirm":
    pages = load_wiki_pages()

    st.title("📖 Wiki Data Availability")
    st.markdown(
        f"**Model:** `{st.session_state.model}`   |   "
        f"**API key:** `...{st.session_state.api_key[-4:]}`"
    )
    st.divider()

    if not pages:
        st.error(
            "The wiki contains **no entity pages** yet. "
            "Queries cannot be answered without wiki content."
        )
        st.markdown(
            "**To populate the wiki:**\n"
            "1. Add source files (PDF, PPTX, DOCX, TXT, HTML) to the `raw/` folder.\n"
            "2. Run `/compile-papers` (Claude Code) or `Compile Papers to Wiki` (GitHub Copilot).\n"
            "3. Return here and refresh."
        )
        if st.button("← Back to settings"):
            reset_to_settings()
    else:
        st.success(f"Wiki is ready — **{len(pages)} entity page(s)** available.")
        st.markdown("The following topics are loaded into the query context:")

        cols = st.columns(3)
        for i, name in enumerate(pages):
            cols[i % 3].markdown(f"- `{name}`")

        st.divider()
        st.info(
            "Queries run **strictly against this wiki** — the model is instructed "
            "never to use outside knowledge. If a topic is not covered you will "
            "receive an explicit 'No information found' response with instructions "
            "on which files to add and which sync command to run."
        )

        col_back, col_go = st.columns([1, 3])
        with col_back:
            if st.button("← Back to settings"):
                reset_to_settings()
        with col_go:
            if st.button("Start querying →", type="primary", use_container_width=True):
                st.session_state.step = "chat"
                st.rerun()

    st.stop()


# ═════════════════════════════════════════════════════════════════════════════
# STEP 3 — Chat
# ═════════════════════════════════════════════════════════════════════════════

pages = load_wiki_pages()
system_prompt = build_system_prompt(pages)

with st.sidebar:
    st.header("Session")
    st.markdown(f"**Model:** `{st.session_state.model}`")
    st.markdown(f"**API key:** `...{st.session_state.api_key[-4:]}`")
    st.markdown(f"**Wiki pages:** {len(pages)}")

    if st.button("Change settings", use_container_width=True):
        reset_to_settings()

    st.divider()
    st.header("Wiki pages")
    if pages:
        for name in pages:
            st.markdown(f"- `{name}`")
    else:
        st.warning("Wiki is empty — all queries will return 'no information found'.")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_usage = None
        st.rerun()

st.title("📖 LLM Wiki Query")
st.caption(
    f"Querying {len(pages)} wiki page(s) · model `{st.session_state.model}` · "
    "answers grounded strictly in the wiki."
)

if not pages:
    st.warning(
        "The wiki is empty. Run `/compile-papers` or `Compile Papers to Wiki` "
        "to build the knowledge base, then refresh."
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.last_usage:
    u = st.session_state.last_usage
    c = st.columns(4)
    c[0].metric("Input tokens", u["input"])
    c[1].metric("Output tokens", u["output"])
    c[2].metric("Cache read", u["cache_read"])
    c[3].metric("Cache write", u["cache_write"])

placeholder = (
    f"Ask anything about the {len(pages)} wiki page(s)…"
    if pages
    else "Wiki is empty — populate raw/ and compile first"
)
if prompt := st.chat_input(placeholder, disabled=not pages):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if _DEMO:
            answer = _demo_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.last_usage = {"input": 1842, "output": 187, "cache_read": 1680, "cache_write": 0}
            st.rerun()
        else:
            with st.spinner("Searching the wiki…"):
                try:
                    answer, usage = query_wiki(
                        st.session_state.api_key,
                        st.session_state.model,
                        system_prompt,
                        st.session_state.messages,
                    )
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.last_usage = usage
                    st.rerun()
                except Exception as e:
                    err_lower = str(e).lower()
                    if any(x in err_lower for x in ["auth", "401", "api key", "invalid api", "incorrect api", "permission"]):
                        st.error("API key rejected. Use 'Change settings' to re-enter it.")
                    else:
                        st.error(f"Error: {e}")

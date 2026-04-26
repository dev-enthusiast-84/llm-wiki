"""
Tests for wiki_query.py

Covers:
  - validate_model_id  : allowlist regex, length cap, whitespace stripping (OWASP A03)
  - validate_api_key   : format validation, length cap, whitespace stripping (OWASP A07)
  - load_wiki_pages    : file discovery, exclusions, non-md filtering
  - build_system_prompt: page count injection, content inclusion, anti-hallucination rules
  - query_wiki         : response parsing, usage mapping, model forwarding

The streamlit mock is installed by conftest.py before this module is imported.
"""

from unittest.mock import MagicMock, patch

import wiki_query


# ── validate_model_id ──────────────────────────────────────────────────────────

class TestValidateModelId:

    # --- happy paths ---

    def test_standard_model_ids_accepted(self):
        models = [
            "gpt-4o",
            "gpt-4o-mini",
            "claude-opus-4-7",
            "claude-sonnet-4-6",
            "claude-haiku-4-5",
            "gemini/gemini-1.5-pro",
            "mistral/mistral-large-latest",
            "cohere/command-r-plus",
        ]
        for model in models:
            val, err = wiki_query.validate_model_id(model)
            assert err is None, f"Unexpected error for {model!r}: {err}"
            assert val == model

    def test_custom_model_with_dot_accepted(self):
        val, err = wiki_query.validate_model_id("my-model.v2")
        assert err is None

    def test_model_with_underscore_accepted(self):
        val, err = wiki_query.validate_model_id("my_model-v2")
        assert err is None

    def test_model_with_provider_prefix_accepted(self):
        val, err = wiki_query.validate_model_id("gemini/gemini-2.0-flash")
        assert err is None
        assert val == "gemini/gemini-2.0-flash"

    def test_strips_leading_trailing_whitespace(self):
        val, err = wiki_query.validate_model_id("  gpt-4o  ")
        assert err is None
        assert val == "gpt-4o"

    def test_exactly_at_max_length_accepted(self):
        # 100 chars: one leading lowercase letter + 99 lowercase letters
        model = "a" + "b" * 99
        val, err = wiki_query.validate_model_id(model)
        assert err is None

    # --- rejection cases ---

    def test_empty_string_rejected(self):
        _, err = wiki_query.validate_model_id("")
        assert err is not None

    def test_whitespace_only_rejected(self):
        _, err = wiki_query.validate_model_id("   ")
        assert err is not None

    def test_exceeds_max_length_rejected(self):
        _, err = wiki_query.validate_model_id("a" * 101)
        assert err is not None
        assert str(wiki_query._MODEL_MAX_LEN) in err

    def test_uppercase_letters_rejected(self):
        _, err = wiki_query.validate_model_id("GPT-4o")
        assert err is not None

    def test_starts_with_digit_rejected(self):
        _, err = wiki_query.validate_model_id("4-model")
        assert err is not None

    def test_internal_space_rejected(self):
        _, err = wiki_query.validate_model_id("gpt 4o")
        assert err is not None

    # --- OWASP A03: injection payloads ---

    def test_shell_semicolon_injection_rejected(self):
        _, err = wiki_query.validate_model_id("gpt4; rm -rf /")
        assert err is not None

    def test_shell_backtick_injection_rejected(self):
        _, err = wiki_query.validate_model_id("gpt4`id`")
        assert err is not None

    def test_shell_subshell_injection_rejected(self):
        _, err = wiki_query.validate_model_id("gpt4$(id)")
        assert err is not None

    def test_pipe_injection_rejected(self):
        _, err = wiki_query.validate_model_id("gpt4|ls")
        assert err is not None

    def test_null_byte_rejected(self):
        _, err = wiki_query.validate_model_id("gpt4\x00opus")
        assert err is not None

    def test_path_traversal_rejected(self):
        _, err = wiki_query.validate_model_id("../../etc/passwd")
        assert err is not None

    def test_html_script_tag_rejected(self):
        _, err = wiki_query.validate_model_id("<script>alert(1)</script>")
        assert err is not None

    def test_sql_injection_rejected(self):
        _, err = wiki_query.validate_model_id("model' OR '1'='1")
        assert err is not None


# ── validate_api_key ───────────────────────────────────────────────────────────

class TestValidateApiKey:

    # --- happy paths ---

    def test_valid_alphanumeric_key_accepted(self):
        key = "mygenericapikey1234567890"
        val, err = wiki_query.validate_api_key(key)
        assert err is None
        assert val == key

    def test_valid_key_with_hyphens_and_underscores(self):
        key = "my-api-key_abc-123-xyz"
        val, err = wiki_query.validate_api_key(key)
        assert err is None

    def test_valid_openai_style_key(self):
        key = "sk-proj-abc123XYZdefghij"
        val, err = wiki_query.validate_api_key(key)
        assert err is None

    def test_valid_anthropic_style_key(self):
        key = "sk-ant-abc123XYZ_-abcdefghij"
        val, err = wiki_query.validate_api_key(key)
        assert err is None

    def test_valid_key_with_dots(self):
        key = "AIzaSy.abc123xyzDEF456"
        val, err = wiki_query.validate_api_key(key)
        assert err is None

    def test_minimum_length_key_accepted(self):
        # exactly 8 chars
        val, err = wiki_query.validate_api_key("abcdefgh")
        assert err is None

    def test_strips_leading_trailing_whitespace(self):
        val, err = wiki_query.validate_api_key("  my-api-key-12345  ")
        assert err is None
        assert val == "my-api-key-12345"

    # --- rejection cases ---

    def test_empty_string_rejected(self):
        _, err = wiki_query.validate_api_key("")
        assert err is not None

    def test_whitespace_only_rejected(self):
        _, err = wiki_query.validate_api_key("   ")
        assert err is not None

    def test_too_short_key_rejected(self):
        # fewer than 8 characters
        _, err = wiki_query.validate_api_key("abcde")
        assert err is not None

    def test_exceeds_max_length_rejected(self):
        _, err = wiki_query.validate_api_key("a" * 301)
        assert err is not None
        assert str(wiki_query._KEY_MAX_LEN) in err

    # --- OWASP A07: injection / special character payloads ---

    def test_sql_injection_in_key_rejected(self):
        _, err = wiki_query.validate_api_key("mykey'; DROP TABLE users--")
        assert err is not None

    def test_html_tag_in_key_rejected(self):
        _, err = wiki_query.validate_api_key("mykey<script>alert(1)</script>")
        assert err is not None

    def test_null_byte_in_key_rejected(self):
        _, err = wiki_query.validate_api_key("myapikey\x00extra")
        assert err is not None

    def test_newline_in_key_rejected(self):
        _, err = wiki_query.validate_api_key("myapikey\nextra12345")
        assert err is not None

    def test_space_in_key_rejected(self):
        _, err = wiki_query.validate_api_key("my api key here")
        assert err is not None


# ── load_wiki_pages ────────────────────────────────────────────────────────────

class TestLoadWikiPages:

    def test_loads_entity_md_files(self, tmp_path, monkeypatch):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        (wiki_dir / "transformer.md").write_text("# Transformer\nContent.")
        (wiki_dir / "attention.md").write_text("# Attention\nMore content.")
        monkeypatch.setattr(wiki_query, "WIKI_DIR", str(wiki_dir))

        pages = wiki_query.load_wiki_pages()

        assert "transformer.md" in pages
        assert "attention.md" in pages

    def test_page_content_is_preserved(self, tmp_path, monkeypatch):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        content = "# Transformer\nUses self-attention."
        (wiki_dir / "transformer.md").write_text(content)
        monkeypatch.setattr(wiki_query, "WIKI_DIR", str(wiki_dir))

        pages = wiki_query.load_wiki_pages()

        assert pages["transformer.md"] == content

    def test_excludes_index_md(self, tmp_path, monkeypatch):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        (wiki_dir / "index.md").write_text("index")
        (wiki_dir / "concept.md").write_text("concept")
        monkeypatch.setattr(wiki_query, "WIKI_DIR", str(wiki_dir))

        pages = wiki_query.load_wiki_pages()

        assert "index.md" not in pages
        assert "concept.md" in pages

    def test_excludes_log_md(self, tmp_path, monkeypatch):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        (wiki_dir / "log.md").write_text("log")
        (wiki_dir / "concept.md").write_text("concept")
        monkeypatch.setattr(wiki_query, "WIKI_DIR", str(wiki_dir))

        pages = wiki_query.load_wiki_pages()

        assert "log.md" not in pages

    def test_empty_wiki_returns_empty_dict(self, tmp_path, monkeypatch):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        monkeypatch.setattr(wiki_query, "WIKI_DIR", str(wiki_dir))

        pages = wiki_query.load_wiki_pages()

        assert pages == {}

    def test_ignores_non_md_files(self, tmp_path, monkeypatch):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        (wiki_dir / "notes.txt").write_text("text file")
        (wiki_dir / "data.json").write_text("{}")
        (wiki_dir / "image.png").write_bytes(b"\x89PNG")
        monkeypatch.setattr(wiki_query, "WIKI_DIR", str(wiki_dir))

        pages = wiki_query.load_wiki_pages()

        assert pages == {}

    def test_returns_sorted_filenames(self, tmp_path, monkeypatch):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir()
        for name in ["zebra.md", "apple.md", "mango.md"]:
            (wiki_dir / name).write_text(name)
        monkeypatch.setattr(wiki_query, "WIKI_DIR", str(wiki_dir))

        pages = wiki_query.load_wiki_pages()

        assert list(pages.keys()) == sorted(pages.keys())


# ── build_system_prompt ────────────────────────────────────────────────────────

class TestBuildSystemPrompt:

    def test_empty_pages_shows_zero_count(self):
        prompt = wiki_query.build_system_prompt({})
        assert "0 pages" in prompt

    def test_page_count_matches_input(self):
        pages = {f"page{i}.md": f"content {i}" for i in range(5)}
        prompt = wiki_query.build_system_prompt(pages)
        assert "5 pages" in prompt

    def test_page_filename_included(self):
        pages = {"transformer.md": "Transformers use attention."}
        prompt = wiki_query.build_system_prompt(pages)
        assert "transformer.md" in prompt

    def test_page_content_included(self):
        pages = {"transformer.md": "Transformers use attention."}
        prompt = wiki_query.build_system_prompt(pages)
        assert "Transformers use attention." in prompt

    def test_all_pages_included(self):
        pages = {"a.md": "alpha", "b.md": "beta", "c.md": "gamma"}
        prompt = wiki_query.build_system_prompt(pages)
        for name, content in pages.items():
            assert name in prompt
            assert content in prompt

    def test_anti_hallucination_must_not_present(self):
        prompt = wiki_query.build_system_prompt({})
        assert "MUST NOT" in prompt

    def test_no_information_found_message_present(self):
        prompt = wiki_query.build_system_prompt({})
        assert "No information found" in prompt

    def test_sync_instructions_present(self):
        prompt = wiki_query.build_system_prompt({})
        # Either the Claude Code or Copilot command should appear
        assert "sync-wiki" in prompt or "Sync Wiki" in prompt

    def test_outside_knowledge_prohibition_present(self):
        prompt = wiki_query.build_system_prompt({})
        assert "outside knowledge" in prompt or "training data" in prompt

    def test_citation_instruction_present(self):
        prompt = wiki_query.build_system_prompt({})
        assert "source:" in prompt or "cite" in prompt.lower()


# ── query_wiki ────────────────────────────────────────────────────────────────

class TestQueryWiki:

    def _mock_response(self, text="Answer.", input_tokens=100, output_tokens=50,
                       cache_read=80, cache_write=20):
        choice = MagicMock()
        choice.message.content = text

        usage = MagicMock()
        usage.prompt_tokens = input_tokens
        usage.completion_tokens = output_tokens
        usage.cache_read_input_tokens = cache_read
        usage.cache_creation_input_tokens = cache_write

        response = MagicMock()
        response.choices = [choice]
        response.usage = usage
        return response

    def _call(self, mock_response, model="gpt-4o", messages=None):
        with patch("wiki_query.litellm.completion") as mock_completion:
            mock_completion.return_value = mock_response
            return wiki_query.query_wiki(
                api_key="generic-testkey-12345",
                model=model,
                system="system prompt",
                messages=messages or [{"role": "user", "content": "question"}],
            ), mock_completion

    def test_returns_text_from_response(self):
        (text, _), _ = self._call(self._mock_response("Wiki says this."))
        assert text == "Wiki says this."

    def test_returns_usage_dict(self):
        (_, usage), _ = self._call(self._mock_response())
        assert isinstance(usage, dict)

    def test_usage_dict_has_required_keys(self):
        (_, usage), _ = self._call(self._mock_response())
        assert set(usage.keys()) == {"input", "output", "cache_read", "cache_write"}

    def test_usage_values_match_response(self):
        resp = self._mock_response(input_tokens=200, output_tokens=75,
                                   cache_read=150, cache_write=50)
        (_, usage), _ = self._call(resp)
        assert usage["input"] == 200
        assert usage["output"] == 75
        assert usage["cache_read"] == 150
        assert usage["cache_write"] == 50

    def test_model_forwarded_to_api(self):
        resp = self._mock_response()
        (_, _), mock_completion = self._call(resp, model="claude-sonnet-4-6")
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["model"] == "claude-sonnet-4-6"

    def test_system_prompt_prepended_to_messages(self):
        resp = self._mock_response()
        (_, _), mock_completion = self._call(resp)
        call_kwargs = mock_completion.call_args[1]
        messages = call_kwargs["messages"]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "system prompt"

    def test_user_messages_appended_after_system(self):
        resp = self._mock_response()
        user_msgs = [{"role": "user", "content": "hello"}]
        (_, _), mock_completion = self._call(resp, messages=user_msgs)
        call_kwargs = mock_completion.call_args[1]
        messages = call_kwargs["messages"]
        assert len(messages) == 2
        assert messages[1]["role"] == "user"

    def test_none_content_returns_empty_string(self):
        choice = MagicMock()
        choice.message.content = None

        usage = MagicMock()
        usage.prompt_tokens = 0
        usage.completion_tokens = 0

        response = MagicMock()
        response.choices = [choice]
        response.usage = usage

        (text, _), _ = self._call(response)
        assert text == ""

    def test_empty_content_returns_empty_string(self):
        choice = MagicMock()
        choice.message.content = ""

        usage = MagicMock()
        usage.prompt_tokens = 0
        usage.completion_tokens = 0

        response = MagicMock()
        response.choices = [choice]
        response.usage = usage

        (text, _), _ = self._call(response)
        assert text == ""

    def test_api_key_passed_to_completion(self):
        resp = self._mock_response()
        with patch("wiki_query.litellm.completion") as mock_completion:
            mock_completion.return_value = resp
            wiki_query.query_wiki(
                api_key="my-specific-key-12345678",
                model="gpt-4o",
                system="sys",
                messages=[{"role": "user", "content": "q"}],
            )
            call_kwargs = mock_completion.call_args[1]
            assert call_kwargs["api_key"] == "my-specific-key-12345678"

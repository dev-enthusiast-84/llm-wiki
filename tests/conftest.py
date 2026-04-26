"""
Pytest configuration.

Sets up a streamlit mock in sys.modules before any test file imports wiki_query.
The mock must be installed at conftest level so it is in place before test
modules (which import wiki_query at the top of the file) are collected.
"""

import sys
from unittest.mock import MagicMock


class _SessionState(dict):
    """
    Dict subclass that also exposes keys as attributes, mimicking
    st.session_state so module-level Streamlit code in wiki_query.py
    can access session state via both st.session_state["key"] and
    st.session_state.key without raising AttributeError.
    """

    def __getattr__(self, key: str):
        return self.get(key)

    def __setattr__(self, key: str, value):
        self[key] = value


def _build_streamlit_mock() -> MagicMock:
    mock = MagicMock(name="streamlit")

    # Seed session state with the same defaults wiki_query._DEFAULTS uses,
    # so the module-level initialisation loop is a no-op (all keys present).
    mock.session_state = _SessionState(
        {
            "step": "settings",
            "api_key": "",
            "model": "",
            "messages": [],
            "last_usage": None,
        }
    )

    # Ensure form widgets return safe, non-triggering values so the module-level
    # conditional blocks (if submitted / if prompt) are never entered during import.
    mock.form_submit_button.return_value = False
    mock.chat_input.return_value = None
    mock.stop = MagicMock()  # no-op so execution continues past st.stop()

    return mock


# Install before test collection begins (wiki_query is imported at test module level)
if "streamlit" not in sys.modules:
    sys.modules["streamlit"] = _build_streamlit_mock()

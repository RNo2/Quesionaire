"""Functional Streamlit checks; API calls are mocked and never incur charges."""

import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from worldview import WORLDVIEW


class AppTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {
            "OPENAI_API_KEY": "",
            "OPENAI_MODEL": "",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.sdk_patch = patch("openai.OpenAI")
        self.sdk = self.sdk_patch.start()
        self.addCleanup(self.sdk_patch.stop)
        self.responses = self.sdk.return_value.__enter__.return_value.responses
        self.responses.create.return_value = SimpleNamespace(
            status="completed", output_text="**Action** still matters."
        )

    def app(self, secrets=None):
        app = AppTest.from_file(str(ROOT / "app.py"))
        if secrets is not None:
            app.secrets.update(secrets)
        app.run()
        self.assertEqual(len(app.exception), 0)
        return app

    def submit(self, app, text):
        app.text_input[0].set_value(text)
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)

    def test_initial_and_blank_submissions_make_no_request(self):
        app = self.app()
        self.assertEqual(app.text_input[0].value, "")
        self.assertEqual(app.session_state.answer, "")
        self.assertIn("what is it you seek", app.markdown[1].value)
        self.assertEqual(len(app.sidebar), 0)
        self.submit(app, "   ")
        self.assertEqual(app.session_state.answer, "")
        self.sdk.assert_not_called()

    def test_full_worldview_markdown_duplicates_and_reruns(self):
        app = self.app({"OPENAI_API_KEY": "test-key", "OPENAI_MODEL": "test-model"})
        self.submit(app, "  Does action matter?  ")
        kwargs = self.responses.create.call_args.kwargs
        self.assertEqual(kwargs["instructions"], WORLDVIEW)
        self.assertEqual(kwargs["input"], "Does action matter?")
        self.assertEqual(kwargs["model"], "test-model")
        self.assertFalse(kwargs["store"])
        self.assertEqual(app.markdown[-1].value, "**Action** still matters.")
        self.assertFalse(app.markdown[-1].proto.allow_html)
        app.run()
        self.submit(app, "Does action matter?")
        self.assertEqual(self.responses.create.call_count, 1)
        self.submit(app, "Why act?")
        self.assertEqual(self.responses.create.call_count, 2)

    def test_environment_model_fallback_with_secrets_key(self):
        os.environ["OPENAI_MODEL"] = "environment-model"
        app = self.app({"OPENAI_API_KEY": "test-key"})
        self.submit(app, "What is freedom?")
        self.assertEqual(self.responses.create.call_args.kwargs["model"], "environment-model")

    def test_environment_key_and_default_model(self):
        os.environ["OPENAI_API_KEY"] = "test-environment-key"
        app = self.app()
        self.submit(app, "What is awareness?")
        self.assertEqual(self.sdk.call_args.kwargs["api_key"], "test-environment-key")
        self.assertEqual(self.responses.create.call_args.kwargs["model"], "gpt-5.5")

    def test_missing_key_has_no_provider_or_technical_message(self):
        app = self.app()
        self.submit(app, "What is truth?")
        self.assertEqual(app.session_state.answer, "The answer could not be reached. Try again shortly.")
        self.sdk.assert_not_called()

    def test_request_error_is_hidden_and_retry_works(self):
        app = self.app({"OPENAI_API_KEY": "test-key"})
        self.responses.create.side_effect = RuntimeError("private technical details")
        self.submit(app, "What is truth?")
        self.assertNotIn("private", app.markdown[-1].value)
        self.assertIsNone(app.session_state.last_question)
        self.responses.create.side_effect = None
        self.submit(app, "What is truth?")
        self.assertEqual(app.session_state.answer, "**Action** still matters.")

    def test_initialization_empty_and_incomplete_fail_quietly(self):
        app = self.app({"OPENAI_API_KEY": "test-key"})
        self.sdk.side_effect = ValueError("private configuration details")
        self.submit(app, "Why?")
        self.assertIsNone(app.session_state.last_question)
        self.sdk.side_effect = None
        for response in [
            SimpleNamespace(status="completed", output_text="   "),
            SimpleNamespace(status="incomplete", output_text="partial"),
        ]:
            with self.subTest(response=response):
                self.responses.create.return_value = response
                self.submit(app, "Why?")
                self.assertIsNone(app.session_state.last_question)
                self.assertEqual(app.session_state.answer, "The answer could not be reached. Try again shortly.")


if __name__ == "__main__":
    unittest.main()

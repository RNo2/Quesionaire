"""Exercise the unchanged interface with real local answers and no services."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from philosophy import answer_question


class AppTests(unittest.TestCase):
    def app(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        self.assertEqual(len(app.exception), 0)
        return app

    def submit(self, app, question):
        app.text_input[0].set_value(question)
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)

    def test_initial_page_and_blank_questions(self):
        app = self.app()
        self.assertEqual(app.text_input[0].value, "")
        self.assertEqual(app.session_state.answer, "")
        self.assertIn("what is it you seek", app.markdown[1].value)
        self.assertEqual(len(app.sidebar), 0)
        for question in ("", "   ", "???"):
            self.submit(app, question)
            self.assertEqual(app.session_state.answer, "")

    def test_real_answer_without_secrets_or_network(self):
        app = self.app()
        with patch("socket.create_connection", side_effect=AssertionError("network forbidden")), \
             patch("socket.socket.connect", side_effect=AssertionError("network forbidden")):
            self.submit(app, "Do I have free will?")
        self.assertEqual(app.session_state.answer, answer_question("Do I have free will?"))
        self.assertIn("caus", app.session_state.answer)
        self.assertFalse(app.markdown[-1].proto.allow_html)

    def test_duplicates_reruns_and_next_question(self):
        with patch("philosophy.answer_question", wraps=answer_question) as engine:
            app = self.app()
            self.submit(app, "Do I have free will?")
            first = app.session_state.answer
            app.run()
            self.submit(app, "  DO I HAVE FREE WILL?  ")
            self.assertEqual(app.session_state.answer, first)
            self.assertEqual(engine.call_count, 1)
            self.submit(app, "What is consciousness?")
            self.assertEqual(engine.call_count, 2)
            self.assertNotEqual(app.session_state.answer, first)
            self.submit(app, "   ")
            self.assertEqual(app.session_state.answer, answer_question("What is consciousness?"))

    def test_markup_is_not_executed_or_reflected(self):
        app = self.app()
        self.submit(app, '<script>alert("bad")</script> what is awareness?')
        self.assertNotIn("<script>", app.markdown[-1].value)
        self.assertFalse(app.markdown[-1].proto.allow_html)


if __name__ == "__main__":
    unittest.main()

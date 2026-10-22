"""Exercise the installed SDK over HTTP without using an external service."""

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch

from openai import OpenAI

from test_app import ROOT, WORLDVIEW
from streamlit.testing.v1 import AppTest


class SDKIntegrationTests(unittest.TestCase):
    def test_responses_http_contract(self):
        captured = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                captured["path"] = self.path
                captured["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                body = json.dumps({
                    "id": "resp_test", "object": "response", "created_at": 1,
                    "status": "completed", "model": "test-model",
                    "output": [{
                        "type": "message", "id": "msg_test", "role": "assistant",
                        "status": "completed", "content": [{
                            "type": "output_text", "text": "**Discipline** is itself a cause.",
                            "annotations": [],
                        }],
                    }],
                }).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            def local_client(**kwargs):
                return OpenAI(base_url=f"http://127.0.0.1:{server.server_port}/v1", **kwargs)

            with patch("openai.OpenAI", side_effect=local_client):
                app = AppTest.from_file(str(ROOT / "app.py"))
                app.secrets.update({"OPENAI_API_KEY": "local-test-only", "OPENAI_MODEL": "test-model"})
                app.run()
                app.text_input[0].set_value("Does discipline matter?")
                app.button[0].click().run()
                self.assertEqual(len(app.exception), 0)
                self.assertEqual(app.session_state.answer, "**Discipline** is itself a cause.")
            self.assertEqual(captured["path"], "/v1/responses")
            self.assertEqual(captured["body"]["instructions"], WORLDVIEW)
            self.assertEqual(captured["body"]["input"], "Does discipline matter?")
            self.assertFalse(captured["body"]["store"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

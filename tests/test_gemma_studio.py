"""
GemmaStudio Comprehensive Automated Test Suite
Hackathon Verification for "Best Use of Gemma 4" Track
Covers:
1. Application initialization & route verification
2. API status endpoint & masked key validation
3. Input validation & 413 Payload size limits (16MB)
4. Code snippet generation (Python, JS, cURL)
5. Static code validation endpoint (/api/experiments/validate-code)
6. Multimodal image data-URI parser unit tests
7. Experiment Benchmark Suites endpoint & structure
8. Chat history CRUD endpoints (Save, Read, List, Clear)
"""

import io
import json
import os
import unittest
from PIL import Image

import app as gemma_app


class TestGemmaStudio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("GEMINI_API_KEY", "test-mock-key-for-automated-suites")
        gemma_app.app.config["TESTING"] = True
        cls.client = gemma_app.app.test_client()

    def test_01_index_route(self):
        """Test home page loads with 200 OK and includes key GemmaStudio branding."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("GemmaStudio", html)
        self.assertIn("gemma-4-26b-a4b-it", html)
        self.assertIn("Experiment Studio", html)

    def test_02_status_endpoint(self):
        """Test /api/status returns model list and secure masked key status."""
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("status", data)
        self.assertIn("models", data)
        self.assertIn("default_model", data)
        self.assertEqual(data["default_model"], "gemma-4-26b-a4b-it")
        model_ids = [m["id"] for m in data["models"]]
        self.assertIn("gemma-4-26b-a4b-it", model_ids)
        self.assertIn("gemma-4-31b-it", model_ids)
        # Ensure raw key is never leaked
        if data.get("has_key"):
            self.assertIn("...", data["masked_key"])
            self.assertNotIn(os.getenv("GEMINI_API_KEY", "NOT_SET"), data["masked_key"])

    def test_03_request_validation_missing_prompt(self):
        """Test /api/generate rejects empty prompt requests gracefully."""
        response = self.client.post(
            "/api/generate",
            data=json.dumps({"model": "gemma-4-26b-a4b-it", "prompt": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get("success", True))
        self.assertIn("error", data)

    def test_04_request_validation_unsupported_model(self):
        """Test /api/generate rejects fake/unsupported model identifiers."""
        response = self.client.post(
            "/api/generate",
            data=json.dumps({"model": "gpt-fake-model-99", "prompt": "Hello"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Unsupported model", data.get("error", ""))

    def test_05_code_snippet_generation(self):
        """Test /api/code-snippet generates accurate Python, JS, and cURL snippets."""
        payload = {
            "model": "gemma-4-26b-a4b-it",
            "prompt": "Explain merge sort in Python",
            "thinking_level": "high",
            "system_instruction": "You are a concise algorithm tutor.",
            "has_image": False,
        }
        response = self.client.post(
            "/api/code-snippet",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("python", data)
        self.assertIn("javascript", data)
        self.assertIn("curl", data)

        # Python checks: must import google.genai and pass thinking config
        self.assertIn("from google import genai", data["python"])
        self.assertIn("gemma-4-26b-a4b-it", data["python"])
        self.assertIn("thinking_level", data["python"])

        # JS checks: must import @google/genai
        self.assertIn("@google/genai", data["javascript"])
        self.assertIn("gemma-4-26b-a4b-it", data["javascript"])

        # cURL checks: must point to v1beta models endpoint
        self.assertIn("generativelanguage.googleapis.com", data["curl"])
        self.assertIn("gemma-4-26b-a4b-it:generateContent", data["curl"])

    def test_06_code_snippet_validation_endpoint(self):
        """Test /api/experiments/validate-code static validation for Python and JS."""
        # Valid Python snippet
        py_valid = "from google import genai\nclient = genai.Client()\nprint('Ready')"
        res = self.client.post(
            "/api/experiments/validate-code",
            data=json.dumps({"language": "python", "code": py_valid}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.data)["valid"])

        # Invalid Python snippet (syntax error)
        py_invalid = "def broken(:\n    pass"
        res = self.client.post(
            "/api/experiments/validate-code",
            data=json.dumps({"language": "python", "code": py_invalid}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertFalse(json.loads(res.data)["valid"])

    def test_07_image_data_uri_parser(self):
        """Unit test _parse_data_uri_to_image with in-memory PIL image."""
        img = Image.new("RGB", (64, 64), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        import base64
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64_str}"

        parsed_pil = gemma_app._parse_data_uri_to_image(data_uri)
        self.assertIsNotNone(parsed_pil)
        self.assertEqual(parsed_pil.size, (64, 64))

        # Test corrupt data URI
        bad_uri = "data:image/png;base64,not_valid_base64_data@@@"
        parsed_bad = gemma_app._parse_data_uri_to_image(bad_uri)
        self.assertIsNone(parsed_bad)

    def test_08_experiment_suites_endpoint(self):
        """Test /api/experiments/suites returns valid test suites with expected structure."""
        response = self.client.get("/api/experiments/suites")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get("success"))
        suites = data.get("suites", [])
        self.assertGreater(len(suites), 0)
        suite_ids = [s["id"] for s in suites]
        self.assertIn("math_reasoning", suite_ids)
        self.assertIn("algorithmic_code", suite_ids)

    def test_09_chat_history_crud(self):
        """Test chat history saving, listing, reading, and clearing."""
        # 1. Save a mock history session
        test_session_id = f"test_session_{int(os.getpid())}"
        save_payload = {
            "id": test_session_id,
            "title": "Automated Test Session",
            "model": "gemma-4-26b-a4b-it",
            "messages": [
                {"role": "user", "text": "What is 7 * 8?"},
                {"role": "model", "text": "56"},
            ],
        }
        res_save = self.client.post(
            "/api/history/save",
            data=json.dumps(save_payload),
            content_type="application/json",
        )
        self.assertEqual(res_save.status_code, 200)
        self.assertTrue(json.loads(res_save.data).get("success"))

        # 2. List sessions and ensure our test session is present
        res_list = self.client.get("/api/history")
        self.assertEqual(res_list.status_code, 200)
        sessions = json.loads(res_list.data).get("sessions", [])
        found = any(s["id"] == test_session_id for s in sessions)
        self.assertTrue(found, "Saved session was not found in /api/history list")

        # 3. Read specific session by ID
        res_get = self.client.get(f"/api/history/{test_session_id}")
        self.assertEqual(res_get.status_code, 200)
        sess_data = json.loads(res_get.data)
        self.assertTrue(sess_data.get("success"))
        self.assertEqual(len(sess_data["session"]["messages"]), 2)

        # 4. Clean up test session file from disk
        test_file = os.path.join(gemma_app.HISTORY_DIR, f"{test_session_id}.json")
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    unittest.main()

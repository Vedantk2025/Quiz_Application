"""
Application level tests for Quiz Application.
Tests app factory, routing, status codes, health endpoint, and error handlers.
"""

import unittest
from app import create_app
from config import TestingConfig
from database.seed import init_database


class AppTestCase(unittest.TestCase):
    """Test general application endpoints and error responses."""

    def setUp(self):
        # Initialize test database
        init_database(TestingConfig.DATABASE_PATH)
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def test_app_starts(self):
        """Verify the Flask application initializes properly."""
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.config["TESTING"])

    def test_home_page_returns_200(self):
        """Test home page '/' loads successfully."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Select Difficulty Level", response.data)
        self.assertIn(b"Interactive", response.data)
        self.assertIn(b"Python Quiz", response.data)

    def test_health_endpoint(self):
        """Test '/health' endpoint returns JSON ok status."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data.get("status"), "ok")

    def test_invalid_route_404(self):
        """Test accessing non-existent route triggers custom 404 handler."""
        response = self.client.get("/non-existent-quiz-route")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page Not Found", response.data)

    def test_restart_route(self):
        """Test '/restart' clears session and redirects to index."""
        with self.client.session_transaction() as sess:
            sess["quiz_in_progress"] = True
            sess["difficulty"] = "easy"

        response = self.client.get("/restart", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify session is cleared
        with self.client.session_transaction() as sess:
            self.assertNotIn("quiz_in_progress", sess)


if __name__ == "__main__":
    unittest.main()

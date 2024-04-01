import unittest
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from app import app
from database import check_database_connection

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('database.check_database_connection')
    def test_database_connection_success(self, mock_connect_to_db):
        # Simular una conexión exitosa a la base de datos
        mock_connection = MagicMock()
        mock_connect_to_db.return_value = mock_connection

        response = self.client.get("/stats")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_connect_to_db.called)

    @patch('database.check_database_connection')
    def test_database_connection_failure(self, mock_connect_to_db):
        # Simular una conexión fallida a la base de datos
        mock_connect_to_db.side_effect = Exception("Database connection failed")

        response = self.client.get("/stats")

        self.assertEqual(response.status_code, 500)
        self.assertTrue(mock_connect_to_db.called)

if __name__ == '__main__':
    unittest.main()

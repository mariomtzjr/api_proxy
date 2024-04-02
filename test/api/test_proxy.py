import os
import unittest

import requests
from dotenv import load_dotenv

load_dotenv()

class TestProxy(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.api_base_url =  os.getenv('URL_FASTAPI_SERVER')
        self.api_base_port = os.getenv('PORT_FASTAPI')
        self.api_url = self.api_base_url + ":" + self.api_base_port + "/proxy"

    def test_categories_success(self):
        """Test for /proxy/categories/MLA1071 endpoint
        """
        path = "/categories/MLA1071"
        result = self.session.get(self.api_url + path)

        data = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(data, dict)
    
    def test_categories_not_found(self):
        """Test for /categories/MLA12345 endpoint
        """
        path = "/categories/MLA12345"
        result = self.session.get(self.api_url + path)

        data = result.json()

        self.assertEqual(data["status"], 404)
        self.assertIn("not found", data["message"])
        self.assertEqual(data["error"], "not_found")
    
    def test_categories_not_found_path(self):
        """Test for /categories/MLA12345 endpoint
        """
        self.api_url = self.api_url[:-6]
        path = "/categories/MLA12345"
        result = self.session.get(self.api_url + path)

        data = result.json()

        self.assertEqual(result.status_code, 404)
    
    def test_categories_error(self):
        """Test for /MLA1071 endpoint
        """
        path = "/MLA1071"
        result = self.session.get(self.api_url + path)

        data = result.json()

        self.assertEqual(data["error"], "resource not found")

if __name__ == '__main__':
    unittest.main()

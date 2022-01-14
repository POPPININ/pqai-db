"""
Test all server routes
"""
import unittest
import sys
import os
from pathlib import Path
import requests

import dotenv

dotenv.load_dotenv()

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

PROTOCOL = 'http'
HOST = '127.0.0.1'
PORT = os.environ['PORT']

class TestServer(unittest.TestCase):

    """Test the REST API routes
    """

    def test_document_route(self):
        """Can retrieve a document's data
        """
        response = self.call_route('/docs/US7654321B2')
        self.assertEqual(200, response.status_code)
        patent = response.json()
        self.assertIsInstance(patent, dict)
        self.assertEqual('US7654321B2', patent['publicationNumber'])

    def test_drawing_listing_route(self):
        """Can retrieve a list of drawings associated with a document
        """
        response = self.call_route('/docs/US7654321B2/drawings')
        self.assertEqual(200, response.status_code)
        drawings = response.json()
        self.assertIsInstance(drawings, list)
        self.assertEqual(8, len(drawings))

    def test_drawing_route(self):
        """Can obtain a drawing
        """
        response = self.call_route('/docs/US7654321B2/drawings/1')
        self.assertEqual(200, response.status_code)

    @staticmethod
    def call_route(route):
        """Make a GET request to a specific route

        Args:
            route (str): Target route

        Returns:
            Response: Response object from `requests` module
        """
        url = f'{PROTOCOL}://{HOST}:{PORT}' + route
        response = requests.get(url)
        return response

if __name__ == '__main__':
    unittest.main()

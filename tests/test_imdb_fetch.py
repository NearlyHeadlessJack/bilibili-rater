import unittest
import requests


class MyTestCase(unittest.TestCase):
    def test_omdb_unitest(self):
        url = "http://www.omdbapi.com/?apikey=123&i=123&Season=123"
        response = requests.get(url).json()
        self.assertEqual(response["Error"], "Invalid API key!")  # add assertion here


if __name__ == "__main__":
    unittest.main()

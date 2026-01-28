import unittest
from bilibili_rater import DirectFetcher


class MyTestCase(unittest.TestCase):
    def test_imdbinfo_fetch(self):
        fetcher = DirectFetcher(is_show_ranking=True, is_show_title=True)
        result = fetcher.fetch(resource_id="tt0397306", season=1, episode=1)
        self.assertEqual(str(result["rating"]), "7.2")
        self.assertEqual(result["title"], "Pilot")
        self.assertEqual(result["ranking"], "16/23")


if __name__ == "__main__":
    unittest.main()

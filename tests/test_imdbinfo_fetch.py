import unittest
from bilibili_rater import DirectFetcher


class MyTestCase(unittest.TestCase):
    def test_imdbinfo_fetch(self):
        fetcher = DirectFetcher(is_show_ranking=True, is_show_title=True)
        result = fetcher.fetch(resource_id="tt0397306", season=1, episode=1)
        self.assertEqual(str(result["rating"]), "7.2")
        self.assertEqual(result["title"], "Pilot")
        self.assertEqual(result["ranking"], "16/23")
        self.assertEqual(result["average"], None)
        self.assertEqual(result["median"], None)

    def test_imdbinfo_all_fields(self):
        fetcher = DirectFetcher(True,True,True,True)
        result = fetcher.fetch(resource_id="tt0397306", season=2, episode=1)
        self.assertEqual(str(result["rating"]), "7.7")
        self.assertEqual(result["title"], "Camp Refoogee")
        self.assertEqual(result["ranking"], "5/19")
        self.assertEqual(result["average"], "7.5")
        self.assertEqual(result["median"], "7.5")


if __name__ == "__main__":
    unittest.main()

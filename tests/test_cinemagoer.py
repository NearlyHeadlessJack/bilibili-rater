import unittest
from imdb import Cinemagoer

class MyTestCase(unittest.TestCase):
    def test_cinamagoer_running(self):
        ia = Cinemagoer()
        movie = ia.get_movie('0133093')
        directors = []
        for director in movie['directors']:
            directors.append(director['name'])
        self.assertEqual(directors,["Lana Wachowski","Lilly Wachowski"])

if __name__ == '__main__':
    unittest.main()

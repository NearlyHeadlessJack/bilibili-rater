import unittest
from bilibili_api import video

class MyTestCase(unittest.TestCase):
    async def test_bilibili_fetch(self):
        v = video.Video(bvid="BV1UTuwzZEHV")
        video_info = await v.get_info()
        self.assertEqual(video_info["desc"], "明年BML我们再见！")


if __name__ == '__main__':
    unittest.main()

from exceptions.CPI_Exceptions import InvalidFile, InvalidParameters
from src.CPI import CPI
import unittest


class TestCPI(unittest.TestCase):

    def test_validate(self):
        with self.assertRaises(FileNotFoundError):
            CPI(file='e.txt')
        with self.assertRaises(InvalidFile):
            CPI(file='e.jpg')
        with self.assertRaises(InvalidFile):
            CPI(file='')
        with self.assertRaises(InvalidParameters):
            CPI()
        with self.assertRaises(InvalidParameters):
            CPI(facebook_page_id='')
        with self.assertRaises(InvalidParameters):
            CPI(access_token='')

    def test_publish_image(self):
        try:
            cpi = CPI('instagram_long_lived_token.txt')
        except InvalidFile:
            return
        self.assertEqual(cpi.publish_image(''), False)
        self.assertEqual(cpi.publish_image('local.jpg'), False)
        self.assertEqual(cpi.publish_image('local.mp3'), False)
        # self.assertEqual(cpi.publish_image('https://samplelib.com/lib/preview/mp4/sample-5s.mp4'), False)
        # self.assertEqual(cpi.publish_image('https://cdn-icons-png.flaticon.com/512/2991/2991148.png'), True)

    def test_publish_video(self):
        try:
            cpi = CPI('instagram_long_lived_token.txt')
        except InvalidFile:
            return
        self.assertEqual(cpi.publish_video(''), False)
        self.assertEqual(cpi.publish_video('local.jpg'), False)
        self.assertEqual(cpi.publish_video('local.mp3'), False)
        #  self.assertEqual(cpi.publish_video('https://cdn-icons-png.flaticon.com/512/2991/2991148.png'), False)
        # self.assertEqual(cpi.publish_video('https://samplelib.com/lib/preview/mp4/sample-5s.mp4'), True)


if __name__ == '__main__':
    unittest.main()

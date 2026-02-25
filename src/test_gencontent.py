import unittest
from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Hello, world!
"""
        self.assertEqual(extract_title(md), "Hello, world!")

    def test_extract_title_multiple_titles(self):
        md = """
# Hello, world!
# Another title
"""
        self.assertEqual(extract_title(md), "Hello, world!")


    def test_extract_title_no_title(self):
        md = """
This is a paragraph.
This is another paragraph.
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_in_middle(self):
        md = """
This is a paragraph.
# Hello, world!
This is another paragraph.
"""
        self.assertEqual(extract_title(md), "Hello, world!")

if __name__ == "__main__":
    unittest.main()

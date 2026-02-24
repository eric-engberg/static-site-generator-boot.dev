import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_code_block(self):
        node      = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )
    def test_bold_block(self):
        node      = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_multiple_bold_blocks(self):
        node      = TextNode("This is text with a **bold block** word and another **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_multiple_code_blocks(self):
        node      = TextNode("This is text with a `code block` word and another `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_bold_and_code_blocks(self):
        node      = TextNode("This is text with a **bold block** word and another `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_italic_block(self):
        node      = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_bold_and_italic_blocks(self):
        node      = TextNode("This is text with a **bold block** word and another *italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_bold_and_italic_and_code_blocks(self):
        node      = TextNode("This is text with a **bold block** word and another _italic block_ word and another `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is an ![image](https://fake.com/image.jpg) and this is also an ![image](https://otherfake.com/otherimage.jpg)"
        )

        self.assertListEqual(
            [
                ("image", "https://fake.com/image.jpg"),
                ("image", "https://otherfake.com/otherimage.jpg")
            ],
            matches
        )

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) and this is also a [link](https://www.othergoogle.com)"
        )
        self.assertListEqual(
            [
                ("link", "https://www.google.com"),
                ("link", "https://www.othergoogle.com")
            ],
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_images_and_links(self):
        images = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)"
        )
        links = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], images)
        self.assertListEqual([("link", "https://www.google.com")], links)

if __name__ == "__main__":
    unittest.main()

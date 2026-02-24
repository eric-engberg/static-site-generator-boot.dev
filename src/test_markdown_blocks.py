from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
import unittest

class TestMarkdownBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_line(self):
        md = "This is a single line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_markdown_to_blocks_multiple_lines(self):
        md = "This is a single line\nThis is another line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line\nThis is another line"])

    def test_markdown_to_blocks_multiple_lines_with_empty_lines(self):
        md = "This is a single line\n\nThis is another line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line", "This is another line"])

    def test_markdown_to_blocks_multiple_lines_with_empty_lines_and_spaces(self):
        md = "This is a single line\n\n\nThis is another line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line", "This is another line"])

    def test_markdown_to_blocks_multiple_lines_with_empty_lines_and_spaces_and_tabs(self):
        md = "This is a single line\n\n\tThis is another line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line", "This is another line"])

    def test_markdown_to_blocks_multiple_lines_with_empty_lines_and_spaces_and_tabs_and_newlines(self):
        md = "This is a single line\n\n\tThis is another line\n\nThis is a third line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line", "This is another line", "This is a third line"])

    def test_block_to_block_type_paragraph(self):
        block = "This is just a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_invalid_heading(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_no_closing_newline(self):
        block = "```\nThis is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_invalid_code(self):
        block = "```\nThis is not a code block```trailing test"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_single_line_quote(self):
        block = "> This is a single line quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_multiple_line_quote(self):
        block = "> This is a single line quote\n> This is another line quote\n> This is a third line quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_invalid_quote(self):
        block = "> This is a single line quote\nThis is another line quote\n> This is a third line quote\n> This is a fourth line quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a unordered list item\n- This is another unordered list item\n- This is a third unordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_invalid_unordered_list(self):
        block = "- This is a unordered list item\nThis is another unordered list item\n- This is a third unordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a ordered list item\n2. This is another ordered list item\n3. This is a third ordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_list(self):
        block = "1. This is a ordered list item\n3. This is another ordered list item\n2. This is a third ordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_to_html_node_paragraph(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text
This is the same paragraph on a new line
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><p>This is <b>bolded</b> paragraph</p><p>This is another paragraph with <i>italic</i> text This is the same paragraph on a new line</p></div>")

    def test_markdown_to_html_node_heading(self):
        md = "## This is a heading"
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><h2>This is a heading</h2></div>")

    def test_markdown_to_html_node_code(self):
        md = """```
This is a code block
```
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><pre><code>This is a code block\n</code></pre></div>")

    def test_markdown_to_html_node_multiline_code(self):
        md = """
```
This is a code block
This is another line of code
And a third line of code```
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><pre><code>This is a code block\nThis is another line of code\nAnd a third line of code</code></pre></div>")

    def test_markdown_to_html_node_inline_code(self):
        md = """
```
This is a code block that has **bold** and _italic_ text```
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><pre><code>This is a code block that has **bold** and _italic_ text</code></pre></div>")

    def test_markdown_to_html_node_quote(self):
        md = """
> This is a quote
> This is another line of quote
> This is a third line of quote
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><blockquote>This is a quote This is another line of quote This is a third line of quote</blockquote></div>")

    def test_markdown_to_html_node_unordered_list(self):
        md = """
- This is a unordered list item
- This is another unordered list item
- This is a third unordered list item
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><ul><li>This is a unordered list item</li><li>This is another unordered list item</li><li>This is a third unordered list item</li></ul></div>")

    def test_markdown_to_html_node_ordered_list(self):
        md = """
1. This is a ordered list item
2. This is another ordered list item
3. This is a third ordered list item
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><ol><li>This is a ordered list item</li><li>This is another ordered list item</li><li>This is a third ordered list item</li></ol></div>")

    def test_markdown_to_html_node_invalid_ordered_list(self):
        md = """
1. This is a ordered list item
3. This is another ordered list item
2. This is a third ordered list item
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><p>1. This is a ordered list item 3. This is another ordered list item 2. This is a third ordered list item</p></div>")

    def test_markdown_to_html_node_invalid_unordered_list(self):
        md = """
- This is a unordered list item
This is another unordered list item
- This is a third unordered list item
"""
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><p>- This is a unordered list item This is another unordered list item - This is a third unordered list item</p></div>")

    def test_markdown_to_html_node_ordered_list_with_inline_markdown(self):
        md = """
1. This is a ordered list item with **bold** and _italic_ text
2. This is another ordered list item with a [link](https://www.google.com)
3. This is a third ordered list item with a ![image](https://www.google.com/image.png)
"""
        html_node = markdown_to_html_node(md)
        self.maxDiff = None
        self.assertEqual(html_node.to_html(), '<div><ol><li>This is a ordered list item with <b>bold</b> and <i>italic</i> text</li><li>This is another ordered list item with a <a href="https://www.google.com">link</a></li><li>This is a third ordered list item with a <img src="https://www.google.com/image.png" alt="image"></li></ol></div>')

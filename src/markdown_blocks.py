import re

from enum import Enum
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_image, split_nodes_link, split_nodes_delimiter

class BlockType(Enum):
    PARAGRAPH      = "paragraph"
    HEADING        = "heading"
    CODE           = "code"
    QUOTE          = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST   = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = [ stripped for block in markdown.split("\n\n") if (stripped := block.strip())]
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    # Headings are lines that start with 1-6 # characters followed by a space and then some text on a single line.
    # 2 Heading lines separated by a single newline should return as a paragraph block for this lesson.
    if re.match(r"^#{1,6} .+$", block):
        return BlockType.HEADING
    # Code blocks are lines that start with ``` and are followed by a single newline and then some text that ends with ```.
    elif re.match(r"^```\n.*```$", block, re.DOTALL):
        return BlockType.CODE
    # Quote blocks must have all lines start with > and be separated by a single newline.
    elif all(re.match(r"^>\s?.*", line) for line in lines):
        return BlockType.QUOTE
    # Unordered list blocks must have all lines start with - and be separated by a single newline.
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    # Ordered list blocks must have all lines start with a number followed by a period and be separated by a single newline.
    elif all(line.startswith(f"{index + 1}. ") for index, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):

            case BlockType.HEADING:
                m = re.match(r"^(#{1,6}) (.*)$", block)
                if m:
                    heading_level = len(m.group(1))
                    heading_text = m.group(2)
                    children = text_to_children(heading_text)
                    html_nodes.append(ParentNode(tag=f"h{heading_level}", children=children))

            case BlockType.CODE:
                block = block.removeprefix("```\n").removesuffix("```")
                code_node = TextNode(block, TextType.CODE)
                code_node = text_node_to_html_node(code_node)
                parent_node = ParentNode(tag="pre", children=[code_node])
                html_nodes.append(parent_node)

            case BlockType.QUOTE:
                quote_text = " ".join([line.removeprefix("> ") for line in block.split("\n")])
                children = text_to_children(quote_text)
                html_nodes.append(ParentNode(tag="blockquote", children=children))

            case BlockType.UNORDERED_LIST:
                html_nodes.append(
                    ParentNode(
                        tag="ul",
                        children=[
                            ParentNode(
                                tag="li",
                                children=text_to_children(line.removeprefix("- "))
                            )
                            for line in block.split("\n")
                        ]
                    )
                )


            case BlockType.ORDERED_LIST:
                html_nodes.append(
                    ParentNode(
                        tag="ol",
                        children=[
                            ParentNode(
                                tag="li",
                                children=text_to_children(line.split(" ", 1)[1])
                            )
                            for line in block.split("\n")
                        ]
                    )
                )

            case BlockType.PARAGRAPH:
                html_nodes.append(ParentNode(tag="p", children=text_to_children(" ".join(block.split("\n")))))

    return ParentNode(tag="div", children=html_nodes)

def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = [text_node_to_html_node(node) for node in nodes]
    return nodes

import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
           new_nodes.append(node)
           continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter: no closing {delimiter} found in text: {node.text}")

        for i, part in enumerate(parts):
            if  part == "":
                continue
            t = text_type if i % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(part, t))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)

def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
           new_nodes.append(node)
           continue

        original_text = node.text
        links = (extract_markdown_images(node.text))
        for text, url in extract_markdown_images(node.text):
            before, original_text = original_text.split(f"![{text}]({url})", 1)
            if before == "":
                new_nodes.append(TextNode(text, TextType.IMAGE, url))
                continue
            else:
                new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.IMAGE, url))

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
           new_nodes.append(node)
           continue

        original_text = node.text
        links = (extract_markdown_links(node.text))
        for text, url in extract_markdown_links(node.text):
            before, original_text = original_text.split(f"[{text}]({url})", 1)
            if before == "":
                new_nodes.append(TextNode(text, TextType.LINK, url))
                continue
            else:
                new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINK, url))

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

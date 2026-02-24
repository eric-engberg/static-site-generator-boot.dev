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
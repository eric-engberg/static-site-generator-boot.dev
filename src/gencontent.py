import re
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if m := re.match(r"^#\s+(.*)$", line):
            return m.group(1).strip()
    raise Exception("No title found in markdown")

def generate_page(src_path, template_path, dest_path):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")
    with open(src_path, "r") as f:
        md = f.read()
    title = extract_title(md)
    with open(template_path, "r") as f:
        template = f.read()
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", markdown_to_html_node(md).to_html())
    with open(dest_path, "w") as f:
        f.write(html)

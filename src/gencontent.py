import re
import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if m := re.match(r"^#\s+(.*)$", line):
            return m.group(1).strip()
    raise Exception("No title found in markdown")

def generate_page(src_path, template_path, dest_path, basepath):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")
    with open(src_path, "r") as f:
        md = f.read()
    title = extract_title(md)
    with open(template_path, "r") as f:
        template = f.read()
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", markdown_to_html_node(md).to_html())
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursively(src_dir, template_path, dest_dir, basepath):
    for file in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, file).replace(".md", ".html")
        if file.endswith(".md") and os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path, basepath)
        elif os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursively(src_path, template_path, dest_path, basepath)

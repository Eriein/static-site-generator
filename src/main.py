import os
import shutil
from copystatic import source_to_destination
from converter import markdown_to_html_node
from utils import extract_title

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(result)

def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(base)

    src = os.path.join(base, "static")
    dst = os.path.join(root, "public")
    
    if os.path.exists(dst):
        shutil.rmtree(dst)
    source_to_destination(src, dst)

    from_path = os.path.join(root, "content", "index.md")
    template_path = os.path.join(root, "template.html")
    dest_path = os.path.join(root, "public", "index.html")
    
    generate_page(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
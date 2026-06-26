import os
import shutil
import sys
from copystatic import source_to_destination
from converter import markdown_to_html_node
from utils import extract_title

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html_content)

    result = result.replace('href="/', f'href="{basepath}')
    result = result.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(result)

def generate_page_recursive(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    for filename in os.listdir(from_path):
        current_src_path = os.path.join(from_path, filename)
        current_dst_path = os.path.join(dest_path, filename)

        if os.path.islink(current_src_path):  # guard before isdir
            continue
        if os.path.isdir(current_src_path):
            generate_page_recursive(current_src_path, template_path, current_dst_path, basepath)
        elif filename.endswith(".md"):
            html_dst = os.path.splitext(current_dst_path)[0] + ".html"
            try:
                generate_page(current_src_path, template_path, html_dst, basepath)
            except Exception as e:
                print(f"Warning: skipping {current_src_path}: {e}")


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    base = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(base)

    src = os.path.join(base, "static")
    dst = os.path.join(root, "docs")
    
    if os.path.exists(dst):
        shutil.rmtree(dst)
    source_to_destination(src, dst)

    from_path = os.path.join(root, "content")
    template_path = os.path.join(root, "template.html")
    dest_path = os.path.join(root, "docs")
    
    generate_page_recursive(from_path, template_path, dest_path, basepath)

if __name__ == "__main__":
    main()
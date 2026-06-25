from textnode import TextNode, TextType
from utils import markdown_to_blocks
import os
import shutil
from copystatic import source_to_destination

def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base, "static")
    dst = os.path.join(os.path.dirname(base), "public")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    source_to_destination(src, dst)

if __name__ == "__main__":
    main()
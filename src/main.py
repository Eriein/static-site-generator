from textnode import TextNode, TextType
from utils import markdown_to_blocks
def main() -> None:
    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
    result = markdown_to_blocks(md)
    print(result)


if __name__ == "__main__":
    main()
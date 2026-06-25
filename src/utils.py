import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        lines = block.split("\n")
        cleaned_block = [line.strip() for line in lines]
        stripped = "\n".join(cleaned_block)
        stripped = stripped.strip()
        if stripped:
            result.append(stripped)
    return result

def is_quote(md: str) -> bool:
    return all(re.match(r'^>', line) for line in md.split("\n"))

def is_unordered_list(md: str) -> bool:
    return all(re.match(r'^- ', line) for line in md.split("\n"))

def is_ordered_list(md: str) -> bool:
    count = 1
    for line in md.split("\n"):
        if not line.startswith(f"{count}. "):
            return False
        count += 1
    return True

def block_to_block_type(md: str) -> BlockType:
    if re.match(r'^#{1,6} ', md):
        return BlockType.HEADING
    elif re.match(r'^```[\s\S]*```$', md):
        return BlockType.CODE
    elif is_quote(md):
        return BlockType.QUOTE
    elif is_unordered_list(md):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(md):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


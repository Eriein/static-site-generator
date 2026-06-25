from enum import Enum
from leafnode import LeafNode
from utils import extract_markdown_links, extract_markdown_images

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        return (self.text == other.text) and (self.text_type.value == other.text_type.value) and (self.url == other.url)

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Unknown type")
    
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            result.append(node)
            continue
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: unclosed delimiter '{delimiter}' in '{node.text}'")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(part, TextType.TEXT))
            else:
                result.append(TextNode(part, text_type))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
            continue
        remaining = node.text
        for anchor, url in links:
            sections = remaining.split(f"[{anchor}]({url})", 1)
            # append a TEXT node for the part before it (if non-empty)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))
            # append a LINK node for the link itself
            result.append(TextNode(anchor, TextType.LINK, url))
            # then advance `remaining` to the part after it
            remaining = sections[1]
        if remaining:
            result.append(TextNode(remaining, TextType.TEXT))
    return result

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue
        remaining = node.text
        for anchor, url in images:
            sections = remaining.split(f"![{anchor}]({url})", 1)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(anchor, TextType.IMAGE, url))
            remaining = sections[1]
        if remaining:
            result.append(TextNode(remaining, TextType.TEXT))
    return result

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
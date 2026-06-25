from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_children
from utils import markdown_to_blocks, block_to_block_type, BlockType


def heading_helper(block: str) -> tuple[str, int]:
    heading_count = 0
    for char in block:
        if char == "#":
            heading_count += 1
        else:
            break
    return block[heading_count + 1:], heading_count


def quote_helper(block: str) -> list[ParentNode]:
    children = []
    for line in block.split("\n"):
        node = ParentNode("p", text_to_children(line[2:]))
        children.append(node)
    return children


def unordered_helper(block: str) -> list[ParentNode]:
    children = []
    for line in block.split("\n"):
        node = ParentNode("li", text_to_children(line[2:]))
        children.append(node)
    return children


def ordered_helper(block: str) -> list[ParentNode]:
    children = []
    strip_length = 3
    for i, line in enumerate(block.split("\n")):
        if i == 9:
            strip_length = 4
        elif i == 99:
            strip_length = 5
        node = ParentNode("li", text_to_children(line[strip_length:]))
        children.append(node)
    return children


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    all_block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            all_block_nodes.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
        elif block_type == BlockType.HEADING:
            text, level = heading_helper(block)
            all_block_nodes.append(ParentNode(f"h{level}", text_to_children(text)))
        elif block_type == BlockType.QUOTE:
            all_block_nodes.append(ParentNode("blockquote", quote_helper(block)))
        elif block_type == BlockType.UNORDERED_LIST:
            all_block_nodes.append(ParentNode("ul", unordered_helper(block)))
        elif block_type == BlockType.ORDERED_LIST:
            all_block_nodes.append(ParentNode("ol", ordered_helper(block)))
        elif block_type == BlockType.CODE:
            text_node = TextNode(block[4:-3], TextType.TEXT)
            code_leaf = text_node_to_html_node(text_node)
            all_block_nodes.append(ParentNode("pre", [ParentNode("code", [code_leaf])]))
    return ParentNode("div", all_block_nodes)

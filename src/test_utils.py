import unittest
from utils import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, BlockType


class TestUtils(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![first](https://example.com/a.png) and ![second](https://example.com/b.png)"
        )
        self.assertListEqual(
            [
                ("first", "https://example.com/a.png"),
                ("second", "https://example.com/b.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("No images here, just plain text.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "Visit [Google](https://www.google.com) for more."
        )
        self.assertListEqual([("Google", "https://www.google.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[one](https://one.com) and [two](https://two.com)"
        )
        self.assertListEqual(
            [("one", "https://one.com"), ("two", "https://two.com")],
            matches,
        )

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("No links here.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        # image syntax must not be captured as a link
        matches = extract_markdown_links(
            "![alt](https://img.com/pic.png) and [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images_ignores_plain_links(self):
        # plain links must not be captured as images
        matches = extract_markdown_images("[link](https://example.com)")
        self.assertListEqual([], matches)

    def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_empty_string(self):
        # empty input should return empty list, not ['']
        blocks = markdown_to_blocks("")
        self.assertListEqual([], blocks)

    def test_markdown_to_blocks_single_block(self):
        # no double newlines means the whole string is one block
        blocks = markdown_to_blocks("Just one paragraph here.")
        self.assertListEqual(["Just one paragraph here."], blocks)

    def test_markdown_to_blocks_strips_leading_trailing_blank_lines(self):
        # leading/trailing blank lines around the whole document are ignored
        blocks = markdown_to_blocks("\n\nHello\n\nWorld\n\n")
        self.assertListEqual(["Hello", "World"], blocks)

    def test_markdown_to_blocks_multiple_blank_lines_between_blocks(self):
        # triple (or more) blank lines still produce just two blocks, no empty entries
        blocks = markdown_to_blocks("First\n\n\n\nSecond")
        self.assertListEqual(["First", "Second"], blocks)

    def test_markdown_to_blocks_strips_inner_line_indentation(self):
        # indented continuation lines inside a block lose their leading spaces
        blocks = markdown_to_blocks("Line one\n    Line two indented")
        self.assertListEqual(["Line one\nLine two indented"], blocks)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_single(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)

    def test_heading_max(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_heading_missing_space(self):
        self.assertEqual(block_to_block_type("##NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> a quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type("> line one\n> line two"), BlockType.QUOTE)

    def test_quote_mixed_lines(self):
        self.assertEqual(block_to_block_type("> quoted\nnot quoted"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item one\n- item two"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        self.assertEqual(block_to_block_type("2. starts at two\n3. three"), BlockType.PARAGRAPH)

    def test_ordered_list_non_incrementing(self):
        self.assertEqual(block_to_block_type("1. first\n3. skipped two"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a plain paragraph."), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()

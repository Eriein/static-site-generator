import unittest
from converter import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        node = markdown_to_html_node("## Hello **world**")
        self.assertEqual(node.to_html(), "<div><h2>Hello <b>world</b></h2></div>")

    def test_quote(self):
        node = markdown_to_html_node("> line one\n> line two")
        self.assertEqual(node.to_html(), "<div><blockquote><p>line one</p><p>line two</p></blockquote></div>")

    def test_unordered_list(self):
        node = markdown_to_html_node("- item one\n- item **two**")
        self.assertEqual(node.to_html(), "<div><ul><li>item one</li><li>item <b>two</b></li></ul></div>")

    def test_ordered_list(self):
        node = markdown_to_html_node("1. first\n2. second\n3. third")
        self.assertEqual(node.to_html(), "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>")

    def test_multiple_block_types(self):
        md = "# Title\n\nA paragraph.\n\n- item one\n- item two"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>A paragraph.</p><ul><li>item one</li><li>item two</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()

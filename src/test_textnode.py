import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_link, split_nodes_images, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_TextType(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("some other text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("some other text", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/cat.png", "alt": "a cat"})

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_list(self):
        nodes = [
            TextNode("plain `code` text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("plain ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ])

    def test_multiple_delimiter_pairs(self):
        node = TextNode("**a** and **b**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("a", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
        ])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This is `unclosed", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and more",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and more", TextType.TEXT),
        ])

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ])

    def test_link_at_start(self):
        node = TextNode("[start](https://example.com) then text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("start", TextType.LINK, "https://example.com"),
            TextNode(" then text", TextType.TEXT),
        ])

    def test_link_at_end(self):
        node = TextNode("text before [end](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("text before ", TextType.TEXT),
            TextNode("end", TextType.LINK, "https://example.com"),
        ])

    def test_link_only(self):
        node = TextNode("[only](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("only", TextType.LINK, "https://example.com"),
        ])

    def test_no_links_passthrough(self):
        node = TextNode("just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_list(self):
        nodes = [
            TextNode("see [this](https://a.com) link", TextType.TEXT),
            TextNode("bold node", TextType.BOLD),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [
            TextNode("see ", TextType.TEXT),
            TextNode("this", TextType.LINK, "https://a.com"),
            TextNode(" link", TextType.TEXT),
            TextNode("bold node", TextType.BOLD),
        ])

    def test_ignores_images(self):
        node = TextNode(
            "![img](https://img.com/pic.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertNotIn(TextNode("img", TextType.LINK, "https://img.com/pic.png"), result)
        self.assertIn(TextNode("link", TextType.LINK, "https://example.com"), result)


class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_single_image(self):
        node = TextNode(
            "Text with ![alt](https://i.imgur.com/abc.png) image",
            TextType.TEXT,
        )
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("Text with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://i.imgur.com/abc.png"),
            TextNode(" image", TextType.TEXT),
        ])

    def test_multiple_images(self):
        node = TextNode(
            "![first](https://example.com/a.png) and ![second](https://example.com/b.png)",
            TextType.TEXT,
        )
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("first", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "https://example.com/b.png"),
        ])

    def test_image_at_start(self):
        node = TextNode("![pic](https://example.com/pic.png) then text", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("pic", TextType.IMAGE, "https://example.com/pic.png"),
            TextNode(" then text", TextType.TEXT),
        ])

    def test_image_at_end(self):
        node = TextNode("text before ![pic](https://example.com/pic.png)", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("text before ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "https://example.com/pic.png"),
        ])

    def test_image_only(self):
        node = TextNode("![only](https://example.com/x.png)", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("only", TextType.IMAGE, "https://example.com/x.png"),
        ])

    def test_no_images_passthrough(self):
        node = TextNode("just plain text", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

    def test_non_text_node_passthrough(self):
        node = TextNode("already italic", TextType.ITALIC)
        result = split_nodes_images([node])
        self.assertEqual(result, [TextNode("already italic", TextType.ITALIC)])

    def test_mixed_list(self):
        nodes = [
            TextNode("see ![pic](https://a.com/p.png) here", TextType.TEXT),
            TextNode("bold node", TextType.BOLD),
        ]
        result = split_nodes_images(nodes)
        self.assertEqual(result, [
            TextNode("see ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "https://a.com/p.png"),
            TextNode(" here", TextType.TEXT),
            TextNode("bold node", TextType.BOLD),
        ])

    def test_ignores_plain_links(self):
        node = TextNode(
            "![img](https://img.com/pic.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        result = split_nodes_images([node])
        self.assertIn(TextNode("img", TextType.IMAGE, "https://img.com/pic.png"), result)
        self.assertNotIn(TextNode("link", TextType.IMAGE, "https://example.com"), result)


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        result = text_to_textnodes("just plain text")
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

    def test_bold(self):
        result = text_to_textnodes("this is **bold** text")
        self.assertEqual(result, [
            TextNode("this is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic(self):
        result = text_to_textnodes("this is _italic_ text")
        self.assertEqual(result, [
            TextNode("this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_code(self):
        result = text_to_textnodes("use `print()` here")
        self.assertEqual(result, [
            TextNode("use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    def test_image(self):
        result = text_to_textnodes("look ![cat](https://example.com/cat.png) here")
        self.assertEqual(result, [
            TextNode("look ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            TextNode(" here", TextType.TEXT),
        ])

    def test_link(self):
        result = text_to_textnodes("visit [boot dev](https://www.boot.dev) now")
        self.assertEqual(result, [
            TextNode("visit ", TextType.TEXT),
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" now", TextType.TEXT),
        ])

    def test_all_types(self):
        result = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and a [link](https://boot.dev)"
        )
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_bold_and_link(self):
        result = text_to_textnodes("**bold** then [link](https://example.com)")
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ])

    def test_image_and_link(self):
        result = text_to_textnodes(
            "![img](https://example.com/a.png) and [link](https://example.com)"
        )
        self.assertEqual(result, [
            TextNode("img", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ])

    def test_empty_string(self):
        result = text_to_textnodes("")
        self.assertEqual(result, [TextNode("", TextType.TEXT)])


if __name__ == "__main__":
    unittest.main()
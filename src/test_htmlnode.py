import unittest 
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "My name is erick")
        node2 = HTMLNode("p", "My name is erick")
        self.assertEqual(node1, node2)
    
    def test_not_eq(self):
        node1 = HTMLNode("p", "My name is Jose")
        node2 = HTMLNode("p", "My name is erick")
        self.assertNotEqual(node1, node2)
    
    def test_props_to_html_eq(self):
        node = HTMLNode(
            props={
                "href": "https://example.com",
                "target": "_blank",
            }
        )
        result = node.props_to_html()
        self.assertEqual(' href="https://example.com" target="_blank"', result)

    def test_props_to_html_is_None(self):
        node = HTMLNode()
        result = node.props_to_html()
        self.assertEqual("", result)
if __name__ == "__main__":
    unittest.main()

import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "text")])
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_deeply_nested(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [LeafNode("b", "deep")])
            ])
        ])
        self.assertEqual(node.to_html(), "<div><section><p><b>deep</b></p></section></div>")

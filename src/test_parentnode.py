import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nested_parent(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        grandchild2_node = LeafNode(tag="b", value="grandchild2")
        child2_node = ParentNode(tag="span", children=[grandchild2_node])
        parent_node = ParentNode(tag="div", children=[child_node, child2_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span><b>grandchild2</b></span></div>",
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode(tag="b", value="great grandchild")
        grandchild_node = ParentNode(tag="span", children=[great_grandchild_node])
        child_node = ParentNode(tag="div", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><div><span><b>great grandchild</b></span></div></div>",
        )

    def test_to_html_with_mixed_children(self):
        leaf_node = LeafNode(tag="b", value="Bold text")
        nested_leaf_node = LeafNode(tag="i", value="italic text")
        child_node = ParentNode(tag="span", children=[nested_leaf_node])
        parent_node = ParentNode(tag="div", children=[child_node, leaf_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><i>italic text</i></span><b>Bold text</b></div>"
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="span", children=None).to_html()

if __name__ == "__main__":
    unittest.main()

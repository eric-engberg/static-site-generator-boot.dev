import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a div node")
        node2 = HTMLNode("div", "This is a div node")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("div", "This is a div node")
        node2 = HTMLNode("span", "This is a span node")
        self.assertNotEqual(node, node2)

    def test_neq_props(self):
        node = HTMLNode("div", "This is a div node", {"class": "container"})
        node2 = HTMLNode("div", "This is a div node", {"class": "container2"})
        self.assertNotEqual(node, node2)

    def test_neq_children(self):
        node = HTMLNode("div", "This is a div node", children=[HTMLNode("span", "This is a span node")])
        node2 = HTMLNode("div", "This is a div node", children=[HTMLNode("link", "This is a link node")])
        self.assertNotEqual(node, node2)

    def test_neq_tag(self):
        node  = HTMLNode("div", "This is a div node")
        node2 = HTMLNode("span", "This is a span node")
        self.assertNotEqual(node.tag, node2.tag)

if __name__ == "__main__":
    unittest.main()
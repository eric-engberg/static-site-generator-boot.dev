import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode("div", "This is a div node")
        node2 = HtmlNode("div", "This is a div node")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HtmlNode("div", "This is a div node")
        node2 = HtmlNode("span", "This is a span node")
        self.assertNotEqual(node, node2)

    def test_neq_props(self):
        node = HtmlNode("div", "This is a div node", {"class": "container"})
        node2 = HtmlNode("div", "This is a div node", {"class": "container2"})
        self.assertNotEqual(node, node2)

    def test_neq_children(self):
        node = HtmlNode("div", "This is a div node", children=[HtmlNode("span", "This is a span node")])
        node2 = HtmlNode("div", "This is a div node", children=[HtmlNode("link", "This is a link node")])
        self.assertNotEqual(node, node2)

    def test_neq_tag(self):
        node  = HtmlNode("div", "This is a div node")
        node2 = HtmlNode("span", "This is a span node")
        self.assertNotEqual(node.tag, node2.tag)

if __name__ == "__main__":
    unittest.main()
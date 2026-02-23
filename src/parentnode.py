from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, *, tag, children, props=None):
        super().__init__(tag=tag, value=None, props=props, children=children )

    def to_html(self):
        if self.tag == None:
            raise ValueError("parent node must have a tag")
        if self.children is None:
            raise ValueError("parent node must have children")

        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()

        return result + f"</{self.tag}>"


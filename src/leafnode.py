from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, *, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None and self.tag != "img":
            raise ValueError("leaf node must have a value")
        if self.tag is None:
            return self.value
        if self.value is None:
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})"

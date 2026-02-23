from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)

        self.tag      = tag
        self.value    = value
        self.props    = props

    def to_html(self):
        if self.value == None:
            raise ValueError("leaf node must have a value")
        if self.tag == None:
            return self.value

        parts = []
        prop_str = ""
        if self.props != None:
            for key, value in self.props.items():
                parts.append(f'{key}="{value}"')
            prop_str = " " + " ".join(parts)
        return f"<{self.tag}{prop_str}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, props={self.props})"

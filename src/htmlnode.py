class HTMLNode                                                       :
    def   __init__(self, *, tag=None, value=None, props=None, children=None):
        self.tag      = tag
        self.value    = value
        self.props    = props
        self.children = children

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        if  self.props is None :
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return self.tag == other.tag and self.value == other.value and self.props == other.props and self.children == other.children

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children is required")
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"

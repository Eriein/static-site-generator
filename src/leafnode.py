from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    VOID_TAGS = {"img", "br", "hr", "input", "meta", "link"}

    def to_html(self) -> str:
        if self.tag in self.VOID_TAGS:
            return f"<{self.tag}{super().props_to_html()}>"
        if self.value is None or len(self.value) == 0:
            raise ValueError("A leaf node must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

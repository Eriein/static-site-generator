from textnode import TextNode, TextType

def main() -> None:
    text = TextNode("Somde text", TextType.BOLD, "https://www.boot.dev")
    print(text)


if __name__ == "__main__":
    main()
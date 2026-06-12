from textnode import TextNode, TextType

def main():
    text = TextNode("Somde text", TextType.BOLD, "https://www.boot.dev")
    print(text)


if __name__ == "__main__":
    main()
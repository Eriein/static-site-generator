import unittest
from utils import extract_markdown_images, extract_markdown_links


class TestUtils(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![first](https://example.com/a.png) and ![second](https://example.com/b.png)"
        )
        self.assertListEqual(
            [
                ("first", "https://example.com/a.png"),
                ("second", "https://example.com/b.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("No images here, just plain text.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "Visit [Google](https://www.google.com) for more."
        )
        self.assertListEqual([("Google", "https://www.google.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[one](https://one.com) and [two](https://two.com)"
        )
        self.assertListEqual(
            [("one", "https://one.com"), ("two", "https://two.com")],
            matches,
        )

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("No links here.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        # image syntax must not be captured as a link
        matches = extract_markdown_links(
            "![alt](https://img.com/pic.png) and [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images_ignores_plain_links(self):
        # plain links must not be captured as images
        matches = extract_markdown_images("[link](https://example.com)")
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()

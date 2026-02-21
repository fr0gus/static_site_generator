import unittest
from regex_extract import extract_markdown_images, extract_markdown_links


class SplitTester(unittest.TestCase):
    
    def test_images(self):
        matches = extract_markdown_images(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)") 
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(matches, expected)

    def test_links(self):
        matches = extract_markdown_links(text='This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev')
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(matches, expected)

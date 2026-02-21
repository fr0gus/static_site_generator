import unittest
from split_delimiter import split_nodes_delimiter, split_nodes_link, split_nodes_images, \
text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):

    def test_bold(self):
        node = TextNode('This is a *bolded* word', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '*', TextType.BOLD)

        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('bolded', TextType.BOLD),
                TextNode(' word', TextType.TEXT)
            ],
            new_nodes
        )

    def test_bold_double(self):
        node = TextNode('This is a **bolded** word and **another**', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)

        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('bolded', TextType.BOLD),
                TextNode(' word and ', TextType.TEXT),
                TextNode('another', TextType.BOLD)
            ],
            new_nodes
        )

    def test_italic(self):
        node = TextNode('This is a _italic_ word', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('italic', TextType.ITALIC),
                TextNode(' word', TextType.TEXT),
            ],
            new_nodes
        )

    def test_italic_and_bold(self):
        node = TextNode('This is a _italic_ and *bold* word', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, '*', TextType.BOLD)

        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('italic', TextType.ITALIC),
                TextNode(' and ', TextType.TEXT),
                TextNode('bold', TextType.BOLD),
                TextNode(' word', TextType.TEXT)
            ],
            new_nodes
        )


    def test_err(self):
        node = TextNode('This is a italic and bold word', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode('This is a italic and bold word', TextType.TEXT),
            ],
            new_nodes
        )

    def test_links1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
         TextNode("This is text with a link ", TextType.TEXT),
         TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
         TextNode(" and ", TextType.TEXT),
         TextNode(
             "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
         ),
     ]

    def test_links2(self):
        text = TextNode('This has [one link](https://example.com).This has [two](https://a.com) and [three](https://b.com)."Starting with [Link](https://start.com) then text.', TextType.TEXT)
        new_nodes = split_nodes_link([text])
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode('one link', TextType.LINK, 'https://example.com'),
            TextNode('.This has ', TextType.TEXT),
            TextNode('two', TextType.LINK, 'https://a.com'),
            TextNode(' and ', TextType.TEXT),
            TextNode('three', TextType.LINK, 'https://b.com'),
            TextNode('."Starting with ', TextType.TEXT),
            TextNode('Link', TextType.LINK, 'https://start.com'),
            TextNode(' then text.', TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)
        
        
    def test_links3(self):
        text = TextNode('[one link](https://example.com).This has [two](https://a.com) and [three](https://b.com)."Starting with [Link](https://start.com) then text.', TextType.TEXT)
        new_nodes = split_nodes_link([text])
        expected = [
            TextNode('one link', TextType.LINK, 'https://example.com'),
            TextNode('.This has ', TextType.TEXT),
            TextNode('two', TextType.LINK, 'https://a.com'),
            TextNode(' and ', TextType.TEXT),
            TextNode('three', TextType.LINK, 'https://b.com'),
            TextNode('."Starting with ', TextType.TEXT),
            TextNode('Link', TextType.LINK, 'https://start.com'),
            TextNode(' then text.', TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_images(self):
        text = TextNode('This has ![one link](https://example.com).This has ![two](https://a.com) and ![three](https://b.com)."Starting with ![Link](https://start.com) then text.', TextType.TEXT)
        new_nodes = split_nodes_images([text])
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode('one link', TextType.IMAGE, 'https://example.com'),
            TextNode('.This has ', TextType.TEXT),
            TextNode('two', TextType.IMAGE, 'https://a.com'),
            TextNode(' and ', TextType.TEXT),
            TextNode('three', TextType.IMAGE, 'https://b.com'),
            TextNode('."Starting with ', TextType.TEXT),
            TextNode('Link', TextType.IMAGE, 'https://start.com'),
            TextNode(' then text.', TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_txt_to_node1(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('text', TextType.BOLD),
            TextNode(' with an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://boot.dev')
        ]

        self.assertListEqual(new_nodes, expected)
 
    def test_txt_to_node2(self):
        text = '[First Link](https://start.com) some middle text [Last Link](https://end.com)'
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode('First Link', TextType.LINK, 'https://start.com'),
            TextNode(' some middle text ', TextType.TEXT ),
            TextNode('Last Link', TextType.LINK,'https://end.com',) 
        ]

        self.assertListEqual(new_nodes, expected)
     
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


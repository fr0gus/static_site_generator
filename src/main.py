from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_blocktype, BlockType
from split_delimiter import text_to_textnodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)

    return html_nodes


def paragraph_to_html(paragraph):
    cleaned = paragraph.strip().replace("\n", " ")
    children = text_to_children(cleaned)

    parent = ParentNode("p", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        btype = block_to_blocktype(block)

        if btype == BlockType.PARAGRAPH:
            paragraph_to_html(block)


def main():
    markdown = """
    # This is a header\n
    Followed up by **bold** and _italic_ text
    """
    newNode = TextNode("Me gusta", TextType.BOLD, "https://www.boot.dev")
    print(newNode)

    markdown_to_html_node(markdown)


if __name__ == "__main__":
    main()

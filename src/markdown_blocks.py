from enum import Enum
from textnode import text_node_to_html_node, TextNode, TextType
from regex_extract import extract_markdown_images, extract_markdown_links
from htmlnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_blocktype(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].strip().startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        text_split = node.text.split(delimiter)

        if len(text_split) % 2 == 0:
            raise Exception("Invalid Markdown syntax")

        for i in range(len(text_split)):
            if text_split[i] == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(text_split[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(text_split[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_images(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        split_nodes = []

        for img in images:
            node.text = node.text.replace(img[0], "").replace(img[1], "")

        text_split = node.text.split("![]()")

        for i in range(len(images)):
            if text_split[i] == "":
                split_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                continue

            split_nodes.append(TextNode(text_split[i], TextType.TEXT))
            split_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))

        if len(text_split) > len(images) and text_split[-1] != "":
            split_nodes.append(TextNode(text_split[-1], TextType.TEXT))

        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        split_nodes = []

        for link in links:
            node.text = node.text.replace(link[0], "").replace(link[1], "")

        text_split = node.text.split("[]()")

        for i in range(len(links)):
            if text_split[i] == "":
                split_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                continue

            split_nodes.append(TextNode(text_split[i], TextType.TEXT))
            split_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))

        if len(text_split) > len(links) and text_split[-1] != "":
            split_nodes.append(TextNode(text_split[-1], TextType.TEXT))

        new_nodes.extend(split_nodes)

    return new_nodes

def clean_text(text, marker=None):
    lines = text.split("\n")
    cleaned = " ".join(line.strip() for line in lines if line.strip() != "")

    if marker:
        cleaned = cleaned.replace(marker, "")

    cleaned = cleaned.strip()

    return cleaned


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)

    return html_nodes


def header_to_html(header):
    cleaned = clean_text(header, "#")
    children = text_to_children(cleaned)

    rank = 0

    rank = 0
    while rank < len(header) and header[rank] == "#":
        rank += 1

    parent = ParentNode(f"h{rank}", children)
    return parent


def ulist_to_html(list):
    lines = list.split("\n")
    list_items = []

    for line in lines:
        if line != "":
            clean_line = clean_text(clean_text(line, "- "), "* ")
            children = text_to_children(clean_line)
            list_item = ParentNode("li", children)
            list_items.append(list_item)

    parent = ParentNode("ul", children=list_items)
    return parent


def olist_to_html(list):
    lines = list.split("\n")
    list_items = []

    for line in lines:
        if line != "":
            clean_line = clean_text(line)

            i = 0

            while clean_line[i].isdigit():
                i += 1

            clean_line = line[i + 2 :]

            children = text_to_children(clean_line)
            list_item = ParentNode("li", children)
            list_items.append(list_item)

    parent = ParentNode("ol", children=list_items)
    return parent


def quote_to_html(quote):
    cleaned = clean_text(quote, ">")
    children = text_to_children(cleaned)

    parent = ParentNode("blockquote", children)
    return parent


def code_to_html(code):
    cleaned = code[4:-3]

    text_node = TextNode(cleaned, TextType.CODE)
    code = text_node_to_html_node(text_node)

    parent = ParentNode("pre", children=[code])

    return parent


def paragraph_to_html(paragraph):
    cleaned = clean_text(paragraph)
    children = text_to_children(cleaned)

    parent = ParentNode("p", children)
    return parent


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []

    for block in blocks:
        btype = block_to_blocktype(block)

        match btype:
            case BlockType.HEADING:
                html_children.append(header_to_html(block))
            case BlockType.PARAGRAPH:
                html_children.append(paragraph_to_html(block))
            case BlockType.CODE:
                html_children.append(code_to_html(block))
            case BlockType.UNORDERED_LIST:
                html_children.append(ulist_to_html(block))
            case BlockType.ORDERED_LIST:
                html_children.append(olist_to_html(block))
            case BlockType.QUOTE:
                html_children.append(quote_to_html(block))

    return ParentNode("div", html_children)



def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_images(nodes)

    return nodes

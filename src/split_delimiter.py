from textnode import TextNode, TextType
from regex_extract import extract_markdown_images, extract_markdown_links

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
            node.text = node.text.replace(img[0], '').replace(img[1], '')


        text_split = node.text.split('![]()')

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
            node.text = node.text.replace(link[0], '').replace(link[1], '')

        text_split = node.text.split('[]()')

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

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]

    nodes = split_nodes_delimiter(nodes,'**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,'_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_images(nodes)

    return nodes


from enum import Enum

from htmlnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text):
    lines = text.split("\n\n")
    stripped = list(map(lambda x: x.strip(), lines))
    blocks = [x for x in stripped if x != ""]

    return blocks


def block_to_blocktype(block):

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block[-3:].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        return BlockType.QUOTE

    if block.startswith("- "):
        return BlockType.UNORDERED_LIST

    if block[0].isnumeric() and block[1:3].startswith(". "):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

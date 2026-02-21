import re

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)*", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)*", text)


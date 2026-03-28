from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_blocks import (
    markdown_to_blocks,
    block_to_blocktype,
    text_to_textnodes,
    markdown_to_html_node,
    BlockType,
)


def main():
    markdown = """
### This is a headern

 Followed up by **bold** and _italic_ text

```
 some **text** should be unaffected
if x > 0:
```

### Followed by a ulist:

- item1
- item2
- item3

### Followed by an olist:

1. item 1
2. item 2
3. item 3
"""
    newNode = TextNode("Me gusta", TextType.BOLD, "https://www.boot.dev")

    print(markdown_to_html_node(markdown))


if __name__ == "__main__":
    main()

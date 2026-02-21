

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('Not implemented')

    def props_to_html(self):
        if self.props == None:
            return ""

        string = ''

        for prop in self.props:
            string += f' {prop}="{self.props[prop]}"'

        return string

    def __repr__(self) -> str:
        return f"tag: <{self.tag}>\n value: {self.value}\n children: {self.children}\n props: {self.props_to_html()}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError('All leaf nodes must have a value')

        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children , props=None) -> None:
        super().__init__(tag = tag, children = children, props = props, value = None)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Tag can't be None")

        if self.children == None:
            raise ValueError("Parent Tag must have children")

        html = ''

        for child in self.children:
            html += f"{child.to_html()}"

        html = f'<{self.tag}{self.props_to_html()}>{html}</{self.tag}>'

        return html
 






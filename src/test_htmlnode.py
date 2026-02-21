import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_raise(self):
        node = HTMLNode('h1', 'Milgusti', ['p'])
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props(self):
        node = HTMLNode('a', 'Milgusti2', ['p', 'p'], {'href': 'https://www.google.com', 'target': '_blank' })
        expected = f' href="https://www.google.com" target="_blank"'

        self.assertEqual(expected, node.props_to_html(), 'Props Test')

    def test_props_none(self):
        node = HTMLNode('a', 'Milgusti2', ['p', 'p'] )
        self.assertEqual('', node.props_to_html(), 'None Props Test')

    def test_repr(self):
        node = HTMLNode(tag='p', value='Milgusti2', props={'href': 'https://www.google.com', 'target': '_blank' })
        expected = f'tag: <p>\n value: Milgusti2\n children: None\n props:  href="https://www.google.com" target="_blank"'

        self.assertEqual(expected, repr(node), "Repr Test")

           
        
class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>", msg='Leaf to html')

    def test_leaf_value_err(self):
        node = LeafNode('a', None)
        self.assertRaises(ValueError, node.to_html)
     
    def test_leaf_to_html_w_props(self):
        node = LeafNode("a", "Click here!", {"href": "https://www.google.com", "target": "_blank"  })
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click here!</a>', msg='Leaf to html props')
 

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node1 = LeafNode("p", "grandchild paragraph")
        grandchild_node2 = LeafNode("a", "grandchild_link", )
        grandchild_node3 = LeafNode("b", "grandchild_bold")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2, grandchild_node3])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p>grandchild paragraph</p><a>grandchild_link</a><b>grandchild_bold</b></span></div>",
        )

    def test_to_html_tag_error(self):
        child_node = ParentNode('p', "notag" )
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()

        self.assertEqual("Parent Tag can't be None", str(cm.exception))

    def test_to_html_children_error(self):
        parent_node = ParentNode('div', None)

        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()

        self.assertEqual("Parent Tag must have children", str(cm.exception))

if __name__ == "__main__":
    unittest.main()

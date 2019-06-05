""" Class to use methods that can't stay in views.py"""
from text.models import TextFragment


def create_fragment(fragment, text):
    """
    Creates a fragment according to its type and adds the fragment
    into text's list of fragments
    """
    print(fragment)
    if fragment['type'] == 'text':
        body = fragment['body']
        text_frag = TextFragment()
        text_frag.body = body
        text_frag.price = len(body) * 0.1
        text_frag.text = text
        text.add(text_frag)


class FragmentIterator:
    """
    Iterates all fragments in text
    """
    def __init__(self, fragments, text):
        self.limit = len(fragments)
        self.position = 0
        self.fragments = fragments
        self.text = text

    def __iter__(self):
        return self

    """
    Finishes when position = limit
    Otherwise, gets the JSON at position in fragments array and
    sends it to create fragment
    """
    def __next__(self):
        print(self.fragments)
        if self.position < self.limit:
            fragment_json = self.fragments[self.position]
            create_fragment(fragment_json, self.text)
            self.position += 1
        else:
            print('position = ', self.position)
            raise StopIteration

""" Class to use methods that can't stay in views.py"""
from text.models import TextFragment, Text


def create_fragment(fragment, text):
    if fragment['type'] == 'text':
        body = fragment['body']
        text_frag = TextFragment()
        text_frag.body = body
        text_frag.price = len(body) * 0.1
        text_frag.text = text
        text.add(text_frag)


class FragmentIterator:
    """ Iterate in text send."""
    def __init__(self, fragments, text):
        self.limit = len(fragments)
        self.position = 0
        self.fragments = fragments
        self.text = text

    def __iter__(self):
        return self

    def __next__(self):
        if self.position < self.limit:
            fragment = self.fragments[self.position]
            create_fragment(fragment, self.text)
            self.position += 1
        else:
            print('position = ', self.position)
            raise StopIteration

""" Class to use methods that can't stay in views.py"""
from text.models import TextFragment


def create_fragment(fragment, text):
    """
    Creates a fragment according to its type and adds the fragment
    into text's list of fragments
    """
    if fragment['type'] == 'text':
        body = fragment['body']
        text_frag = TextFragment()
        text_frag.body = body
        text_frag.price = len(body) * 0.1
        text_frag.text = text
        text_frag.total_words = len(body.split())
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
        if self.position < self.limit:
            fragment_json = self.fragments[self.position]
            create_fragment(fragment_json, self.text)
            self.position += 1
        else:
            print('position = ', self.position)
            raise StopIteration


def get_all_fragments(text):
    """
    Inserts the text fragments in text
    """
    text_fragments = TextFragment.objects.filter(text=text)
    for i in text_fragments:
        text.add(i)

    # It's possible to add more fragments types
    text.sort_fragments()  


def percent_of_fragments(username, text_id):
    fragments = TextFragment.objects.filter(text=text_id)
    username_fragments = TextFragment.objects.filter(
        text=text_id).filter(fragment_translator=username)
    total_fragments = float(len(fragments))
    username_fragments = float(len(username_fragments))
    percent_of_text = username_fragments / total_fragments
    print(username_fragments, total_fragments)
    if percent_of_text >= 0.3:
        return False
    return True

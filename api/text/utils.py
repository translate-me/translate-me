""" Class to use methods that can't stay in views.py"""
from text.models import Fragment, Text


def create_fragment(identifier, body, price):
    """ Commit on fragment table."""
    text = Text.objects.get(id=identifier)
    Fragment.objects.create(text_id=text,
                            body=body,
                            price=price)


class FragmentIterator:
    """ Iterate in text send."""
    def __init__(self, body, breakpoints, identifier):
        self.limit = len(body) - 1
        self.body = body
        self.breakpoints = breakpoints
        self.limit_2 = len(breakpoints) - 1
        self.identifier = identifier
        self.breakpoint = 0
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Boundary case
        if self.count > self.limit_2:
            fragment_body = self.body[self.breakpoint:]
            price = len(fragment_body) * 0.1
            create_fragment(self.identifier, fragment_body, price)
            raise StopIteration

        end = self.breakpoints[self.count]
        fragment_body = self.body[self.breakpoint:end]
        self.breakpoint = end
        price = len(fragment_body) * 0.1
        # boundary cases
        if self.breakpoint >= self.limit:
            fragment_body = self.body[self.breakpoint:]
            price = len(fragment_body) * 0.1
            create_fragment(self.identifier, fragment_body, price)
            raise StopIteration
        self.count += 1
        return create_fragment(self.identifier, fragment_body, price)

""" Class to use methods that can't stay in views.py"""
from text.models import Fragment


def create_fragment(identifier, body, price):
    Fragment.objects.create(text_id=identifier,
                            body=body,
                            price=price)


class FragmentIterator:
    def __init__(self, body, breakpoints, identifier):
        self.limit = len(body) - 1
        self.body = body
        self.breakpoints = breakpoints
        self.identifier = identifier

    def __iter__(self):
        self.breakpoint = 0
        self.count = 0
        return self

    def next(self):
        end = self.breakpoints[self.count]
        fragment_body = self.body[self.breakpoint:end]
        self.breakpoint = end
        price = len(fragment_body) * 0.1
        if self.breakpoint >= self.limit:
            raise StopIteration
        self.count += 1
        return create_fragment(self.identifier, fragment_body, price)

from abc import ABC


"""
    Event handler base class
"""
class BaseEventHandler(ABC):
    def handle_create(self, *args, **kwargs):
        raise NotImplementedError

    def handle_update(self, *args, **kwargs):
        raise NotImplementedError

    def handle_delete(self, *args, **kwargs):
        raise NotImplementedError

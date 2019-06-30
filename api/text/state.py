from abc import ABCMeta, abstractmethod

class StateInterface(metaclass=ABCMeta):
            
    @abstractmethod
    def change_state(self, fragment) -> None:
        pass

class TranslationAssigned(StateInterface):

    def change_state(self, fragment):
        state = '2'
        fragment.notify_observers(state)
        fragment.state = state

class TranslationRefused(StateInterface):

    def change_state(self, fragment):
        state = '1'
        fragment.notify_observers(state)
        fragment.state = state

class WaitingReview(StateInterface):
    
    def change_state(self, fragment):
        state = '3'
        fragment.notify_observers(state)
        fragment.state = state

class Reviewing(StateInterface):
    
    def change_state(self, fragment):
        state = '4'
        fragment.notify_observers(state)
        fragment.state = state

class ToFinish(StateInterface):

    def change_state(self, fragment):
        state = '5'
        fragment.notify_observers(state)
        fragment.state = state

class Finished(StateInterface):

    def change_state(self, fragment):
        state = '6'
        fragment.notify_observers(state)
        fragment.state = state
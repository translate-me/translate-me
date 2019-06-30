from abc import ABCMeta, abstractmethod

class StateInterface(metaclass=ABCMeta):
            
    @abstractmethod
    def change_state(self, fragment) -> None:
        pass

class TranslatingState(StateInterface):

    def change_state(self, fragment):
        print('entrou aqui ########')
        state = '2'
        fragment.notify_observers(state)
        fragment.state = state
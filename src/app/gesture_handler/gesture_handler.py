from abc import ABC, abstractmethod

from src.app.config import KBH_START_STATE
from src.app.gesture_handler.state import get_state


class GestureHandler(ABC):

    @abstractmethod
    def handle(self, value) -> None:
        pass


class KeyboardGestureHandler(GestureHandler):

    def __init__(self):
        self.__state = get_state(KBH_START_STATE)

    def handle(self, value) -> None:
        self.__state.action(value)
        self.__state = self.__state.next_state(value)

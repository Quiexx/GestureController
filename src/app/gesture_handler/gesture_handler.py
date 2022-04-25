from abc import ABC, abstractmethod

from src.app.config import START_STATE
from src.app.gesture_handler.state import get_state


class GestureHandler(ABC):

    @abstractmethod
    def handle(self, value, data) -> None:
        pass


class KBMGestureHandler(GestureHandler):

    def __init__(self) -> None:
        self.__state = get_state(START_STATE, self)
        self.__taskbar_active = False
        self.__current_data = None

    def handle(self, value, data) -> None:
        self.__current_data = data
        self.__state.action(value)
        self.__state = self.__state.next_state(value)

    @property
    def is_taskbar_active(self) -> bool:
        return self.__taskbar_active

    @is_taskbar_active.setter
    def is_taskbar_active(self, value: bool) -> None:
        self.__taskbar_active = value

    @property
    def current_data(self) -> list:
        return self.__current_data



from abc import ABC, abstractmethod
from typing import Any

from src.app.config import START_STATE
from src.app.gesture_handler.state import get_state


class GestureHandler(ABC):
    """
    Abstract class for Gesture Handler
    """

    @abstractmethod
    def handle(self, value: Any, data: Any) -> None:
        """
        Handles a gesture
        :param value: gesture identifier
        :param data: data of the gesture like coordinates
        :return: None
        """
        pass


class KBMGestureHandler(GestureHandler):
    """
    Gesture Handler that operates with keyboard and mouse.
    States are loaded from json file.
    """

    def __init__(self) -> None:
        """
        Creates the handler
        """
        self.__state = get_state(START_STATE, self)
        self.__taskbar_active = False
        self.__current_data = None

    def handle(self, value: Any, data: Any) -> None:
        """
        Handles a gesture
        :param value: gesture identifier
        :param data: data of the gesture like coordinates
        :return: None
        """
        self.__current_data = data
        self.__state.action(value)
        self.__state = self.__state.next_state(value)

    @property
    def is_taskbar_active(self) -> bool:
        """
        Get task bar status
        :return: True if task bar is active else False
        """
        return self.__taskbar_active

    @is_taskbar_active.setter
    def is_taskbar_active(self, value: bool) -> None:
        """
        Set task bar status
        :param value: True if task bar is active else False
        :return: None
        """
        self.__taskbar_active = value

    @property
    def current_data(self) -> list:
        """
        Get current gesture data
        :return: gesture data
        """
        return self.__current_data

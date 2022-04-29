from abc import ABC, abstractmethod
from typing import Any

import pyautogui as pyautogui


class Action(ABC):
    """
    An action that is triggered in response to a gesture
    """

    @abstractmethod
    def __init__(self, instance: Any) -> None:
        """
        Creates Action
        :param instance: GestureHandler instance
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        Executes action
        :return: None
        """
        pass


class DoNothing(Action):
    """
    Action that does nothing
    """

    def __init__(self, instance: Any) -> None:
        """
        Creates Action
        :param instance: GestureHandler instance
        """
        pass

    def execute(self) -> None:
        """
        Executes action
        :return: None
        """
        pass


class NextTab(Action):
    """
    Switch to the next tab in browser or task bar
    """

    def __init__(self, instance: Any) -> None:
        """
        Creates Action
        :param instance: GestureHandler instance
        """
        self.__handler = instance

    def execute(self) -> None:
        """
        Executes action
        :return: None
        """
        if self.__handler.is_taskbar_active:
            pyautogui.hotkey('right')
        else:
            pyautogui.hotkey('ctrl', 'tab')


class PrevTab(Action):

    def __init__(self, instance: Any) -> None:
        """
        Creates Action
        :param instance: GestureHandler instance
        """
        self.__handler = instance

    def execute(self) -> None:
        """
        Executes action
        :return: None
        """
        if self.__handler.is_taskbar_active:
            pyautogui.hotkey('left')
        else:
            pyautogui.hotkey('ctrl', 'shift', 'tab')


class OpenTaskBar(Action):

    def __init__(self, instance: Any) -> None:
        """
        Creates Action
        :param instance: GestureHandler instance
        """
        self.__handler = instance

    def execute(self) -> None:
        """
        Executes action
        :return: None
        """
        if self.__handler.is_taskbar_active:
            pyautogui.hotkey('enter')
        else:
            pyautogui.hotkey('win', 'tab')
        self.__handler.is_taskbar_active = not self.__handler.is_taskbar_active


class MoveMouse(Action):
    def __init__(self, instance: Any):
        """
        Creates Action
        :param instance: GestureHandler instance
        """
        self.__handler = instance

    def execute(self) -> None:
        """
        Executes action
        :return: None
        """
        w, h = pyautogui.size()
        x, y = self.__handler.current_data[8][0], self.__handler.current_data[8][1]
        y = min(max(y - 0.14, 0) / 0.33, 1)
        x = min(max(x - 0.17, 0) / 0.53, 1)
        x, y = int((1 - x) * w), int(y * h)
        x, y = min(max(x, 2), w - 2), min(max(y, 2), h - 2)
        pyautogui.moveTo(x, y)


class Click(Action):
    def __init__(self, instance: Any) -> None:
        """
        Creates Action
        :param instance: GestureHandler instance
        """
        pass

    def execute(self) -> None:
        """
        Executes action
        :return: None
        """
        pyautogui.click()

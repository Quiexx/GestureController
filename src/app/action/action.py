from abc import ABC, abstractmethod
from typing import Any

import pyautogui as pyautogui


class Action(ABC):

    @abstractmethod
    def __init__(self, instance: Any):
        pass

    @abstractmethod
    def execute(self) -> None:
        pass


class DoNothing(Action):

    def __init__(self, instance: Any):
        pass

    def execute(self) -> None:
        pass


class NextTab(Action):

    def __init__(self, instance: Any):
        self.__handler = instance

    def execute(self) -> None:
        if self.__handler.is_taskbar_active:
            pyautogui.hotkey('right')
        else:
            pyautogui.hotkey('ctrl', 'tab')


class PrevTab(Action):

    def __init__(self, instance: Any):
        self.__handler = instance

    def execute(self) -> None:
        if self.__handler.is_taskbar_active:
            pyautogui.hotkey('left')
        else:
            pyautogui.hotkey('ctrl', 'shift', 'tab')


class OpenTaskBar(Action):

    def __init__(self, instance: Any):
        self.__handler = instance

    def execute(self) -> None:
        if self.__handler.is_taskbar_active:
            pyautogui.hotkey('enter')
        else:
            pyautogui.hotkey('win', 'tab')
        self.__handler.is_taskbar_active = not self.__handler.is_taskbar_active


class MoveMouse(Action):
    def __init__(self, instance: Any):
        self.__handler = instance

    def execute(self) -> None:
        w, h = pyautogui.size()
        x, y = self.__handler.current_data[8]
        y = min(max(y - 0.14, 0) / 0.33, 1)
        x = min(max(x - 0.17, 0) / 0.53, 1)
        pyautogui.moveTo(int((1 - x) * w), int(y * h))


class Click(Action):
    def __init__(self, instance: Any):
        pass

    def execute(self) -> None:
        pyautogui.click()

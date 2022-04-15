from abc import ABC, abstractmethod

import pyautogui as pyautogui


class Action(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass


class DoNothing(Action):

    def execute(self) -> None:
        pass


class NextTab(Action):

    def execute(self) -> None:
        pyautogui.hotkey('ctrl', 'tab')


class PrevTab(Action):

    def execute(self) -> None:
        pyautogui.hotkey('ctrl', 'shift', 'tab')

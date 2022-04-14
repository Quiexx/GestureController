import json
from abc import ABC, abstractmethod

import keyboard

from src.app.config import STATE_TRANS_PATH, ACTIONS_PATH


class State(ABC):

    @abstractmethod
    def next_state(self, value) -> 'State':
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def action(self, value) -> None:
        pass


def get_state(name: str) -> 'State':
    with open(STATE_TRANS_PATH, 'r') as f:
        state_dict = json.load(f)

    with open(ACTIONS_PATH, 'r') as f:
        actions_dict = json.load(f)

    trans = state_dict.get(name)
    if trans is None:
        raise ValueError("No such state name in {}: {}".format(STATE_TRANS_PATH, name))

    actions = actions_dict.get(name)
    if actions is None:
        raise ValueError("No such state name in {}: {}".format(ACTIONS_PATH, name))

    class NewState(State):

        def next_state(self, value) -> 'State':
            if value is None:
                return self
            return get_state(trans.get(str(value)))

        def get_name(self) -> str:
            return name

        def action(self, value) -> None:

            if value is None:
                return

            kb_action = actions.get(str(value))
            if kb_action:
                keyboard.press(kb_action)
                keyboard.release(kb_action)

    return NewState()

import json
from abc import ABC, abstractmethod
from typing import Any

from src.app.action import action
from src.app.config import STATE_TRANS_PATH, ACTIONS_PATH


class State(ABC):

    @abstractmethod
    def next_state(self, gest_num: int) -> 'State':
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def action(self, gest_num: int) -> None:
        pass


def get_state(name: str, instance: Any) -> 'State':
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

    class HandlerState(State):

        def next_state(self, gest_num: int) -> 'State':
            return get_state(trans.get(str(gest_num)), instance)

        def get_name(self) -> str:
            return name

        def action(self, gest_num: int) -> None:
            action_name = actions.get(str(gest_num))
            getattr(action, action_name)(instance).execute()

    return HandlerState()

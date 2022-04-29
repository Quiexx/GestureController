import json
from abc import ABC, abstractmethod
from typing import Any

from src.app.action import action
from src.app.config import STATE_TRANS_PATH, ACTIONS_PATH


class State(ABC):
    """
    State of gesture handler
    """

    @abstractmethod
    def next_state(self, gest_num: int) -> 'State':
        """
        Get next state
        :param gest_num: gesture index
        :return: new state
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get name of the state
        :return: name, str
        """
        pass

    @abstractmethod
    def action(self, gest_num: int) -> None:
        """
        Execute action
        :param gest_num: index of new gesture
        :return: None
        """
        pass


def get_state(name: str, instance: Any) -> 'State':
    """
    Function that creates states depending on json configurations for states and actions
    :param name: Name of the state you want to create
    :param instance: instance of gesture handler
    :return: new state
    """
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

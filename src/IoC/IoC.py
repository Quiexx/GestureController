from typing import Any

from src.model.Gesture.EmptyGesture import EmptyGesture


def ioc(key: str, *args, **kwargs) -> Any:
    if key == "Gesture.Get":
        return EmptyGesture("unknown")

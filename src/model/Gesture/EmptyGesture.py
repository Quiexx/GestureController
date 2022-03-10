from src.model.Gesture.IGesture import IGesture


class EmptyGesture(IGesture):

    def __init__(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name
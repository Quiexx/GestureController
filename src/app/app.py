from typing import Any

from kivy.app import App
from kivy.uix.actionbar import ActionBar, ActionButton, ActionView, ActionPrevious, ActionGroup
from kivy.uix.boxlayout import BoxLayout

from src.app.widgets.recognition_view import RecognitionView


class UI(BoxLayout):
    """
    Application UI class
    """

    def __init__(self, **kwargs):
        """
        Initialize user interface
        """
        super().__init__(**kwargs)

        # Main layout
        self.main_layout = BoxLayout(orientation='vertical')

        # Action bar
        self.bar = ActionBar(orientation='horizontal')
        aview = ActionView()

        ap = ActionPrevious(title='Gesture Controller', with_previous=False)
        aview.add_widget(ap)

        # Camera Control
        camera_group = ActionGroup(text="Camera")

        open_camera_button = ActionButton(text="Open")
        open_camera_button.bind(on_press=self.open_camera)
        close_camera_button = ActionButton(text="Close")
        close_camera_button.bind(on_press=self.close_camera)
        show_camera_button = ActionButton(text="Show camera")
        show_camera_button.bind(on_press=self.show_camera)
        change_camera_button = ActionButton(text="Change")
        change_camera_button.bind(on_press=self.change_camera)

        camera_group.add_widget(open_camera_button)
        camera_group.add_widget(close_camera_button)
        camera_group.add_widget(show_camera_button)
        camera_group.add_widget(change_camera_button)

        aview.add_widget(camera_group)

        # Hands
        hands_group = ActionGroup(text="Hands")
        show_hands_button = ActionButton(text="Show hands")
        show_hands_button.bind(on_press=self.show_hands)
        hands_group.add_widget(show_hands_button)
        aview.add_widget(hands_group)

        # Gesture control
        gesture_group = ActionGroup(text="Gesture control")
        show_gesture_button = ActionButton(text="Show gesture")
        show_gesture_button.bind(on_press=self.show_gesture)
        gesture_group.add_widget(show_gesture_button)
        aview.add_widget(gesture_group)

        self.cur_cam = 0
        self.camera = RecognitionView(index=self.cur_cam, play=True, height=800, show_hands=False)
        self.bar.add_widget(aview)
        self.main_layout.add_widget(self.bar)
        self.main_layout.add_widget(self.camera)
        self.add_widget(self.main_layout)

    def open_camera(self, obj: Any) -> None:
        """
        Turn current camera on
        :param obj: object from which the method was called
        :return: None
        """
        self.camera.change_camera(self.cur_cam)
        self.camera.play = True

    def show_camera(self, obj: Any) -> None:
        """
        Show / hide camera image
        :param obj: object from which the method was called
        :return: None
        """
        self.camera.show_cam = not self.camera.show_cam

    def close_camera(self, obj: Any) -> None:
        """
        Close current camera
        :param obj: object from which the method was called
        :return: None
        """
        self.camera.close_cam()
        self.camera.play = False

    def change_camera(self, obj: Any) -> None:
        """
        Switch to another camera
        :param obj: object from which the method was called
        :return: None
        """
        self.cur_cam = (self.cur_cam + 1) % 2
        self.camera.change_camera(self.cur_cam)

    def show_hands(self, obj: Any) -> None:
        """
        Show / hide hand landmarks
        :param obj: object from which the method was called
        :return: None
        """
        self.camera.show_hands = not self.camera.show_hands

    def show_gesture(self, obj: Any) -> None:
        """
        Show / hide recognized gesture
        :param obj: object from which the method was called
        :return: None
        """
        self.camera.show_gesture = not self.camera.show_gesture


class GestureController(App):
    """
    Main app class
    """

    def build(self):
        '''Initializes the application; it will be called only once.
        If this method returns a widget (tree), it will be used as the root
        widget and added to the window.

        :return:
            None or a root :class:`~kivy.uix.widget.Widget` instance
            if no self.root exists.'''
        return UI()


if __name__ == '__main__':
    GestureController().run()

from kivy.app import App
from kivy.uix.actionbar import ActionBar, ActionButton, ActionView, ActionPrevious, ActionGroup
from kivy.uix.boxlayout import BoxLayout

from src.app.widgets.recognition_view import RecognitionView


class UI(BoxLayout):
    def __init__(self, **kwargs):
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
        change_camera_button = ActionButton(text="Change")
        change_camera_button.bind(on_press=self.change_camera)

        camera_group.add_widget(open_camera_button)
        camera_group.add_widget(close_camera_button)
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
        self.camera = RecognitionView(index=self.cur_cam, play=False, height=800, show_hands=False)
        self.bar.add_widget(aview)
        self.main_layout.add_widget(self.bar)
        self.main_layout.add_widget(self.camera)
        self.add_widget(self.main_layout)

    def open_camera(self, obj):
        self.camera.change_camera(self.cur_cam)
        self.camera.play = True

    def close_camera(self, obj):
        self.camera.close_cam()
        self.camera.play = False

    def change_camera(self, obj):
        self.cur_cam = (self.cur_cam + 1) % 2
        self.camera.change_camera(self.cur_cam)

    def show_hands(self, obj):
        self.camera.show_hands = not self.camera.show_hands

    def show_gesture(self, obj):
        self.camera.show_gesture = not self.camera.show_gesture


class GestureController(App):
    def build(self):
        return UI()


if __name__ == '__main__':
    GestureController().run()

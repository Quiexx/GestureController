from typing import Any

import PIL
import numpy as np
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.core.camera import Camera as CoreCamera
from kivy.properties import NumericProperty, ListProperty, \
    BooleanProperty

from src.app.model.model_manager import GestureModelManager, ModelManager


class RecognitionView(Image):
    """
    Widget that uses camera and GestureModelManager to handle gestures and show camera images.
    """
    play = BooleanProperty(False)
    '''Boolean indicating whether the camera is playing or not.
    You can start/stop the camera by setting this property::

        # start the camera playing at creation
        cam = RecognitionView(play=True)

        # create the camera, and start later (default)
        cam = RecognitionView(play=False)
        # and later
        cam.play = True

    :attr:`play` is a :class:`~kivy.properties.BooleanProperty` and defaults to
    False.
    '''

    index = NumericProperty(-1)
    '''Index of the used camera, starting from 0.

    :attr:`index` is a :class:`~kivy.properties.NumericProperty` and defaults
    to -1 to allow auto selection.
    '''

    resolution = ListProperty([-1, -1])
    '''Preferred resolution to use when invoking the camera. If you are using
    [-1, -1], the resolution will be the default one::

        # create a camera object with the best image available
        cam = RecognitionView()

        # create a camera object with an image of 320x240 if possible
        cam = RecognitionView(resolution=(320, 240))

    .. warning::

        Depending on the implementation, the camera may not respect this
        property.

    :attr:`resolution` is a :class:`~kivy.properties.ListProperty` and defaults
    to [-1, -1].
    '''
    show_hands = BooleanProperty(False)
    """
    Boolean indicating whether hand landmarks are shown or not
    """
    show_gesture = BooleanProperty(False)
    """
    Boolean indicating whether recognized gesture is shown or not
    """
    show_cam = BooleanProperty(False)
    """
    Boolean indicating whether image from camera is shown or not
    """

    def __init__(self, **kwargs) -> None:
        self._camera = None
        super(RecognitionView, self).__init__(**kwargs)
        if self.index == -1:
            self.index = 0
        on_index = self._on_index
        fbind = self.fbind
        fbind('index', on_index)
        fbind('resolution', on_index)
        if self.play:
            on_index()

        self.model_manager: ModelManager = GestureModelManager()

    def on_tex(self, camera: Any) -> None:
        """
        Updates widget image
        :param camera: camera widget instance
        :return: None
        """
        texture = camera.texture
        size = texture.size
        pixels = texture.pixels
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size, data=pixels).convert('RGB')
        frame = np.array(pil_image)

        frame = self.model_manager.handle_image(frame)

        self.texture = Texture.create(texture.size, colorfmt='rgb')
        self.texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt="ubyte")

        self.texture_size = list(self.texture.size)
        self.canvas.ask_update()

    def _on_index(self, *largs) -> None:
        """
        Initialize camera
        :return: None
        """
        self._camera = None
        if self.index < 0:
            return
        if self.resolution[0] < 0 or self.resolution[1] < 0:
            self._camera = CoreCamera(index=self.index, stopped=True)
        else:
            self._camera = CoreCamera(index=self.index,
                                      resolution=self.resolution, stopped=True)
        if self.play:
            self._camera.start()

        self._camera.bind(on_texture=self.on_tex)

    def on_play(self, instance: Any, value: bool) -> None:
        """
        Turn camera ON or OFF
        :param instance: object from which method was called
        :param value: True to turn camera on, False to turn camera off
        :return: None
        """
        if not self._camera:
            return
        if value:
            self._camera.start()
        else:
            self._camera.stop()
            self._camera = None

    def close_cam(self) -> None:
        """
        Close camera
        :return: None
        """
        if not self._camera:
            return

        self._camera.stop()
        self._camera = None

    def change_camera(self, index: int) -> None:
        """
        Switch camera by camera index
        :param index: camera index to turn on
        :return: None
        """
        self.index = index
        self._on_index()

    def on_show_hands(self, instance: Any, value: bool) -> None:
        """
        Method is called when the show_hands property is changed
        :param instance: object from which method was called
        :param value: new value of show_hands property
        :return: None
        """
        self.model_manager.draw_hands = value

    def on_show_gesture(self, instance: Any, value: bool) -> None:
        """
        Method is called when the show_gesture property is changed
        :param instance: object from which method was called
        :param value: new value of show_gesture property
        :return: None
        """
        self.model_manager.draw_result = value

    def on_show_cam(self, instance: Any, value: bool) -> None:
        """
        Method is called when the show_cam property is changed
        :param instance: object from which method was called
        :param value: new value of show_cam property
        :return: None
        """
        self.model_manager.show_image = value

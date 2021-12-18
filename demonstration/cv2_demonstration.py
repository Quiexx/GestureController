import cv2

from src.model.HandTracker.AllMarksHandTracker import AllMarksHandTracker
from src.model.VideoStream.WebCamVideoStream import WebCamVideoStream
from demonstration.tools import draw_marks

stream = WebCamVideoStream(0)
hand_tracker = AllMarksHandTracker()

while stream.is_ready():
    img = stream.read()
    result = hand_tracker.find_hands(img)

    if not result:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.flip(img, 1)
        cv2.imshow("StreamTest", img)

        if cv2.waitKey(5) & 0xFF == 27:
            break
        continue

    img = draw_marks(img, result, pt_clr=(70, 130, 180), con_clr=(176, 196, 222))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.flip(img, 1)
    cv2.imshow("StreamTest", img)

    if cv2.waitKey(5) & 0xFF == 27:
        break

stream.close()

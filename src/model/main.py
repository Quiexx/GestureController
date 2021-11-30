import cv2

from src.model.HandTracker.SimpleHandTracker import SimpleHandTracker
from src.model.VideoStream.WebCamVideoStream import WebCamVideoStream

stream = WebCamVideoStream(0)
hand_tracker = SimpleHandTracker()

while stream.is_ready():
    img = stream.read()
    result = hand_tracker.find_hands(img)

    if not result:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow("StreamTest", img)
    else:
        x, y = result
        new_img = cv2.circle(img, (x, y), 7, (255, 0, 0), -1)
        new_img = cv2.cvtColor(new_img, cv2.COLOR_RGB2BGR)
        cv2.imshow("StreamTest", new_img)

    if cv2.waitKey(5) & 0xFF == 27:
        break

stream.close()
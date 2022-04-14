import os
# Gesture classifier

GESTURE_CLASSIFIER_LEARNED_MODEL = "WristGestureClassifierModel_v1.0.pth"
GESTURE_CLASSIFIER_DEVICE = "cpu"
GESTURE_CLASSIFIER_PATH = os.path.abspath(os.path.join("model/learned_models/", GESTURE_CLASSIFIER_LEARNED_MODEL))

# Mediapipe hands

MODEL_COMPLEXITY = 0
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# KB Gesture Handler

STATE_TRANS_PATH = os.path.abspath("kbh_state_trans.json")
ACTIONS_PATH = os.path.abspath("kbh_actions.json")
KBH_START_STATE = "DEFAULT"



import os
import json
from PIL import Image

# Gesture classifier

GESTURE_CLASSIFIER_LEARNED_MODEL = "gesture3D_BLRLS_cls9_acc966.pkl"
GESTURE_CLASSIFIER_DEVICE = "cpu"
GESTURE_CLASSIFIER_PATH = os.path.abspath(os.path.join("src/app/model/learned_models/", GESTURE_CLASSIFIER_LEARNED_MODEL))

# Mediapipe hands

MODEL_COMPLEXITY = 0
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Gesture Handler

STATE_TRANS_PATH = os.path.abspath("src/app/handler_config/kbm_state_trans.json")
ACTIONS_PATH = os.path.abspath("src/app/handler_config/kbm_actions.json")
START_STATE = "NEUTRAL"

# Gesture Manager
gesture_name_mapping = os.path.abspath("src/app/gesture_names_mapping.json")

with open(gesture_name_mapping, "r", encoding="utf8") as f:
    GESTURE_NAMES = {int(num): name for num, name in json.load(f).items()}


gesture_icons_mapping = os.path.abspath("src/app/gesture_icons_mapping.json")
gesture_icons_path = os.path.abspath("src/icons/gesture")

with open(gesture_icons_mapping, "r", encoding="utf8") as f:
    GESTURE_ICONS = {int(num): Image.open(os.path.join(gesture_icons_path, icon_file)).convert('RGB')
                     for num, icon_file in json.load(f).items()}

MIN_GESTURE_CONFIDENCE = 0.8



import cv2

connections = {
    0: [1, 5, 17],
    1: [2],
    2: [3],
    3: [4],
    5: [6, 9],
    6: [7],
    7: [8],
    9: [10, 13],
    10: [11],
    11: [12],
    13: [14, 17],
    14: [15],
    15: [16],
    17: [18],
    18: [19],
    19: [20],
}


def draw_marks(img, result, pt_clr=(0, 255, 255), con_clr=(224, 255, 255)):
    for mark in result:
        x, y = mark['x'], mark['y']
        img = cv2.circle(img, (x, y), 6, pt_clr, -1)

    for pt1, pts in connections.items():
        for pt2 in pts:
            img = cv2.line(img, (result[pt1]['x'], result[pt1]['y']), (result[pt2]['x'], result[pt2]['y']), con_clr)

    return img

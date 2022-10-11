import cv2
from cv2 import ( CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT,
                 CAP_PROP_FPS)

cap = cv2.VideoCapture(1)  # /dev/video0

size = (int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT)))
            # 帧率
fps = cap.get(CAP_PROP_FPS)
print("{},{}".format(size, fps))
cap.release()


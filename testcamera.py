import cv2

# 引入库
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("{},{}".format(size, fps))
    # 读取内容
    if cv2.waitKey(10) == ord("q"):
        break

# 随时准备按q退出
cap.release()
cv2.destroyAllWindows()
# 停止调用，关闭窗口
#!/usr/bin/env python
# coding:utf8
"""
@Time       :   2019/12/9
@Author     :   fls
@Contact    :   fls@darkripples.com
@Desc       :   海康威视网络摄像头

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/9 10:53   fls        1.0         create
"""
from os import path, makedirs
from cv2 import (VideoCapture, imencode, namedWindow, imshow, waitKey, destroyAllWindows, VideoWriter_fourcc,
                 VideoWriter, WINDOW_NORMAL, WINDOW_KEEPRATIO, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT,
                 CAP_PROP_FPS)
import cv2
from ez_utils import fmt_date, FMT_DATE, FMT_DATETIME
from tools.RingBuffer import RingBuffer
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
import threading
import copy
import gc

def consoleLog(*args):
    print(*args)


class HKCManage:
    def __init__(self, place, ip, port, user, pwd, logPre=">"):
        """
        主码流：
            rtsp://admin:12345@192.0.0.64:554/Streaming/Channels/1
        子码流：
            rtsp://admin:12345@192.0.0.64/Streaming/Channels/2
        :param place:
        :param ip:
        :param port:
        :param user:
        :param pwd:
        :param logPre:
        """
        self.logPre = logPre
        self.USB_URL=1  #usb3.0的任意一个口
        self.URL = f"rtsp://{user}:{pwd}@{ip}:{port}/Streaming/Channels/1"
        # 截图或视频保存位置
        img_dir = path.join(BASE_DIR, "logs", "camera_img", place, fmt_date(fmt=FMT_DATE))
        if not path.exists(img_dir):
            makedirs(img_dir)
        self.buff = RingBuffer()
        threading.Thread(target=self.videotape_buff).start()
        threading.Thread(target=self.take_picture).start()
        threading.Thread(target=self.videotape_save).start()
        # 截图保存文件名
        self.img_path = path.join(img_dir, "{now}" + ".jpg")
        # 视频保存文件名
        self.video_path = path.join(img_dir, "{now}" + ".avi")

    def take_picture(self):
        """
        截图一帧
        :param carNo:
        :param show_view:
        :return:
        """
        try:
            # 打开rtsp
            cap = VideoCapture(self.USB_URL)
            consoleLog(self.logPre, "start take picture thread")
            size = (int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT)))
            # 帧率
            fps = cap.get(CAP_PROP_FPS)
            print("{},{}".format(size, fps))
            while True:
                ret, frame = cap.read()
                if self.buff.take_picture == True:
                    img_name = self.img_path.format(now=fmt_date(fmt=FMT_DATETIME))
                    consoleLog(self.logPre, "start take picture {}".format(img_name))
                    if not ret:
                        consoleLog(self.logPre, "no frame")
                    imencode('.jpg', frame)[1].tofile(img_name)
                    consoleLog(self.logPre, "save image finish")
                    self.buff.take_picture = False
        except Exception as e:
            consoleLog(self.logPre, "save picture exception:", repr(e))
        finally:
            if cap:
                cap.release()
            destroyAllWindows()

    def videotape_buff(self):
        """
        录像
        :param carNo:
        :param show_view:
        :return:
        """
        try:
            # 打开rtsp
            consoleLog(self.logPre, "start record")
            cap = VideoCapture(self.URL)
            ret, frame = cap.read()
            size = (int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT)))
            # 帧率
            fps = cap.get(CAP_PROP_FPS)
            print("{},{}".format(size,fps))
            while ret:
                ret, frame = cap.read()
                self.buff.append(frame)
            else:
                consoleLog(self.logPre, "no frame")
        except Exception as e:
            consoleLog(self.logPre, "record video exception:", repr(e))
        finally:
            if cap:
                cap.release()
            destroyAllWindows()

    def videotape_save(self):
        """
        录像
        :param carNo:
        :param show_view:
        :return:
        """
        try:
            while True:
                if self.buff.save_video ==True:
                    self.buff.save_video = False
                    # 打开rtsp
                    # 视频分辨率
                    size = (1920, 1080)
                    fourcc = VideoWriter_fourcc(*'XVID')
                    # 视频保存obj
                    frames = copy.deepcopy(self.buff.get())
                    video_name = self.video_path.format(now=fmt_date(fmt=FMT_DATETIME))
                    consoleLog(self.logPre, "save video:{}".format(video_name))
                    outfile = VideoWriter(video_name, fourcc, 25, size)
                    for frame in frames:
                        outfile.write(frame)
                    consoleLog(self.logPre, "save video finish")
                    del frames
                    gc.collect()

        except Exception as e:
            consoleLog(self.logPre, "save video exception:", repr(e))
        finally:
            if outfile:
                outfile.release()

    def show(self):
        """
        预览
        :return:
        """
        namedWindow('view', WINDOW_NORMAL | WINDOW_KEEPRATIO)
        # 打开rtsp
        cap = VideoCapture(1,cv2.CAP_DSHOW)
        # 视频分辨率
        size = (int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT)))
        # 帧率
        fps = cap.get(CAP_PROP_FPS)
        print(size)
        print(fps)
        ret, frame = cap.read()
        while ret:
            ret, frame = cap.read()
            imshow("view", frame)
            if waitKey(1) & 0xFF == ord('q'):
                break
        else:
            consoleLog("未读取到视频")
        cap.release()



if __name__ == '__main__':
    pass

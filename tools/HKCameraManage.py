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
import copy
import threading

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
        self.USB_URL=1
        self.URL = f"rtsp://{user}:{pwd}@{ip}:{port}/Streaming/Channels/1"
        # 截图或视频保存位置
        img_dir = path.join(BASE_DIR, "logs", "camera_img", place, fmt_date(fmt=FMT_DATE))
        if not path.exists(img_dir):
            makedirs(img_dir)
        self.buff = RingBuffer()
        threading.Thread(target=self.videotape_buff).start()
        # 截图保存文件名
        self.img_path = path.join(img_dir, "{now}" + ".jpg")
        # 视频保存文件名
        self.video_path = path.join(img_dir, "{now}" + ".mp4")

    def take_picture(self):
        """
        截图一帧
        :param carNo:
        :param show_view:
        :return:
        """
        try:
            # 打开rtsp
            cap = VideoCapture(self.USB_URL,cv2.CAP_DSHOW)
            ret, frame = cap.read()
            img_name= self.img_path.format( now=fmt_date(fmt=FMT_DATETIME))
            consoleLog(self.logPre, "开始拍照")
            size = (int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT)))
            # 帧率
            fps = cap.get(CAP_PROP_FPS)
            print("{},{}".format(size, fps))
            if not ret:
                consoleLog(self.logPre, "未捕获到帧")

            imencode('.jpg', frame)[1].tofile(img_name)
        except Exception as e:
            consoleLog(self.logPre, "保存截图异常:", repr(e))
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
            consoleLog(self.logPre, "开始录制")
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
                consoleLog(self.logPre, "未捕获到帧")
        except Exception as e:
            consoleLog(self.logPre, "视频录制异常:", repr(e))
        finally:
            if cap:
                cap.release()
            destroyAllWindows()

    def videotape_save(self ):
        """
        录像
        :param carNo:
        :param show_view:
        :return:
        """
        try:
            # 打开rtsp
            # 视频分辨率
            size = (1920, 1080)
            fourcc = VideoWriter_fourcc('m', 'p', '4', 'v')
            # 视频保存obj
            frames = copy.deepcopy(self.buff.get())
            video_name = self.video_path.format(now=fmt_date(fmt=FMT_DATETIME))
            consoleLog(self.logPre, "保存视频:{}".format(video_name))
            outfile = VideoWriter(video_name,fourcc, 25, size)
            for frame in frames:
                outfile.write(frame)

        except Exception as e:
            consoleLog(self.logPre, "视频录制异常:", repr(e))
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

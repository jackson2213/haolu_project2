import time
from os import path
from ez_utils import read_conf
from tools.HKCameraManage import HKCManage
from tools.RingBuffer import RingBuffer

BASE_DIR = path.dirname(path.abspath(__file__))



if __name__ == "__main__":
    confObj = read_conf(path.join(BASE_DIR, "conf", "conf.ini"))
    confHK = confObj["HIKVISION_" + "01"]
    f = HKCManage(confHK.place, confHK.ip, eval(confHK.port), confHK.user, confHK.pwd)
    time.sleep(10)
    f.videotape_save()
    f.take_picture()
    time.sleep(1000)
    exit()



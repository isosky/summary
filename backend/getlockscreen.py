import os
import hashlib
from PIL import Image

dir = "C://Users//fengy//AppData//Local//Packages//Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy//LocalState//Assets"
dir_h = "f://lockscreen_h"
dir_w = "f://lockscreen_w"


def checkdir():

    if not os.path.exists(dir_h):
        os.mkdir(dir_h)

    if not os.path.exists(dir_w):
        os.mkdir(dir_w)


def initmd5s():
    md5s = []
    for root, dirs, files in os.walk(dir_h, topdown=False):
        for name in files:
            with open(os.path.join(root, name), 'rb') as f:
                md5hash = hashlib.md5(f.read())
                md5 = md5hash.hexdigest()
                md5s.append(md5)

    for root, dirs, files in os.walk(dir_w, topdown=False):
        for name in files:
            with open(os.path.join(root, name), 'rb') as f:
                md5hash = hashlib.md5(f.read())
                md5 = md5hash.hexdigest()
                md5s.append(md5)

    return md5s


def getlocksreen():
    checkdir()
    md5s = initmd5s()
    # print(md5s)
    temp = 0
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            with open(os.path.join(root, name), 'rb') as f:
                md5hash = hashlib.md5(f.read())
                md5 = md5hash.hexdigest()
                # print(md5)
                if md5 not in md5s:
                    image = Image.open(os.path.join(root, name))
                    if image.width == 1080:
                        # print(os.path.join(dir_h,name+'.jpg'))
                        image.save(os.path.join(dir_h, name+'.jpg'))
                    elif image.width == 1920:
                        image.save(os.path.join(dir_w, name+'.jpg'))
                    temp += 1
    print("新增了"+str(temp)+"张图片")

# print('s')


if __name__ == "__main__":
    # checkdir()
    getlocksreen()

import os
import cv2
from PIL import Image
from matplotlib import pyplot as plt
import shutil
import time
from getpath import get_abs_path


class ImageOperation:
    def __init__(self):
        self.root_path = get_abs_path()

    def save_screen_img(self, d, picture_name, device_name, *sizes):
        """
        保存手机截图并返回文件路径,不要有中文，会影响断言
        :return:
        """
        base_path = os.path.join(self.root_path, f"statics\\screenshot\\{device_name}")
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        image_path = os.path.join(base_path, f'{str(int(time.time()))}_{str(device_name)}_{picture_name}.jpg')
        im = d.screenshot()
        if sizes:
            im = im.resize(sizes[0])
        im.save(image_path)
        return image_path

    def save_compare_img(self, image1, image2, device_name, is_show=False):
        """
        保存对比图用以展示
        :return:
        """
        base_path = os.path.join(self.root_path, "statics", "compare_image", f"{device_name}")

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        image_path = os.path.join(base_path, f'{str(int(time.time()))}_{str(device_name)}.jpg')
        img1 = cv2.imread(image1)
        img2 = cv2.imread(image2)

        plt.subplot(121)
        plt.imshow(Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)))
        plt.subplot(122)
        plt.imshow(Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)))
        plt.savefig(image_path)
        if is_show:
            plt.show()
        return image_path

    def remove_empty_key(self, info):
        """
        去除为空项，用于mysql数据插入
        :param info:
        :return:
        """
        if isinstance(info, dict):
            info_re = dict()
            for key, value in info.items():
                if isinstance(value, dict) or isinstance(value, list):
                    re = self.remove_empty_key(value)
                    if len(re):
                        info_re[key] = re
                elif value not in ['', {}, [], 'null', None]:
                    info_re[key] = value
            return info_re
        elif isinstance(info, list):
            info_re = list()
            for value in info:
                if isinstance(value, dict) or isinstance(value, list):
                    re = self.remove_empty_key(value)
                    if len(re):
                        info_re.append(re)
                elif value not in ['', {}, [], 'null', None]:
                    info_re.append(value)
            return info_re
        else:
            print('输入非列表/字典')

    @staticmethod
    def copy3(src, dst):
        try:
            names = os.walk(src)
            for root, dirs, files in names:
                for i in files:
                    src_name = os.path.join(root, i)
                    dir_str = root.replace(src, '')
                    dir_name = dst + dir_str
                    if os.path.exists(dir_name):
                        pass
                    else:
                        os.makedirs(dir_name)
                    dir_f_name = os.path.join(dir_name, i)
                    shutil.copy2(src_name, dir_f_name)

        except Exception as e:
            return e
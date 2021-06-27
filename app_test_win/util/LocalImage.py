# 图片相似度计算(校验时图片路径不能有中文)

import cv2
import numpy as np
from PIL import Image
import matplotlib
from matplotlib import pyplot as plt


matplotlib.use('TkAgg')


class LocalImages:
    """
        方式：
        1. 直方图
        2. 图像指纹(将图像按照一定的哈希算法，经过运算后得出的一组二进制数字) ,汉明距离(一组二进制数据变成另一组数据所需的步骤数，显然，
        这个数值可以衡量两张图片的差异，汉明距离越小，则代表相似度越高 ,汉明距离为0，即代表两张图片完全一样。)
            以下三种哈希算法计算得出汉明距离：
                -- 平均哈希法(aHash): 比较灰度图每个像素与平均值来实现
                -- 感知哈希算法(pHash): 采用的是DCT（离散余弦变换）来降低频率的方法
                -- dHash算法: 基于渐变实现

        3. 余弦相似度(cosin)
        4. 图片SSIM(结构相似度量)
        https://zhuanlan.zhihu.com/p/68215900
    """

    @staticmethod
    def calculate(pre_img, rear_img):
        # 计算单通道的直方图的相似值
        hist1 = cv2.calcHist([pre_img], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([rear_img], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree

    def classify_hist_with_split(self, pre_img, rear_img, size=(256, 256)):
        """
            直方图算法: 计算图片直方图的重合程度
            缺点：按照颜色的全局分布来计算，无法描述颜色的局部分布和色彩所处的位置
            适用于：速度较快，比较有着极高相似度的图片
            :return:
        """
        # 将图像resize后，R,G,B分离为三个通道(可查询RGB图像之灰度级和通道)，再计算每个通道的相似值
        sub_image1 = cv2.split(cv2.resize(pre_img, size))
        sub_image2 = cv2.split(cv2.resize(rear_img, size))
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += self.calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data

    @staticmethod
    def aHash(img):
        """
        均值哈希算法, 基于比较灰度图每个像素与平均值来实现
        速度比较快，但是常常不太精确,适合缩略图搜索
        如果对图像进行伽马校正或者进行直方图均值化都会影响均值，从而影响哈希值的计算
        """
        # 缩放为8*8
        img = cv2.resize(img, (8, 8))
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # s为像素和初值为0，hash_str为hash值初值为''
        s = 0
        hash_str = ''
        # 遍历累加求像素和
        for i in range(8):
            for j in range(8):
                s = s + gray[i, j]
        # 求平均灰度
        avg = s / 64
        # 灰度大于平均值为1相反为0生成图片的hash值
        for i in range(8):
            for j in range(8):
                if gray[i, j] > avg:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    @staticmethod
    def dHash(img):
        """
        相比pHash，dHash的速度要快的多，相比aHash，dHash在效率几乎相同的情况下的效果要更好，它是基于渐变实现的。
        """
        # 差值哈希算法
        # 缩放8*8
        img = cv2.resize(img, (9, 8))
        # 转换灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hash_str = ''
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    @staticmethod
    def pHash(img):
        """
         离散余弦变换（DCT）是种图像压缩算法，它将图像从像素域变换到频率域。然后一般图像都存在很多冗余和相关性的，所以转换到频率域之后，
         只有很少的一部分频率分量的系数才不为0，大部分系数都为0（或者说接近于0）
        """
        # 感知哈希算法
        hash_len = 32
        # 转换为灰度图
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # 缩放32*32
        resize_gray_img = cv2.resize(gray_img, (hash_len, hash_len), cv2.INTER_AREA)
        # 将灰度图转为浮点型
        h, w = resize_gray_img.shape[:2]
        vis0 = np.zeros((h, w), np.float32)
        vis0[:h, :w] = resize_gray_img

        # 离散余弦变换
        vis1 = cv2.dct(cv2.dct(vis0))
        vis1.resize(hash_len, hash_len)
        img_list = vis1.flatten()
        # 计算均值
        avg = sum(img_list) * 1. / len(img_list)
        avg_list = []
        for i in img_list:
            if i < avg:
                tmp = '0'
            else:
                tmp = '1'
            avg_list.append(tmp)

        p_hash_str = ''
        for x in range(0, hash_len * hash_len, 4):
            p_hash_str += '%x' % int(''.join(avg_list[x:x + 4]), 2)
        return p_hash_str

    @staticmethod
    def ham_dist(x, y):
        """
        Get the hamming distance of two values.
            hamming distance(汉明距)
        :param x:
        :param y:
        :return: the hamming distance
        """
        assert len(x) == len(y)
        return sum([ch1 != ch2 for ch1, ch2 in zip(x, y)])

    @staticmethod
    def cmpHash(hash1, hash2):
        """
         Hamming distance = 0  -> particular like
         Hamming distance < 5  -> very like
         hamming distance > 10 -> different picture
        """
        # Hash值对比
        # 算法中1和0顺序组合起来的即是图片的指纹hash。顺序不固定，但是比较的时候必须是相同的顺序。
        # 对比两幅图的指纹，计算汉明距离，即两个64位的hash值有多少是不一样的，不同的位数越小，图片越相似
        # 汉明距离：一组二进制数据变成另一组数据所需要的步骤，可以衡量两图的差异，汉明距离越小，则相似度越高。汉明距离为0，即两张图片完全一样
        n = 0
        # hash长度不同则返回-1代表传参出错
        if len(hash1) != len(hash2):
            return -1
        # 遍历判断
        for i in range(len(hash1)):
            # 不相等则n计数+1，n最终为相似度
            if hash1[i] != hash2[i]:
                n = n + 1
        return n

    def runAllSimilarFun(self, pre_img, rear_img):
        # 均值、差值、感知哈希算法三种算法值越小，则越相似,相同图片值为0
        # 三直方图算法和单通道的直方图 0-1之间，值越大，越相似。 相同图片为1
        pre_img = cv2.imread(pre_img)
        rear_img = cv2.imread(rear_img)
        keys = ['aHash', 'dHash', 'pHash', 'classify_hist_with_split', 'calculate']
        result = []
        n1 = self.cmpHash(self.aHash(pre_img), self.aHash(rear_img))
        # print('均值哈希算法相似度aHash：', n1)
        result.append(n1)

        n2 = self.cmpHash(self.dHash(pre_img), self.dHash(rear_img))
        # print('差值哈希算法相似度dHash：', n2)
        result.append(n2)

        n3 = self.ham_dist(self.pHash(pre_img), self.pHash(rear_img))
        # print('感知哈希算法相似度pHash：', n3)
        result.append(n3)

        n4 = self.classify_hist_with_split(pre_img, rear_img)
        if isinstance(n4, np.ndarray):
            n4 = n4.tolist()[0]

        # print('三直方图算法相似度：', n4)
        result.append(n4)

        n5 = self.calculate(pre_img, rear_img)
        if isinstance(n5, np.ndarray):
            n5 = n5.tolist()[0]
        # print("单通道的直方图", n5)
        result.append(n5)

        res = dict(zip(keys, result))

        return res

    def ssim(self):
        """
        SSIM是一种全参考的图像质量评价指标，分别从亮度、对比度、结构三个方面度量图像相似性。
        没搞定
        """
        pass


if __name__ == '__main__':
    image1 = r"D:\work\code\project_test\ebuy_app\statics\screenshot\28b05a0b\1604470479_28b05a0b_my_found_page.jpg"
    image2 = r"D:\work\code\project_test\ebuy_app\statics\screenshot\28b05a0b\1604470483_28b05a0b_applet_page.jpg"
    image_path = r"/statics/screenshot/28b05a0b/111111111111.jpg"
    a = ImagesLocal()
    # print(a.get_token())
    # print(a.baidu_save_image())
    # print(a.baidu_query_image())
    # print(a.classify_hist_with_split(ex_image, act_img))
    # img1 = cv2.imread(image2)
    # img2 = cv2.imread(image2)
    # b = a.pHash(img1)
    # c = a.pHash(img2)
    # print(a.ham_dist(b, c))
    print(a.runAllSimilarFun(image1, image2, image_path, True))
    # a.ssim(image1, image2)



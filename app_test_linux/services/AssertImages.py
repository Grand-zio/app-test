import re
from util.Log import Logger
from util.ImageOperation import ImageOperation
from services.ImageRecognition import ImageRecognition


class AssertImages:
    def __init__(self):
        self.log = Logger().logger

    def assert_images(self, devices, exc_img, act_img, comment):
        """
        断言：
            1.预期图片&实际图片
            2.分词识别正确
        """

        # 校验ocr
        img_str = ImageRecognition().imgOCR(act_img)['words_result']
        self.log.info(f'ocr光学文字识别结果：{img_str}')

        count = 0
        for i in comment:
            res = re.search(i, str(img_str))
            if res:
                count += 1
        if count == len(comment):
            ocr_result = True
        else:
            ocr_result = False

        img_similar = ImageRecognition().imgSimilar(exc_img, act_img)
        self.log.info(f'图像相似度结果: {img_similar}')

        image_path = ImageOperation().save_compare_img(exc_img, act_img, devices)

        mes = {
            'ocr_result': ocr_result,
            'ocr_description': img_str,
            'compare_img_path': image_path,
            'similar_data': img_similar
        }
        return mes


if __name__ == '__main__':
    a = AssertImages()
    path1 = r"D:\work\code\project_test\ebuy_app\statics\exce_img\e_buy_home_online.jpg"
    path2 = r"D:\work\code\project_test\ebuy_app\statics\exce_img\e_buy_home_offline.jpg"
    comments = ["微信", "扫一扫", "摇一摇", "搜一搜"]
    # print(a.assert_images(img1, img2, comment))
    print(a.assert_images("c2a1596b", path1, path2, comments))

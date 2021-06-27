import matplotlib
from util.OCR import OCR
from util.BDImageSimilar import Images
from util.LocalImage import LocalImages
matplotlib.use('TkAgg')


class ImageRecognition:
    """
    1. 返回ocr结果
        -- 百度文字识别接口，一天一万次免费（测试已足够）
        -- python 自带第三方库，需另外做训练
    2. 返回图片相似度匹配结果
        -- 百度图像相似度检索接口（存图--检索--清理），存取免费一天一万次，识别一天500次上限
        -- 图像相似度识别算法
            - 1. 直方图
            - 2. 图像指纹（平均哈希法(aHash)，感知哈希算法(pHash)，差异哈希算法（phash））
        -- 余弦相似度(cosin)（未使用）
        -- 图片SSIM(结构相似度量)（未使用）
    https://cloud.tencent.com/developer/news/193546
    """

    @staticmethod
    def imgOCR(img_path):
        """
        免费10000次
        先调用百度，次数消耗完成后使用python库
        :return:
        """
        result = OCR().baidu_ocr(img_path)

        words_result = result['words_result']
        if not words_result:
            result = OCR().python_ocr(img_path)
        return result

    @staticmethod
    def imgSimilar(pre_img, rear_img, platform='baidu'):
        """
        检索相似每天五百次
        """
        result = {}

        if platform == 'baidu':
            baidu_api = Images(pre_img, rear_img)
            # 存img1
            res_add = baidu_api.baidu_save_image()
            cont_sign = res_add.get('cont_sign')
            # 根据img2，检索所有img
            res = baidu_api.baidu_query_image()
            image_list = res.get('result')
            if image_list:
                score = []
                for i in image_list:
                    if i.get('cont_sign') == cont_sign:
                        score.append(i.get('score'))
                result.update({'platform': 'baidu', 'result': score[0]})
            else:
                result.update({'platform': 'baidu', 'result': None})

            # 删除百度相似图库 img1
            baidu_api.baidu_delete_image()

        # 相关算法
        res = LocalImages().runAllSimilarFun(pre_img, rear_img)
        result.update({'default': res})
        return result


if __name__ == '__main__':
    a = ImageRecognition()
    path1 = r"D:\work\code\project_test\ebuy_app\statics\exce_img\e_buy_home_online.jpg"
    path2 = r"D:\work\code\project_test\ebuy_app\statics\exce_img\e_buy_home_offline.jpg"
    path3 = r"D:\work\code\project_test\ebuy_app\statics\compare_image\1.jpg"
    print(a.imgOCR(path1))
    print(a.imgSimilar(path1, path2, path3))






























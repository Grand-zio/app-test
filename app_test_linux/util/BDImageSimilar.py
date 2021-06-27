import requests
from config.config import ReadConfig
import base64
# 图片相似度计算
# from skimage.measure import compare_ssim


class Images:
    """
    image similar
    baidu
    """
    def __init__(self, exec_img, actual_img):
        self.exec_img = exec_img
        self.act_img = actual_img
        self.APP_ID = ReadConfig().getImgAppId()
        self.API_KEY = ReadConfig().getImgApiKey()[0]
        self.SECRET_KEY = ReadConfig().getImgSecretKey()[0]

    def get_token(self):
        try:
            # client_id 为官网获取的AK， client_secret 为官网获取的SK
            host = f'https://aip.baidubce.com/oauth/2.0/token?' \
                   f'grant_type=client_credentials&client_id={self.API_KEY}&client_secret={self.SECRET_KEY}'
            response = requests.get(host)
            if response:
                res = response.json()
                token = res.get('access_token')
                return token

        except Exception as e:
            return e

    def baidu_save_image(self):
        """
        相似图片搜索—入库, 保存预期图片，10000次/天免费
        """
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/add"
        # 二进制方式打开图片文件
        img_name = self.exec_img.split('\\')[-1]
        f = open(self.exec_img, 'rb')
        img = base64.b64encode(f.read())

        comment = "{'name': %s, 'comment': '预期结果'}" % img_name
        params = {"brief": comment, "image": img, "tags": "1,1"}

        access_token = self.get_token()
        request_url = request_url + "?access_token=" + access_token

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            mes = response.json()
            return mes

    def baidu_query_image(self):
        """
        相似图片搜索—检索, 一天五百次免费
        """
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/search"
        # 二进制方式打开图片文件
        f = open(self.act_img, 'rb')
        img = base64.b64encode(f.read())

        params = {"image": img}
        access_token = self.get_token()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            mes = response.json()
            return mes

    def baidu_delete_image(self):
        """
        相似图片搜索—删除样本，不限次, 延时四小时生效
        """
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/delete"
        # 二进制方式打开图片文件
        f = open(self.exec_img, 'rb')
        img = base64.b64encode(f.read())

        params = {"image": img}
        access_token = self.get_token()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            mes = response.json()
            return mes


if __name__ == '__main__':
    a = r"D:\work\code\project_test\ebuy_app\statics\exce_img\e_buy_home_offline.jpg"
    b = r"D:\work\code\project_test\ebuy_app\statics\screenshot\28b05a0b\1604473447_28b05a0b_my_found_page.jpg"
    c = Images(a, b)
    print(c.get_token())
    # print(c.baidu_save_image())
    print(c.baidu_query_image())

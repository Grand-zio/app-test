from aip import AipOcr
from config.config import ReadConfig
from util.FileOperation import Files
from PIL import Image
import pytesseract  # 另需安装官方程序tesseract


class OCR:
    def __init__(self):
        self.APP_ID = ReadConfig().getOCRAppId()[0]
        self.API_KEY = ReadConfig().getOCRApiKey()[0]
        self.SECRET_KEY = ReadConfig().getOCRSecretKey()[0]
        self.tesseract = ReadConfig().getTesseract()[0]

    def baidu_ocr(self, img_path):
        """
        百度api ocr光学文字识别，一天五万次
        错误参数：https://ai.baidu.com/ai-doc/OCR/4k3h7yeze
        """
        try:
            client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
            image = Files().read(img_path)
        except Exception:
            raise
        return client.basicGeneral(image)

    def python_ocr(self, img_path):
        """
        Tesseract只能识别标准的ASCII字符串,开源识别率较差,不过有官方提供的训练工具
        :return:
        """
        try:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract
            image = Image.open(img_path)
            text = pytesseract.image_to_string(image)
        except Exception:
            raise
        return text


if __name__ == '__main__':
    path = r"/statics/screenshot/28b05a0b/1604470483_28b05a0b_applet_page.jpg"
    a = OCR()
    print(a.baidu_ocr(path))

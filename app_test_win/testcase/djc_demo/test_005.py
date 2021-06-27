import sys, os
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
import allure
import time
from util.Log import Logger
from config import AllureReport
from util.ImageOperation import ImageOperation
import uiautomator2 as u2
from services.AssertImages import AssertImages

log = Logger().logger
as_i = AssertImages()
img = ImageOperation()


class TestAppLets:

    @allure.feature('UI测试demo')
    @allure.title("打开微信，进入小程序首页，断言成功")
    @allure.severity('blocker')
    @allure.description("打开微信，登录小程序，进入小熊麦麦首页")
    def test_into_home_000(self, device_name):
        d = u2.connect(device_name)
        log.info(d)
        try:
            e_buy_home_img_except = "D:\\work\\code\\project_test\\ebuy_app\\statics\\exce_img\\e_buy_home_offline.jpg"

            d.implicitly_wait(15.0)

            screen_status = d.info.get('screenOn')
            if not screen_status:
                d.screen_on()
                d.swipe_ext("up", 0.6)
                time.sleep(3)

            d.press("home")
            d.press("home")
            d.press("home")
            time.sleep(1)

            d(description="第2屏").click()
            d(resourceId="com.miui.home:id/icon_icon", description="微信").click()

            # d.app_start("com.tencent.mm", wait=True)
            time.sleep(3)

            # 判断是否在微信首页-发现页
            found_icon = d(resourceId="com.tencent.mm:id/dub", text="发现")
            if not found_icon.exists:
                # d(resourceId="com.tencent.mm:id/dn", description="返回").click()
                d.press("back")
            found_icon.click(timeout=10)
            time.sleep(3)
            my_found_pic = img.save_screen_img(d, 'my_found_page', device_name)  # 发现页截图

            # 进入小程序
            applet_icon = d(resourceId="android:id/title", text="小程序")
            applet_icon.click()
            time.sleep(3)
            applets_pic = img.save_screen_img(d, 'applet_page', device_name)  # 小程序页截图

            d.xpath('//androidx.appcompat.widget.LinearLayoutCompat').click()
            time.sleep(1)
            d.send_keys("云品智能", clear=True)
            time.sleep(1)

            d.click(0.222, 0.193)
            time.sleep(5)
            shou_ye = img.save_screen_img(d, 'shou_ye', device_name)

            time.sleep(15)

            d.press("home")
            d.app_stop("com.tencent.mm")

            comment = ['e Buy Life', 'For your better life!', '精选商品']
            result = as_i.assert_images(device_name, e_buy_home_img_except, shou_ye, comment)
            log.info(3)
            # ocr 结果
            ocr_result = result.get('ocr_result')
            ocr_description = str(result.get('ocr_description'))

            # 图片对比
            compare_img = result.get('compare_img_path')

            similar_description = str(result.get('similar_data'))
            pHash = result.get('similar_data').get('pHash')
            aHash = result.get('similar_data').get('aHash')
            third_res = result.get('similar_data').get('third_res')
            log.info(4)
            if ocr_result:
                if pHash < 25 and aHash < 10:
                    if third_res and third_res > 0.95:
                        is_similar = True
                    else:
                        is_similar = True
                else:
                    is_similar = False
            else:
                is_similar = False
            log.info(5)
            # 截图
            AllureReport.show_step('手机型号', device_name)
            AllureReport.show_pic(e_buy_home_img_except, '预期-首页截图')
            AllureReport.show_pic(my_found_pic, '发现页截图')
            AllureReport.show_pic(applets_pic, '小程序页截图')
            AllureReport.show_pic(shou_ye, '实际-首页截图')
            AllureReport.show_pic(compare_img, '预期-实际比对效果')

            AllureReport.show_step('ocr光学文字识别', ocr_description)
            AllureReport.show_step('图像相似度计算结果', similar_description)

        except Exception as e:
            log.error(e)
            AllureReport.show_pic(img.save_screen_img(d, 'img_error', device_name), '报错截图')
            assert 1 == 2
            # if self.clear == 'on':
            #     coupons.clear_data(mes_response)

        else:
            assert is_similar





























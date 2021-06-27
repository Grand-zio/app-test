from multiprocessing import Pool
import pytest
from util.Log import Logger
from services.DeviceManger import DeviceManger
from services import FindCase
import os
import shutil
import time
import sys
import getopt
from services.ConfigEmail import SendEmail
from util.FileOperation import Files
from config.config import ReadConfig

time_limit = 5  # set timeout time 5s
log = Logger().logger
dm = DeviceManger()
read = ReadConfig()


def getCaseName():
    case_name = None
    try:
        args = sys.argv[1:]
        opts, args = getopt.getopt(args, "-n:", ["case_name="])

    except getopt.GetoptError:
        print('python test.py -n <case_name>/--case_name=<case_name>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-n", "--case_name"):
            case_name = arg

    n = len(sys.argv)  # 参数个数

    all_test_case = FindCase.findTestCases(case_name)
    return all_test_case


def files(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def main():
    # 清除历史报告
    abs_path = os.path.split(os.path.realpath(__file__))[0]
    xml_path = os.path.join(abs_path, 'reports', 'xml')
    html_path = os.path.join(abs_path, 'reports', 'html')
    html_zip_path = os.path.join(abs_path, 'reports', 'zipfiles')
    show_html_path = os.path.join(abs_path, 'reports', 'show_html')

    files(xml_path)
    files(html_path)
    files(html_zip_path)
    files(show_html_path)

    try:
        all_test_case = getCaseName()
        p = Pool()
        xml_report_list = []
        html_report_list = []
        show_report_list = []

        # 获取可用设备list
        devices = DeviceManger().checkDevices()

        if devices:
            method = devices["device_info"]["method"]
            device_list = devices["device_info"]["devices"]
            if method.lower() == "server":
                remote_id = devices["device_info"]["remote_id"]
                for i in range(len(device_list)):
                    dm.bindDevice(device_list[i], 3600)
                    xml_report = os.path.join(xml_path, device_list[i])
                    html_report = os.path.join(html_path, device_list[i])
                    show_report = os.path.join(show_html_path, f"{device_list[i]}.html")
                    files(xml_report)
                    files(html_report)
                    xml_report_list.append(xml_report)
                    html_report_list.append(html_report)
                    show_report_list.append(show_report)

                    for case_path in all_test_case:
                        cmd_string = case_path + '|--html={}|--self-contained-html|--reruns=1|' \
                                                 '--reruns-delay=1|--device={}|--alluredir={}' \
                                     .format(show_report, remote_id[i], xml_report)
                        cmd_list = cmd_string.split('|')
                        p.apply_async(pytest.main, args=(cmd_list,))
            else:
                for i in range(len(device_list)):
                    dm.bindDevice(device_list[i], 3600)
                    xml_report = os.path.join(xml_path, device_list[i])
                    html_report = os.path.join(html_path, device_list[i])
                    show_report = os.path.join(show_html_path, f"{device_list[i]}.html")
                    files(xml_report)
                    files(html_report)
                    xml_report_list.append(xml_report)
                    html_report_list.append(html_report)
                    show_report_list.append(show_report)

                    for case_path in all_test_case:
                        cmd_string = case_path + '|--html={}|--self-contained-html|--reruns=1|' \
                                                 '--reruns-delay=1|--device={}|--alluredir={}' \
                            .format(show_report, device_list[i], xml_report)
                        cmd_list = cmd_string.split('|')
                        p.apply_async(pytest.main, args=(cmd_list,))

            p.close()
            p.join()

    except Exception as e:
        return e

    else:
        log.info("-----用例执行完成------")
        for i in range(len(xml_report_list)):
            cmd = f"allure generate {xml_report_list[i]} -o {html_report_list[i]}"
            # cmd = "cmd.exe /c allure generate reports/xml -o reports/html"
            log.info(cmd)
            os.system(cmd)

        log.info("-----报告转换完成------")
        zip_file_name = time.strftime("%Y-%m-%d-", time.localtime()) + 'html.zip'
        Files().zipFile(html_path, html_zip_path, zip_file_name)
        log.info("-----报告压缩完成------")

        for templates in show_report_list:
            SendEmail().SendEmail(html_zip_path, zip_file_name, templates)
        log.info("-----邮件发送完成------")

        for uuid in devices["device_info"]["devices"]:
            dm.unbindDevice(uuid)
        log.info(f"设备{devices}已释放")
        log.info("--------------结束---------------")


if __name__ == '__main__':
    main()
    # print(get_case_name())
    # 执行方式：切换到main目录， python main.py -n 用例名称/项目名称

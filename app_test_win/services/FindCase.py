import os
import re
from getpath import get_abs_path
from util.Log import Logger

log = Logger().logger


def findTestCases(path_name):
    """
    查询待执行测试用例
    输入：
    1. 用例文件名  -- 执行指定用例文件
    2. 用例目录  -- 执行目录下所有 test_开头文件
    """

    root_path = get_abs_path()
    base_path = os.path.join(root_path, 'testcase')

    # testcase下遍历所有文件及目录
    g = os.walk(base_path)

    file_name_list = []
    dir_name_list = []
    for path, dir_list, file_list in g:
        for file_name in file_list:
            file_name_list.append(os.path.join(path, file_name))

        for dir_name in dir_list:
            dir_name_list.append(os.path.join(path, dir_name))

    dir_name_list.insert(0, base_path)
    # 头插testcase目录本身， 输入testcase可以执行所有用例

    ret = re.match(r"^test_(.*?)", path_name)

    if ret:
        # 指定测试用例
        file_lists = []
        for i in file_name_list:
            if i.find('__pycache__') > 0:
                continue

            if i.split('\\')[-1].find(path_name) <= -1:
                # 未包含指定测试用例
                continue

            file_lists.append(i)
        return file_lists

    else:
        # 指定目录下所有用例
        dir_lists = []

        for i in dir_name_list:
            if i.split('\\')[-1].find(path_name) <= -1:
                continue
            dir_lists.append(i)

        for j in dir_lists:
            gt = os.walk(j)
            j_list = []
            j_path_list = []
            for path, dir_list, file_list in gt:
                for file_name in file_list:
                    j_list.append(os.path.join(path, file_name))

            for k in j_list:
                if k.find('__pycache__') > 0:
                    continue

                if k.find('__init__') > 0:
                    continue

                if k.split('\\')[-1].find("test_") <= -1:
                    continue

                j_path_list.append(k)
            return j_path_list
        return dir_lists


# def findAllTestReport(test_report_path, test_report_path_list=[]):
#     dir_list = os.listdir(test_report_path)
#     for dir_path in dir_list:
#         base_path = test_report_path + '/' + str(dir_path)
#         if os.path.isdir(base_path):
#             if base_path.find('.py') < 0:
#                 find_all_test_report(base_path, test_report_path_list)
#             else:
#                 test_report_path_list.append(base_path)
#     return test_report_path_list


if __name__ == '__main__':
    print(findTestCases("testcase"))

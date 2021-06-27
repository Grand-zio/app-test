#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Time    : 2020/3/10 15:17
# @Author  : djc
# @File    : getData.py
from util.Log import Logger
from getpath import get_abs_path
import configparser  # 配置文件解析
from xlrd import open_workbook
import yaml
import zipfile
import os
from bs4 import BeautifulSoup


class Files:
    def __init__(self):
        self.ach = configparser.ConfigParser()
        self.root_path = get_abs_path()
        self.log = Logger().logger

    def read(self, file_path, parm1=None, parm2=None):
        # 读取文件
        if file_path.split(".")[1] == "xlsx":
            # parm1该Excel的sheet名称
            cls = []
            try:
                file = open_workbook(file_path)  # 打开用例Excel
                sheet = file.sheet_by_name(parm1)  # 获得打开Excel的sheet
                # 获取这个sheet内容行数
                rows = sheet.nrows
                for i in range(rows):  # 根据行数做循环
                    cls.append(sheet.row_values(i))
                return cls
            except Exception as e:
                self.log.error(e)
                return None

        elif file_path.split(".")[1] == "yaml":
            with open(file_path, 'r') as stream:
                try:
                    dict_res = yaml.load(stream)
                    return dict_res
                except yaml.YAMLError as exc:
                    self.log.error(exc)
                    return None

        elif file_path.split(".")[1] == "ini":
            try:
                self.ach.read(file_path, encoding='UTF-8')
                value = self.ach.get(parm1, parm2)
                return value
            except Exception as e:
                self.log.error(e)
                return None

        elif file_path.split(".")[1].lower() in ['jpg', 'png', 'jpeg']:
            try:
                with open(file_path, 'rb') as fp:
                    return fp.read()

            except Exception as e:
                self.log.error(e)
                return None

        elif file_path.split(".")[1].lower() == 'html':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return BeautifulSoup(f.read(), 'html.parser')

            except Exception as e:
                self.log.error(e)
                return None

        else:
            self.log.error("文件不在这几种类型中")
            return None

    def dfs_get_zip_file(self, input_path, result):
        files = os.listdir(input_path)
        for file in files:
            if os.path.isdir(input_path+'/'+file):
                self.dfs_get_zip_file(input_path+'/'+file, result)
            else:
                result.append(input_path+'/'+file)

    def zipFile(self, input_path, output_path, output_name):
        """
        压缩文件
        """
        f = zipfile.ZipFile(output_path+'/'+output_name, 'w', zipfile.ZIP_DEFLATED)
        file_lists = []
        self.dfs_get_zip_file(input_path, file_lists)

        for file in file_lists:
            f.write(file)
        f.close()
        return output_path+r"/" + output_name

    @staticmethod
    def setPages(data, page_index, page_size):
        """
        内存操作分页
        :return:
        """
        n = len(data)
        if page_size <= 0:
            return 'out of index'
        if page_size >= n:
            return data

        total_page = len(data) // page_size + 1
        if page_index <= 0 or page_index >= total_page:
            return 'out of index'

        ps = page_size * (page_index - 1)
        pi = page_index * page_size
        result = data[ps:pi]
        return result




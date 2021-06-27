#!/usr/bin/env python 
# -*-coding:utf-8-*-
# @Time    : 2020/3/11 10:16
# @Author  : djc
# @File    : getpath.py
import os


def get_abs_path():
    path = os.path.split(os.path.realpath(__file__))[0]
    return path


if __name__ == '__main__':  # 执行该文件，测试下是否OK
    print('测试路径是否OK,路径为：', get_abs_path())

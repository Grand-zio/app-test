#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from util.FileOperation import Files


proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        self.cf = Files()

    def getMethod(self):
        value = self.cf.read(configPath, "DEVICES", 'method')
        return value

    def getServerUrl(self):
        value = self.cf.read(configPath, "DEVICES", "server")
        return value

    def getServerToken(self):
        value = self.cf.read(configPath, "DEVICES", "token")
        return value

    def getPhones(self):
        value = self.cf.read(configPath, "DEVICES", "test_phone")
        return value.split('|')

    def getDevicesIp(self):
        value = self.cf.read(configPath, "DEVICES", "IP")
        return value.split('|')

    def getApkUrl(self):
        value = self.cf.read(configPath, "APP", "apk_url")
        return value

    def getApkPath(self):
        value = self.cf.read(configPath, "APP", "apk_path")
        return value

    def getPkgName(self):
        value = self.cf.read(configPath, "APP", "pkg_name")
        return value

    def getOnOff(self):
        value = self.cf.read(configPath, "EMAIL", "on_off")
        return value

    def getSubject(self):
        value = self.cf.read(configPath, "EMAIL", "subject")
        return value

    def getMailHost(self):
        value = self.cf.read(configPath, "EMAIL", "mail_host")
        return value

    def getMailUser(self):
        value = self.cf.read(configPath, "EMAIL", "mail_user")
        return value

    def getMailPass(self):
        value = self.cf.read(configPath, "EMAIL", "mail_pass")
        return value

    def getSender(self):
        value = self.cf.read(configPath, "EMAIL", "sender")
        return value

    def getAddressee(self):
        value = self.cf.read(configPath, "EMAIL", "addressee")
        return value.split('|')

    def getCC(self):
        value = self.cf.read(configPath, "EMAIL", "cc")
        return value.split('|')

    def getOCRAppId(self):
        value = self.cf.read(configPath, "baidu_ocr", "app_id")
        return value.split('|')

    def getOCRApiKey(self):
        value = self.cf.read(configPath, "baidu_ocr", "api_key")
        return value.split('|')

    def getOCRSecretKey(self):
        value = self.cf.read(configPath, "baidu_ocr", "secret_key")
        return value.split('|')

    def getImgAppId(self):
        value = self.cf.read(configPath, "baidu_image", "app_id")
        return value.split('|')

    def getImgApiKey(self):
        value = self.cf.read(configPath, "baidu_image", "api_key")
        return value.split('|')

    def getImgSecretKey(self):
        value = self.cf.read(configPath, "baidu_image", "secret_key")
        return value.split('|')

    def getTesseract(self):
        value = self.cf.read(configPath, "tesseract", "path")
        return value.split('|')

if __name__ == '__main__':
    a = ReadConfig()
    print(a.getMailHost())



















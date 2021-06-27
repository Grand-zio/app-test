#!/usr/bin/env python 
# -*-coding:utf-8-*-
# @Time    : 2020/3/10 15:11
# @Author  : djc
# @File    : ConfigEmail.py.py
import os
from config.config import ReadConfig
from util.MailTemplates import MailTemplates
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
from getpath import get_abs_path
from util.Log import Logger


class SendEmail:

    """
    这个文件主要是配置发送邮件的主题、正文等，将测试报告发送并抄送到相关人邮箱的逻辑。
    """
    def __init__(self):
        self.subject = ReadConfig().getSubject()  # 从配置文件中读取，邮件主题
        self.sender = ReadConfig().getSender()
        self.receivers = ReadConfig().getAddressee()  # 从配置文件中读取，邮件收件人
        self.cc = ReadConfig().getCC()  # 从配置文件中读取，邮件抄送人
        self.mail_host = ReadConfig().getMailHost()
        self.mail_user = ReadConfig().getMailUser()
        self.mail_pass = ReadConfig().getMailPass()
        self.log = Logger().logger
        # self.path = getpath.get_abs_path()

    def SendEmail(self, mail_path, filename, templates):
        message = MIMEMultipart()
        message['From'] = Header("自动化测试组", 'utf-8')
        message['To'] = Header("ebuy特工小队", 'utf-8')
        message['Subject'] = Header(self.subject, 'utf-8')

        filepath = os.path.join(mail_path, filename)
        # 邮件正文内容

        message.attach(MIMEText(templates, _subtype='html', _charset='utf-8'))

        with open(filepath, 'rb') as f:
            # 设置附件的MIME和文件名，这里是rar类型:
            mime = MIMEBase('zip', 'zip', filename=filename)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 读取附件内容:
            mime.set_payload(f.read())
            # 用Base64编码
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart
        message.attach(mime)

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            self.log.error(smtplib.SMTPException)
            print("Error: 无法发送邮件")
        return "发送成功"


if __name__ == '__main__':
    root_path = get_abs_path()
    path = os.path.join(root_path, 'reports//html')
    mail = "2432854771@qq.com"
    rem = MailTemplates().get_templates(mail)
    SendEmail().SendEmail(path, 'Mobile.vue', rem)



import os
from util.FileOperation import Files
from getpath import get_abs_path
import re


class MailTemplates:
    """
    解析邮箱模板
    """
    def __init__(self):
        self.root_path = get_abs_path()

    @staticmethod
    def assert_mail(mail):
        str_mail = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[0-9a-zA-z]{1,13}\.[com,cn,net]{1,3}$'
        if re.match(str_mail, mail):
            return True
        return False

    def get_templates(self, mail):
        templates_path = os.path.join(self.root_path, 'templates')
        is_mail = MailTemplates.assert_mail(mail)
        if not is_mail:
            return 'please confirm mail~'
        mail_suffix = mail.split('@', 1)[1]

        if mail_suffix.lower() == 'qq.com':
            templates_name = os.path.join(templates_path, 'QQcom.html')

        elif mail_suffix.lower() == 'gmail.com':
            templates_name = os.path.join(templates_path, 'Googlecom.html')

        elif mail_suffix.lower() == '163.com':
            templates_name = os.path.join(templates_path, '163com.html')

        else:
            return None

        email_html = Files().read(templates_name)
        return email_html


if __name__ == '__main__':
    Email = "2432854771@qq.com"
    MailTemplates().get_templates(Email)

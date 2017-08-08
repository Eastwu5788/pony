from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header
import smtplib

# 网易SMTP服务器地址
SMTP_SERVER = "smtp.ym.163.com"
# 网易SMTP服务器端口号
SMTP_PORT = 25

SEND_EMAIL = "wudong@eastwu.cn"
SEND_PASSWORD = "Eastwu08.22"


class Email(object):

    @classmethod
    def format_email_address(cls, ori_address=""):
        """
        格式化编码邮件地址
        :param ori_address:原始邮件地址字符串
        :return: 格式化后的email地址
        """
        name, addr = parseaddr(ori_address)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def __init__(self, subject="", to_address="", message=""):
        self.subject = subject
        self.to_address = to_address
        self.message = message

    def config_message(self):
        format_message = MIMEText(self.message, "plain", "utf-8")
        format_message["From"] = Email.format_email_address(SEND_EMAIL)
        format_message["To"] = Email.format_email_address(self.to_address)
        format_message['Subject'] = Header(self.subject, 'utf-8').encode()
        return format_message

    def send_email(self):
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1)

        server.login(SEND_EMAIL, SEND_PASSWORD)
        server.sendmail(SEND_EMAIL, [self.to_address], self.config_message().as_string())
        server.quit()


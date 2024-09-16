import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import *
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from app.models.lock import Lock
# Get the absolute path of the templates_mail directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
print(template_dir)
file_loader = FileSystemLoader(template_dir)
env = Environment(loader=file_loader)

template_SUCCESS = env.get_template('success.html')
template_WAITING = env.get_template('waiting.html')

class Mail:
    sender_email = "gabsoundhelp@yandex.ru"
    sender_password = "grynwbquarjgqqdc"
    smtp_server = "smtp.yandex.ru"
    smtp_port = 587

    def __init__(self, lock: Lock):
        self.message = None
        self.lock = lock
        self.senders: List[str] = [self.lock.email, self.sender_email]
        self.customerMail = self.statusMail()
    
    def statusMail(self) -> str:
        if self.lock.event_data.DATA.status == 0:
            return template_SUCCESS.render(lock=self.lock, user=self.user)
        else:
            return template_WAITING.render(lock=self.lock, user=self.user)

    def send_message(self):
        context = ssl.create_default_context()
        for sender in self.senders:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                self.message: MIMEMultipart = MIMEMultipart()
                self.message["From"]: str = self.sender_email
                self.message["Subject"] = "Спасибо вам за предзаказ | EAZY GAB" if sender != self.sender_email else f"Заказ - №{self.user.payment.orderid} оформлен | EAZY GAB"
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)

                html = self.customerMail if sender == self.user.email else self.creatorMail
                self.message['To'] = sender
                self.message.attach(MIMEText(html, 'html'))

                server.sendmail(self.sender_email, sender, self.message.as_string())
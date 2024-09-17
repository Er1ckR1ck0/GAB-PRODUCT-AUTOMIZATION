import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Union, Tuple
from jinja2 import Environment, FileSystemLoader
from app.models.lock import Lock
from app.models.branch import Branch
from app.models.event import Event

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

    def __init__(self, lock: Union[Lock, Event]):
        self.message = None

        if isinstance(lock, Event):
            self.lock = Lock(
                name=lock.data_.name,
                lock_id=None,
                lock_name=None,
                passcode=None,
                start_time=lock.data_.record,
                end_time=None,
                cooperator_id=lock.data_.cooperator_id,
                event_data=lock,
                branch_info=Branch.from_dict(cooperator_id=lock.data_.cooperator_id)
            )
        else:
            self.lock = lock

        self.senders: list = [self.lock.event_data.data_.email, self.sender_email]
        self.customerMail, self.title = self.statusMail()

    def statusMail(self) -> Tuple[str, str]:
        if self.lock.event_data.data_.status == 0:
            return template_SUCCESS.render(lock=self.lock), "Спасибо за бронирование"
        else:
            return template_WAITING.render(lock=self.lock), "Осталось совсем чуть-чуть"

    def send_message(self):
        context = ssl.create_default_context()
        for sender in self.senders:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                self.message = MIMEMultipart()
                self.message["From"] = self.sender_email
                self.message["Subject"] = self.title
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)

                html = self.customerMail
                self.message['To'] = sender
                self.message.attach(MIMEText(html, 'html'))

                server.sendmail(self.sender_email, sender, self.message.as_string())
from flask_mail import Mail, Message


class MailService:
    def __init__(self, app):
        self.mail = Mail(app)

    def send_mail(self, receiver: str, subject:str, content: str) -> None:
        msg = Message(subject=subject, body=content, recipients=[receiver], sender='athletemailer@gmail.com')
        self.mail.send(msg)

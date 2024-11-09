import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr


def SendEmailWithAttachment(config, recipient, subject, body, attachment_path, attachment_name):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['To'] = recipient
    message['From'] = formataddr((config['smtp']['sender']["name"], config['smtp']['sender']["email"]))

    body_part = MIMEText(body)
    message.attach(body_part)

    with open(attachment_path, 'rb') as file:
        message.attach(MIMEApplication(file.read(), Name=attachment_name))

    with smtplib.SMTP(config['smtp']['host'], config['smtp']['port']) as server:
        server.send_message(message)

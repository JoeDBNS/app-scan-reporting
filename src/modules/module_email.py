import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, Disposition
)


def SendEmailWithAttachment(config, recipients, subject, body, attachment_path, attachment_name):
    message = Mail(
        from_email = (config['smtp']['sender']['email'], config['smtp']['sender']['name']),
        to_emails = recipients,
        subject = subject,
        html_content = body
    )

    file_path = attachment_path
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()

    encoded = base64.b64encode(data).decode()

    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_name = FileName(attachment_name)
    attachment.disposition = Disposition('attachment')

    message.attachment = attachment

    try:
        sendgrid_client = SendGridAPIClient(config['smtp']['api_key'])
        response = sendgrid_client.send(message)

    except Exception as e:
        print(e.message)
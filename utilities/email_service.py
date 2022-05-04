import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from settings.base import SENDER_EMAIL


class EmailFactory:
    """
        Class responsible for sending emails using AWS SES Service.
    """
    email_subject = None

    def __init__(self, start_date, end_date, subject):
        self.email_subject = subject + " " + str(start_date)

    def send_email_with_attachment(self, attachment, receiver):
        """
        Sends report to receiver's email with zip file attachment...
        :param attachment: dictionary
        :param receiver: string(email_address)
        :return: json response from email server
        """
        ses = boto3.client('ses')
        msg = MIMEMultipart()
        msg['Subject'] = self.email_subject
        # what a recipient sees if they don't use an email reader
        msg.preamble = 'Multipart message.\n'

        # the message body
        part = MIMEText(self.email_subject)
        msg.attach(part)

        # the attachment
        part = MIMEApplication(attachment['content'].getvalue())
        part.add_header('Content-Disposition', 'attachment', filename=attachment['name'])
        msg.attach(part)

        result = ses.send_raw_email(Source=SENDER_EMAIL, Destinations=[receiver], RawMessage={'Data': msg.as_string()})
        return result

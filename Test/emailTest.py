__author__ = 'sulantha'
from Utils.EmailClient import EmailClient


emailClient = EmailClient()
emailClient.send_email('a', 'First test email subject', 'Body of text. ')




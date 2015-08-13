__author__ = 'sulantha'
import Config.EmailConfig as ec
from Utils.EmailClient import EmailClient


emailClient = EmailClient()
emailClient.send_email(ec.EmailRecList_admin, 'First test email subject', 'Body of text. ')




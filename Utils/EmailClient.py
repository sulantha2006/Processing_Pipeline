__author__ = 'sulantha'
import smtplib
import Config.EmailConfig as ec

class EmailClient:
    def __init__(self):
        pass

    @staticmethod
    def send_email(rec_list, subject, body):

        userName = ec.EmailUserName
        passWd = ec.EmailPassWd
        FROM = ec.EmailFrom
        TO = rec_list[0]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(userName, passWd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('Successfully sent the mail')
        except:
            print('Failed to send mail')

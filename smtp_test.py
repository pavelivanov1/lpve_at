import smtplib
from email.mime.text import MIMEText

class EmailClient():

    def __init__(self, my_address):
        self.my_address = my_address

    def send(self, message, subject, user, email):

        header = "Hello " + str(user) + ",\n\n"
        footer = "\n\n-Your Boss"
        msg = MIMEText(header + message + footer)

        msg['Subject'] = subject
        msg['From'] = self.my_address
        msg['To'] = email

        s = smtplib.SMTP('localhost')
        s.sendmail(self.my_address, [email], msg.as_string())
        s.quit()

EClient = EmailClient("MyEmail@University.edu")
EClient.send("This is a test Email", "Test Subject", "John Doe", "jdoe@University.edu")
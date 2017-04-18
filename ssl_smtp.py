import smtplib

email_fromaddr = 'selenium.probe@vidyo.io.test'
email_toaddrs  = 'pavlo.ivanov@globallogic.com'
email_msg = 'There was a terrible error that occured and I wanted you to know!'


# Credentials (if needed)
email_username = 'pavlo.ivanov@globallogic.com'
email_password = 'Balzatul1!'

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(email_username,email_password)
server.sendmail(email_fromaddr, email_toaddrs, email_msg)
server.quit()
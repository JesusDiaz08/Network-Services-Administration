import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params


#mailsender = "dummycuenta3@gmail.com"
mailsender  = "pruebatanibet@gmail.com"
#mailreceip = "dummycuenta3@gmail.com"
mailreceip  = "pruebatanibet@gmail.com"
mailserver = 'smtp.gmail.com: 587'
#password = 'Secreto123'
password = "contraredes3"

def send_alert_attached(subject, pngpath):
    """ Will send e-mail, attaching png
    files in the flist.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(pngpath+'deteccion.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)

    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()

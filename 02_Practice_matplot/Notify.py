import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
COMMASPACE = ', '
# Define params


#mailsender = "dummycuenta3@gmail.com"
mailsender  = "pruebatanibet@gmail.com"
#mailreceip = "dummycuenta3@gmail.com"
mailreceip  = "pruebatanibet@gmail.com"
mailserver = 'smtp.gmail.com: 587'
#password = 'Secreto123'
password = "contraredes3"

def send_alert_attached(subject, pngpath, pngname, name):
    """ Will send e-mail, attaching png
    files in the flist.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(pngpath+pngname, 'rb')

    rrd_file = open(pngpath + name, "rb")
    p = MIMEBase("application", "octet-stream")
    p.set_payload((rrd_file).read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment", filename = name)

    img = MIMEImage(fp.read())
    img.add_header("Content-Disposition", "attachment", filename = pngname)
    rrd_file.close()
    fp.close()

    msg.attach(img)
    msg.attach(p)
    #msg.attach(MIMEText("Equipo 6 grupo 4CM3","plain"))

    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)

    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()

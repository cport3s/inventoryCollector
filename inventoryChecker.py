import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mailCredentials
import mysql.connector
from datetime import datetime

# Azure App ID: a096e4a2-15ef-42bc-a55d-8843e5695362
# Client Secret Value: lnhQG_dT1Z5-_fS~QN8oRtTv~C7-z~07cR
# Client Secret ID: e50a3cce-4b22-43db-987d-4cf4784d6e24
# Tenant ID: f3cd872a-497f-40ac-931d-b228d81cdaf9

def sendMailNotification(cred, mail_from, mail_to, mail_subject, mail_body):
    mimeMsg = MIMEMultipart()
    mimeMsg['From'] = mail_from
    mimeMsg['To'] = mail_to
    mimeMsg['Subject'] = mail_subject
    mimeMsg.attach(MIMEText(mail_body, 'plain'))
    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(cred.username, cred.password)
    connection.send_message(mimeMsg)
    connection.quit()

# Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)
currentDate = (datetime.now()).strftime("%Y-%m-%d")
yesterdayDate = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")

# Close DB Connection
pointer.close()
connectr.close()

cred = mailCredentials.credentials()
mail_from = 'caportes@altice.com.do'
mail_to = 'ran-operaciones@altice.com.do'
mail_subject = 'Python Test'
mail_body = 'Test'

sendMailNotification(cred, mail_from, mail_to, mail_subject, mail_body)
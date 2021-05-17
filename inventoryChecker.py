import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mailCredentials
import mysql.connector
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import classes

# Azure App ID: a096e4a2-15ef-42bc-a55d-8843e5695362
# Client Secret Value: lnhQG_dT1Z5-_fS~QN8oRtTv~C7-z~07cR
# Client Secret ID: e50a3cce-4b22-43db-987d-4cf4784d6e24
# Tenant ID: f3cd872a-497f-40ac-931d-b228d81cdaf9

def sendMailNotification(cred, mail_from, mail_to, mail_subject, mail_body):
    mimeMsg = MIMEMultipart()
    mimeMsg['From'] = mail_from
    mimeMsg['To'] = mail_to
    mimeMsg['Subject'] = mail_subject
    mimeMsg.attach(MIMEText(mail_body, 'html'))
    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(cred.username, cred.password)
    connection.send_message(mimeMsg)
    connection.quit()

dbPara = classes.dbCredentials()

# Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)
# Get current date
currentDate = (datetime.now()).strftime("%Y-%m-%d")
#currentDate = datetime(2021, 5, 5).strftime("%Y-%m-%d")
# Get yesterday's date
yesterdayDate = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
#yesterdayDate = (datetime(2021, 5, 5)-timedelta(days=1)).strftime("%Y-%m-%d")
# Query today's data
query = 'select nename,hardwaretype,serialnumber,description from alticedr_sitedb.networkinventory a where a.lastupdate >= \'{today}\' and not exists (select 1 from alticedr_sitedb.networkinventory b where b.lastupdate >= \'{yesterday}\' and b.lastupdate <  \'{today}\' and b.nename = a.nename and ifnull(b.serialnumber, \'x\') = ifnull(a.serialnumber, \'x\'))'.format(today=currentDate, yesterday=yesterdayDate)
pointer.execute(query)
queryRaw = pointer.fetchall()
queryPayload = np.array(queryRaw)
currentDataframe = pd.DataFrame(queryPayload, columns=['nename','hardwaretype','serialnumber','description'])
# Close DB Connection
pointer.close()
connectr.close()
#print(currentDataframe)
cred = mailCredentials.credentials()
mail_from = 'caportes@altice.com.do'
mail_to = 'ran-operaciones@altice.com.do'
mail_subject = '[RANventory Manager] Daily Hardware Report'
mail_body = '<p>Good morning,</p><p>Here is a list of newly added or replaced hardware on the RAN for yesterday:</p>' + currentDataframe.to_html(index=False) + '<p>Regards, </p>'

sendMailNotification(cred, mail_from, mail_to, mail_subject, mail_body)
from ftplib import FTP
from io import BytesIO, StringIO

# Recieves ftpLogin credentials and ftp File Path and returns the filename list
def getFtpPathFileList(ftpLogin, filePath):
    fileName = ""
    # Instantiate FTP connection
    ftp = FTP(host=ftpLogin.hostname)
    ftp.login(user=ftpLogin.username, passwd=ftpLogin.password)
    # Move to desired path
    ftp.cwd(filePath)
    fileName = ftp.nlst()
    return fileName

# Takes ftpLogin object, filepath and file name and returns file content in memory
def downloadFtpFileByte(ftpLogin, filePath, fileName):
    # Instantiate FTP connection
    ftp = FTP(host=ftpLogin.hostname)
    ftp.login(user=ftpLogin.username, passwd=ftpLogin.password)
    # Move to desired path
    ftp.cwd(filePath)
    # Instantiate a BytesIO object to temp store the xlsx file from the FTP server
    b = BytesIO()
    # Return file as binary with retrbinary functon. Must send according RETR command as part of FTP protocol
    ftp.retrbinary('RETR ' + fileName, b.write)
    # Open as Dataframe
    ftp.quit()
    return b

# Takes ftpLogin object, filepath and file name and returns file content in memory
def downloadFtpFileString(ftpLogin, filePath, fileName):
    # Instantiate FTP connection
    ftp = FTP(host=ftpLogin.hostname)
    ftp.login(user=ftpLogin.username, passwd=ftpLogin.password)
    # Move to desired path
    ftp.cwd(filePath)
    # Instantiate a StringIO object to temp store the file from the FTP server
    s = StringIO()
    # Return file as string with retrlines functon. Must send according RETR command as part of FTP protocol
    ftp.retrlines('RETR ' + fileName, s.write)
    # Open as Dataframe
    ftp.quit()
    return s
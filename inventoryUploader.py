import csv
import pandas as pd
from io import StringIO, BytesIO
# Custom libraries
import uploaderFunctions
import classes

testFilePath = '/configuration_files/NBI_Inventory/InvtTimerExport/'
bscFileList = []
rncFileList = []
btsFileList = []
picoFileList = []

ftpLogin = classes.ranFtpCredentials()
dirList = uploaderFunctions.getFtpPathFileList(ftpLogin, testFilePath)
# Loop through the filename list
for fileName in dirList:
    # Check for keywords to form each NE filename list
    if 'BSC6900UMTS' in fileName or 'BSC6910UMTS' in fileName:
        rncFileList.append(fileName)
    if 'BSC6910GSM' in fileName:
        bscFileList.append(fileName)
    if '_BTS3900' in fileName or '_BTS5900' in fileName or 'eNodeB' in fileName:
        btsFileList.append(fileName)
    if 'PICO' in fileName:
        picoFileList.append(fileName)
#fileContent = uploaderFunctions.downloadFtpFileByte(ftpLogin, testFilePath, btsFileList[0])
fileContent = uploaderFunctions.downloadFtpFileString(ftpLogin, testFilePath, btsFileList[0])
fileValue = fileContent.getvalue()
print(fileValue)
#with open(fileValue, 'rb') as input_file:
#    csv_reader = csv.reader(input_file)
#    for row in csv_reader:
#        if 'Board' in row:
#            print('Found!')
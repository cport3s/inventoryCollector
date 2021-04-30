import csv
import pandas as pd
from io import StringIO, BytesIO
import mysql.connector
# Custom libraries
import uploaderFunctions
import classes

testFilePath = '/configuration_files/NBI_Inventory/InvtTimerExport/'
bscFileList = []
rncFileList = []
btsFileList = []
picoFileList = []

# DB Connection Parameters
dbPara = classes.dbCredentials()
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
# BTS File Inventory
# Get file content
fileContent = uploaderFunctions.downloadFtpFileString(ftpLogin, testFilePath, btsFileList[0])
# Move to index 0, to start reading at the beginning.
fileContent.seek(0)
# Convert file content to dataframe
dataframe = pd.read_csv(fileContent)
hwType = []
partNumbers = []
serialNumberList = []
descList = []
# Parse df columns as lists (all CSV data is stored as columns)
data = list(dataframe.columns)
# Find all keyword's position inside the array
keywordsDict = {}
for c in range(len(data)):
    if '[Cabinet]' in data[c]:
        keywordsDict['[Cabinet]'] = c
    if '[Subrack]' in data[c]:
        keywordsDict['[Subrack]'] = c
    if '[Slot]' in data[c]:
        keywordsDict['[Slot]'] = c
    if '[Board]' in data[c]:
        keywordsDict['[Board]'] = c
    if '[Port]' in data[c]:
        keywordsDict['[Port]'] = c
    if '[Antenna]' in data[c]:
        keywordsDict['[Antenna]'] = c
    if '[HostVer]' in data[c]:
        keywordsDict['[HostVer]'] = c

# Move index to desired position (depending on document section)
k = keywordsDict['[Cabinet]'] + 18
j = k + 5
i = k + 10
# Cabinet Section
while i < keywordsDict['[Subrack]']:
    hwType.append(data[k])
    k += 16
    serialNumberList.append(data[j])
    j += 16
    descList.append(data[i])
    i += 16
# Subrack Section
# Move index to desired position (depending on document section)
k = keywordsDict['[Subrack]'] + 22
j = k + 7
i = k + 12
while i < keywordsDict['[Slot]']:
    hwType.append(data[k])
    k += 19
    serialNumberList.append(data[j])
    j += 19
    descList.append(data[i])
    i += 19
# Board Section
# Move index to desired position (depending on document section)
k = keywordsDict['[Board]'] + 39
j = k + 5
i = k + 10
while i < keywordsDict['[Port]']:
    hwType.append(data[k])
    k += 31
    serialNumberList.append(data[j])
    j += 31
    descList.append(data[i])
    i += 31

# Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)
#for i in hwType:
#    query = 'INSERT INTO `networkinventory` (`nename`,`hardwaretype`,`serialnumber`,`description`,`lastupdate`) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'.format()
# Close DB Connection
pointer.close()
connectr.close()
print(len(hwType))
print(len(serialNumberList))
print(len(descList))
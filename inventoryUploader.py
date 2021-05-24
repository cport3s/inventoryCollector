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

# Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)
# BTS File Inventory
for fileName in btsFileList:
    # Get file content
    fileContent = uploaderFunctions.downloadFtpFileString(ftpLogin, testFilePath, fileName)
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
    # Get NE Name
    neNameStart = data[0].find('[NEName]')
    neNameEnd = data[0].find('[NEType]')
    neName = data[0][neNameStart+8:neNameEnd]
    # Move index to desired position (depending on document section)
    #k = keywordsDict['[Cabinet]'] + 18
    #j = k + 5
    #i = k + 10
    ## Cabinet Section
    #while i < keywordsDict['[Subrack]']:
    #    # Rack Type Column
    #    hwType.append(data[k])
    #    k += 16
    #    # Serial Number Column
    #    if len(data[j]) < 10:
    #        serialNumberList.append(data[k])
    #    else:
    #        serialNumberList.append(data[j])
    #    j += 16
    #    # Manufacturer Data Column
    #    if len(data[i]) < 10:
    #        descList.append(data[k])
    #    else:
    #        descList.append(data[i])
    #    i += 16
    # Subrack Section
    # Move index to desired position (depending on document section)
    k = keywordsDict['[Subrack]'] + 22
    j = k + 7
    i = k + 12
    while i < keywordsDict['[Slot]']:
        # Check if serial number value is valid
        if len(data[j]) > 8:
            # Board Type Column
            hwType.append(data[k])
            k += 19
            # Serial Number Column
            serialNumberList.append(data[j])
            j += 19
            # Manufacturer Data Column
            descList.append(data[i])
            i += 19
        else:
            k += 19
            j += 19
            i += 19
    # Board Section
    # Move index to desired position (depending on document section)
    k = keywordsDict['[Board]'] + 39
    j = k + 5
    i = k + 10
    while i < keywordsDict['[Port]']:
        # If the serial number cell has a whitespace in, then skip the row
        if " " in data[j]:
            k += 31
            j += 31
            i += 31
        else:
            # Board Type Column
            hwType.append(data[k])
            k += 31
            # Serial Number Column
            serialNumberList.append(data[j])
            j += 31
            # Manufacturer Data Column
            descList.append(data[i])
            i += 31

    for i in range(len(hwType)):
        query = 'INSERT INTO `alticedr_sitedb`.`networkinventory` (`nename`,`hardwaretype`,`serialnumber`,`description`) VALUES (\'{}\',\'{}\',\'{}\',\'{}\');'.format(neName, hwType[i], serialNumberList[i], descList[i])
        pointer.execute(query)
        connectr.commit()

# Close DB Connection
pointer.close()
connectr.close()
# inventoryCollector
 Huawei OSS Network Inventory Collector
inventoryUploader.py: Reads al CSV files exported from Huawei OSS and uploads data to a db table. Access to CSV files is made through an FTP connection.

inventoryChecker.py: Compares data on alticedr_sitedb.networkinventory table, between current date and current date - 1, then sends a report via mail on the differences.
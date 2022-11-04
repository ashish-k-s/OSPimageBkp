#!/usr/bin/python3
import csv
from os import system
import smtplib
from email.message import EmailMessage

with open ("images_in_bps.txt", 'r') as bpsImageFile:
    bpsImages = set(bpsImageFile.readlines())

with open("images_on_disk.txt", 'r') as diskImageFile:
    diskImages = set(diskImageFile.readlines())

with open("images_on_cluster.txt", 'r') as clusterImageFile:
    clusterImages = set(clusterImageFile.readlines())

allImages=bpsImages.union(diskImages)
allImages=allImages.union(clusterImages)

with open('table1.csv', 'w', newline='') as table1:
    t1=csv.writer(table1)
    t1.writerow(["imageName","inBPs","onDisk","onCluster","Status"])

    for imageName in allImages:
        if imageName in bpsImages:
            inBPs=True
        else:
            inBPs=False

        if imageName in diskImages:
            onDisk=True
        else:
            onDisk=False

        if imageName in clusterImages:
            onCluster=True
        else:
            onCluster=False

        if inBPs and not onDisk and not onCluster:
            Status="ALERT"
        if inBPs and not onDisk and onCluster:
            Status="bkpMissing"
        if inBPs and onDisk and not onCluster:
            Status="imageMissing"
        if inBPs and onDisk and onCluster:
            Status="ALLGOOD"
        if not inBPs:
            Status="DeleteImage"

        t1.writerow([imageName,inBPs,onDisk,onCluster,Status])

bpsImageFile.close()
diskImageFile.close()
clusterImageFile.close()
table1.close()

DeleteImageList = []
imageMissingList = []
bkpMissingList = []
ALERTList = []
ALLGOODList = []

with open('table1.csv', 'r') as table1:
    t1=csv.DictReader(table1)
    for line in t1:
        if line['Status'] == 'imageMissing':
            imageMissingList.append(line['imageName'])

        if line['Status'] == 'ALERT':
            ALERTList.append(line['imageName'])

        if line['Status'] == 'bkpMissing':
            bkpMissingList.append(line['imageName'])

        if line['Status'] == 'DeleteImage':
            DeleteImageList.append(line['imageName'])

        if line['Status'] == 'ALLGOOD':
            ALLGOODList.append(line['imageName'])

with open("ImageDelete.txt", 'w') as DeleteImageFile:
    for item in DeleteImageList:
        DeleteImageFile.write(item)

with open("ImageMissing-Cluster.txt", 'w') as imageMissingFile:
    for item in imageMissingList:
        imageMissingFile.write(item)

with open("ImageMissing-Disk.txt", 'w') as bkpMissingFile:
    for item in bkpMissingList:
        bkpMissingFile.write(item)

with open("ALERT.txt", 'w') as ALERTFile:
    for item in ALERTList:
        ALERTFile.write(item)

with open("ALLGOOD.txt", 'w') as ALLGOODFile:
    for item in ALLGOODList:
        ALLGOODFile.write(item)

DeleteImageFile.close()
imageMissingFile.close()
bkpMissingFile.close()
ALERTFile.close()
ALLGOODFile.close()

mymsg="""Greetings!

This is an auto generated email to notify the status of the images related to your NovelloShell setup.
Manual action may be needed only on the ALERT message below. Rest all will be auto corrected!
"""
msg = EmailMessage()

with open('ALERT.txt') as fp:
    mymsg = mymsg + "\nALERT: Below images used by your labs are missing from cluster and backup disk as well: \n" + fp.read()

with open('ImageDelete.txt') as fp:
    mymsg = mymsg + "\nBelow images are not in use by any of the labs. These will be deleted from your setup: \n" + fp.read()

with open('ImageMissing-Cluster.txt') as fp:
    mymsg = mymsg + "\nBelow images being used are missing from the cluster. The images will be restored from the available backup: \n" + fp.read()

with open('ImageMissing-Disk.txt') as fp:
    mymsg = mymsg + "\nNo backup found for below images being used. Backup on disk will be created automatically: \n" + fp.read()

#with open('ALLGOOD.txt') as fp:
#    mymsg = mymsg + "\nAll is well with below images: \n" + fp.read()


msg.set_content(mymsg)

msg['Subject'] = f'[INFO] Status of images on your lab setup with NovelloShell'
## REPLACE FROM and TO email IDs below
msg['From'] = 'FROM@DOMAIN'
msg['To'] = 'TO@DOMAIN'

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()


#!/usr/bin/python3
import csv
from os import system

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


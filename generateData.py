#!/usr/bin/python3
import csv
from os import system

with open ("images_in_bps.txt", 'r') as bpsImageFile:
    bpsImages = set(bpsImageFile.readlines())

with open("images_on_disk.txt", 'r') as diskImageFile:
    diskImages = set(diskImageFile.readlines())

with open("images_on_cluster.txt", 'r') as clusterImageFile:
    clusterImages = set(clusterImageFile.readlines())

print (bpsImages)
print (diskImages)
print (clusterImages)

allImages=bpsImages.union(diskImages)
allImages=allImages.union(clusterImages)

with open('table1.csv', 'w', newline='') as table1:
    t1=csv.writer(table1)
    t1.writerow(["imageName","inBPs","onDisk","inCluster","Status"])

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
            inCluster=True
        else:
            inCluster=False

        if inBPs and not onDisk and not inCluster:
            Status="ALERT"
        if inBPs and not onDisk and inCluster:
            Status="bkpMissing"
        if inBPs and onDisk and not inCluster:
            Status="imageMissing"
        if inBPs and onDisk and inCluster:
            Status="ALLGOOD"
        if not inBPs:
            Status="DeleteImage"

        t1.writerow([imageName,inBPs,onDisk,inCluster,Status])

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
            print ("Handle missing image for " + line['imageName'])
            imageMissingList.append(line['imageName'])

        if line['Status'] == 'ALERT':
            print ("Handle alert for " + line['imageName'])
            ALERTList.append(line['imageName'])

        if line['Status'] == 'bkpMissing':
            print ("Handle missing backup for " + line['imageName'])
            bkpMissingList.append(line['imageName'])

        if line['Status'] == 'DeleteImage':
            print ("Handle delete image for " + line['imageName'])
            DeleteImageList.append(line['imageName'])

        if line['Status'] == 'ALLGOOD':
            print ("Handle all good for " + line['imageName'])
            ALLGOODList.append(line['imageName'])


print("DeleteImageList")
print(DeleteImageList)
print("imageMissingList")
print(imageMissingList)
print("bkpMissingList")
print(bkpMissingList)
print("ALERTList")
print(ALERTList)
print("ALLGOODList")
print(ALLGOODList)

with open("DeleteImage.txt", 'w') as DeleteImageFile:
    for item in DeleteImageList:
        DeleteImageFile.write(item)

with open("imageMissing.txt", 'w') as imageMissingFile:
    for item in imageMissingList:
        imageMissingFile.write(item)

with open("bkpMissing.txt", 'w') as bkpMissingFile:
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


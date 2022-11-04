# ospImageBkp
Tool for auto backup and restore of OpenStack images.

## Objective

This tool can be used for auto backup and restore of OpenStack images.
This provides self-healing mechanism for images on OpenStack cluster.
This tool can also be used for migration of images from one cluster to another.

## How it works

![Alt text](image.png?raw=true "How OSP image backup works")

Images being used in the heat template is the primary database of valid images.
The tool looks for these images on the cluster and alos on backup disk. 
If image is missing on any one of the places, either cluster or the backup disk, the image is auto restored from the other place.
If image is missing on both the places, this is ALERT situation and need to be handled manually.
If either cluster or backup disk has an image that is not being used by any of the heat templates, such images will be deleted.

## About involved scripts and other files:

generate-image-files.sh:
This script calls below 3 scripts to generate list of the images available on the setup (i.e. heat template, osp cluster and backup dir)

generate-bps-image-file.sh:
This script generates file (images_in_bps.txt) cotaining list of valid images being used in blueprints (heat tempates).

generate-cluster-image-file.sh
This script generates file (images_on_cluster.txt) containing list of valid images available on the OpenStack cluster.

generate-disk-image-file.sh:
This script generates file (images_on_disk.txt) containing list of valid images available on the backup disk.

generateData.py:
This script parses the data generated by above scripts and generates table for status of the lab environment setup. 
Below are the files generated by this script:
- ALERT.txt - has list of images being used by lab but associated image is missing from the cluster as well as from the backup.
- ALLGOOD.txt - this has list of images being used by lab which has associated image on the cluster and backup of image is also available on the disk.
- ImageDelete.txt - this contains list of images which are available on cluster and/or disk but the image is not being used by any of the labs.
- ImageMissing-Cluster.txt - contains list of images missing on the cluster, this will be restored from disk.
- ImageMissing-Disk.txt - contains list of images whose backup is missing. The image file will be downloaded from the cluster.
- table1.csv - contains consolidated status of available images on the cluster.

![Alt text](table1.png?raw=true "Table created by generateData.py by using sampledata")

actData.sh:
This script reads the data generated by generateData.py script.
It refers to the status column in table1.csv to takes required corrective actions on the lab setup.

create-image-on-cluster.sh:
This scipt is used by actData.sh to restore the missing images on OSP cluster.

download-image-on-disk.sh:
This scipt is used by actData.sh to download missing backup images on the disk.

## sampledata
This directory contains sample files representing various states of the images on the lab setup.
Files in this directory can be used for demo run of this tool.
Refer to the instructions in `sampledata/samplerun.md` file. 

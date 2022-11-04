### This script accepts two arguments:
### the name of the image to be downloaded from the cluster and 
### path to the directory where image is to be stored
### Change this script with suitable command to download the image in your cluster environment.
openstack image save --file $2/$1 $1

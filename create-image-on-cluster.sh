### This script accepts two arguments 
### the name of the image to be uploaded to the cluster and 
### the path where images are stored on the disk.
### Change this script with suitable command to upload the image in your cluster environment.
if [[ $1 == *"-iso"* ]]
then
  ImageType="iso"
else
  ImageType="raw"
fi
openstack image create --disk-format $ImageType --container-format bare --public --file $2/$1 $1
##openstack image create --disk-format $ImageType --container-format bare --file $2/$1 $1
##script-to-publish-image.sh

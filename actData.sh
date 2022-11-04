CONFIGFILE="/etc/novelloshell.cfg"

if [ ! -f "$CONFIGFILE" ]
then
echo -e "ERROR: $CONFIGFILE does not exist"
exit 1
fi

BPSDIR=$(grep BPSDIR $CONFIGFILE  | grep -v ^#)
TAG=$(grep TAG $CONFIGFILE  | grep -v ^#)
ADMINRC=$(grep ADMINRC $CONFIGFILE  | grep -v ^#)
IMGBKPATH=$(grep IMGBKPATH $CONFIGFILE  | grep -v ^#)
LOGFILE=$(grep LOGFILE= $CONFIGFILE  | grep -v ^#)

eval $BPSDIR
eval $TAG
eval $ADMINRC
eval $IMGBKPATH
eval $LOGFILE

USERNAME=$(whoami)

source $ADMINRC

AlertDataFile="ALERT.txt"
AllgoodDataFile="ALLGOOD.txt"
ImageDeleteFile="ImageDelete.txt"
ImageMissingClusterFile="ImageMissing-Cluster.txt"
ImageMissingDiskFile="ImageMissing-Disk.txt"
images_in_bps_file="images_in_bps.txt"
images_on_cluster_file="images_on_cluster.txt"
images_on_disk_file="images_on_disk.txt"

echo -e "$0 START" | tee -a $LOGFILE
echo -e "Deleting images not in use..." | tee -a $LOGFILE
for file in `cat $ImageDeleteFile`
do
  grep $file $images_on_cluster_file
  if [ $? -eq 0 ]
  then
    echo -e "Marking $file for deletion in the cluster" | tee -a $LOGFILE
    ImageNameDel=$USERNAME-$file-DELETE-$RANDOM
    openstack image set --name $ImageNameDel $file
  fi

  grep $file $images_on_disk_file
  if [ $? -eq 0 ]
  then
    echo -e "Marking $file for deletion on the disk" | tee -a $LOGFILE
    ImageNameDel=$USERNAME-$file-DELETE-$RANDOM
    mv $IMGBKPATH/$file $IMGBKPATH/$ImageNameDel
  fi
done

echo -e "Restoring images on the cluster..." | tee -a $LOGFILE
for file in `cat $ImageMissingClusterFile`
do
  echo -e "Creating image $file on cluster" | tee -a $LOGFILE
  create-image-on-cluster.sh $file $IMGBKPATH
done

echo -e "Done with restoring images on the cluster..." | tee -a $LOGFILE

echo -e "Downloading images on the disk..." | tee -a $LOGFILE
for file in `cat $ImageMissingDiskFile`
do
  echo -e "Downloading image $file on disk" | tee -a $LOGFILE
  download-image-on-disk.sh $file $IMGBKPATH
done

echo -e "Done with downloading images on the disk..." | tee -a $LOGFILE

echo -e "$0 END" | tee -a $LOGFILE

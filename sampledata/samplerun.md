This file has the steps to be carried out for demonstration of this tool using files in sampledata directory.

#### Create /etc/novelloshell-demo.cfg as below:
ADMINRC="/path/to/rc/file"
BPSDIR="/mnt/NovelloShell/PROJECTS/BPS-demo"
LOGFILE="/mnt/NovelloShell/STATS/novelloshell-demo.log"
TAG="novelloshelldemo"
IMGBKPATH="/mnt/NovelloShell/PROJECTS/IMAGES-demo"

mkdir /mnt/NovelloShell/PROJECTS/BPS-demo
mkdir /mnt/NovelloShell/PROJECTS/IMAGES-demo

#### Create disk images based on sampledata
for file in `cat * | sort -n | uniq`; do echo $file ; dd if=/dev/zero of=$file-novelloshelldemo bs=1024 count=1024; done

#### Move created disk images to appropriate directory e.g. /mnt/NovelloShell/PROJECTS/IMAGES-demo/

#### Create images which are supposed to be available on cluster
for image in `ls -1 | grep 1-CLUSTER`; do echo $image; openstack image create --disk-format raw --container-format bare --file $image $image; done

#### Create files in BPS-demo with below name and associated contents within it.
BPS-demo/test1/stack_user.yaml
image: 1-BP-0-CLUSTER-0-DISK-novelloshelldemo

BPS-demo/test2/stack_user.yaml
image: 1-BP-0-CLUSTER-1-DISK-novelloshelldemo

BPS-demo/test3/stack_user.yaml
image: 1-BP-1-CLUSTER-0-DISK-novelloshelldemo

BPS-demo/test4/stack_user.yaml
image: 1-BP-1-CLUSTER-1-DISK-novelloshelldemo


#### Delete the image files which are not supposed to be available on disk
cd /mnt/NovelloShell/PROJECTS/IMAGES-demo
rm -f `ls | grep 0-DISK`

#### Switch to an empty directory e.g. samplerun
mkdir samplerun; cd samplerun
generate-image-files.sh
(Make sure to set appropriate path or copy the script in appropriate path to be able to run it from samplerun directory)

#### Verify images files are created with appropriate content in it
ll images_*

python3 /path/to/generateData.py
#### Verify the table and action file are generated with appropriate contents.

sh /path/to/actData.sh

#### Verify corrective action is taken i.e. missing images uploaded to cluster, missing backup downloaded to disk, etc.

#### Create new empty directory samplerun2 and re-run the scripts in that directory
mkdir samplerun2; cd samplerun2
/path/to/generate-image-files.sh
python3 /path/to/generateData.py
sh /path/to/actData.sh

#### Verify the corrective actions taken by earlier run of actData.sh script is considered and now the images on cluster and backup disk are in place.
#### Ideal scenario when no corrective action is required would be - ALERT.txt ImageDelete.txt ImageMissing-Cluster.txt ImageMissing-Disk.txt are empty and ALLGOOD.txt file has name of the images being used.


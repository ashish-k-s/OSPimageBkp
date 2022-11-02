CONFIGFILE="/etc/novelloshell.cfg"

if [ ! -f "$CONFIGFILE" ]
then
echo -e "ERROR: $CONFIGFILE does not exist"
exit 1
fi

IMGBKPATH=$(grep IMGBKPATH $CONFIGFILE  | grep -v ^#)
TAG=$(grep TAG $CONFIGFILE  | grep -v ^#)

eval $TAG
eval $IMGBKPATH

if [ -z "$TAG" ]
then
echo TAG is not set
exit 1
fi

if [ -z "$IMGBKPATH" ]
then
echo IMGBKPATH is not set
exit 1
fi

ls -1 $IMGBKPATH | grep -i $TAG | sort -n > images_on_disk.txt


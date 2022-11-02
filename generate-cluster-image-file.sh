CONFIGFILE="/etc/novelloshell.cfg"

if [ ! -f "$CONFIGFILE" ]
then
echo -e "ERROR: $CONFIGFILE does not exist"
exit 1
fi

ADMINRC=$(grep ADMINRC $CONFIGFILE  | grep -v ^#)
TAG=$(grep TAG $CONFIGFILE  | grep -v ^#)

eval $TAG
eval $ADMINRC

source $ADMINRC
openstack image list -c Name -f value | grep -i $TAG | sort -n > images_on_cluster.txt


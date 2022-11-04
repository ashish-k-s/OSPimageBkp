CONFIGFILE="/etc/novelloshell.cfg"

if [ ! -f "$CONFIGFILE" ]
then
echo -e "ERROR: $CONFIGFILE does not exist"
exit 1
fi

BPSDIR=$(grep BPSDIR $CONFIGFILE  | grep -v ^#)
TAG=$(grep TAG $CONFIGFILE  | grep -v ^#)
eval $BPSDIR
eval $TAG

cd $BPSDIR

grep -h image $(find . | grep -v './dev-' | grep -v './test-' | grep -w "stack_user.yaml$")  | sed 's/^[[:blank:]]*//;s/[[:blank:]]*$//' | grep ^image | cut -d : -f2 | tr -d '"' | tr -d "'" | sort -n | uniq | grep -i $TAG | sed 's/^[[:blank:]]*//;s/[[:blank:]]*$//' > $OLDPWD/images_in_bps.txt


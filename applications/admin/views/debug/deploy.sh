#!/bin/sh
##	$Id: deploy.sh,v 1.2 2011/12/29 21:58:24 weiwang Exp $;
##
##	Shell script to deploy files to NetApps.

DIRS=""
BINFILES="breakpoints.html          index.html                interact.html"
ETCFILES=""
LIBFILES=""

export IMHOST1=${IMHOST1:-'uhnetmanspr1.umhs.med.umich.edu'}
export IMHOST2=${IMHOST2:-'uhnetmanspr4.umhs.med.umich.edu'}
export IMHOST3=${IMHOST3:-'uhnetmanspr5.umhs.med.umich.edu'}
export IMapRDIR="${IMapRDIR:-'/cygdrive/e/Program Files (x86)/InterMapper/InterMapper Settings/Tools'}"

for xhost in "$IMHOST1" "$IMHOST2" "$IMHOST3" ; do
	if [ "$xhost" = "-" ]; then continue; fi
	echo ====: Deploying web2py to "${USER}@$xhost:$IMapRDIR/"
	rsync -auvz $@ --rsh=ssh $FILES "${USER}@$xhost:$IMapRDIR/"
done

export NSSHOST1=${NSSHOST1:-'nssapp-prod01.med.umich.edu'}
export NSSHOST2=${NSSHOST2:-'nssapp-prod06.med.umich.edu'}
export EMPFHOST1=${EMPFHOST1:-'empfapp-prod01.med.umich.edu'}
export EMPFHOST2=${EMPFHOST2:-'empfapp-prod02.med.umich.edu'}
export EMPFBIN=${EMPFBIN:-'/opt/miops/web2py/applications/admin/views'}/${SUBDIR:-debug}
export EMPFLIB=${EMPFLIB:-'/opt/miops/lib/python'}
export EMPFETC=${EMPFETC:-'/opt/miops/etc'}
export SPLUNKUSER=${SPLUNKUSER:-"splunk-admin"}

for xhost in "$EMPFHOST1" "$EMPFHOST2" "$EMPFHOST3" ; do
    if [ "$xhost" = "-" ]; then continue; fi
    chgrp www $BINFILES $ETCFILES $LIBFILES
    chmod 0660 $BINFILES $ETCFILES $LIBFILES
    if [ "$BINFILES" != "" ]; then
	echo ====: Deploying web2py to "${USER}@$xhost:$EMPFBIN/"
	rsync -auvz $@ --rsh=ssh $BINFILES "${USER}@$xhost:$EMPFBIN/"
    fi
    if [ "$ETCFILES" != "" ]; then
	echo ====: Deploying web2py to "${USER}@$xhost:$EMPFETC/"
	rsync -auvz $@ --rsh=ssh $ETCFILES "${USER}@$xhost:$EMPFETC/"
    fi
    if [ "$LIBFILES" != "" ]; then
	echo ====: Deploying web2py to "${USER}@$xhost:$EMPFLIB/"
	rsync -auvz $@ --rsh=ssh $LIBFILES "${USER}@$xhost:$EMPFLIB/"
    fi
done

for xd in $DIRS; do
	export SUBDIR="$xd"
	( cd $xd && [ -x ./deploy.sh ] && ./deploy.sh "$@" )
done

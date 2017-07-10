#!/bin/sh
##	$Id: deploy.sh,v 1.2 2011/12/29 21:58:24 weiwang Exp $;
##
##	Shell script to deploy files to NetApps.

DIRS="applications gluon"
BINFILES="	logging.conf	miops.py	modpythonhandler.py
		routes.py	run-18443.sh	web2py.py
	VERSION"
ETCFILES=""
LIBFILES=""

export IMHOST1=${IMHOST1:-'uhnetmanspr1.umhs.med.umich.edu'}
export IMHOST2=${IMHOST2:-'uhnetmanspr4.umhs.med.umich.edu'}
export IMHOST3=${IMHOST3:-'uhnetmanspr5.umhs.med.umich.edu'}
export IMapRDIR="${IMapRDIR:-'/cygdrive/e/Program Files (x86)/InterMapper/InterMapper Settings/Tools'}"
export NSSUSER=${USER}

for xhost in "$IMHOST1" "$IMHOST2" "$IMHOST3" ; do
	if [ "$xhost" = "-" ]; then continue; fi
	echo ====: Deploying web2py to "${NSSUSER}@$xhost:$IMapRDIR/"
	rsync -auvz $@ --rsh=ssh $FILES "${NSSUSER}@$xhost:$IMapRDIR/"
done

export NSSHOST1=${NSSHOST1:-'nssapp-prod01.med.umich.edu'}
export NSSHOST2=${NSSHOST2:-'nssapp-prod06.med.umich.edu'}
export EMPFHOST1=${EMPFHOST1:-'empfapp-prod01.med.umich.edu'}
export EMPFHOST2=${EMPFHOST2:-'empfapp-prod02.med.umich.edu'}
export EMPFBIN=${EMPFBIN:-'/opt/miops/web2py'}
export EMPFLIB=${EMPFLIB:-'/opt/miops/lib/python'}
export EMPFETC=${EMPFETC:-'/opt/miops/etc'}
export EMPFUSER=${EMPFUSER:-"splunk-admin"}

for xhost in "$EMPFHOST1" "$EMPFHOST2" "$EMPFHOST3" ; do
    if [ "$xhost" = "-" ]; then continue; fi
    chgrp www $BINFILES $ETCFILES $LIBFILES
    chmod 0660 $LIBFILES $ETCFILES $BINFILES
    if [ "$BINFILES" != "" ]; then
	echo ====: Deploying web2py to "${EMPFUSER}@$xhost:$EMPFBIN/"
	rsync -auvz $@ --rsh=ssh $BINFILES "${EMPFUSER}@$xhost:$EMPFBIN/"
    fi
    if [ "$ETCFILES" != "" ]; then
	echo ====: Deploying web2py to "${EMPFUSER}@$xhost:$EMPFETC/"
	rsync -auvz $@ --rsh=ssh $ETCFILES "${EMPFUSER}@$xhost:$EMPFETC/"
    fi
    if [ "$LIBFILES" != "" ]; then
	echo ====: Deploying web2py to "${EMPFUSER}@$xhost:$EMPFLIB/"
	rsync -auvz $@ --rsh=ssh $LIBFILES "${EMPFUSER}@$xhost:$EMPFLIB/"
    fi
done

for xd in $DIRS; do
	export SUBDIR="$xd"
	( cd $xd && [ -x ./deploy.sh ] && ./deploy.sh "$@" )
done

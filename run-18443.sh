if [ "$1" = "" ]; then
	# VBOX = 10.17.84.21
	IP=`python -c 'import c9r.net.l3 as l3; print(l3.get_lan_ip())'`
else
	IP="$1"
fi
if [ "$2" = "" ]; then
	PORT=18443
else
	PORT="$2"
fi

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/bin/X11:/usr/X11R6/bin:/usr/games:/usr/lib64/jvm/jre/bin:/usr/lib/mit/bin:/usr/lib/mit/sbin
export PYTHONHOME=/usr:/usr/local
export PYTHONPATH=${PYTHONPATH}:/opt/miops/lib/python:/usr/local/lib64/python2.6/site-packages
env python ./web2py.py -p "${PORT}" -i "${IP}" -a "<recycle>"\
	--ssl_certificate=ssl/server.cer\
	--ssl_private_key=ssl/server.key

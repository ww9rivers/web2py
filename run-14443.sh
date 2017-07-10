if [ "$1" = "" ]; then
	# VBOX = 10.17.84.21
	IP=`python -c 'import c9r.net.l3 as l3; print(l3.get_lan_ip())'`
else
	IP="$1"
fi
if [ "$2" = "" ]; then
	PORT=14443
else
	PORT="$2"
fi
PYTHONPATH=/home/weiwang/oss/netopy \
env python ./web2py.py -p "${PORT}" -i "${IP}" -a "<recycle>"\
	--ssl_certificate=ssl/server.cer\
	--ssl_private_key=ssl/server.key

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to manually start the "miops" portal site on HTTPS port 18443.
#

import os
import sys

if '__file__' in globals():
    path = os.path.dirname(os.path.abspath(__file__))
elif hasattr(sys, 'frozen'):
    path = os.path.dirname(os.path.abspath(sys.executable))  # for py2exe
else:  # should never happen
    path = os.getcwd()
os.chdir(path)

sys.path += [ p for p in [path,
                          os.path.join(os.environ['HOME'], 'oss', 'netopy'),
                          os.path.join(os.sep, 'opt', 'miops', 'lib', 'python')
                          ] if os.path.isdir(p) and not p in sys.path]

# Setup defaults for manual miops run:
no_ip = True
no_port = True
no_cert = True
no_key = True
no_pw = True
for arg in sys.argv:
    if arg == '-i' or arg.startswith('--ip='):
        no_ip = False
    elif arg == '-p' or arg.startswith('--port='):
        no_port = False
    elif arg.startswith('--ssl_certificate='):
        no_cert = False
    elif arg.startswith('--ssl_private_key='):
        no_key = False
    elif arg == '-a' or arg.startswith('--password='):
        no_pw = False
if no_ip:
    from c9r.net import l3
    ip = l3.get_lan_ip()
    if not ip is None:
        sys.argv += [ '-i', ip ]
if no_port:
    sys.argv += [ '-p', '18443' ]
if no_cert:
    sys.argv += [ '-c', '/opt/miops/etc/ssl/midash.cer' ]
if no_key:
    sys.argv += [ '-k', '/opt/miops/etc/ssl/midash.key' ]
if no_pw:
    sys.argv += [ '-a', '<recycle>' ]

# import gluon.import_all # <-------------------- This should be uncommented for py2exe.py
import gluon.widget

# Start Web2py and Web2py cron service!
if __name__ == '__main__':
    try:
        from multiprocessing import freeze_support
        freeze_support()
    except:
        sys.stderr.write('Sorry, -K only supported for python 2.6-2.7\n')
    if os.environ.has_key("COVERAGE_PROCESS_START"):
        try:
            import coverage
            coverage.process_startup()
        except:
            pass
    gluon.widget.start(cron=True)

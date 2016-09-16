import os
from saml2.entity_category.edugain import COC
from saml2 import BINDING_HTTP_REDIRECT
from saml2 import BINDING_HTTP_POST
from saml2.saml import NAME_FORMAT_URI

try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None


if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary(["/opt/local/bin","/usr/local/bin"])
else:
    xmlsec_path = '/usr/local/bin/xmlsec1'

# Make sure the same port number appear in service_conf.py
BASE = "https://wsdf0040.umhs.med.umich.edu:18443"
APPNAME = 'midash'
PATH = os.path.join('/home/weiwang/oss/web2py/applications', APPNAME, "private")
CONFIG = {
    "entityid": "{0}/{1}/static/sp.xml".format(BASE, APPNAME),
    'entity_category': [COC],
    "accepted_time_diff": 5, # very important
    "description": "miops-dev",
    "service": {
        "sp": {
            "endpoints": {
                "assertion_consumer_service": [
                    ("%s/%s/default/user/login" % (BASE, APPNAME), BINDING_HTTP_REDIRECT),
                    ],
                }
            },
        },
    "key_file": os.path.join(PATH, 'pki', 'mykey.pem'),
    "cert_file": os.path.join(PATH, 'pki', 'mycert.pem'),
    "xmlsec_binary": xmlsec_path,
    "metadata": {"local": [os.path.join(PATH,"idp.xml")]},
    "name_form": NAME_FORMAT_URI,
    }

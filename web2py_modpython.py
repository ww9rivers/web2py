# $Id: web2py_modpython.py,v 1.2 2014/05/21 19:49:43 weiwang Exp $

from mod_python import apache
import modpythonhandler

def handler(req):
    req.subprocess_env['PATH_INFO'] = '/miops/default/index' if req.uri == '/' else req.uri
    ## req.subprocess_env['SCRIPT_URL']
    return modpythonhandler.handler(req)

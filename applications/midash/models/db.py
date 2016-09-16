# -*- coding: utf-8 -*-
#
# Model for midash.

import os
import ext
from gluon import current
from storage import Storage
from gluon.tools import Auth, Crud, Service, PluginManager, prettydate

## Mandate SSL/HTTPS:
request.requires_https()

appconf = ext.Appconf('appconf', '.')
db = DAL(appconf.db)

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

#  To work with Angular JS: Use these brackets in views rather than {{ }}
response.delimiters = ('{<','>}')

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# To store session information in db:
# http://web2py.com/books/default/chapter/29/04/the-core#session
session.connect(request, response, db, masterapp=None)

auth = Auth(db)
current.auth = auth
crud, service, plugins = Crud(db), Service(), PluginManager()

# Assign application logger to a global var  
logger = ext.configured_logger()
current.logger = logger

appconf.reset_tag() # The tag is set every time the app's "default/view" function is called.

if (request.application == 'midash' and
    request.controller == 'default' and
    request.function == 'user' and
    request.args[0] == 'login'):
    for xk, xv in request.vars.iteritems():
        if xk == 'password':
            xv = '<password is longer than 4>' if len(xv) > 4\
                else '<password is not longer than 4>'
        logger.debug("LOGIN_DEBUG: request.vars[%s] = (%s)" % (xk, format(xv)))
    for xk, xv in request.cookies.iteritems():
        logger.debug("LOGIN_DEBUG: request.cookie[%s] = (%s)" % (xk, format(xv)))

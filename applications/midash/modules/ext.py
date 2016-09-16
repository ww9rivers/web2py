# -*- coding: utf-8 -*-
#
# $Id: ext.py,v 1.5 2015/07/28 22:16:40 weiwang Exp $
#
# Module for viewing external app.

import json, os, urllib
import urlparse
import logging, logging.handlers
from gluon.storage import Storage
from gluon import *


def configured_logger(name=None):
    request = current.request
    if name is None:
        name = request.application
    logger = logging.getLogger(name)
    if (len(logger.handlers) == 0):
        # This logger has no handlers, so we can assume it hasn't yet been configured
        # (Configure logger)

        # Create default handler
        if request.env.web2py_runtime_gae:
            # Create GAEHandler
            handler = GAEHandler()
        else:
            # Create RotatingFileHandler
            formatter="%(asctime)s %(levelname)s %(process)s %(thread)s %(funcName)s():%(lineno)d %(message)s"
            handler = logging.handlers.RotatingFileHandler(os.path.join(request.folder,'private/app.log'),maxBytes=1024,backupCount=2)
            handler.setFormatter(logging.Formatter(formatter))
        handler.setLevel(logging.DEBUG)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # Test entry:
        logger.debug(name + ' logger created')
    else:
        # Test entry:
        logger.debug(name + ' already exists')
    return logger


class Appconf(Storage):
    def __init__(self, app=None, cat='config'):
        '''Returns configuration for a dashboard app.

        @param /request/  Current web2py request.
        @param /app/      Name of the external app.
        @param /cat/      Subcategory: subfolder in 'private' -- config, public, etc.
        '''
        fn = os.path.join(current.request.folder,'private',cat,(app or 'default')+'.json')
        Storage.__init__(self, json.load(open(fn, 'r')))
        self.logger = configured_logger()
        self.logger.debug("App config loaded: ({0})".format(fn))

    def dashbar(self, logoff=None, appid=None):
        '''Build and return the dashbar.
        '''
        logout = logoff or self.logout or URL('default', 'user', args='logout')
        user = current.auth.user
        self.logger.debug("logout=({0})".format(logout))
        self.logger.debug("User=({0})".format(user))
        authed = logout != None and user != None
        # Display something like: "user: weiwang | logoff"
        return DIV(('user: %s |'%(user['username'])) if authed else '',
                   A(current.T('MCIT Dashboards'),_href='/'),
                   SPAN(XML('&laquo;'+appid.upper()) if appid else '', _class='id'), ' |',
                   A(current.T('logoff'),_href=logout) if authed\
                       else A(current.T('logon'),_href=URL('default','user/login')),
                   _class='dashbar')

    def reset_tag(self, tag=None):
        '''Add cookie for dashboard reverse-proxy in Apache.
        '''
        current.response.cookies['midash_view_tag'] = tag
        current.response.cookies['midash_view_tag']['path'] = '/en-US'
        self.logger.debug("reset_tag(%s)" % (format(tag)))

    def view(self, layout='extapp.html', cat='config'):
        '''Default view of an app: Login required.

        Parameters:

        /layout/        HTML layout template to use for the page.
        /cat/           Category of embedded app: Default is "config", which
                        requires user logon; The other category is "public",
                        which does not require logon.
        '''
        current.response.view = layout
        request = current.request
        app = request.vars.get('app')
        if app is None:
            # HACK!!! -- Try to remedy a NetIQ bug which quotes the parameters:
            # Reference: globals.Request.parse_get_vars()
            qstr = request.env.query_string
            self.logger.debug('Trying parsing app from {0}'.format(qstr))
            try:
                dget = urlparse.parse_qs(qstr, keep_blank_values=1)
                get_vars = Storage(dget)
                for (key, value) in get_vars.iteritems():
                    if isinstance(value, list) and len(value) == 1:
                        get_vars[key] = value[0]
                app = get_vars.get('app')
                request.vars.update(get_vars)
            except IndexError:
                self.logger.error('No app specified: {0}'.format(request.env.path_info))
                pass
        self.logger.debug('{0}/{1}/{2}?{3}'.format(request.application, request.controller, request.function, app))
        conf = Appconf(app, cat)
        ifconf = conf.iframe
        appid = ifconf.get('id')
        # weiwang 2014-02-11: Temporary rollback.
        spweb = ifconf.get('splunkweb')
        appsrc = ifconf.get('app')
        if spweb is None:
            # Setup for Apache reverse proxying:
            appsrc = urllib.urlencode(appsrc) if isinstance(appsrc, dict) else urllib.quote(appsrc)
            if appid:
                appsrc = '/_/%s/%s'%(appid, appsrc)
                self.reset_tag(appid)
        else:
            # In this case, use configured (insecure) login - Ideally, use one time password. 
            appsrc = '%s%s&%s' % (spweb.url, spweb.login, urllib.urlencode(appsrc))
        iframe = IFRAME(_src=appsrc, _scrolling="no", _style=ifconf['style'])
        return dict(dashbar=self.dashbar(conf.logout, appid),
                    content=iframe,
                    extra_js = [ 'midash.js' ],
                    height=self.get('height', None),
                    title=self.get('title', False),
                    conf=self)

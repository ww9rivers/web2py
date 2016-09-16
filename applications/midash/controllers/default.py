# -*- coding: utf-8 -*-
##
## This program is licensed under the GPL v3.0, which is found at the URL below:
##	http://opensource.org/licenses/gpl-3.0.html
##
## Copyright (c) 2011 Regents of the University of Michigan.
## All rights reserved.
##
## Redistribution and use in source and binary forms are permitted
## provided that this notice is preserved and that due credit is given
## to the University of Michigan at Ann Arbor. The name of the University
## may not be used to endorse or promote products derived from this
## software without specific prior written permission. This software
## is provided ``as is'' without express or implied warranty.

'''
Default controller for this app:
-  index is the default action of any application
-  user is required for authentication and authorization
-  download is for downloading files uploaded in the db (does streaming)
-  call exposes all registered services (none by default)
'''
from itertools import izip


#@auth.requires(session.saml2_info.get('username')!='')
@auth.requires_login()
def index():
    """
    Build HTML contents for an <iframe> embedded dashboard.
    """
    ref = request.env.get('http_referer')
    portal = URL('apps', 'index')
    if ref is None:
        redirect(portal)
    app = ref.split('?')
    if len(app) < 2:
        redirect(portal)
    kv = iter(app[1].split('='))
    redir = dict(izip(kv, kv)).get('_next')
    redirect(redir if redir else portal)

@auth.requires_login()
def view():
    '''Default view of an app: Login required.

    Here, /appconf/ is a global from models/db.py configuring this app.
    '''
    return appconf.view()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    form=auth()
    if request.args(0)=='login':
        session.proxy_session = None
        if not 'register' in auth.settings.actions_disabled:
            form.add_button(T('Register'),URL(args='register'),_class='btn')
        if not 'request_reset_password' in auth.settings.actions_disabled:
            form.add_button(T('Lost Password'),URL(args='request_reset_password'),_class='btn')
        # Give the form a 'formname' AND a 'name' attribute for NetIQ Access Manager form fill:
        if form.__getitem__('_formname') == None:
            form['_formname'] = 'login'
        if form.__getitem__('_name') == None:
            form['_name'] = 'login'
        # DEBUGGING for p-miops: Force the login form action.
        if form['_action'] == "#":
            form['_action'] = URL(args=request.args)
    elif request.args(0)=='logout':
        session.proxy_session = None

    return dict(form=form, title="UMHS Level-2", height='200%')

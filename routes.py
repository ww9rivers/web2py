# -*- coding: utf-8 -*-

'''
Doctesting for routes.py.

Use filter_url() to test incoming or outgoing routes;
filter_err() for error redirection.

filter_url() accepts overrides for method and remote host:
filter_url(url, method='get', remote='0.0.0.0', out=False)

filter_err() accepts overrides for application and ticket:
filter_err(status, application='app', ticket='tkt')

>>> import sys
>>> import os
>>> path = os.path.dirname(os.path.abspath(__file__))
>>> sys.path = [path] + [p for p in sys.path if not p == path]
>>> os.chdir(path)
>>> import gluon.main
>>> from gluon.rewrite import load, filter_url, filter_err, get_effective_router
>>> load(routes=os.path.basename(__file__))
...

#>>> os.path.relpath(filter_url('http://domain.com/favicon.ico'))
#'applications/miops/static/favicon.ico'

>>> filter_url('http://domain.com/abc')
'/abc/default/index'
>>> filter_url('http://domain.com/index/abc')
'/index/abc/index'

#>>> filter_url('http://domain.com/midash/abc.css')
#'/midash/default/abc.css'

>>> filter_url('http://domain.com/default/index/abc')
'/default/index/abc'
>>> filter_url('http://domain.com/default/index/a bc')
'/default/index/a_bc'

>>> filter_url('https://domain.com/app/ctr/fcn', out=True)
'/app/ctr/fcn'
>>> filter_url('https://domain.com/welcome/ctr/fcn', out=True)
'/welcome/ctr/fcn'
>>> filter_url('https://domain.com/welcome/default/fcn', out=True)
'/welcome/default/fcn'
>>> filter_url('https://domain.com/welcome/default/index', out=True)
'/welcome/default/index'
>>> filter_url('https://domain.com/welcome/appadmin/index', out=True)
'/welcome/appadmin/index'
>>> filter_url('http://domain.com/welcome/default/fcn?query', out=True)
'/welcome/default/fcn?query'
>>> filter_url('http://domain.com/welcome/default/fcn#anchor', out=True)
'/welcome/default/fcn#anchor'
>>> filter_url('http://domain.com/welcome/default/fcn?query#anchor', out=True)
'/welcome/default/fcn?query#anchor'

>>> filter_err(200)
200
>>> filter_err(399)
399
>>> filter_err(400)
400

>>> filter_url('http://domain.com/')
'/midash/portal/index'
>>> filter_url('http://domain.com/miops/apps?app=abc')
'/miops/apps/index ?app=abc'
>>> filter_url('http://domain.com/midash/default/user/login?_next=/midash')
"/midash/default/user ['login'] ?_next=/midash"
>>> filter_url('http://domain.com/midash/user/login?_next=/midash')
'/midash/user/login ?_next=/midash'

>>> filter_url('http://domain.com/miops/xyz/abc')
'/miops/xyz/abc'
>>> filter_url('http://domain.com/midash/xyz/abc')
'/midash/xyz/abc'
>>> filter_url('http://domain.com/midash/admin/access')
'/midash/admin/access'
'''

#  Based on web2py/routes.example.py.

default_application='midash'

routes_in = (
    #   Logout user in case not running behind the Access Manager:
    ('/AGLogout', '/midash/default/user/logout'),

    #   Routes "/":
    ('/', '/midash/apps'),

    #   Reroute favicon and robots:
    ('/favicon.ico', '/midash/static/favicon.ico'),
    ('/robots.txt', '/midash/static/robots.txt'),

    #   Routing for splunkjs:
    ('/splunkjs/$anything', '/$app/static/splunkjs/$anything'),

    #   Proxying to Splunk:
    #('/splunk/(?P<any>.*)', '/midash/proxy/splunk.html'),
    #('/en-US/(?P<any>.*)', '/midash/proxy/splunk.html'),
)

logging = 'debug'

if __name__ == '__main__':
    import doctest
    doctest.testmod()

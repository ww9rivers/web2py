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


@auth.requires_login()
def requires_authorization(groups=["splunk-admin"]):
    '''Decorator to require login, as well as certain authorization, e.g., group
    membership.'''
    def decorator(action):
        def f(*a, **b):
            return action(*a, **b)

        f.__doc__ = action.__doc__
        f.__name__ = action.__name__
        f.__dict__.update(action.__dict__)
        return f

    return decorator

@requires_authorization()
def settings():
    return dict()


@requires_authorization()
def access():
    return dict()

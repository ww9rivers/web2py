import os

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = appconf['mail']['server']
mail.settings.sender = appconf['mail']['sender']
mail.settings.login = appconf['mail']['login']

## configure auth policy
if appconf['sso'] == 'saml2':
    from gluon.contrib.login_methods.saml2_auth import Saml2Auth                             
    ## configure auth policy
    auth.settings.registration_requires_verification = False
    auth.settings.registration_requires_approval = False
    auth.settings.reset_password_requires_verification = True

    # :maps: is extracted from debug output from NetIQ:
    auth.settings.login_form=Saml2Auth(
        config_file = os.path.join(request.folder,'private','sp_conf'),
        maps=dict(
            username=lambda v: v['/UserAttribute[@ldap:targetAttribute="cn"]'][0],
            email=lambda v: v['/UserAttribute[@ldap:targetAttribute="mail"]'][0],
            user_id=lambda v: v['/UserAttribute[@ldap:targetAttribute="cn"]'][0]
            ))

    auth.settings.actions_disabled = \
        ['register', 'change_password', 'request_reset_password']
else: # LDAP
    auth.settings.create_user_groups = False
    auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username','profile']

    #    you don't have to remember me
    auth.settings.remember_me_form = False

    # ldap authentication and not save password on web2py
    from gluon.contrib.login_methods.ldap_auth import ldap_auth
    auth.settings.login_methods = [ ldap_auth(**(appconf['ldap'])) ]
    auth.settings.logout_next = URL(r=request, c='apps', f='index')

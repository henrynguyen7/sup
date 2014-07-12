
# -*- coding: utf-8 -*-

from gluon.tools import Crud, Service, PluginManager
crud, service, plugins = Crud(db), Service(), PluginManager()


""" GENERAL """

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

#  Reloads modules on every request... remove from production
from gluon.custom_import import track_changes
if request.is_local:
    track_changes(True)


## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'


""" AUTH """

###
### Auth customizations
###
auth.settings.password_min_length = 8
auth.settings.create_user_groups = False
auth.settings.login_next = URL('dashboard', 'index')
auth.settings.logout_next = URL('default', 'index')
auth.settings.profile_next = URL('index')
auth.settings.register_next = URL('dashboard', 'index')
auth.settings.retrieve_username_next = URL('index')
auth.settings.retrieve_password_next = URL('index')
auth.settings.change_password_next = URL('index')
auth.settings.request_reset_password_next = URL('user', args='login')
auth.settings.reset_password_next = URL('user', args='login')
auth.settings.verify_email_next = URL('user', args='login')

# The two options below allow the user to login immediately after registration but will require them to confirm in their email before logging in again.
auth.settings.registration_requires_verification = False
auth.settings.login_after_registration = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.messages.verify_email = 'Click on the link http://' + request.env.http_host + URL(r=request,c='default',f='user',args=['verify_email']) + '/%(key)s to verify your email'
auth.messages.reset_password = 'Click on the link http://' + request.env.http_host + URL(r=request,c='default',f='user',args=['reset_password']) + '/%(key)s to reset your password'


""" LOGGING """
import logging
logger = logging.getLogger(request.application)
logger.setLevel(logging.DEBUG)


""" CURRENT """
## Assign db and logger to current to allow for access from modules (from: http://stackoverflow.com/questions/11959719/web2py-db-is-not-defined)
from gluon import current
current.db = db
current.logger = logger
current.auth = auth
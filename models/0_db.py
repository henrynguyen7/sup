
# -*- coding: utf-8 -*-

import json
import os

from gluon.tools import Auth

""" DB """

# load mysql login credentials from resource file
resource_file = os.path.join(request.folder, "private", "resources.json")
with open(resource_file) as resource:
    resource_data = json.load(resource)

mysql_username, mysql_password, mysql_database, mysql_host, mysql_port = (
    resource_data.get("mysql").get("username"),
    resource_data.get("mysql").get("password"),
    resource_data.get("mysql").get("database"),
    resource_data.get("mysql").get("host"),
    resource_data.get("mysql").get("port")
)

# TODO: Set migrate=False when db development is complete
db = DAL('mysql://' + mysql_username + ':' + mysql_password + '@' + mysql_host + ':' + mysql_port + '/' + mysql_database, pool_size=3, check_reserved=['mysql'], migrate=True)
# The "migrate=False" parameter prevents automatic modification of schema if it differs from its definition here. Schema mods should be done deliberately and manually.

auth = Auth(db)

########################################################################
# Reference: valid web2py field types
# field type                default field validators
# string                    IS_LENGTH(length) default length is 512
# text                      IS_LENGTH(65536)
# blob                      None
# boolean                   None
# integer                   IS_INT_IN_RANGE(-1e100, 1e100)
# double                    IS_FLOAT_IN_RANGE(-1e100, 1e100)
# decimal(n,m)              IS_DECIMAL_IN_RANGE(-1e100, 1e100)
# date                      IS_DATE()
# time                      IS_TIME()
# datetime                  IS_DATETIME()
# password                  None
# upload                    None
# reference <table>         IS_IN_DB(db,table.field,format)
# list:string               None
# list:integer              None
# list:reference <table>    IS_IN_DB(db,table.field,format,multiple=True)
# json                      IS_JSON()
# bigint                    None
# big-id                    None
# big-reference             None
########################################################################

# Field(name, 'string', length=None, default=None,
#       required=False, requires='<default>',
#       ondelete='CASCADE', notnull=False, unique=False,
#       uploadfield=True, widget=None, label=None, comment=None,
#       writable=True, readable=True, update=None, authorize=None,
#       autodelete=False, represent=None, compute=None,
#       uploadfolder=os.path.join(request.folder,'uploads'),
#       uploadseparate=None,uploadfs=None)

## define extra fields for auth_* tables
auth.settings.extra_fields['auth_user'] = [
    Field('device_platform', 'string', readable=False, writable=False),
    Field('gcm_id', 'string', readable=False, writable=False),
    Field('apn_id', 'string', readable=False, writable=False),
    Field('sup_count', 'integer', uploadfield=False, readable=False, writable=False, default=0),
    Field('login_count', 'integer', uploadfield=False, readable=False, writable=False, default=0),
    Field('logged_in_on', 'datetime', uploadfield=False, readable=False, writable=False, default=None),
    auth.signature
]

auth.define_tables(username=True, signature=True)

db.auth_user.first_name.readable = db.auth_user.first_name.writable = False
db.auth_user.last_name.readable = db.auth_user.last_name.writable = False
db.auth_user.email.readable = db.auth_user.email.writable = False

###
### Settings Tables
###
db.define_table(
    'system_settings',
    Field('name', 'string', readable=False, writable=False),
    Field('description', 'string', readable=False, writable=False),
    Field('value', 'string', readable=False, writable=False)
)
db.system_settings.id.readable = db.system_settings.id.writable = False

db.define_table(
    'contacts',
    Field('auth_user_id', 'reference auth_user', readable=False, writable=False),
    Field('name', 'string', readable=False, writable=False),
    Field('created_on', 'datetime', notnull=True, uploadfield=False, readable=False, writable=False, default=request.now),
    Field('updated_on', 'datetime', notnull=True, uploadfield=False, readable=False, writable=False, default=request.now, update=request.now)
)
db.contacts.id.readable = db.contacts.id.writable = False

db.define_table(
    'friends',
    Field('auth_user_id_1', 'reference auth_user', readable=False, writable=False),
    Field('auth_user_id_2', 'reference auth_user', readable=False, writable=False),
)
db.friends.id.readable = db.friends.id.writable = False
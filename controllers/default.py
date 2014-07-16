"""
Controller for /default service.

Author: Henry Nguyen (henry@dxconcept.com)
"""

# -*- coding: utf-8 -*-


def index():

    def login_onaccept(form):
        db(db.auth_user.id==auth.user.id).update(login_count=db.auth_user.login_count+1)
        return dict()

    def register_onaccept(form):
        auth.add_membership(role='user')
        db.user_settings.insert(auth_user_id=auth.user.id,)
        db(db.auth_user.id == auth.user.id).update(
            device_platform=request.vars.device_platform,
            gcm_id=request.vars.gcm_id,
            apn_id=request.vars.apn_id,
        )

    auth.settings.login_onaccept = login_onaccept
    auth.settings.register_onaccept = register_onaccept

    form_login = auth()
    # Two lines below are so we can select it with Javascript
    form_login['_id'] = 'form_login'
    form_login.custom.begin = XML("<" + form_login.tag + " " + form_login._xml()[0] +">")
    form_login.custom.widget.username['_placeholder'] = "USERNAME"
    form_login.custom.widget.password['_placeholder'] = "PASSWORD"

    form_register = auth.register()
    # Two lines below are so we can select it with Javascript
    form_register['_id'] = 'form_registration'
    form_register.custom.begin = XML("<" + form_register.tag + " " + form_register._xml()[0] +">")
    form_register.custom.widget.username['_placeholder'] = "CHOOSE USERNAME"
    form_register.custom.widget.password['_placeholder'] = "CHOOSE PASSWORD"

    return dict(
        form_login=form_login,
        form_register=form_register,
    )


def user():
    redirect(URL('index'))


def terms():
    return dict(content=None)


def privacy():
    return dict(content=None)
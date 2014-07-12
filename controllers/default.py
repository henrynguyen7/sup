"""
Controller for /default service.

Author: Henry Nguyen (henry@dxconcept.com)
"""

# -*- coding: utf-8 -*-

def index():

    def login_onaccept(form):
        db(db.auth_user.id==auth.user.id).update(login_count=db.auth_user.login_count+1)
        return dict()

    auth.settings.login_onaccept = login_onaccept
    form = auth()
    form['_id'] = 'form_login' # So we can select it with Javascript

    return dict(form=form)


def register():

    def register_onaccept(form):
        auth.add_membership(role='user')
        db.user_settings.insert(
            auth_user_id=auth.user.id,
        )
        db(db.auth_user.id == auth.user.id).update(
            gcm_id=request.vars.gcm_id,
            device_platform=request.vars.device_platform,
        )

    logger.debug(request.vars)

    auth.settings.register_onaccept = register_onaccept
    form = auth.register()
    form['_id'] = 'form_registration' # So we can select it with Javascript

    return dict(form=form)


def user():
    redirect(URL('index'))
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
        db.user_settings.insert(
            auth_user_id=auth.user.id
        )

    auth.settings.login_onaccept = login_onaccept
    auth.settings.register_onaccept = register_onaccept
    return dict(form=auth())

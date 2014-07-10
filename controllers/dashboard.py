"""
Controller for /dashboard service.

Author: Henry Nguyen (henry@dxconcept.com)
"""

# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL('overview'))


@auth.requires_login()
def overview():
    return dict(message=None)


@auth.requires_login()
def settings():
    return dict(message=None)

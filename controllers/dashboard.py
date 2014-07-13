"""
Controller for /dashboard service.

Author: Henry Nguyen (henry@dxconcept.com)
"""

# -*- coding: utf-8 -*-

from gcmclient import *


def logout():
    auth.logout()


@auth.requires_login()
def index():
    users = db(db.auth_user.device_platform != None).select()
    if request.args:
        result = Utils.send_sup(request.args[0])
        db(db.auth_user.id == request.args[0]).update(sup_count=db.auth_user.sup_count+1) # Increment user's sup_count
        response.flash = 'Sup sent to ' + Utils.get_user(auth_user_id=request.args[0]).get('username') + '!'

    return dict(users=users)


##
## Utils
##
class Utils(object):

    @staticmethod
    def get_user(auth_user_id):
        query = (db.auth_user.id == auth_user_id)
        user = db(query).select().first()
        return user.as_dict() if user else None

    @staticmethod
    def send_sup(recipient_auth_user_id):

        recipient = Utils.get_user(auth_user_id=recipient_auth_user_id)

        if recipient.get('device_platform') == 'Android':

            Utils.send_gcm_message(
                sender_auth_user_id=auth.user.id,
                recipient_auth_user_id=recipient_auth_user_id
            )

        elif user.get('device_platform') == 'iOS':

            # TODO
            pass


    @staticmethod
    def send_gcm_message(sender_auth_user_id, recipient_auth_user_id):

        try:
            resource_file = os.path.join(current.request.folder, "private", "resources.json")
            with open(resource_file) as resource:
                resource_data = json.load(resource)

            API_KEY = resource_data["gcm"]["api_key"]
            gcm = GCM(API_KEY)
            sender = Utils.get_user(auth_user_id=sender_auth_user_id)
            recipient = Utils.get_user(auth_user_id=recipient_auth_user_id)

            multicast = JSONMessage(
                [recipient.get('gcm_id')],
                {"message": "Sup from " + sender.get('username')},
                collapse_key='collapse_key',
                dry_run=False if request.is_local else False
            )

        except Exception, e:
            logger.error(e)

        try:
            # attempt send
            result_multicast = gcm.send(multicast)

            for result in [result_multicast]:

                # nothing to do on success
                for registration_id, msg_id in result.success.items():
                    logger.info("GCM: Successfully sent %s as %s" % (registration_id, msg_id))

                # update your registration ID's
                for registration_id, new_registration_id in result.canonical.items():
                    db(db.device_android.device_id == device_id).validate_and_update(gcm_registration_id=new_registration_id)
                    logger.info("GCM: Updated %s with %s in database" % (registration_id, new_registration_id))

                # probably app was uninstalled
                for registration_id in result.not_registered:
                    db(db.device_android.device_id == device_id).validate_and_update(gcm_registration_id=None)
                    logger.info("GCM: Removed %s from database" % registration_id)

                # unrecoverably failed, these ID's will not be retried
                # consult GCM manual for all error codes
                for registration_id, error_code in result.failed.items():
                    db(db.device_android.device_id == device_id).validate_and_update(gcm_registration_id=None)
                    logger.error("GCM: Removed %s because %s" % (registration_id, error_code))

                # if some registration ID's have recoverably failed
                if result.needs_retry():
                    # construct new message with only failed regids
                    retry_msg = result.retry()
                    # you have to wait before attemting again. delay()
                    # will tell you how long to wait depending on your
                    # current retry counter, starting from 0.
                    logger.info("GCM: Wait or schedule task after %s seconds" % result.delay(retry))
                    # retry += 1 and send retry_msg again

        except GCMAuthenticationError:
            # stop and fix your settings
            logger.error("GCM: Your Google API key is rejected")
        except ValueError, e:
            # probably your extra options, such as time_to_live,
            # are invalid. Read error message for more info.
            logger.error("GCM: Invalid message/option or invalid GCM response")
            logger.error(e.args[0])
        # except Exception:
        #     # General Exception... comment this out to let web2py spit out the entire stacktrace
        #     logger.error("GCM: Exception... something's wrong somewhere...")

        db.commit()

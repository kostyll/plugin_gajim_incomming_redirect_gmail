#-*- coding: utf-8 -*-

try:

    import os
    from collections import namedtuple
    import smtplib


    from common import gajim
    from common import ged

    from plugins import GajimPlugin
    from plugins.helpers import log_calls


    PLAGIN_NAME = "RedirectPlagin"

    config = namedtuple("config", "NOTIFIER_LOGIN NOTIFIER_PASSWORD")(
        NOTIFIER_LOGIN=os.environ.get("NOTIFIER_LOGIN", ""),
        NOTIFIER_PASSWORD=os.environ.get("NOTIFIER_PASSWORD", ""),
    )
    print config


    def notify(email, subj, msg):
        try:
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s
                """ % (config.NOTIFIER_LOGIN, ", ".join(email), subj, msg)
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(config.NOTIFIER_LOGIN, config.NOTIFIER_PASSWORD)
            server.sendmail(config.NOTIFIER_LOGIN, email, message)
            server.close()
            return True
        except Exception as e:
            return False


    class IncommingRedirectPlugin(GajimPlugin):
        
        @log_calls(PLAGIN_NAME)
        def init(self):
            print "calling IncommingRedirectPlugin"
            self.config_dialog = None
            self.active = None
            self.events_handlers = {
                'message-received': (ged.PREGUI2, self.redirect_message,),
                'message': (ged.PREGUI2, self.redirect_message,)
            }


        def redirect_message(self, obj):
            print "called redirect_message"
            if not self.active:
                return

            contact = gajim.contacts.get_contact_from_full_jid(obj.conn.name,
                obj.fjid)
            print contact
            if not contact:
                return

            notify(
                os.environ.get("TARGET_REDIRECTED_EMAIL", ""),
                "new message from %s" % str(contact),
                "")

        @log_calls(PLAGIN_NAME)
        def activate(self):
            self.active = True
            print "ACTIVATED %s" % PLAGIN_NAME

        @log_calls(PLAGIN_NAME)
        def deactivate(self):
            self.active = False
            print "DEACTIVATED %s" % PLAGIN_NAME

except Exception as e:
    print e
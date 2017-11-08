#-*- coding: utf-8 -*-

import os
from collections import namedtuple
import smtplib


from plugins import GajimPlugin
from plugins.helpers import log_calls


PLAGIN_NAME = "RedirectPlagin"

config = namedtuple("config", "NOTIFIER_LOGIN NOTIFIER_PASSWORD")(
	NOTIFIER_LOGIN=os.environ.get("NOTIFIER_LOGIN", ""),
	NOTIFIER_PASSWORD=os.environ.get("NOTIFIER_PASSWORD", ""),
)



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
        log("notified")
        return True
    except Exception as e:
        log_traceback()
        return False


class IncommingRedirectPlugin(GajimPlugin):
	
	@log_calls(PLAGIN_NAME)
	def __init__(self):
		self.config_dialog = None
		self.active = None
		self.events_handlers = {
			'message-received': (self.redirect_message,)
		}

	def redirect_message(self, obj):
		if not self.active:
            return

    	contact = gajim.contacts.get_contact_from_full_jid(obj.conn.name,
            obj.fjid)
        if not contact:
            return

        notify(
        	os.environ.get("TARGET_REDIRECTED_EMAIL", ""),
        	"new message from %s" % str(contact),
        	"")

	@log_calls(PLAGIN_NAME)
    def activate(self):
    	self.active = True

    @log_calls(PLAGIN_NAME)
    def deactivate(self):
        self.active = False

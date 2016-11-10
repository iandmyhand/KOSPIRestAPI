import logging
import pythoncom
import tornado.web
import win32com.client

import settings

from utils.slack import send_message_via_slack

logger = logging.getLogger('tornado.application')


class Xing(tornado.web.RequestHandler):

    class XASessionEventHandler:
        login_state = 0
        result = {
            'code': None,
            'msg': None
        }

        def OnLogin(self, code, msg):
            Xing.XASessionEventHandler.result = {
                'code': code,
                'msg': msg
            }
            if code == '0000':
                Xing.XASessionEventHandler.login_state = 1
                _message = "Succeed to login for Xing."
                logger.info(_message)
            else:
                _message = "Failed to login for Xing."
                logger.info(_message)
                send_message_via_slack('errors', _message)
            logger.info("Result: %s" % str(Xing.XASessionEventHandler.result))

    def login(self):
        sessionInstance = win32com.client.DispatchWithEvents('XA_Session.XASession', Xing.XASessionEventHandler)
        sessionInstance.ConnectServer(settings.HOST, 20001)
        sessionInstance.Login(settings.USERID, settings.PASSWD, settings.CERT_PASSWD, 0, 0)

        while Xing.XASessionEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()
        return sessionInstance

    def get_code_by_name(self, constants, name):
        for _constant in constants:
            if _constant[1] == name:
                return _constant[0]
        return None

    def write_error(self, status_code, **kwargs):
        for _kwarg in kwargs:
            logger.error("%s: %s" % (str(_kwarg), str(kwargs.get(_kwarg))))
        self.write("Unknown error occurred: ")
        self.finish()

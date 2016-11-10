import logging
import pythoncom
import tornado.web
import win32com.client

import settings

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
                logger.info("Succeed to login for Xing.")
                Xing.XASessionEventHandler.login_state = 1
            else:
                logger.info("Failed to login for Xing.")

    def login(self):
        xaSession = win32com.client.DispatchWithEvents('XA_Session.XASession', Xing.XASessionEventHandler)
        xaSession.ConnectServer(settings.HOST, 20001)
        xaSession.Login(settings.USERID, settings.PASSWD, settings.CERT_PASSWD, 0, 0)

        while Xing.XASessionEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()
        return xaSession

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

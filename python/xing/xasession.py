import logging
import pythoncom
import tornado.web
import win32com.client

import settings

from xing.xing import Xing

logger = logging.getLogger('tornado.application')


class XingXASessionGetAccountListHandler(Xing):

    def fetch_data(self):
        xaSession = self.login()
        _result = {
            'accounts': list()
        }
        for i in range(xaSession.GetAccountListCount()):
            _account = xaSession.GetAccountList(i)
            _result['accounts'].append(_account)
        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        
        """
        _result = self.fetch_data()
        self.write(_result)
        self.finish()

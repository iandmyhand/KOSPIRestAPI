import logging
import tornado.web

import settings

from xing.xing import Xing

logger = logging.getLogger('tornado.application')


class XingXASessionGetAccountListHandler(Xing):

    def fetch_data(self):
        sessionInstance = self.login()
        _result = {
            'accounts': list()
        }
        for i in range(sessionInstance.GetAccountListCount()):
            _account = sessionInstance.GetAccountList(i)
            _result['accounts'].append(_account)
        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        
        """
        _result = self.fetch_data()
        self.write(_result)
        self.finish()

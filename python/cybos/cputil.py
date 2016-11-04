import logging
import tornado.web
import win32com.client

logger = logging.getLogger("tornado.application")


class CpCybosIsConnectHandler(tornado.web.RequestHandler):

    _cpCybos = None

    @tornado.web.asynchronous
    def get(self):
        if not self._cpCybos:
            self._cpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        try:
            _is_connect = int(self._cpCybos.IsConnect)
        except Exception as e:
            logger.error(str(e))
            _is_connect = 0
        self.write({"cybosIsConnect": _is_connect})
        self.flush()
        self.finish()


class CpStockCodeGetCountHandler(tornado.web.RequestHandler):

    _cpStockCode = None

    @tornado.web.asynchronous
    def get(self):
        if not self._cpStockCode:
            self._cpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
        self.write({"stockCodeCount": self._cpStockCode.GetCount()})
        self.flush()
        self.finish()

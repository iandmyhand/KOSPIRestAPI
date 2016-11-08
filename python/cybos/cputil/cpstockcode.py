import logging
import tornado.web
import tornado.gen
import win32com.client

from cybos.cybos import Cybos

logger = logging.getLogger("tornado.application")


class CpStockCode(Cybos):

    _hts_instance = None

    def get_hts_instance(self):
        if not self._hts_instance:
            self._hts_instance = win32com.client.Dispatch("CpUtil.CpStockCode")
        return self._hts_instance


class CpStockCodeCodeToNameHandler(CpStockCode):

    def fetch_data(self, code):
        _instance = self.get_hts_instance()
        _result = {
            "name": int(_instance.CodeToName(code))
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        _code = self.get_query_argument("code")
        _result = self.fetch_data(_code)
        self.write(_result)
        self.finish()


class CpStockCodeNameToCodeHandler(CpStockCode):

    def fetch_data(self, name):
        _instance = self.get_hts_instance()
        _result = {
            "code": int(_instance.CodeToName(name))
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        _name = self.get_query_argument("name")
        _result = self.fetch_data(_name)
        self.write(_result)
        self.finish()


class CpStockCodeGetCountHandler(CpStockCode):

    def fetch_data(self):
        _instance = self.get_hts_instance()
        _result = {
            "stockCodeCount": int(_instance.GetCount())
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        _result = self.fetch_data()
        self.write(_result)
        self.finish()

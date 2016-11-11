import logging
import pythoncom
import tornado.web
import win32com.client

from datetime import datetime

import settings

from xing.xing import Xing

logger = logging.getLogger('tornado.application')


MARKET_CODES = (
    (0, 'ALL'),
    (1, 'KOSPI'),
    (2, 'KOSDAQ')
)


class XingT8430StockCodesHandler(Xing):

    class XAQueryEventHandlerT8430:
        query_state = 0
        result = {
            'code': None
        }

        def OnReceiveData(self, code):
            XingT8430StockCodesHandler.XAQueryEventHandlerT8430.query_state = 1
            XingT8430StockCodesHandler.XAQueryEventHandlerT8430.result['code'] = code
            logger.info("Result: %s" % str(XingT8430StockCodesHandler.XAQueryEventHandlerT8430.result))

    def fetch_data(self, gubun):
        self.login()
        queryInstance = win32com.client.DispatchWithEvents(
            "XA_DataSet.XAQuery", 
            XingT8430StockCodesHandler.XAQueryEventHandlerT8430)
        queryInstance.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t8430.res"
        queryInstance.SetFieldData("t8430InBlock", "gubun", 0, gubun)
        logger.info("Request with %s" % str(gubun))
        queryInstance.Request(0)

        while XingT8430StockCodesHandler.XAQueryEventHandlerT8430.query_state == 0:
            pythoncom.PumpWaitingMessages()

        _count = queryInstance.GetBlockCount("t8430OutBlock")
        logger.info("Result count %s" % str(_count))
        _result = {
            'stockCodeList': list()
        }

        for i in range(_count):
            _name = queryInstance.GetFieldData("t8430OutBlock", "hname", i)  # 종목명
            _stock_code = queryInstance.GetFieldData("t8430OutBlock", "shcode", i)  # 단축코드
            _expcode = queryInstance.GetFieldData("t8430OutBlock", "expcode", i)  # 확장코드
            _etf_gubun = queryInstance.GetFieldData("t8430OutBlock", "etfgubun", i)  # ETF구분(1:ETF)
            _uplmtprice = queryInstance.GetFieldData("t8430OutBlock", "uplmtprice", i)  # 상한가
            _dnlmtprice = queryInstance.GetFieldData("t8430OutBlock", "dnlmtprice", i)  # 하한가
            _jnilclose = queryInstance.GetFieldData("t8430OutBlock", "jnilclose", i)  # 전일가
            _memedan = queryInstance.GetFieldData("t8430OutBlock", "memedan", i)  # 주문수량단위
            _recprice = queryInstance.GetFieldData("t8430OutBlock", "recprice", i)  # 기준가
            _gubun = queryInstance.GetFieldData("t8430OutBlock", "gubun", i)  # 구분(1:KOSPI, 2:KOSDAQ)
            _result['stockCodeList'].append({
                'name': _name if _name else None,
                'stockCode': _stock_code if _stock_code else None,
                'expCode': _expcode if _expcode else None,
                'eftGubun': int(_etf_gubun) if _etf_gubun and _etf_gubun.isdigit() else None,
                'uplmtprice': int(_uplmtprice) if _uplmtprice and _uplmtprice.isdigit() else None,
                'dnlmtprice': int(_dnlmtprice) if _dnlmtprice and _dnlmtprice.isdigit() else None,
                'jnilclose': int(_jnilclose) if _jnilclose and _jnilclose.isdigit() else None,
                'memedan': int(_memedan) if _memedan and _memedan.isdigit() else None,
                'recprice': int(_recprice) if _recprice and _recprice.isdigit() else None,
                'gubun': int(_gubun) if _gubun and _gubun.isdigit() else None,
            })

        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        
        """
        _result = self.fetch_data(
            gubun=self.get_code_by_name(MARKET_CODES, self.get_query_argument("marketCode"))
        )
        self.write(_result)
        self.finish()

import logging
import pythoncom
import tornado.web
import win32com.client

from datetime import datetime

import settings

from xing.xing import Xing

logger = logging.getLogger('tornado.application')


class XingT1102MarketPriceHandler(Xing):

    class XAQueryEventHandlerT1102:
        query_state = 0
        result = {
            'code': None
        }

        def OnReceiveData(self, code):
            XingT1102MarketPriceHandler.XAQueryEventHandlerT1102.query_state = 1
            XingT1102MarketPriceHandler.XAQueryEventHandlerT1102.result['code'] = code
            logger.info("Result: %s" % str(XingT1102MarketPriceHandler.XAQueryEventHandlerT1102.result))

    def fetch_data(self, code):
        self.login()
        queryInstance = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XingT1102MarketPriceHandler.XAQueryEventHandlerT1102)
        queryInstance.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1102.res"
        queryInstance.SetFieldData("t1102InBlock", "shcode", 0, code)
        logger.info("Request with %s" % str(code))
        queryInstance.Request(0)

        while XingT1102MarketPriceHandler.XAQueryEventHandlerT1102.query_state == 0:
            pythoncom.PumpWaitingMessages()

        _name = queryInstance.GetFieldData("t1102OutBlock", "hname", 0)
        _price = queryInstance.GetFieldData("t1102OutBlock", "price", 0)
        _sign = queryInstance.GetFieldData("t1102OutBlock", "sign", 0)
        _change = queryInstance.GetFieldData("t1102OutBlock", "change", 0)
        _diff = queryInstance.GetFieldData("t1102OutBlock", "diff", 0)
        _volume = queryInstance.GetFieldData("t1102OutBlock", "volume", 0)
        _recprice = queryInstance.GetFieldData("t1102OutBlock", "recprice", 0)
        _avg = queryInstance.GetFieldData("t1102OutBlock", "avg", 0)
        _uplmtprice = queryInstance.GetFieldData("t1102OutBlock", "uplmtprice", 0)
        _jnilvolume = queryInstance.GetFieldData("t1102OutBlock", "jnilvolume", 0)
        _volumediff = queryInstance.GetFieldData("t1102OutBlock", "volumediff", 0)
        _open = queryInstance.GetFieldData("t1102OutBlock", "open", 0)
        _opentime = queryInstance.GetFieldData("t1102OutBlock", "opentime", 0)
        _high = queryInstance.GetFieldData("t1102OutBlock", "high", 0)
        _hightime = queryInstance.GetFieldData("t1102OutBlock", "hightime", 0)

        _result = {
            'name': _name if _name else None,
            'price': int(_price) if _price and _price.isdigit() else None,
            'sign': int(_sign) if _sign and _sign.isdigit() else None,
            'change': int(_change) if _change and _change.isdigit() else None,
            'diff': int(_diff) if _diff and _diff.isdigit() else None,
            'volume': int(_volume) if _volume and _volume.isdigit() else None,
            'recprice': int(_recprice) if _recprice and _recprice.isdigit() else None,
            'avg': int(_avg) if _avg and _avg.isdigit() else None,
            'uplmtprice': int(_uplmtprice) if _uplmtprice and _uplmtprice.isdigit() else None,
            'jnilvolume': int(_jnilvolume) if _jnilvolume and _jnilvolume.isdigit() else None,
            'volumediff': int(_volumediff) if _volumediff and _volumediff.isdigit() else None,
            'open': int(_open) if _open and _open.isdigit() else None,
            'opentime': str(datetime.now().replace(hour=int(_opentime[:2]), minute=int(_opentime[2:4]), second=int(_opentime[4:6]), microsecond=0)) if _opentime and _opentime.isdigit() else None,
            'high': int(_high) if _high and _high.isdigit() else None,
            'hightime': str(datetime.now().replace(hour=int(_hightime[:2]), minute=int(_hightime[2:4]), second=int(_hightime[4:6]), microsecond=0)) if _hightime and _hightime.isdigit() else None,
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        
        """
        _result = self.fetch_data(
            code=self.get_query_argument("code")
        )
        self.write(_result)
        self.finish()

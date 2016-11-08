import logging
import tornado.web
import tornado.gen
import win32com.client

from cybos.cybos import Cybos

logger = logging.getLogger("tornado.application")


LIMIT_TYPE = (
  (0, 'LT_TRADE_REQUEST'),
  (1, 'LT_NONTRADE_REQUEST'),
  (2, 'LT_SUBSCRIBE'),
)


class CpCybos(Cybos):
    """
    CpCybos
    설명: CYBOS의 각종 상태를 확인할 수 있음.
    모듈위치: CpUtil.dll
    """

    _hts_instance = None

    def get_hts_instance(self):
        if not self._hts_instance:
            self._hts_instance = win32com.client.Dispatch("CpUtil.CpCybos")
        return self._hts_instance


class CpCybosIsConnectHandler(CpCybos):

    def fetch_data(self):
        _instance = self.get_hts_instance()
        _is_connect = int(_instance.IsConnect)
        _result = {
            "cybosIsConnect": _is_connect,
            "cybosIsConnectText": "연결 정상" if 1 == _is_connect else "연결 끊김",
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        (읽기전용) CYBOS의 통신 연결상태를 반환 합니다.
        """
        _result = self.fetch_data()
        self.write(_result)
        self.finish()


class CpCybosServerTypeHandler(CpCybos):

    def fetch_data(self):
        _instance = self.get_hts_instance()
        _server_type = int(_instance.ServerType)
        if 0 == _server_type:
            _server_type_text = "연결 끊김"
        if 1 == _server_type:
            _server_type_text = "cybosplus 서버"
        elif 2 == _server_type:
            _server_type_text = "HTS 보통서버(cybosplus 서버 제외)"
        else:
            _server_type_text = "Unknown"
        _result = {
            "cybosServerType": _server_type,
            "cybosServerTypeText": _server_type_text,
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        (읽기전용) 연결된 서버 종류를 반환합니다
        """
        _result = self.fetch_data()
        self.write(_result)
        self.finish()


class CpCybosLimitRequestRemainTimeHandler(CpCybos):

    def fetch_data(self):
        _instance = self.get_hts_instance()
        _result = {
            "cybosLimitRequestRemainTime": int(_instance.LimitRequestRemainTime),
            "cybosLimitRequestRemainTimeExplanation": "요청 개수를 재계산하기까지 남은 시간(단위:milisecond)",
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        (읽기전용) 요청 개수를 재계산하기까지 남은 시간을 반환합니다. 즉 리턴한 시간동안 남은 요청개수보다 더 요청하면 요청제한이 됩니다.
        """
        _result = self.fetch_data()
        self.write(_result)
        self.finish()


class CpCybosGetLimitRemainCountHandler(CpCybos):

    def fetch_data(self, limit_type):
        _instance = self.get_hts_instance()
        _result = {
            "cybosLimitRemainCount": _instance.GetLimitRemainCount(limit_type),
            "cybosLimitRemainCountExplanation": "제한을 하기 전까지의 남은 요청개수",
        }
        return _result

    @tornado.web.asynchronous
    def get(self):
        """
        limitType에 대한 제한을 하기까지 남은 요청개수를 반환합니다.
        
        Args:
            limitType: 요쳥에 대한 제한타입
                LT_TRADE_REQUEST - 주문관련 RQ 요청
                LT_NONTRADE_REQUEST - 시세관련 RQ 요청
                LT_SUBSCRIBE - 시세관련 SB

        """
        _limit_type = self.get_query_argument("limitType", "LT_NONTRADE_REQUEST")
        _limit_type = self.get_code_by_name(LIMIT_TYPE, _limit_type)
        _result = self.fetch_data(_limit_type)
        self.write(_result)
        self.finish()

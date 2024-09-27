import logging

from wifi_connect import WiFiConnect, WiFiError
from requests_login import RequestsLogin, online_status, WebpageError, NetworkError, UnknownError


username = ''
password = ''
ISP =  ''     # 移动：’cmcc‘   联通：‘unicom’   电信：‘telecom’    校园网：‘’


def set_loglevel():
    fhandler = logging.FileHandler('CUMTLogin.log', mode='w', encoding='utf-8')
    format_pattern = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    fhandler.setFormatter(format_pattern)
    fhandler.setLevel(logging.INFO)

    logger = logging.getLogger('CUMTLogin')
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)
    return logger

logger = set_loglevel()


class Connect:
    def __init__(self, username=username, password=password, ISP=ISP):
        self._logger = logging.getLogger('CUMTLogin')
        self.username = username
        self.password = password
        self.ISP = ISP

        print('Start')
        try:
            stat = online_status()
            if not stat:
                self.connect()
        except (WebpageError, NetworkError) as e:
            self._logger.warning(e.args[0])
            self.connect()
        except UnknownError as e:
            self._logger.warning(e.args[0])
        print('Online')

    def connect(self):
        print('Connect WiFi')
        wifi = WiFiConnect()
        if not wifi.connect():
            raise NetworkError('Failed to connect to WiFi')
        print('Connected')
        print('Login')
        try:
            login = RequestsLogin(self.username, self.password, self.ISP)
            if not login.connect():
                raise UnknownError('Failed to login')
        except ValueError as e:
            self._logger.warning(e.args[0])

if __name__ == '__main__':
    a = Connect()
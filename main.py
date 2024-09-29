from time import sleep

from Utils.requests_login import UnknownError
from Utils.wifi_connect import WiFiError
from connect import Connect, logger


gap = 20        # min


def cycle():
    while True:
        try:
            Connect()
        except WiFiError as e:
            logger.error(e.args[0])
        except UnknownError as e:
            logger.error(e.args[0])
        # except Exception as e:
        #     logger.error('未知错误 连接失败')
        sleep(gap*60)


if __name__ == '__main__':
    print('启动循环')
    cycle()
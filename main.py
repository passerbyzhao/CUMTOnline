import logging
from time import sleep

from connect import Connect, logger


gap = 20        # min


def cycle():
    while True:
        try:
            Connect()
        except Exception as e:
            logger.warning(e.args[0])
        sleep(gap*60)


if __name__ == '__main__':
    print('启动循环')
    cycle()
from time import sleep, time
import logging

import pywifi       # https://pypi.org/project/pywifi/

Scan_delay = 0.5      # WiFi扫描延迟 s
Connect_delay = 0.5   # WiFi连接延迟 s
Connect_timeout = 7 # WiFi连接超时 s

DISCONNECTED = pywifi.const.IFACE_DISCONNECTED
SCANNING = pywifi.const.IFACE_SCANNING
INACTIVE = pywifi.const.IFACE_INACTIVE
CONNECTING = pywifi.const.IFACE_CONNECTING
CONNECTED = pywifi.const.IFACE_CONNECTED

profile = pywifi.Profile()
profile.ssid = 'CUMT_Stu'
profile.auth = pywifi.const.AUTH_ALG_OPEN
profile.akm.append(pywifi.const.AKM_TYPE_NONE)
profile.cipher = pywifi.const.CIPHER_TYPE_NONE
profile.key = None


class WiFiError(Exception):
    pass


class WiFiConnect:
    def __init__(self, Scan_delay=Scan_delay, Connect_delay=Connect_delay):
        self._logger = logging.getLogger('CUMTLogin')
        self.Scan_delay = Scan_delay
        self.Connect_delay = Connect_delay
        wifi = pywifi.PyWiFi()
        self.iface = wifi.interfaces()[0]

        self.connect()

    def connect(self):
        if self.scan():
            tmp_profile = self.iface.add_network_profile(profile)
            self.iface.connect(tmp_profile)
            sleep(self.Connect_delay)

            s = time()
            while time() - s < Connect_timeout:
                if self.iface.status() == CONNECTING:
                    while self.iface.status() == CONNECTING:
                        pass
                if self.iface.status() == CONNECTED:
                    return True
                else:
                    self.iface.connect(tmp_profile)
            raise WiFiError('连接超时')

    def scan(self):     # 检查WiFi中是否有CUMT_Stu
        self.iface.scan()
        sleep(self.Scan_delay)
        result = self.iface.scan_results()

        s = time()
        while True:
            if time() - s > Connect_timeout:
                raise WiFiError('疑似找不到CUMT_Stu')
            for i in result:
                # print(i.ssid)
                if i.ssid == "CUMT_Stu":
                    return True


if __name__ == '__main__':
    WiFi = WiFiConnect()
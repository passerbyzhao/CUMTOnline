from time import sleep, time
import logging

import pywifi       # https://pypi.org/project/pywifi/

Scan_delay = 0      # WiFi扫描延迟 s
Connect_delay = 0   # WiFi连接延迟 s
Connect_timeout = 3 # WiFi连接超时 s

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
            if self.status_check():
                return True
            else:
                profile.auth = pywifi.const.AUTH_ALG_SHARED
                tmp_profile = self.iface.add_network_profile(profile)
                self.iface.connect(tmp_profile)
                sleep(self.Connect_delay)
                s = time()
                while not self.status_check():
                    if time()-s > Connect_timeout:
                        raise WiFiError('连接超时')
                return True
        raise WiFiError('疑似找不到CUMT_Stu')

    def scan(self):     # 检查WiFi中是否有CUMT_Stu
        self.iface.scan()
        sleep(self.Scan_delay)
        result = self.iface.scan_results()

        s = time()
        while True:
            if time() - s > Connect_timeout:
                return False
            for i in result:
                if i.ssid == "CUMT_Stu":
                    return True


    def status_check(self):     # 检查连接状态
        status = self.iface.status()
        if status == CONNECTED:
            return True
        elif status == DISCONNECTED:
            return False
        else:
            return False


if __name__ == '__main__':
    WiFi = WiFiConnect()
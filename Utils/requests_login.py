import re
import time
import logging

import requests


username = ''
password = ''
ISP =  ''     # 移动：’cmcc‘   联通：‘unicom’   电信：‘telecom’    校园网：‘’


class WebpageError(Exception):
    pass

class NetworkError(Exception):
    pass

class UnknownError(Exception):
    pass


def online_status():
    try:
        r = requests.get("http://10.2.5.251/")
    except Exception as e:
        raise NetworkError("疑似WiFi未连接")
    if r.status_code != 200:
        raise NetworkError('疑似连接错误WiFi')    # '无法加载网页，请检查网络连接状态'
    else:
        if '上网登录页' in r.text:
            return False
        elif '注销页' in r.text:
            return True
        else:
            raise UnknownError('网页异常 非登录页')


class RequestsLogin:
    def __init__(self, username=username, password=password, ISP=ISP):
        self._logger = logging.getLogger('CUMTLogin')
        self.username = username
        self.password = password
        self.ISP = ISP

    def connect(self):
        status = online_status()
        if status:
            return True
        r = requests.get("http://10.2.5.251/")
        if r.status_code != 200:
            raise WebpageError('无法加载登录页，请检查网络连接状态')
        html_text = r.text
        url = self.get_url(html_text, self.username, self.password ,self.ISP)
        r = requests.get(url)
        if r.status_code != 200:
            raise WebpageError('无法加载注销页，请检查网络连接状态')
        if '"result":"0"' in r.text:
            raise ValueError('用户名、密码或运营商错误')
        # {"result":"1","msg":"è®"}
        # {"result":"0","msg":"dXNlc","ret_code":"1"}
        self._logger.info('登陆成功')
        return online_status()

    def get_url(self, html_text, username, password, ISP):
        timestamp =  re.match(r'.*?timet=(.*?);.*?', html_text, re.S).group(1)
        wlan_user_ip = re.match(r'.*?ss5="(.*?)".*?', html_text, re.S).group(1)
        wlan_user_mac = re.match(r'.*?ss4="(.*?)".*?', html_text, re.S).group(1)
        port = re.match(r'.*?authloginport=(.*?);.*?', html_text, re.S).group(1)
        # print(timestamp, wlan_user_ip, wlan_user_mac, port)
        url = (f'http://10.2.5.251:{port}'
               f'/eportal/?c=Portal&a=login'
               f'&callback=dr{int(time.time())}'
               f'&login_method=1'
               f'&user_account={username}%40{ISP}'
               f'&user_password={password}'
               f'&wlan_user_ip={wlan_user_ip}'
               f'&wlan_user_mac={wlan_user_mac}'
               f'&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.0'
               f'&_={timestamp}')
        return url


if __name__ == '__main__':
    pass
    a = RequestsLogin()
    a.connect()
    # print(get_url(k, username, password, ISP))

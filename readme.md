<div align="center">  

# 中国矿业大学校园网自动登录

</div>

# `readme待完善`

# 主要功能
如题所示，可以自动连接矿大校园网（指WiFi）。

目前只试了笔记本、不连网线、windows系统的情况。可能存在各种各样的bug。


# 使用方法

### 准备(0)
安装依赖

### 准备(1)
在 `connect.py` 文件中，
依次将用户名（username）、
密码（password）、
运营商（ISP）填入
`username = ''
password = ''
ISP =  ''`。
其中运营商代码见下表：

|  运营商  |    代码     |
|:-----:|:---------:|
|  移动   |   cmcc    |
|  联通   |  unicom   |
|  电信   |  telecom  |
|  校园网  |    留空     |


## 1. 单次登录
完成准备(0)和(1)后可以直接运行 `connect.py` 文件，即可自动登录。

如果想实现一键登录，可以完成准备(2)后，运行 `online.bat` 登录。


### 准备(2)
`待完善`

修改 `online.bat` 的内容。

具体过程可以百度，
或者看[这个](https://blog.csdn.net/O3OTZ/article/details/126136943)




## 2. 循环登录
`待完善`

完成准备(0)和(1)。

修改 `stay_online.bat` 和 `stay_online.vbs` 的内容，
可以通过后台循环尝试登陆，以实现保持在线的功能。




# 依赖

[pywifi](https://github.com/awkman/pywifi/tree/master)  

comtypes（pywifi的依赖）

requests





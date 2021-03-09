import base64
import hmac
import time
from urllib.parse import quote

PRO_ID = "407495"           # 产品ID
DEV_ID = "690805501"        # 设备ID
DEV_NAME = "RaspberryPi"    # 设备名
KEY = "XTxOJG5WaD89cmQ6Yl8xQWkkWy5BbDVyRlByYGxyUnQ="        # 设备Key
ACCESS_KET = "f/WWN59X1ePhP7phxaSa6LRSqRjKywsIbiASyPi4isY=" # AccessKey

def token(_PRO_ID, _DEV_NAME, _KEY):
    version = '2018-10-31'
    # res = 'products/%s' % id  # 通过产品ID访问产品API
    res = 'products/%s/devices/%s' % (_PRO_ID, _DEV_NAME)  # 通过设备访问
    # 用户自定义token过期时间
    et = str(int(time.time()) + 3600)
    # 签名方法，支持md5、sha1、sha256
    method = 'sha1'
    # 对设备key进行decode
    key = base64.b64decode(_KEY)
    # 计算sign
    org = et + '\n' + method + '\n' + res + '\n' + version
    sign_b = hmac.new(key=key, msg=org.encode(), digestmod=method)
    sign = base64.b64encode(sign_b.digest()).decode()
    # value 部分进行url编码，method/res/version值较为简单无需编码
    sign = quote(sign, safe='')
    res = quote(res, safe='')
    # token参数拼接
    token = 'version=%s&res=%s&et=%s&method=%s&sign=%s' % (version, res, et, method, sign)
    return token

if __name__ == '__main__':
    print("Token: " + token(PRO_ID, DEV_NAME, KEY))

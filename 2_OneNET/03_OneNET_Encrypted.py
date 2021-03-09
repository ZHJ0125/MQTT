import paho.mqtt.client as mqtt
from urllib.parse import quote
import base64
import hmac
import time

PRO_ID = "407495"               # 产品ID
DEV_ID = "690805501"            # 设备ID
DEV_NAME = "RaspberryPi"        # 设备名
KEY = "XTxOJG5WaD89cmQ6Yl8xQWkkWy5BbDVyRlByYGxyUnQ="        # 设备Key
ACCESS_KET = "f/WWN59X1ePhP7phxaSa6LRSqRjKywsIbiASyPi4isY=" # AccessKey
HOST = "mqttstls.heclouds.com"  # 加密接口地址
PORT = "8883"                   # 加密端口

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

# 当客户端收到来自服务器的CONNACK响应时的回调
def on_connect(client, userdata, flags, rc):
    print("连接结果:" + mqtt.connack_string(rc))
# 从服务器接收发布消息时的回调
def on_message(client, userdata, msg):
    print(str(msg.payload,'utf-8'))
# 当消息已经被发送给中间人时的回调
def on_publish(client, userdata, mid):
    print(str(mid))

def main():
    passw = token(PRO_ID, DEV_NAME, KEY)
    print("passw: " + passw)
    client = mqtt.Client(DEV_NAME,protocol=mqtt.MQTTv311)
    client.tls_set(certfile='/home/zhj/MQTT/2_OneNET/MQTTS-certificate.pem') #鉴权证书
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect(HOST, port=int(PORT))
    client.username_pw_set(PRO_ID, passw)
    client.loop_forever()

if __name__ == '__main__':
    main()

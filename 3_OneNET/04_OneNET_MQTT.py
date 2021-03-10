# -*- coding: utf-8 -*-
# 2021-03-10

import paho.mqtt.client as mqtt
from urllib.parse import quote
import time
import json
import random
import base64
import hmac

# HOST = "mqttstls.heclouds.com"    # 加密地址
# PORT = "8883"                     # 加密端口
HOST = "mqtts.heclouds.com"         # 未加密地址
PORT = "1883"                       # 未加密端口
PRO_ID = "407648"                   # 产品ID
DEV_ID = "691289818"                # 设备ID
DEV_NAME = "RaspberryPi"            # 设备名称
DEV_KEY = "6NlxW8h95mhTsodULVvo8mx/X/Bf8up6AmSnyoFYDho="        # 设备Key
ACCESS_KET = "tg23t7tZgkW8MWudgiZ8R+Ih+TxPiCmSbjKzFuq31xE="     # 产品AccessKey

# 控制LED亮灭的函数
def LED_Control(cmd):
    if(cmd == "b'ON'"):             # 开灯命令 [ON]
        ts_print("[Command] --> LED ON")
    elif(cmd == "b'OFF'"):          # 关灯命令 [OFF]
        ts_print("[Command] --> LED OFF")

# 用于生成Token的函数
def token(_pid, dname, access_key):
    version = '2018-10-31'
    # res = 'mqs/%s' % id           # 通过MQ_ID访问
    # res = 'products/%s' % id      # 通过产品ID访问产品API
    res = 'products/%s/devices/%s' % (_pid, dname)  # 通过MQTTS产品id和设备名称访问
    # 用户自定义token过期时间
    et = str(int(time.time()) + 3600000)
    # 签名方法，支持md5、sha1、sha256
    method = 'md5'
    # 对access_key进行decode
    key = base64.b64decode(access_key)
    # print(key)
    # 计算sign
    org = et + '\n' + method + '\n' + res + '\n' + version
    # print(org)
    sign_b = hmac.new(key=key, msg=org.encode(), digestmod=method)
    sign = base64.b64encode(sign_b.digest()).decode()
    # print(sign)
    # value 部分进行url编码，method/res/version值较为简单无需编码
    sign = quote(sign, safe='')
    res = quote(res, safe='')
    # token参数拼接
    token = 'version=%s&res=%s&et=%s&method=%s&sign=%s' % (version, res, et, method, sign)
    return token

# 定义了带时间戳的输出格式
def ts_print(*args):
    t = time.strftime("[%Y-%m-%d %H:%M:%S")
    ms = str(time.time()).split('.')[1][:3]
    t += ms + ']:'
    print(t, *args)

# 当MQTT代理响应客户端连接请求时触发
def on_connect(client, userdata, flags, rc):
    ts_print("<<<<CONNACK")
    ts_print("connected with result code: " + mqtt.connack_string(rc), rc)
    client.subscribe(topic=topic_cmd, qos=1)        # 订阅由OneNET平台下发的命令
    client.subscribe(topic=topic_dp, qos=1)         # 订阅上传数据的响应结果

# 当接收到MQTT代理发布的消息时触发
def on_message(client, userdata, msg):
    ts_print('on_message')
    ts_print("Topic: " + str(msg.topic))
    ts_print("Payload: " + str(msg.payload))
    LED_Control(str(msg.payload))
    if topic_cmds in msg.topic:                     # 命令响应的主题
        responseTopic = str(msg.topic).replace("request","response",1)
        # print(responseTopic)
        client.publish(responseTopic,'OK',qos = 1)  # 发布命令响应

# 当客户端调用publish()发布一条消息至MQTT代理后被调用
def on_publish(client, userdata, mid):
    ts_print("Puback:mid: " + str(mid))
    ts_print("Puback:userdata: " + str(userdata))

# 当MQTT代理响应订阅请求时被调用
def on_subscribe(client, obj, mid, granted_qos):
    ts_print("Subscribed: message:" + str(obj))
    ts_print("Subscribed: mid: " + str(mid) + "  qos:" + str(granted_qos))

# 当客户端与代理服务器断开连接时触发
def on_disconnect(client):
    ts_print('DISCONNECTED')

# 从树莓派发布到服务器的数据内容
def data(ds_id,value):
    message = {
        "id": int(ds_id),
        "dp": {
            "distance": [{      # 距离传感器采集的数据
                "v": value
            }],
            "random": [{        # Python产生的随机数
                "v": random.randint(20,80)
            }]
        }
    }
    # print(message)
    message = json.dumps(message).encode('ascii')
    return message

if __name__ == '__main__':

    # 配置MQTT连接信息
    client_id = DEV_NAME
    username = PRO_ID
    password = token(PRO_ID, DEV_NAME, DEV_KEY)
    print('username:' + username)
    print('password:' + password)
    client = mqtt.Client(client_id=client_id, clean_session=True, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=username, password=password)
    # client.tls_set(ca_certs='MQTTS-certificate.pem')              # 加密方式需要使用鉴权证书
    # client.tls_insecure_set(True) #关验证
    client.connect(HOST, int(PORT), keepalive=1200)

    # 按照OneENT要求的格式，配置数据发布和订阅的主题
    topic_dp = '$sys/%s/%s/dp/post/json/+' % (username, DEV_NAME)   # 设备上报数据主题
    topic_cmd = '$sys/%s/%s/cmd/#' % (username, DEV_NAME)           # 设备接受命令主题
    topic_cmds = '$sys/%s/%s/cmd/request/' % (username, DEV_NAME)   # 设备接受命令主题
    topic_publish = '$sys/%s/%s/dp/post/json' %(username,DEV_NAME)
    client.loop_start()

    count = 0
    while True:
        count += 1
        # 树莓派循环发布数据到OneNET
        client.publish(topic=topic_publish, payload=data(count, random.randint(0,100)), qos=1)
        print("-------------------------------------------------------------------------------")
        time.sleep(3)

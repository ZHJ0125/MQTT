# -*- coding: utf-8 -*-
# 2021-03-10

import paho.mqtt.client as mqtt

USER_NAME = "student"
PASSWORD  = "kkxxb401"
HOST = "47.95.13.239"
PORT = "1883"
TOPIC_TEMP = "Distance"
TOPIC_CTRL = "Control"

def on_connect(client, userdata, flags, rc):
    print("连接结果: " + mqtt.connack_string(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if(str(msg.payload) == "b'1'"):
        print("LED ON")
    elif(str(msg.payload) == "b'0'"):
        print("LED OFF")

client = mqtt.Client()
# 设置用户名和密码
client.username_pw_set(USER_NAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
# client.on_disconnect = on_disconnect
# 连接 IP port keepalive
client.connect(HOST, int(PORT), 600)
# 订阅的 topic
client.subscribe(TOPIC_CTRL, qos=0)
client.loop_forever()

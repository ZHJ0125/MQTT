# -*- coding: utf-8 -*-
# 2021-03-10

import paho.mqtt.client as mqtt
import time

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

client = mqtt.Client()
# 设置用户名和密码
client.username_pw_set(USER_NAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
# 连接 IP port keepalive
client.connect(HOST, int(PORT), 600)

# 发布 topic 内容
# client.publish(TOPIC_TEMP, payload="This is a message.", qos=0)
# client.publish(TOPIC_TEMP, payload="1", qos=0)
# client.publish(TOPIC_TEMP, payload="0", qos=0)
while True:
    for i in range(20, 25):
        _payload = "Distance is: %s" % i
        client.publish(topic=TOPIC_TEMP, payload=_payload, qos=0)
        print("Published to " + TOPIC_TEMP + ": " + _payload)
        time.sleep(2)

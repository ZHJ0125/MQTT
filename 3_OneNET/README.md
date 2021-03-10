* 测试产品

|     参数    |                      内容                         |       含义      |
|------------|---------------------------------------------------|-----------------|
| HOST       | "mqttstls.heclouds.com"                           |   加密地址       |
| PORT       | "8883"                                            |   加密端口       |
| HOST       | "mqtts.heclouds.com"                              |   未加密地址      |
| PORT       | "1883"                                            |   未加密端口      |
| PRO_ID     | "407495"                                          |   产品ID         |
| DEV_ID     | "690805501"                                       |   设备ID         |
| DEV_NAME   | "RaspberryPi"                                     |   设备名称        |
| DEV_KEY    | "XTxOJG5WaD89cmQ6Yl8xQWkkWy5BbDVyRlByYGxyUnQ="    |   设备Key        |
| ACCESS_KET | "f/WWN59X1ePhP7phxaSa6LRSqRjKywsIbiASyPi4isY="    |   产品AccessKey  |


* 二次测试

|     参数    |                      内容                         |       含义      |
|------------|---------------------------------------------------|-----------------|
| HOST       | "mqttstls.heclouds.com"                           |   加密地址       |
| PORT       | "8883"                                            |   加密端口       |
| HOST       | "mqtts.heclouds.com"                              |   未加密地址      |
| PORT       | "1883"                                            |   未加密端口      |
| PRO_ID     | "407648"                                          |   产品ID         |
| DEV_ID     | "691289818"                                       |   设备ID         |
| DEV_NAME   | "RaspberryPi"                                     |   设备名称        |
| DEV_KEY    | "6NlxW8h95mhTsodULVvo8mx/X/Bf8up6AmSnyoFYDho="    |   设备Key        |
| ACCESS_KET | "tg23t7tZgkW8MWudgiZ8R+Ih+TxPiCmSbjKzFuq31xE="    |   产品AccessKey  |


# README

## 安装paho-mqtt

在树莓派的终端输入以下命令，检查环境

```sh
python3 -V      # 显示python3的版本
pip3 -V         # 显示pip包管理工具的版本
```

输入以下命令安装paho-mqtt

```sh
pip3 install paho-mqtt
```

看到 `Successfully installed paho-mqtt-1.5.1` 说明安装成功

实验过程需要编写一些代码，可以点击[链接]查看，或者使用以下指令下载代码

```sh
git clone 
```
from util import HttpRequest
from util.Log import Logger
from config.config import ReadConfig
import time
import subprocess
import re


class DeviceMethod:
    """
    1.ATXserver remote control mobiles
    2.local_devices: connect mobiles by usb
    """
    def __init__(self):
        self.log = Logger().logger
        self.token = ReadConfig().getServerToken()
        self.server_url = ReadConfig().getServerUrl()

    def getAvailableDevice(self):
        """
        获取服务器上的设备
        :return:
        """
        keys = ['platform', 'device', 'isOnline', 'isUsing']
        device_list = []
        available_device = []
        try:
            ret = HttpRequest.HttpRequest.request_api("/api/v1/devices", self.token, self.server_url)

            for i in ret.get('devices'):
                device = [i.get('platform'), i.get('udid'), i.get('present'), i.get('using')]
                device_info = dict(zip(keys, device))
                device_list.append(device_info)
                if i.get('present') and not i.get('using'):
                    available_device.append(i.get('udid'))
            info = {'availableDevice': available_device, 'devices': device_list}
            return info

        except Exception as e:
            self.log.error(e)
            return []

    def checkAlive(self, device):
        try:
            devices = self.getAvailableDevice()
            available_devices = devices.get('availableDevice')

            if str(device) not in available_devices:
                raise Exception(f"query error {device}: 无此设备或设备已占用")
            else:
                return True

        except Exception as e:
            self.log.error(e)
            return False

    def bindDevice(self, devices, bind_time=None):
        """
        占用手机
        :param devices:
        :param bind_time: seconds
        :return:
        """
        data = {"udid": devices}
        if bind_time:
            data.update({"idleTimeout": int(bind_time)})

        res = self.checkAlive(devices)

        if not res:
            return False

        try:
            ret = HttpRequest.HttpRequest.request_api("/api/v1/user/devices", self.token, self.server_url,
                                                      method="post", json=data)
            if not ret.get("success"):
                raise Exception(f"{devices}占用失败")
            return True

        except Exception as e:
            self.log.error(e)
            return False

    def unbindDevice(self, devices):
        """
        释放手机
        :param devices:
        :return:
        """
        try:
            HttpRequest.HttpRequest.request_api("/api/v1/user/devices/" + devices, self.token, self.server_url,
                                                method="delete")
            # if not ret.get("success"):
            #     raise Exception(f"{devices} 释放失败, 未查询到此设备或设备已释放")
            return True
        except Exception as e:
            self.log.error(e)
            return False

    def getDeviceInfo(self, mobile):
        """
        获取设备详细信息
        """
        ret = HttpRequest.HttpRequest.request_api("/api/v1/user/devices/" + mobile, self.token, self.server_url)
        source = ret['device']['source']
        return source['atxAgentAddress']

    def getLocalDevices(self):
        """
        获取本地的设备列表（USB或者WIFI连接）
        """
        output = subprocess.check_output(['adb', 'devices'])
        pattern = re.compile(
            r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
        matches = pattern.findall(output.decode())
        valid_serials = [m[0] for m in matches if m[1] == 'device']

        if valid_serials:
            mes = f'Start check {len(valid_serials)} devices connected on PC: {valid_serials} '
            self.log.info(mes)
            return valid_serials

        if len(valid_serials) == 0:
            mes = "No available android devices detected."
            self.log.error(mes)
            return []


if __name__ == '__main__':
    a = DeviceMethod()
    # print(a.bindDevice('79d340b8', 500))
    print(a.unbindDevice('79d340b8'))
    # print(a.bindDevice('79d340b8', 50))
    # time.sleep(10)
    # print(a.bindDevice('79d340b8', 50))

    # time.sleep(10)
    # print(a.unbindDevice('79d340b8'))

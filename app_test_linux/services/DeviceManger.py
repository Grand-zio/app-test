from util.Log import Logger
from config.config import ReadConfig
from util import DeviceMethod


class DeviceManger:
    """
    get mobiles & init mobile
    """
    uuid_list = []
    remote_address_list = []

    def __init__(self):
        self.device_method = DeviceMethod.DeviceMethod()
        self.log = Logger().logger
        self.config = ReadConfig()

    def checkDevices(self):
        method = self.config.getMethod()
        test_phones = self.config.getPhones().remove('')
        remote_ids = []

        if method.upper() == 'SERVER':
            # 远程真机
            self.log.info('Get available online devices from ATX-Server...')

            # 所有有效设备（有且未被占用）
            devices = self.device_method.getAvailableDevice().get('availableDevice')

            if not devices:
                self.log.info('There has no online devices in ATX-Server')
                return []

            # 指定设备
            if test_phones:
                for i in test_phones:
                    if i not in devices:
                        test_phones.remove(i)
                        continue
                    remote_ids.append(self.device_method.getDeviceInfo(i))
                message = {"device_info": {"method": "SERVER", "type": "指定设备", "devices": test_phones,
                                           "remote_id": remote_ids}}
                self.log.info(message)
                return message

            for j in devices:
                remote_ids.append(self.device_method.getDeviceInfo(j))
            message = {"device_info": {"method": "SERVER", "type": "全部设备", "devices": devices,
                                       "remote_id": remote_ids}}
            self.log.info(message)
            return message

        elif method.upper() == 'USB' or 'WIFI':
            # 本地连接
            devices = self.device_method.getLocalDevices()

            if test_phones:
                for i in test_phones:
                    if i not in devices:
                        test_phones.remove(i)
                message = {"device_info": {"method": "USB or WIFI", "type": "全部设备", "devices": test_phones}}
                self.log.info(message)
                return message

            message = {"device_info": {"method": "USB or WIFI", "type": "全部设备", "devices": devices}}
            self.log.info(message)
            return message

        else:
            return []

    def bindDevice(self, device, bind_time):
        return self.device_method.bindDevice(device, bind_time)

    def unbindDevice(self, device):
        return self.device_method.unbindDevice(device)


if __name__ == '__main__':
    a = DeviceManger()
    # print(a.unbindDevice('79d340b8'))
    # print(a.get_device_list())
    print(a.checkDevices())

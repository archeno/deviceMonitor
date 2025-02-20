import asyncio
import logging
from modbus_client import ModbusDevice
from websocket_client import WebSocketClient

class DeviceManager:
    def __init__(self, config):
        """
        初始化设备管理器，接收配置作为参数
        :param config: 配置字典，包含 modbus 和 server 信息
        """
        self.config = config  # 保存配置
        self.modbus_device = ModbusDevice(config['modbus']['port'], config['modbus']['baudrate'], config['modbus']['slave_id'])
        self.ws_client = WebSocketClient(config['server']['url'])

    async def start(self):
        """启动设备管理"""
        await self.modbus_device.connect()
        await self.ws_client.connect()

        while True:
            # 每隔一定时间读取设备数据
            data = await self.modbus_device.read_data(self.config['modbus']['read_address'], self.config['modbus']['register_count'])
            print("read data: ", data)
            if data:
                await self.ws_client.send_data({"action": "update", "data": data})

            await asyncio.sleep(self.config['modbus']['poll_interval'])

    async def stop(self):
        """停止设备管理"""
        await self.modbus_device.close()
        await self.ws_client.close()
        logging.info("设备管理已停止。")

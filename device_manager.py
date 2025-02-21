import logging
import asyncio
from modbus_client import ModbusDevice
from websocket_client import WebSocketClient

class DeviceManager:
    def __init__(self, config):
        self.config = config
        self.modbus_device = ModbusDevice(config['modbus']['port'], 
                                        config['modbus']['baudrate'], 
                                        config['modbus']['slave_id'])
        self.ws_client = WebSocketClient(config['server']['url'])
        self.running = False

    async def manage_connections(self):
        """管理设备连接状态"""
        while self.running:
            if not self.modbus_device.connected:
                await self.modbus_device.connect()
            if not self.ws_client.connected:
                await self.ws_client.connect()
            await asyncio.sleep(5)  # 每5秒检查一次连接状态

    async def read_and_send_data(self):
        """读取并发送数据"""
        while self.running:
            try:
                if self.modbus_device.client.connected :
                    data = await self.modbus_device.read_data(
                        self.config['modbus']['read_address'],
                        self.config['modbus']['register_count']
                    )
                    if   data:
                        await self.ws_client.send_data({
                            "action": "update",
                            "data": data
                        })
            except Exception as e:
                logging.error(f"读取或发送数据时出错: {e}")
            await asyncio.sleep(self.config['modbus']['poll_interval'])

    async def receive_commands(self):
        """接收服务器命令"""
        while self.running:
            try:
                if self.ws_client.connected:
                    data = await self.ws_client.receive_data()
                    if data:
                        # 处理接收到的命令
                        logging.info(f"收到命令: {data}")
            except Exception as e:
                logging.error(f"接收命令时出错: {e}")
            await asyncio.sleep(0.1)

    async def start(self):
        """启动设备管理"""
        self.running = True
        try:
            await asyncio.gather(
                self.manage_connections(),
                self.read_and_send_data(),
                self.receive_commands()
            )
        except Exception as e:
            logging.error(f"运行时出错: {e}")
        finally:
            await self.stop()

    async def stop(self):
        """停止设备管理"""
        self.running = False
        self.modbus_device.close()
        await self.ws_client.close()
        logging.info("设备管理已停止")

import logging
import asyncio
from pymodbus.client import AsyncModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException

class ModbusDevice:
    def __init__(self, port, baudrate, slave_id, retries=3, timeout=2):
        """
        初始化Modbus设备客户端
        :param port: 串口号
        :param baudrate: 波特率
        :param slave_id: 从站ID
        :param retries: 重试次数
        :param timeout: 超时设置
        """
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.retries = retries
        self.timeout = timeout
        self.client = None

    async def connect(self):
        """连接Modbus设备，重试机制"""
        for attempt in range(self.retries):
            try:
                self.client = ModbusClient(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout
                )
                await self.client.connect()
                logging.info("Modbus 设备连接成功")
                return
            except ModbusException as e:
                logging.error(f"Modbus 设备连接失败: {e}")
                if attempt < self.retries - 1:
                    await asyncio.sleep(2)  # 等待重试

        logging.critical("无法连接到Modbus设备")

    async def read_data(self, address, count):
        """读取数据"""
        try:
            result = await self.client.read_holding_registers(address, count=count, slave=self.slave_id)
            if result.isError():
                logging.error(f"读取数据失败，地址: {address}, 错误: {result}")
                return None
            return result.registers
        except ModbusException as e:
            logging.error(f"读取数据时出错: {e}")
            return None

    async def close(self):
        """关闭Modbus连接"""
        if self.client:
            await self.client.close()
            logging.info("Modbus 连接关闭")

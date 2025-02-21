import logging
from log_filter import LogFilter
import asyncio
from datetime import datetime, timedelta
from pymodbus.client import AsyncModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException
from serial.serialutil import SerialException
class ModbusDevice(LogFilter):
    def __init__(self, port, baudrate, slave_id, retries=3, timeout=2):
        """
        初始化Modbus设备客户端
        :param port: 串口号
        :param baudrate: 波特率
        :param slave_id: 从站ID
        :param retries: 重试次数
        :param timeout: 超时设置
        """
        super().__init__() 
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.retries = retries
        self.timeout = timeout
        self.client = None
        self.connected = False
          # 错误状态追踪
        self.last_error_time = {}
        self.error_counts = {}
        self.error_threshold = 60  # 相同错误的最小间隔时间(秒)

    def _should_log_error(self, error_key):
        """
        检查是否应该记录错误
        :param error_key: 错误类型的唯一标识
        :return: bool 是否应该记录该错误
        """
        current_time = datetime.now()
        last_time = self.last_error_time.get(error_key)
        
        if last_time is None or (current_time - last_time) > timedelta(seconds=self.error_threshold):
            self.last_error_time[error_key] = current_time
            self.error_counts[error_key] = 1
            return True
        
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        return self.error_counts[error_key] == 1  # 只在第一次出现时返回True
    
    async def connect(self):
        """连接Modbus设备，重试机制"""
        if self.connected:
            return

        for attempt in range(self.retries):
            try:
                if not self.client:
                    self.client = ModbusClient(
                        port=self.port,
                        baudrate=self.baudrate,
                        timeout=self.timeout
                    )
                if await self.client.connect():
                    self.connected = True
                    logging.info(f"Modbus 设备连接成功 (端口: {self.port} boradrate: {self.baudrate} slave_id: {self.slave_id})")
                    return
            except ModbusException as e:
                if self._should_log_error('connection_error'):
                    logging.error(f"Modbus 设备连接失败: {e}")
                    if attempt < self.retries - 1:
                        await asyncio.sleep(2)

        self.connected = False
        # logging.critical("无法连接到Modbus设备")

    async def read_data(self, address, count):
        """读取数据"""
        if not self.connected:
            return None
        try:
            result = await self.client.read_holding_registers(
                address, count=count, slave=self.slave_id
            )
            if result.isError():
                # self.connected = False
                if self._should_log_error('read_error'):
                    logging.error(f"读取数据失败: {result}")
                return None
            return result.registers
        except SerialException as e:
            if self._should_log_error('serial_error'):
                logging.error(f"串口连接异常（设备可能已断开）: {e}")
            self.client.close()
            return None
        except ModbusException as e:
            if self._should_log_error('modbus_error'):
                logging.error(f"Modbus 通信错误: {e}")
            return None
        except Exception as e:
            self.connected = False
            if self._should_log_error('unknown_error'):
                logging.error(f"读取数据时出错: {e}")
            return None

    def close(self):
        """关闭Modbus连接"""
        if self.client:
            self.connected = False
            self.client.close()
            print("@@@@",self.client)
            logging.info("Modbus 连接关闭")

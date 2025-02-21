import logging
from log_filter import LogFilter
import asyncio
import websockets
import json

class WebSocketClient(LogFilter):
    def __init__(self, url, retries=3, timeout=10):
        """
        初始化WebSocket客户端
        :param url: WebSocket 服务器URL
        :param retries: 重试次数
        :param timeout: 超时设置
        """
        super().__init__()
        self.url = url
        self.retries = retries
        self.timeout = timeout
        self.websocket = None
        self.connected = False

    async def connect(self):
        """连接WebSocket服务器，重试机制"""
        if self.connected:
            return

        for attempt in range(self.retries):
            try:
                self.websocket = await asyncio.wait_for(
                    websockets.connect(self.url), 
                    timeout=self.timeout
                )
                self.connected = True
                if self._should_log_error("websocket_connect_success"):
                    logging.info(f"WebSocket 连接成功: {self.url}")
                return
            except Exception as e:
                if self._should_log_error("websocket_connect_error"):
                    logging.error(f"WebSocket 连接失败: {e}")
                if attempt < self.retries - 1:
                    await asyncio.sleep(2)

        self.connected = False
        if self._should_log_error("websocket_connect_critical"):
            logging.critical(f"无法连接到 WebSocket 服务器: {self.url}")

    async def send_data(self, data):
        """发送数据到服务器"""
        if not self.connected:
            return
        try:
            await self.websocket.send(json.dumps(data))
            logging.info(f"已发送数据: {data}")
        except Exception as e:
            self.connected = False
            if self._should_log_error("websocket_send_data_error"):
                logging.error(f"发送数据失败: {e}")

    async def receive_data(self):
        """接收服务器数据"""
        if not self.connected:
            return None
        try:
            data = await self.websocket.recv()
            return json.loads(data)
        except Exception as e:
            self.connected = False
            if self._should_log_error("websocket_receive_data_error"):
                logging.error(f"接收数据失败: {e}")
            return None

    async def close(self):
        """关闭WebSocket连接"""
        if self.websocket:
            self.connected = False
            await self.websocket.close()
            logging.info("WebSocket 连接关闭")

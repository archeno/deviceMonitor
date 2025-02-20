import asyncio
import websockets
import logging

class WebSocketClient:
    def __init__(self, url, retries=3, timeout=10):
        """
        初始化WebSocket客户端
        :param url: WebSocket 服务器URL
        :param retries: 重试次数
        :param timeout: 超时设置
        """
        self.url = url
        self.retries = retries
        self.timeout = timeout
        self.websocket = None

    async def connect(self):
        """连接WebSocket服务器，重试机制"""
        for attempt in range(self.retries):
            try:
                self.websocket = await asyncio.wait_for(websockets.connect(self.url), timeout=self.timeout)
                logging.info(f"WebSocket 连接成功: {self.url}")
                return
            except (websockets.exceptions.WebSocketException, asyncio.TimeoutError) as e:
                logging.error(f"WebSocket 连接失败: {e}")
                if attempt < self.retries - 1:
                    await asyncio.sleep(2)  # 等待重试

        logging.critical(f"无法连接到 WebSocket 服务器: {self.url}")

    async def send_data(self, data):
        """发送数据到服务器"""
        if self.websocket:
            try:
                await self.websocket.send(data)
                logging.info(f"已发送数据: {data}")
            except websockets.exceptions.WebSocketException as e:
                logging.error(f"发送数据失败: {e}")

    async def close(self):
        """关闭WebSocket连接"""
        if self.websocket:
            await self.websocket.close()
            logging.info("WebSocket 连接关闭")

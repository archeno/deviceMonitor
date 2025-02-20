import logging
import asyncio
from device_manager import DeviceManager
from config import load_config

# 配置日志
logging.basicConfig(level=logging.INFO)

# 加载配置
config = load_config()

# 启动设备管理
device_manager = DeviceManager(config)

# 异步启动
async def main():
    await device_manager.start()

# 启动事件循环
if __name__ == "__main__":
    asyncio.run(main())

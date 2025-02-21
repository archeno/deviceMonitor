import logging
import asyncio
import signal
import sys
from device_manager import DeviceManager
from config import load_config
from pymodbus.logging import Log

# Configure PyModbus logging
Log.setLevel(logging.CRITICAL)  # Only show critical errors from pymodbus
# Or completely disable PyModbus logging:
# Log.setLevel(logging.FATAL)


# 配置日志 - 放在最开始
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)  # 为当前模块创建logger

def signal_handler(device_manager):
    """信号处理函数"""
    async def cleanup():
        await device_manager.stop()
        sys.exit(0)
    asyncio.create_task(cleanup())

async def main():
    try:
        # 加载配置
        config = load_config()
        
        # 创建设备管理器
        device_manager = DeviceManager(config)
        
        # 注册信号处理 - Windows 兼容方式
        if sys.platform == 'win32':
            signal.signal(signal.SIGINT, lambda s, f: signal_handler(device_manager))
            signal.signal(signal.SIGTERM, lambda s, f: signal_handler(device_manager))
        
        # 启动设备管理
        await device_manager.start()
        
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
    finally:
        if 'device_manager' in locals():
            await device_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())

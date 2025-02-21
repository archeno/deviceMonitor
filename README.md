# Device Monitor / 设备监控系统

A Python-based device monitoring system that reads Modbus data and forwards it to a WebSocket server.  
基于 Python 的设备监控系统，用于读取 Modbus 数据并转发给 WebSocket 服务器。

## Features / 功能特点

- **Modbus RTU Communication / Modbus RTU 通信**:  
  Communicates with devices over serial ports. / 通过串口与设备通信。

- **WebSocket Integration / WebSocket 集成**:  
  Real-time data transmission via WebSocket. / 通过 WebSocket 实现实时数据传输。

- **Automatic Reconnection / 自动重连**:  
  Automatically attempts to reconnect on connection failures. / 连接失败时自动重连。

- **Configurable Polling / 可配置轮询**:  
  Set polling intervals according to your needs. / 可根据需要设定轮询间隔。

- **Error Handling with Rate Limiting / 带速率限制的错误处理**:  
  Prevents excessive logging through rate limiting. / 防止过多日志记录。

## Requirements / 环境要求

- Python 3.11+  
- pymodbus  
- websockets  
- asyncio

## Configuration / 配置说明

The system is configured via a JSON file (`config.json`).  
系统通过 JSON 文件 (`config.json`) 进行配置。

Example configuration:

```json
{
    "modbus": {
        "port": "COM5",
        "baudrate": 115200,
        "slave_id": 1,
        "read_address": 0,
        "register_count": 10,
        "poll_interval": 1
    },
    "server": {
        "url": "ws://your-server:8000/ws"
    }
}
```


## Usage / 使用方法

Run the main program with the following command:
使用如下命令启动主程序：

python main.py

Once started, the system will:
启动后系统将会：

* Connect to the Modbus device / 连接到 Modbus 设备
* Establish a WebSocket connection / 建立 WebSocket 连接
* Continuously read and forward data / 持续读取并转发数据
* Automatically reconnect if the connection is lost / 连接丢失时自动重连

## Project Structure / 项目结构
* main.py - Main program entry point / 主程序入口
* device_manager.py - Manages device operations / 设备管理模块
* modbus_client.py - Handles Modbus communication / Modbus 通信模块
* websocket_client.py - Manages WebSocket communications / WebSocket 通信模块
* config.py - Handles configuration file logic / 配置管理模块
* log_filter.py - Implements log rate limiting / 日志速率限制模块

## Error Handling / 错误处理
The system includes mechanisms for error handling, including automatic reconnection and rate-limited error * logs to avoid log flooding.
系统具有自动重连以及速率限制的错误日志功能，以避免日志过多。

## License / 许可证
Specify your project's license here.
在此处指定您的项目许可证。

## Contributing / 贡献
Feel free to open issues or submit pull requests if you have suggestions or improvements.
如果您有建议或改进，欢迎提交 issue 或 pull request。




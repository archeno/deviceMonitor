# import json

# class Config:
#     """配置类，用于读取串口和WebSocket配置"""
#     def __init__(self, config_file='config.json'):
#         self.config_file = config_file
#         self.config = self.load_config()

#     def load_config(self):
#         """加载配置文件"""
#         with open(self.config_file, 'r') as file:
#             return json.load(file)

import json

def load_config(filename='config.json'):
    with open(filename, 'r') as f:
        return json.load(f)

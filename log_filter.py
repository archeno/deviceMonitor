import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LogFilter:
    """日志过滤基类"""
    def __init__(self):
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
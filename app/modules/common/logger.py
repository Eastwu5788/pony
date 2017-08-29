import logging
import json
import sys
from app.modules.common.encoder import DateEncoder

# 普通用户使用的log
user_logger = logging.getLogger("pony")


def add_error_log(code, messages):
    structure = {
        "code": code,
        "message": messages
    }
    user_logger.error(json.dumps(structure, cls=DateEncoder))


# 未捕获异常的处理log
# _crash_logger = logging.getLogger("crash")
# 初始化log处理器
# _crash_handler = logging.FileHandler("/data/wwwlogs/crash_error.log")
# 为处理器设置输出格式
# _crash_handler.setFormatter(logging.Formatter("%(message)s"))
# 为logger添加处理器
# _crash_logger.addHandler(_crash_handler)
# 设置日志级别
# _crash_logger.setLevel(logging.ERROR)


# def uncaught_exception_handler(exc_type, exc_value, exc_traceback):
#     print("异常捕获")
#     if issubclass(exc_type, KeyboardInterrupt):
#         sys.__excepthook__(exc_type, exc_value, exc_traceback)
#         return
#     print("异常捕获")
#     _crash_logger.error("Uncaught exception", esc_info=(exc_type, exc_value, exc_traceback))







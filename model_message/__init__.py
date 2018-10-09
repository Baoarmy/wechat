import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask_cors import CORS
from werkzeug.utils import import_string

from config import WeChatConfig


blueprints = [
    "model_message.message:message"
]


def create_app():
    """
    # 创建app
    :return:
    """
    app = Flask(__name__)

    CORS(app)

    # regist blueprints
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp, url_prefix="/" + bp_name.split(":")[1])

    # ---------------- logger settings -----------------------------------------
    fmt_str = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s"
    debug_formatter = Formatter(fmt_str)
    debug_handler = TimedRotatingFileHandler(WeChatConfig.LOG_PATH + "debug.log",
                                             "D", 1, 10)
    debug_handler.suffix = "%Y%m%d.log"
    debug_handler.setFormatter(debug_formatter)
    debug_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(debug_handler)

    error_formatter = Formatter('''Message type:   %(levelname)s
Location:       %(pathname)s:%(lineno)d
Module:         %(module)s
Function:       %(funcName)s
Time:           %(asctime)s
Message:        %(message)s
----------------------------------------------------------------------------''')
    error_handler = TimedRotatingFileHandler(WeChatConfig.LOG_PATH + "error.log",
                                             "D", 1, 10)
    error_handler.suffix = "%Y%m%d.log"
    error_handler.setFormatter(error_formatter)
    error_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_handler)

    return app
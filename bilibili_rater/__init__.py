#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/16 04:12
# ide： PyCharm
# file: __init__.py
from .bilibili_rater import BilibiliRater
from .handler import *
import os
import sys
import logging
from .scheduler import Scheduler
import datetime
from pathlib import Path

try:
    _is_debug = os.environ["IS_DEBUG"]
except KeyError:
    _is_debug = "0"



if _is_debug == "1":
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    home_dir = Path.home()
    log_dir = home_dir / '.bilibiliraterlog'
    log_dir.mkdir(exist_ok=True)
    log_file_path = log_dir / f'log_{current_time}.log'
    logging.basicConfig(

        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # 输出到文件
            logging.FileHandler(log_file_path, mode='a', encoding='utf-8'),
            # 同时输出到控制台
            logging.StreamHandler()
        ]
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


__all__ = [
    "BilibiliRater",
    "SeasonEpisodeHandler",
    "DotHandler",
    "NormalLetterHandler",
    "OnlyNumberHandler",
    "Scheduler",
]

__version__ = "0.1.0"

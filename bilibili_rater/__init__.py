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
import logging
from .scheduler import Scheduler

try:
    _is_debug = os.environ["IS_DEBUG"]
except KeyError:
    _is_debug = "0"

if _is_debug == "1":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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

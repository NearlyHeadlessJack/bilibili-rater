#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/17 10:25
# ide： PyCharm
# file: _cache.py
import logging
import os
from .exceptions import DescHandlerError


class Cache:
    def __init__(self, uid: int, handler_name: str):
        self.uid: int = uid
        self.handler_name: str = handler_name
        logging.info(f"创建缓存实例, uid:{uid}, handler_name: {handler_name}")
        self.path = f"./.bilibiliratercache/{uid}_{handler_name}"

    def use_cache(self, bvid: str) -> bool:
        file_path = self.path
        logging.info("正在检查缓存")
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content != bvid:
                        logging.info("缓存未命中")
                        with open(file_path, "w", encoding="utf-8") as ff:
                            ff.write(f"{bvid}")
                        return False
                    logging.info("缓存命中")
                    return True
            else:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"{bvid}")
                logging.info("新建缓存")
                return False
        except Exception as e:
            logging.error(f"使用缓存时发生错误:{e}")
            raise DescHandlerError(f"使用缓存时发生错误:{e}")

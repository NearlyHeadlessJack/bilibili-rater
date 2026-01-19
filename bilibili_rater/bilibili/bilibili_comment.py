#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/17 01:44
# ide： PyCharm
# file: bilibili_comment.py
from bilibili_api import Credential, comment
from bilibili_rater.exceptions import DescHandlerError
from bilibili_rater.cache import Cache
import logging, os



class BilibiliComment:
    def __init__(self, credential: Credential, resource_cn_name: str):
        """
        :param credential: 登录凭证
        :param resource_cn_name:  节目中文名
        """
        logging.debug("创建BilibiliComment实例")
        self.credential: Credential = credential
        self.cn_name = resource_cn_name

    def create_comment(
        self, s: int, e: int, rate: str, title=None, is_show_title=None
    ) -> str:
        msg1 = f"本集是《{self.cn_name}》第{s}季，第{e}集。"
        msg2 = f"标题为{title}。"
        msg3 = f"本集imdb评分为{rate}。"
        if is_show_title:
            msg = msg1 + msg2 + msg3
            logging.info(f"准备发送评论: {msg}")
            return msg
        else:
            msg = msg1 + msg3
            logging.info(f"准备发送评论: {msg}")
            return msg

    async def post_comment(self, bvid: str, msg: str, cache:Cache):
        logging.info("正在发送评论")
        try:
            is_debug = os.environ.get("IS_DEBUG")
        except KeyError:
            is_debug = "0"

        if is_debug == "1":
            logging.debug("debug模式，不发送评论")
            return
        try:
            resp = await comment.send_comment(
                text=msg,
                oid=bvid,
                credential=self.credential,
                type_=comment.CommentResourceType.VIDEO,
            )
            logging.info("评论发送成功！", resp)
            logging.debug(f"更新缓存, bvid: {bvid}")
            cache.update_cache(bvid=bvid)
            logging.info(f"缓存更新成功, bvid: {bvid}")

        except Exception as e:
            logging.error(f"评论发送失败，错误信息：{e}")
            raise DescHandlerError(f"评论发送失败，错误信息：{e}")

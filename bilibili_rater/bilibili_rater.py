#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/16 04:12
# ide： PyCharm
# file: bilibili_rater.py
import logging, os
from .imdb import ImdbFetcher
from bilibili_api import Credential
from .bilibili import BilibiliFetcher, BilibiliComment
from .exceptions import DescHandlerError
from .cache import Cache


class BilibiliRater:
    def __init__(
        self,
        uploader_uid: int,
        credential: Credential,
        handler,
        resource_id: str,
        api_key: str,
        resource_cn_name: str,
        is_show_title: bool,
        seconds: int = 60 * 15,
    ):
        """
        :param uploader_uid: 被跟踪up主的uid
        :param credential: 登录凭证
        :param handler: 简介第一行信息的解析函数
        :param resource_id: 节目的imdb的id(注意是总节目的id，不是单集的id)
        :param api_key: OMDB API KEY
        :param resource_cn_name: 节目中文名，用于评论区
        :param is_show_title: 是否显示单集标题(注意合规)
        :param seconds: 每隔多少秒运行一次
        """

        logging.debug("创建BilibiliRater实例")
        self._is_show_title: bool = is_show_title

        self._imdb_fetcher = ImdbFetcher(
            api_key=api_key, resource_id=resource_id, is_show_title=is_show_title
        )
        # 上传者uid
        self._uploader: int = uploader_uid

        # 视频资源id
        self._resource_id: str = resource_id

        # 匹配模式（简介第一行）
        self._handler = handler

        # 视频资源中文名
        self._resource_cn_name: str = resource_cn_name

        self._credential: Credential = credential

        self._commenter = BilibiliComment(
            credential=self._credential, resource_cn_name=resource_cn_name
        )
        self._cache = Cache(uid=self._uploader, handler_name=handler.__qualname__)

        self._seconds = seconds

        self.job_name = (
            f"{self._uploader}-{self._handler.__qualname__}-{self._resource_cn_name}"
        )

    async def _run_fetch_new_video_desc(self):
        latest_video = await BilibiliFetcher(uploader=self._uploader).fetch()
        logging.debug(f"最新视频简介：{repr(latest_video['desc'])}")
        logging.debug(f"最新视频BVID: {latest_video['bvid']}")
        try:
            season, episode = self._handler(desc=latest_video["desc"])
            if season == 0:
                logging.error("简介解析失败")
                raise DescHandlerError
            return season, episode, latest_video["bvid"]
        except Exception as e:
            logging.error(f"在解析简介时发生错误:{e}")
            raise DescHandlerError

    def _fetch_imdb_rating(self, season: int, episode: int):
        try:
            rating = self._imdb_fetcher.fetch(season=season, episode=episode)
            return rating
        except Exception:
            logging.error("IMDB获取出错")
            raise DescHandlerError

    async def run(self):
        try:
            s, e, bvid = await self._run_fetch_new_video_desc()
            logging.info(
                f"解析到节目为：{self._resource_cn_name} 第{s}季 第{e}集，BV号：{bvid}"
            )

            if self._cache.use_cache(bvid=bvid):
                logging.info("缓存命中，本次更新已跳过")
                return

            imdb_msg = self._imdb_fetcher.fetch(season=s, episode=e)
            msg = self._commenter.create_comment(
                s=s,
                e=e,
                rate=imdb_msg["rating"],
                title=imdb_msg["title"],
                is_show_title=self._is_show_title,
            )
            await self._commenter.post_comment(bvid=bvid, msg=msg)

        except DescHandlerError as ee:
            logging.error(f"发生错误:{ee}，本次更新已跳过")
            return
        except Exception as e:
            logging.error(f"发生未知错误：{e}")
            return

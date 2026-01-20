#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/16 23:54
# ide： PyCharm
# file: fetch_imdb.py
import requests
import logging
from bilibili_rater.exceptions import DescHandlerError


def get_imdb_rating(
    imdb_id: str, season: int, _episode: int, api: str, is_show_title=False
) -> dict:
    """
    获取IMDB评分
    :param imdb_id: IMDB ID  一般以tt开头
    :param season: 剧集季号
    :param _episode: 集号
    :param api: OMDB网站的api
    :param is_show_title: 是否需要单集标题
    :return: 评分信息及标题信息(如需要)
    """
    logging.info(
        f"正在获取IMDB评分，IMDB ID：{imdb_id}，季号：{season}，集号：{_episode}，显示标题：{is_show_title}"
    )
    url = f"http://www.omdbapi.com/?apikey={api}&i={imdb_id}&Season={str(season)}"
    response = requests.get(url).json()
    for episode in response["Episodes"]:
        if episode["Episode"] == str(_episode):
            logging.info(
                f"找到目标资源imdb信息: S{season}E{episode['Episode']} 标题: {episode['Title']} 评分: {episode['imdbRating']}"
            )
            if is_show_title:
                return {"title": episode["Title"], "rating": episode["imdbRating"]}
            return {"rating": episode["imdbRating"], episode: None}
    return {"rating": None, "title": None}


class ImdbFetcher:
    def __init__(self, api_key: str, resource_id: str, is_show_title=False):
        self.api_key = api_key
        self.id = resource_id
        self.is_show_title = is_show_title

    def fetch(self, season: int, episode: int):
        try:
            result = get_imdb_rating(
                self.id, season, episode, self.api_key, self.is_show_title
            )
            return result
        except Exception as e:
            logging.error(f"获取IMDB信息过程中发生错误：{e}")
            raise DescHandlerError(f"获取IMDB信息过程中发生错误：{e}")

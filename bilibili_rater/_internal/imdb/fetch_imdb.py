#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/16 23:54
# ide： PyCharm
# file: fetch_imdb.py
import requests
import logging
from bilibili_rater.exceptions import DescHandlerError, ImdbItemNotFound
from abc import ABC


def omdb_get_imdb_rating_no_ranking(
    imdb_id: str, season: int, _episode: int, api: str
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

    url = f"http://www.omdbapi.com/?apikey={api}&i={imdb_id}&Season={str(season)}"
    response = requests.get(url).json()
    for episode in response["Episodes"]:
        if episode["Episode"] == str(_episode):
            logging.info(
                f"找到目标资源imdb信息: S{season}E{episode['Episode']} 标题: {episode['Title']} 评分: {episode['imdbRating']}"
            )
            return {
                "rating": episode["imdbRating"],
                "title": episode["Title"],
                "ranking": None,
            }
    logging.error(f"未找到S{season}E{_episode}的imdb信息")
    raise ImdbItemNotFound(f"未找到S{season}E{_episode}的imdb信息")


def omdb_get_imdb_rating_with_ranking(
    imdb_id: str, season: int, _episode: int, api: str, is_show_title=False
) -> dict:
    url = f"http://www.omdbapi.com/?apikey={api}&i={imdb_id}&Season={str(season)}"
    response = requests.get(url).json()
    a = response["Episodes"]
    try:
        sorted_movies = sorted(a, key=lambda x: float(x["imdbRating"]), reverse=True)
        i = 0
        total = len(sorted_movies)
        for episode in sorted_movies:
            i += 1
            if episode["Episode"] == str(_episode):
                rank = f"{i}/{total}"
                logging.info(
                    f"找到目标资源imdb信息: S{season}E{episode['Episode']} 评分: {episode['imdbRating']} 排名: {rank}"
                )
                return {
                    "title": episode["Title"],
                    "rating": episode["imdbRating"],
                    "ranking": rank,
                }

    except ValueError:
        logging.error("本季有无法解析的IMDB评分，不提供ranking排名")
        return omdb_get_imdb_rating_no_ranking(
            imdb_id=imdb_id, season=season, _episode=_episode, api=api
        )
    except Exception as e:
        logging.error(f"获取IMDB信息过程中发生错误：{e}")
        raise ImdbItemNotFound(f"获取IMDB信息过程中发生错误：{e}")
    logging.error(f"未找到S{season}E{_episode}的imdb信息")
    raise ImdbItemNotFound(f"未找到S{season}E{_episode}的imdb信息")


class ImdbFetcher(ABC):
    def __init__(self, is_show_ranking: bool | None, is_show_title: bool | None):
        self.is_show_title = is_show_title
        self.is_show_ranking = is_show_ranking
        pass

    def fetch(self, resource_id: str, season: int, episode: int):
        pass


class OmdbFetcher(ImdbFetcher):
    def __init__(self, api_key: str, is_show_ranking=False, is_show_title=False):
        super().__init__(is_show_ranking, is_show_title)
        self.api_key = api_key

    def fetch(self, resource_id: str, season: int, episode: int):
        logging.info(
            f"正在获取IMDB评分，IMDB ID：{resource_id}，季号：{season}，集号：{episode}，显示标题：{self.is_show_title},显示排名:{self.is_show_ranking}"
        )
        if not self.is_show_ranking:
            try:
                result = omdb_get_imdb_rating_no_ranking(
                    resource_id, season, episode, self.api_key
                )
                return result
            except ImdbItemNotFound:
                raise ImdbItemNotFound(f"未找到S{season}E{episode}的imdb信息")
            except Exception as e:
                logging.error(f"获取IMDB信息过程中发生错误：{e}")
                raise DescHandlerError(f"获取IMDB信息过程中发生错误：{e}")
        else:
            try:
                result = omdb_get_imdb_rating_with_ranking(
                    resource_id, season, episode, self.api_key
                )
                return result
            except ImdbItemNotFound:
                raise ImdbItemNotFound(f"未找到S{season}E{episode}的imdb信息")
            except Exception as e:
                logging.error(f"获取IMDB信息过程中发生错误：{e}")
                raise DescHandlerError(f"获取IMDB信息过程中发生错误：{e}")

#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/26 17:11
# ide： PyCharm
# file: imdbinfo_fetcher.py
from imdbinfo import get_movie, get_season_episodes
from bilibili_rater._internal.imdb.fetch_imdb import ImdbFetcher
import logging


class DirectFetcher(ImdbFetcher):
    def __init__(self, is_show_ranking: bool | None, is_show_title: bool | None):
        super().__init__(is_show_ranking, is_show_title)
        self.is_show_title = is_show_title
        self.is_show_ranking = is_show_ranking

    def fetch(self, resource_id: str, season: int, episode: int):
        logging.info(
            f"正在获取IMDB评分，IMDB ID：{resource_id}，季号：{season}，集号：{episode}，显示标题：{self.is_show_title},显示排名:{self.is_show_ranking}"
        )
        resource = get_movie(resource_id)
        resource_season = get_season_episodes(resource.imdb_id, season=season).episodes
        season_episodes_num = len(resource_season)
        requested_episode = resource_season[episode - 1]
        requested_episode_rating, requested_episode_title = (
            requested_episode.rating,
            requested_episode.title,
        )
        logging.info(
            f"找到目标资源信息, 本集标题为{requested_episode_title}, 本集评分为{requested_episode_rating}"
        )
        if self.is_show_title and not self.is_show_ranking:
            return {
                "title": requested_episode_title,
                "rating": requested_episode_rating,
                "ranking": None,
            }
        elif self.is_show_title and self.is_show_ranking:
            sorted_season = sorted(
                resource_season, key=lambda x: x.rating, reverse=True
            )
            idx = 1
            for _episode in sorted_season:
                if _episode.episode == episode:
                    break
                idx += 1
            return {
                "title": requested_episode_title,
                "rating": requested_episode_rating,
                "ranking": f"{idx}/{season_episodes_num}",
            }
        else:
            return {"rating": requested_episode_rating, "title": None, "ranking": None}

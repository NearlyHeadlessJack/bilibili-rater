#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2026/1/17 11:27
# ide： PyCharm
# file: _scheduler.py
import asyncio, logging, pytz
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from .bilibili_rater import BilibiliRater


class Scheduler:
    _jobstores = {"default": MemoryJobStore()}

    _executors = {"default": ThreadPoolExecutor(1)}  # 只使用1个工作线程

    _job_defaults = {
        "coalesce": False,  # 错过的任务不合并执行
        "max_instances": 1,  # 每个任务同时只能有1个实例运行
        "misfire_grace_time": 30,  # 任务错过执行后，最多容忍30秒
    }

    def __init__(self):
        logging.info("创建Scheduler实例")
        self._scheduler = AsyncIOScheduler(
            jobstores=self._jobstores,
            executors=self._executors,
            job_defaults=self._job_defaults,
            timezone=pytz.timezone("Asia/Shanghai"),  # 设置时区
        )
        self._now = datetime.now()

    def add_job(self, rater: BilibiliRater):
        logging.info(f"添加任务: {rater.job_name}")
        job_num = len(self._scheduler.get_jobs())
        self._scheduler.add_job(
            rater.run,
            "interval",
            seconds=rater._seconds,
            start_date=self._now + timedelta(seconds=20 * job_num),
            id="bilibili_rater_" + str(job_num),
            replace_existing=True,
        )

    async def run_forever(self):
        logging.info(f"开始循环运行")
        self._scheduler.start()
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()
            logging.info("程序运行结束")
        except Exception as e:
            logging.error(f"运行时发生错误：{e}")

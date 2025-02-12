# from celery import shared_task
from .task import run_task
import time
import asyncio
from celery import shared_task


@shared_task
def run_scraping(start_index):
        run_task(start_index)



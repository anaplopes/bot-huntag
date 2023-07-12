import json
import sys

from src.repository.filter import FilterRepository
from src.utils.logger import logger


def data_filter():
    repo = FilterRepository()
    list_filter = repo.select_all()
    if not list_filter:
        path = "migration\\filter_huntag_v2.json"
        if sys.platform.startswith("linux"):
            path = "migration/filter_huntag_v2.json"

        logger.info("Creating filters.")
        file = open(file=path, mode="r", encoding="utf-8")
        data = json.load(file)
        repo.insert_filter(data)
        logger.info("Filter created successfully.")
        file.close()
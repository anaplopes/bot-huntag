import json
from src.utils.logger import logger

from src.repository.filter import FilterRepository


def data_filter():
    repo = FilterRepository()
    list_filter = repo.select_all()
    if not list_filter:
        logger.info("Creating filters.")
        file = open(file="src\\data\\filter_huntag_v2.json", mode="r", encoding="utf-8")
        data = json.load(file)
        repo.insert_filter(data)
        logger.info("Filter created successfully.")
        file.close()

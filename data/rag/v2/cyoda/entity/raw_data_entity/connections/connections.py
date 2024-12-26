import logging

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_data_helper(code, country, name):
    #you need to write code here
    pass


def ingest_data(code=None, country=None, name=None):
    data = _get_data_helper(code, country, name)
    logger.info(data)
    return data


def main():
    ingest_data(code="579000282425", country="", name="")


if __name__ == "__main__":
    main()

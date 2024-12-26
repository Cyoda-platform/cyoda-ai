import logging

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_balance_responsible_parties(code=None, country=None, name=None):
    url = "https://api.opendata.esett.com/EXP01/BalanceResponsibleParties"
    params = {}
    if code:
        params["code"] = code
    if country:
        params["country"] = country
    if name:
        params["name"] = name
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else response.text


def ingest_data(code=None, country=None, name=None):
    data = get_balance_responsible_parties(code, country, name)
    logger.info(data)
    return data


def main():
    ingest_data(code="579000282425", country="", name="")


if __name__ == "__main__":
    main()

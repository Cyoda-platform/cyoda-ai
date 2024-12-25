import requests

BASE_URL = "https://api.opendata.esett.com"


def get_balance_responsible_parties(code=None, country=None, name=None):
    """Retrieve a list of Balance Responsible Parties based on optional parameters."""
    endpoint = "/EXP01/BalanceResponsibleParties"
    params = {}
    if code:
        params["code"] = code
    if country:
        params["country"] = country
    if name:
        params["name"] = name
    response = requests.get(BASE_URL + endpoint, params=params)
    return response.json()


def ingest_data(code=None, country=None, name=None):
    """Ingest data from the external data source."""
    data = get_balance_responsible_parties(code, country, name)
    return data


def main():
    # Test the ingest_data function
    print(ingest_data(code="7080005051286", country="FI", name=""))


if __name__ == "__main__":
    main()

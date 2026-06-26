import requests


def get_country_info(country_name: str):
    """
    External API tool using REST Countries API.
    """
    url = f"https://restcountries.com/v3.1/name/{country_name}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {"error": "Could not fetch country information."}

        data = response.json()[0]

        currencies = data.get("currencies", {})
        currency_codes = list(currencies.keys()) if currencies else ["Unknown"]

        return {
            "name": data.get("name", {}).get("common", "Unknown"),
            "capital": data.get("capital", ["Unknown"])[0],
            "region": data.get("region", "Unknown"),
            "population": data.get("population", "Unknown"),
            "currency": currency_codes,
        }

    except Exception as e:
        return {"error": str(e)}
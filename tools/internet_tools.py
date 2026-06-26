import requests
from urllib.parse import quote


HEADERS = {
    "User-Agent": "MultiAgentRAGAssistant/1.0 (learning-project)"
}


def clean_query(query: str) -> str:
    return query.strip().replace(" ", "_")


def get_wikipedia_summary_by_title(title: str):
    try:
        title = quote(title)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            return None

        data = response.json()
        extract = data.get("extract")

        if extract:
            return extract

        return None

    except Exception as e:
        print("Wikipedia title error:", e)
        return None


def search_wikipedia_title(query: str):
    try:
        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "opensearch",
            "search": query,
            "limit": 1,
            "namespace": 0,
            "format": "json",
        }

        response = requests.get(url, params=params, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            return None

        data = response.json()

        if len(data) >= 2 and data[1]:
            return data[1][0]

        return None

    except Exception as e:
        print("Wikipedia search error:", e)
        return None


def get_duckduckgo_answer(query: str):
    try:
        url = "https://api.duckduckgo.com/"

        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 0,
        }

        response = requests.get(url, params=params, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            return None

        data = response.json()

        return (
            data.get("AbstractText")
            or data.get("Answer")
            or data.get("Definition")
        )

    except Exception as e:
        print("DuckDuckGo error:", e)
        return None


def get_internet_answer(query: str):
    direct_title = clean_query(query)
    answer = get_wikipedia_summary_by_title(direct_title)

    if answer:
        return answer

    searched_title = search_wikipedia_title(query)

    if searched_title:
        answer = get_wikipedia_summary_by_title(searched_title)

        if answer:
            return answer

    answer = get_duckduckgo_answer(query)

    if answer:
        return answer

    return (
        "I could not find reliable information from free internet sources. "
        "Please check your internet connection or try a more specific question."
    )
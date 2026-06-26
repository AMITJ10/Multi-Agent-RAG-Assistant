from tools.api_tools import get_country_info


def extract_country_name(question: str):
    """
    Simple rule-based country extraction.
    """
    question = question.lower()

    countries = [
        "india", "united states", "usa", "america", "china", "japan",
        "russia", "france", "germany", "canada", "australia",
        "united kingdom", "uk", "brazil", "south africa"
    ]

    for country in countries:
        if country in question:
            if country in ["usa", "america"]:
                return "United States"
            if country == "uk":
                return "United Kingdom"
            return country.title()

    words = question.replace("?", "").split()
    return words[-1].title() if words else "India"


def format_country_answer(api_result):
    """
    Formats API result into readable answer.
    """
    if isinstance(api_result, dict) and "error" in api_result:
        return api_result["error"]

    return (
        f"Country: {api_result.get('name')}\n"
        f"Capital: {api_result.get('capital')}\n"
        f"Region: {api_result.get('region')}\n"
        f"Population: {api_result.get('population')}\n"
        f"Currency: {', '.join(api_result.get('currency', []))}"
    )


def api_agent(state):
    """
    API agent without OpenAI dependency.
    """
    question = state["question"]

    country_name = extract_country_name(question)
    api_result = get_country_info(country_name)
    answer = format_country_answer(api_result)

    return {
        "api_result": str(api_result),
        "draft_answer": answer
    }
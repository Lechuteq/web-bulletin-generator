def get_link_system_prompt():
    """
    Silniejszy prompt systemowy: wymusza odpowiedź wyłącznie w JSON-ie,
    bez dodatkowych wyjaśnień, bez komentarzy i bez formatowania w blokach kodu.
    """
    return (
        "You are an assistant that MUST respond only with valid JSON and nothing else. "
        "Do not add any explanation, commentary, or markdown. Do not wrap the JSON in ```."
        "Given a list of links from a website, return a JSON object with a single key "
        '"links" containing an array of objects with keys "type" and "url". '
        "Example:\n"
        '{"links":[{"type":"about page","url":"https://example.com/about"}]}'
    )



def get_links_user_prompt(website):
    """Prompt użytkownika — przekazuje listę linków z danej strony"""
    user_prompt = (
        f"Here is the list of links on the website {website.url}. "
        "Please decide which are relevant links for a brochure about the company. "
        "Respond in JSON with full https URLs. "
        "Do not include Terms of Service, Privacy, or email links.\n\nLinks:\n"
    )
    user_prompt += "\n".join(website.links)
    return user_prompt

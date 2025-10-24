import requests
from bs4 import BeautifulSoup

class Website:
    def __init__(self, url: str):
        self.url = url
        self.html = None
        self.links = []

    def get_contents(self):
        """Pobiera treść HTML strony i zapisuje w self.html"""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.html = response.text
            self._extract_links()
            return self.html
        except requests.RequestException as e:
            return f"Błąd podczas pobierania strony: {e}"

    def _extract_links(self):
        """Ekstrahuje wszystkie linki z treści HTML"""
        if not self.html:
            return
        soup = BeautifulSoup(self.html, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("http"):
                self.links.append(href)
            elif href.startswith("/"):
                # konwersja linków względnych na absolutne
                base = self.url.rstrip("/")
                self.links.append(f"{base}{href}")

from datetime import datetime
from scraper import Website
from llm_utils import query_local_llm
import streamlit as st


def summarize_page(url: str, summary_instruction: str) -> str:
    """
    Pobiera treść strony i generuje streszczenie przy użyciu lokalnego LLM.
    """
    try:
        site = Website(url)
        html = site.get_contents()
        if "Błąd" in html or len(html) < 200:
            return "Nie udało się pobrać zawartości strony."
        # zapytanie do lokalnego LLM
        response = query_local_llm(
            system_prompt="You are a helpful assistant that summarizes web pages clearly and briefly.",
            user_prompt=f"{summary_instruction}\n\nTreść strony:\n{html[:5000]}"
        )
        return response.strip()
    except Exception as e:
        return f"Błąd podczas analizy: {e}"


def build_bulletin(links_data, summary_instruction):
    """
    Tworzy kompletny biuletyn informacyjny w formacie Markdown.
    Dla każdego linku generuje streszczenie treści strony przy użyciu lokalnego LLM.
    """
    if not links_data:
        return "⚠️ Brak danych do wygenerowania biuletynu."

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = f"# 📰 Biuletyn informacyjny\n\n📅 Data: {now}\n\n---\n\n## 🌐 Wybrane strony\n\n"
    sections = []

    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(links_data)

    for i, link in enumerate(links_data, start=1):
        link_type = link.get("type", "Strona")
        link_url = link.get("url", "Brak adresu URL")

        status_text.text(f"Analiza {i}/{total}: {link_url}")
        summary = summarize_page(link_url, summary_instruction)

        section = (
            f"### {i}. {link_type.capitalize()}\n"
            f"🔗 [{link_url}]({link_url})\n\n"
            f"**Streszczenie:**\n{summary}\n\n"
            "---\n"
        )
        sections.append(section)

        progress_bar.progress(i / total)

    status_text.text("✅ Zakończono generowanie biuletynu.")
    progress_bar.empty()

    return header + "\n".join(sections)

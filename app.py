# Project web scraper with Streamlit

import streamlit as st
import json
import re
from scraper import Website
from prompts import get_link_system_prompt, get_links_user_prompt
from llm_utils import query_local_llm
from report_generator import build_bulletin


# -----------------------------------
# 🔧 Pomocnicza funkcja do parsowania JSON
# -----------------------------------
def extract_json_from_text(text: str):
    """Heurystyka: znajduje najbardziej prawdopodobny fragment JSON w tekście."""
    if not text or not isinstance(text, str):
        return None

    cleaned = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).strip()

    starts = [m.start() for m in re.finditer(r"\{", cleaned)]
    ends = [m.start() for m in re.finditer(r"\}", cleaned)]

    if not starts or not ends:
        try:
            return json.loads(cleaned)
        except Exception:
            return None

    candidates = []
    for i in starts:
        for j in reversed(ends):
            if j > i:
                candidates.append(cleaned[i:j+1])
    candidates = sorted(set(candidates), key=len, reverse=True)

    for c in candidates:
        try:
            return json.loads(c)
        except Exception:
            continue

    try:
        return json.loads(cleaned)
    except Exception:
        return None


# -----------------------------------
# 🧭 Konfiguracja strony
# -----------------------------------
st.set_page_config(page_title="Web Bulletin Generator", page_icon="📰", layout="centered")
st.title("🕸️ Web Bulletin Generator")
st.markdown("Podaj adres strony, aby stworzyć biuletyn informacyjny na podstawie analizy linków i treści.")


# -----------------------------------
# 💾 Inicjalizacja stanu aplikacji
# -----------------------------------
if "parsed_links" not in st.session_state:
    st.session_state.parsed_links = None

if "selected_links" not in st.session_state:
    st.session_state.selected_links = []

if "bulletin" not in st.session_state:
    st.session_state.bulletin = None


# -----------------------------------
# 🧮 Formularz wejściowy
# -----------------------------------
with st.form("scrape_form"):
    url = st.text_input("🔗 Adres URL strony", placeholder="https://example.com")
    submitted = st.form_submit_button("🔍 Rozpocznij analizę strony")


# -----------------------------------
# 🧠 Główna logika aplikacji
# -----------------------------------
if submitted:
    if not url.strip():
        st.warning("⚠️ Podaj poprawny adres URL.")
    else:
        website = Website(url)
        html_content = website.get_contents()

        if "Błąd" in html_content:
            st.error(html_content)
        else:
            st.success(f"✅ Strona pobrana. Znaleziono {len(website.links)} linków.")
            st.markdown("### 🔗 Przykładowe linki ze strony:")
            st.write(website.links[:10])

            with st.spinner("🧠 Analizuję linki lokalnym modelem..."):
                system_prompt = get_link_system_prompt()
                user_prompt = get_links_user_prompt(website)
                response = query_local_llm(system_prompt, user_prompt)

            st.markdown("### 🧩 Wynik analizy linków:")
            parsed = extract_json_from_text(response)

            if parsed is None:
                st.warning("⚠️ Model nie zwrócił poprawnego JSON. Pokażę surową odpowiedź:")
                st.code(response)
            else:
                st.json(parsed)
                st.session_state.parsed_links = parsed["links"]


# -----------------------------------
# ✅ Wybór linków przez użytkownika
# -----------------------------------
if st.session_state.parsed_links:
    st.markdown("### 🧩 Wybierz linki do biuletynu:")

    selected_links = []
    for i, link in enumerate(st.session_state.parsed_links):
        label = f"{i+1}. {link.get('type', 'Link')} — {link.get('url', '')}"
        if st.checkbox(label, key=f"chk_{i}"):
            selected_links.append(link)

    st.session_state.selected_links = selected_links

    if selected_links:
        if st.button("📄 Generuj biuletyn informacyjny"):
            with st.spinner("✍️ Tworzę biuletyn..."):
                bulletin = build_bulletin(
                    selected_links,
                    "Streszcz każdy link jasno i zwięźle — opisz jego treść i znaczenie biznesowe."
                )
                st.session_state.bulletin = bulletin


# -----------------------------------
# 💾 Prezentacja i pobieranie pliku
# -----------------------------------
if st.session_state.bulletin:
    st.markdown("### 📰 Biuletyn informacyjny:")
    st.markdown(st.session_state.bulletin)
    st.download_button(
        label="💾 Pobierz biuletyn (Markdown)",
        data=st.session_state.bulletin,
        file_name="biuletyn.md",
        mime="text/markdown"
    )


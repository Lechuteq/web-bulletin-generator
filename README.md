# 🕸️ Web Bulletin Generator

A Streamlit-based application that scrapes a website, analyzes its links using a **local LLM (via Ollama)**, and generates an **informative Markdown bulletin** summarizing the content of selected pages.

---

## 🚀 Features

- 🔍 Scrapes any website and extracts hyperlinks  
- 🧠 Uses a **local LLM (Ollama)** for intelligent link analysis  
- 📰 Builds a structured **information bulletin (.md)** with summaries of selected links  
- ✅ Interactive **link selection interface** in Streamlit  
- 📊 Progress bar showing real-time summarization status  
- 💾 Export bulletin as a Markdown file

---

## 🧩 Project Structure

web_bulletin_generator/  
│  
├── app.py # Main Streamlit app  
├── scraper.py # Web scraping logic  
├── prompts.py # LLM prompt templates  
├── llm_utils.py # Ollama LLM connection  
├── report_generator.py # Bulletin generation with progress tracking  
├── requirements.txt # Python dependencies  
└── README.md # Project documentation  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

git clone https://github.com/Lechuteq/web-bulletin-generator.git
cd web-bulletin-generator

### 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

### 3️⃣ Install dependencies
pip install -r requirements.txt

streamlit
beautifulsoup4
requests
ollama

### 4️⃣ Ensure Ollama is running locally

Install Ollama (if not yet):

https://ollama.ai
ollama pull hf.co/SpeakLeash/Bielik-11B-v2.6-Instruct-GGUF:Q4_K_M
ollama run hf.co/SpeakLeash/Bielik-11B-v2.6-Instruct-GGUF:Q4_K_M

### ▶️ Running the App

Once Ollama is running locally, launch the Streamlit app:
python -m streamlit run app.py

## 🧠 Usage Workflow

1. Enter a website URL

2. Click “🔍 Analyze Website”

3. Review the extracted links and select which ones to summarize

4. Click “📄 Generate Bulletin”

5. Watch the progress bar as your local LLM summarizes each page

6. Download your finished Markdown bulletin

# 🗂️ Output Example

Biuletyn informacyjny (Markdown):

# 📰 Web Bulletin
📅 Date: 2025-10-25

---

## 🌐 Selected Pages

### 1. Blog
🔗 https://example.com/blog

**Summary:**
The page discusses new AI-driven web tools and content analysis using local language models.

---

🧑‍💻 Technology Stack

Python 3.10+

Streamlit – interactive UI

BeautifulSoup4 – web scraping

Ollama – local LLM inference

Markdown Export – structured report generation

🌟 Future Improvements

 Add asynchronous summarization

 Add user-configurable LLM parameters (temperature, tokens, model name)

 Cache summaries for large sites

 Add export to PDF/HTML

👨‍💻 Author

Lesław Nowakowski  
AI Enthusiast | Python Developer | BI & KYC Analyst | DPO | Automatization Specialist  
🔗 www.linkedin.com/in/leslaw-nowakowski

🖤 License

MIT License – free for use and modification with attribution.


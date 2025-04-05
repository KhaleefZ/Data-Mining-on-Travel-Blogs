# 🌍 Travel Blog Scraper 🧳✈️  
**Your Personal Guide to Exploring the World Through Blogs**

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Tkinter GUI](https://img.shields.io/badge/Tkinter-GUI-blueviolet)
![Web Scraping](https://img.shields.io/badge/Web--Scraping-BeautifulSoup-brightgreen)
![NLP](https://img.shields.io/badge/NLP-TextBlob-orange)

---

## 📌 Overview

**Travel Blog Scraper** is a user-friendly desktop application that scrapes travel blogs from [Nomadic Matt](https://www.nomadicmatt.com) based on user input and performs intelligent content analysis. With just a location name, you can:

- ✨ Extract blog titles and links
- 💾 Save full blog content as text
- 🌥 Generate word clouds
- 📊 Calculate ML prediction metrics
- 📈 Analyze top keywords & sentiment

---

## 🚀 Features

| Feature                        | Description |
|-------------------------------|-------------|
| 🔍 Blog Search                | Search blogs by location keyword |
| 💾 Save Blog                  | Save full blog content as `.txt` |
| 🌤 Word Cloud Visualization   | Auto-generate cloud of top words |
| 🧠 ML Metric Calculation      | TP, FP, TN, FN, Precision, Recall |
| 💬 Sentiment Analysis         | Analyze tone of content (Polarity & Subjectivity) |
| 🔑 Keyword Search             | Search and highlight specific keywords |
| 🎨 GUI                        | Intuitive Tkinter-based interface |


---

## 🛠️ Tech Stack

- **Python 3.10+**
- `Tkinter` – for GUI interface
- `requests` & `BeautifulSoup` – for web scraping
- `TextBlob` – sentiment analysis
- `WordCloud` – for visual representation
- `scikit-learn` & `joblib` – for ML classification
- `Pillow` – image handling in GUI

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/travel-blog-scraper.git
cd travel-blog-scraper
pip install -r requirements.txt
python main.py

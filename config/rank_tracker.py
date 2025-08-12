import os
import time
from serpapi import GoogleSearch

# قراءة الكلمات من الملف
with open("config/keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]

# مفتاح SerpAPI (هات المفتاح المجاني من serpapi.com)
API_KEY = os.getenv("SERPAPI_KEY", "YOUR_API_KEY_HERE")

# دالة لجلب الترتيب
def get_rank(keyword):
    search = GoogleSearch({
        "q": keyword,
        "location": "Kuwait",
        "hl": "ar",
        "gl": "kw",
        "google_domain": "google.com",
        "api_key": API_KEY
    })
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    for i, result in enumerate(organic_results, start=1):
        if "khedmakw.com" in result.get("link", ""):
            return i
    return None

# تنفيذ التتبع
for kw in keywords:
    rank = get_rank(kw)
    print(f"{kw} -> {rank if rank else 'Not Found'}")
    time.sleep(2)  # عشان ما يتعملش حظر من API

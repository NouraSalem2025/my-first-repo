import os, csv, time, pathlib
from datetime import datetime
from serpapi import GoogleSearch

# إعدادات عامة
TARGET_DOMAIN = os.getenv("TARGET_DOMAIN", "khedmakw.com").lower()  # عدّل الدومين لو عايز
API_KEY = os.getenv("SERPAPI_KEY", "YOUR_API_KEY_HERE")  # هنضيف المفتاح كـ Secret بعدين

KEYWORDS_FILE = "config/keywords.txt"
REPORTS_DIR = pathlib.Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = REPORTS_DIR / "rank_history.csv"

def ensure_csv_header(path):
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(
                ["timestamp","keyword","position","result_url","result_title"]
            )

def get_rank(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "google_domain": "google.com",
        "gl": "kw",   # الكويت
        "hl": "ar",
        "num": "100",
        "api_key": API_KEY
    }
    results = GoogleSearch(params).get_dict()
    organic = results.get("organic_results", []) or []
    for i, r in enumerate(organic, start=1):
        link = (r.get("link") or "").lower()
        if TARGET_DOMAIN and TARGET_DOMAIN in link:
            return i, r.get("link",""), r.get("title","")
    return 101, "", ""   # لو مش موجود ضمن أول 100

def main():
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        raise SystemExit("حط SERPAPI_KEY كمُتغيّر سرّي (Secret) قبل التشغيل.")

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords = [ln.strip() for ln in f if ln.strip()]

    ensure_csv_header(CSV_PATH)
    ts = datetime.utcnow().isoformat()

    rows = []
    for kw in keywords:
        try:
            pos, url, title = get_rank(kw)
            rows.append([ts, kw, pos, url, title])
            print(f"{kw} -> {pos}")
            time.sleep(1.5)  # تهدئة بسيطة
        except Exception as e:
            rows.append([ts, kw, "ERROR", "", str(e)])

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

if __name__ == "__main__":
    main()

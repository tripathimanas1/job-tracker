import csv
import os
from datetime import datetime

LOG_FILE = "logs/applications.csv"

HEADERS = [
    "Date", "Company", "Role", "URL",
    "Match Score", "Verdict", "Tech Skills",
    "Gaps", "Cover Letter Path"
]


def ensure_log():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()


def save_cover_letter(company: str, role: str, cover_letter: str) -> str:
    os.makedirs("logs/cover_letters", exist_ok=True)
    safe_name = f"{company}_{role}".replace(" ", "_").replace("/", "-")
    path = f"logs/cover_letters/{safe_name}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(cover_letter)
    return path


def log_application(url: str, parsed_jd: dict, score_result: dict, cover_letter_path: str):
    ensure_log()
    row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Company": parsed_jd.get("Company", "Unknown"),
        "Role": parsed_jd.get("Role", "Unknown"),
        "URL": url,
        "Match Score": score_result.get("Score", "N/A"),
        "Verdict": score_result.get("Verdict", "N/A"),
        "Tech Skills": parsed_jd.get("Tech Skills", "N/A"),
        "Gaps": score_result.get("Gaps", "N/A"),
        "Cover Letter Path": cover_letter_path,
    }
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(row)

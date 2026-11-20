import re
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.jra.go.jp/datafile/seiseki/replay/jyusyo.html"
YEAR = 2026

# 日本時間の今日
today = datetime.now(ZoneInfo("Asia/Tokyo")).date()

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; UniversityResearch/1.0)"
}

# JRAのページを取得
response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()
response.encoding = response.apparent_encoding

soup = BeautifulSoup(response.text, "html.parser")

# 2026年の重賞一覧テーブルを探す
target_table = None

for table in soup.find_all("table"):
    text = table.get_text(" ", strip=True)
    if "レース名" in text and "競馬場" in text and "コース" in text:
        target_table = table
        break

if target_table is None:
    raise RuntimeError("重賞一覧テーブルが見つかりませんでした")

races = []

for tr in target_table.find_all("tr"):
    cells = [
        cell.get_text(" ", strip=True)
        for cell in tr.find_all(["th", "td"], recursive=False)
    ]

    if len(cells) < 5:
        continue

    date_text, race_text, venue, condition, course = cells[:5]

    # 日付を抽出（例：10月18日日曜）
    date_match = re.search(r"(\d+)月(\d+)日", date_text)

    if not date_match:
        continue

    month = int(date_match.group(1))
    day = int(date_match.group(2))

    try:
        race_date = datetime(YEAR, month, day).date()
    except ValueError:
        continue

    # 今日より前のレースを除外
    if race_date < today:
        continue

    # グレードを判定
    normalized = race_text.replace("Ⅰ", "I").replace("Ⅱ", "II").replace("Ⅲ", "III")
    normalized = normalized.replace("１", "1").replace("２", "2").replace("３", "3")

    grade_match = re.match(r"^G\s*(III|II|I|3|2|1)", normalized)

    if not grade_match:
        continue

    grade = grade_match.group(1)
    grade = {"I": "G1", "II": "G2", "III": "G3"}.get(
        grade, "G" + grade
    )

    race_name = normalized[grade_match.end():].strip()

    # 距離を抽出
    distance_match = re.search(r"([\d,]+)\s*メートル", course)
    distance = (
        int(distance_match.group(1).replace(",", ""))
        if distance_match else None
    )

    surface = (
        "芝" if "芝" in course
        else "ダート" if "ダ" in course
        else "障害" if "障" in course
        else "不明"
    )

    races.append({
        "開催日": race_date.isoformat(),
        "レース名": race_name,
        "グレード": grade,
        "競馬場": venue,
        "距離(m)": distance,
        "コース": surface,
        "出走条件": condition
    })

df = pd.DataFrame(races)

if df.empty:
    print("今後の重賞レースが見つかりませんでした")
else:
    df = df.drop_duplicates()
    df = df.sort_values(["開催日", "競馬場"])

    print(df.to_string(index=False))

    df.to_csv(
        "data/jra_2026_upcoming_grades.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\n取得件数：{len(df)}件")
    print("CSV保存完了！")
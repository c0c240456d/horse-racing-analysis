import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


def show_upcoming_races():

    # タイトル
    st.title("🏇 開催予定レース")
    st.caption("JRA重賞レースの開催情報をチェックしよう")

    # CSVの読み込み
    CSV_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "jra_2026_upcoming_grades.csv"
    )

    if not CSV_PATH.exists():
        st.error("CSVファイルが見つかりません。")
        return

    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    # 日付の変換
    df["開催日"] = pd.to_datetime(df["開催日"])

    # 終了したレースを除外
    today = datetime.now(ZoneInfo("Asia/Tokyo")).date()
    df = df[df["開催日"].dt.date >= today]

    # 開催日順に並べ替え
    df = df.sort_values("開催日")

    # レース件数
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("開催予定レース", len(df))
    col2.metric("G1", len(df[df["グレード"] == "G1"]))
    col3.metric("G2", len(df[df["グレード"] == "G2"]))
    col4.metric("G3", len(df[df["グレード"] == "G3"]))

    st.divider()

    # 絞り込み機能
    st.subheader("レースを探す")

    col1, col2, col3 = st.columns(3)

    with col1:
        month = st.selectbox(
            "開催月",
            ["すべて"] + sorted(df["開催日"].dt.month.unique().tolist())
        )

    with col2:
        grade = st.selectbox(
            "グレード",
            ["すべて", "G1", "G2", "G3"]
        )

    with col3:
        venue = st.selectbox(
            "競馬場",
            ["すべて"] + sorted(df["競馬場"].unique().tolist())
        )

    # 絞り込み処理
    filtered = df.copy()

    if month != "すべて":
        filtered = filtered[filtered["開催日"].dt.month == month]

    if grade != "すべて":
        filtered = filtered[filtered["グレード"] == grade]

    if venue != "すべて":
        filtered = filtered[filtered["競馬場"] == venue]

    st.divider()

    # レース一覧
    st.subheader("開催予定レース一覧")
    st.caption(f"{len(filtered)}件のレースが見つかりました")

    # グレード別カラー
    colors = {
        "G1": "blue",
        "G2": "red",
        "G3": "green"
    }

    if filtered.empty:
        st.warning("該当するレースがありません。")

    else:
        for index, race in filtered.iterrows():

            with st.container(border=True):

                col1, col2, col3 = st.columns([1, 4, 1])

                with col1:
                    st.markdown(
                        race["開催日"].strftime("%m月%d日")
                    )

                    color = colors.get(race["グレード"], "gray")

                    st.markdown(
                        f":{color}[**{race['グレード']}**]"
                    )

                with col2:
                    st.markdown(f"### {race['レース名']}")

                    st.caption(
                        f"{race['競馬場']}競馬場 ｜ "
                        f"{race['コース']} ｜ "
                        f"{race['距離(m)']}m"
                    )

                with col3:
                    detail = st.button(
                        "詳細を見る",
                        key=f"race_{index}"
                    )

                if detail:
                    st.session_state["selected_race"] = index

                if st.session_state.get("selected_race") == index:
                    st.divider()
                    st.write("開催日：", race["開催日"].strftime("%Y年%m月%d日"))
                    st.write("レース名：", race["レース名"])
                    st.write("グレード：", race["グレード"])
                    st.write("競馬場：", race["競馬場"])
                    st.write("距離：", f"{race['距離(m)']}m")
                    st.write("コース：", race["コース"])
                    st.write("出走条件：", race["出走条件"])
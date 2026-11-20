
import streamlit as st
from yougo import show_glossary


st.set_page_config(
    page_title="競馬データ分析ツール",
    page_icon="🐎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 画面の状態
if "page" not in st.session_state:
    st.session_state.page = "メインダッシュボード"

if "search_type" not in st.session_state:
    st.session_state.search_type = "馬検索"


def change_page(page, search_type=None):
    st.session_state.page = page
    if search_type is not None:
        st.session_state.search_type = search_type


# サイドバー
with st.sidebar:
    st.title("🐎 メニュー")

    st.button(
        "🏠 メインダッシュボード",
        use_container_width=True,
        on_click=change_page,
        args=("メインダッシュボード",)
    )

    with st.expander("🔍 検索", expanded=True):
        for search_type in [
            "馬検索",
            "騎手検索",
            "過去レース検索",
            "条件別検索"
        ]:
            st.button(
                search_type,
                key=f"sidebar_{search_type}",
                use_container_width=True,
                on_click=change_page,
                args=("検索", search_type)
            )

    st.button(
        "📅 開催予定レース",
        use_container_width=True,
        on_click=change_page,
        args=("開催予定レース",)
    )

    st.button(
        "📖 用語集",
        use_container_width=True,
        on_click=change_page,
        args=("用語集",)
    )


# メインダッシュボード
if st.session_state.page == "メインダッシュボード":
    st.title("🐎 競馬データ分析ツール")
    st.write("初心者でも簡単に競馬データを検索・比較できるアプリです。")

    st.divider()
    st.subheader("🔍 検索メニュー")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "🐎 馬から検索",
            use_container_width=True,
            on_click=change_page,
            args=("検索", "馬検索")
        )
        st.caption("馬の過去成績・勝率などを確認")

        st.button(
            "🏆 過去レースから検索",
            use_container_width=True,
            on_click=change_page,
            args=("検索", "過去レース検索")
        )
        st.caption("過去のレース結果を確認")

    with col2:
        st.button(
            "🏇 騎手から検索",
            use_container_width=True,
            on_click=change_page,
            args=("検索", "騎手検索")
        )
        st.caption("騎手の勝率・条件別成績を確認")

        st.button(
            "📊 条件別検索",
            use_container_width=True,
            on_click=change_page,
            args=("検索", "条件別検索")
        )
        st.caption("競馬場・距離・馬場状態などで検索")

    st.divider()
    st.subheader("📚 その他の機能")

    col3, col4 = st.columns(2)

    with col3:
        st.button(
            "📅 開催予定レース",
            key="home_upcoming",
            use_container_width=True,
            on_click=change_page,
            args=("開催予定レース",)
        )

    with col4:
        st.button(
            "📖 用語集",
            key="home_terms",
            use_container_width=True,
            on_click=change_page,
            args=("用語集",)
        )


# 検索画面
elif st.session_state.page == "検索":
    st.title("🔍 検索")

    search_types = [
        "馬検索",
        "騎手検索",
        "過去レース検索",
        "条件別検索"
    ]

    selected = st.selectbox(
        "検索方法",
        search_types,
        index=search_types.index(st.session_state.search_type)
    )

    st.session_state.search_type = selected

    st.subheader(selected)

    if selected == "馬検索":
        st.text_input("馬名を入力")
    elif selected == "騎手検索":
        st.text_input("騎手名を入力")
    elif selected == "過去レース検索":
        st.date_input("開催日")
        st.selectbox(
            "競馬場",
            ["選択してください", "東京", "中山", "京都", "阪神"]
        )
    elif selected == "条件別検索":
        st.selectbox(
            "コース",
            ["芝", "ダート"]
        )
        st.slider("距離（m）", 1000, 3600, 1600, 100)

    st.info("検索・分析機能は担当者が今後実装します。")


# 開催予定レース画面
elif st.session_state.page == "開催予定レース":
    st.title("📅 開催予定レース")
    st.info("開催予定レースの表示機能は現在開発中です。")


# 用語集画面
elif st.session_state.page == "用語集":
    show_glossary()

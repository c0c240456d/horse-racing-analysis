
import streamlit as st


def show_mainmenu():

    # タイトル
    st.title("🏇 競馬データ分析ツール")
    st.write("競馬データを簡単に検索・比較できるアプリケーション")

    st.divider()
    st.subheader("🔍 検索メニュー")

    # 画面切り替え
    def move_to_search(search_type):
        st.session_state.page = "検索"
        st.session_state.search_type = search_type
        st.rerun()

    # 2列に配置
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("🐎 馬検索")
            st.write("馬のプロフィールや過去成績を確認できます。")

            if st.button("馬検索へ", use_container_width=True):
                move_to_search("馬検索")

        with st.container(border=True):
            st.subheader("🏆 過去レース検索")
            st.write("開催日や競馬場から過去のレースを検索できます。")

            if st.button("過去レース検索へ", use_container_width=True):
                move_to_search("過去レース検索")

    with col2:
        with st.container(border=True):
            st.subheader("🏇 騎手検索")
            st.write("騎手の勝率や過去の騎乗成績を確認できます。")

            if st.button("騎手検索へ", use_container_width=True):
                move_to_search("騎手検索")

        with st.container(border=True):
            st.subheader("📊 条件別検索")
            st.write("競馬場・距離・馬場状態などから検索できます。")

            if st.button("条件別検索へ", use_container_width=True):
                move_to_search("条件別検索")

    st.divider()
    st.subheader("📚 その他の機能")

    col3, col4 = st.columns(2)

    with col3:
        if st.button("📅 開催予定レース",
                     use_container_width=True):
            st.session_state.page = "開催予定レース"
            st.rerun()

    with col4:
        if st.button("📖 競馬用語集",
                     use_container_width=True):
            st.session_state.page = "用語集"
            st.rerun()

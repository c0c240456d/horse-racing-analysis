
import streamlit as st


# ==========================================
# デザイン設定
# ==========================================

def apply_menu_style():

    css = """
<style>

/* トップバナー */
.hero {
    background: linear-gradient(115deg, #103b30, #24624c);
    padding: 42px 44px;
    border-radius: 18px;
    margin-bottom: 30px;
    box-shadow: 0 8px 24px rgba(10,55,37,0.12);
}

.hero-label {
    color: #ebcf90;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 14px;
}

.hero-title {
    color: #ffffff;
    font-size: clamp(26px, 3vw, 38px);
    font-weight: 800;
    line-height: 1.4;
    margin-bottom: 14px;
}

.hero-text {
    color: #d9e9e1;
    font-size: 15px;
    line-height: 1.8;
}

/* セクション見出し */
.menu-section {
    font-size: 23px;
    font-weight: 750;
    margin-top: 12px;
    margin-bottom: 5px;
}

.section-description {
    color: #829187;
    font-size: 14px;
    margin-bottom: 18px;
}

/* 検索カード */
.card-label {
    color: #b49a64;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.card-title {
    font-size: 22px;
    font-weight: 750;
    margin-top: 12px;
    margin-bottom: 8px;
}

.card-description {
    color: #89978f;
    font-size: 14px;
    line-height: 1.8;
    min-height: 52px;
}

/* メインメニューのボタンのみ装飾 */
.st-key-btn_horse_card button,
.st-key-btn_jockey_card button,
.st-key-btn_race_card button,
.st-key-btn_condition_card button,
.st-key-btn_upcoming button,
.st-key-btn_glossary button {
    border-radius: 10px;
    border: 1px solid #bad5c5;
    background-color: #edf6ef;
    color: #20543c;
    font-weight: 600;
    min-height: 45px;
    transition: all 0.2s ease;
}

/* ホバー時 */
.st-key-btn_horse_card button:hover,
.st-key-btn_jockey_card button:hover,
.st-key-btn_race_card button:hover,
.st-key-btn_condition_card button:hover,
.st-key-btn_upcoming button:hover,
.st-key-btn_glossary button:hover {
    background-color: #20543c;
    color: #ffffff;
    border-color: #20543c;
    box-shadow: 0 4px 14px rgba(32,84,60,0.18);
}

/* フッター */
.menu-footer {
    text-align: center;
    color: #93a096;
    font-size: 12px;
    padding-top: 30px;
    padding-bottom: 10px;
}

</style>
"""

    st.markdown(css, unsafe_allow_html=True)


# ==========================================
# ページ移動処理
# ==========================================

def move_page(page, search_type=None):

    st.session_state.page = page

    if search_type is not None:
        st.session_state.search_type = search_type

    st.rerun()


# ==========================================
# 検索カード
# ==========================================

def search_card(icon, english, title, description,
                button_label, search_type, card_key):

    with st.container(border=True):

        st.markdown(
            f'<div class="card-label">{english}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="card-title">{icon} {title}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="card-description">{description}</div>',
            unsafe_allow_html=True
        )

        if st.button(
            button_label,
            key=f"btn_{card_key}",
            use_container_width=True
        ):
            move_page("検索", search_type)


# ==========================================
# メインメニュー
# ==========================================

def show_mainmenu():

    apply_menu_style()

    # --------------------------------------
    # トップバナー（HTML表示問題を修正）
    # --------------------------------------

    # HTMLを1行の文字列として構築することで
    # Markdownのインデント解釈を回避する

    hero_html = (
        '<div class="hero">'
        '<div class="hero-label">'
        'HORSE RACING ANALYTICS'
        '</div>'
        '<div class="hero-title">'
        '🏇 競馬データ分析ツール'
        '</div>'
        '<div class="hero-text">'
        '競馬をもっと分かりやすく、もっと深く。<br>'
        '馬・騎手・レースの情報を検索し、'
        'データから競馬を分析しよう。'
        '</div>'
        '</div>'
    )

    st.markdown(hero_html, unsafe_allow_html=True)

    # --------------------------------------
    # 検索メニュー
    # --------------------------------------

    st.markdown(
        '<div class="menu-section">🔍 データを探す</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        '調べたい情報に合わせて検索方法を選択してください。'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------
    # 1段目：馬検索・騎手検索
    # --------------------------------------

    col1, col2 = st.columns(2, gap="large")

    with col1:
        search_card(
            "🐎",
            "HORSE SEARCH",
            "馬検索",
            "馬のプロフィールや過去のレース成績、勝率などを確認できます。",
            "馬を検索する →",
            "馬検索",
            "horse_card"
        )

    with col2:
        search_card(
            "🏇",
            "JOCKEY SEARCH",
            "騎手検索",
            "騎手の勝率や騎乗成績などを確認し、比較できます。",
            "騎手を検索する →",
            "騎手検索",
            "jockey_card"
        )

    # --------------------------------------
    # 2段目：過去レース・条件別検索
    # --------------------------------------

    col3, col4 = st.columns(2, gap="large")

    with col3:
        search_card(
            "🏆",
            "RACE HISTORY",
            "過去レース検索",
            "開催日や競馬場から、過去のレース結果を調べられます。",
            "レースを検索する →",
            "過去レース検索",
            "race_card"
        )

    with col4:
        search_card(
            "📊",
            "ADVANCED SEARCH",
            "条件別検索",
            "距離・競馬場・馬場状態などの条件を指定して検索できます。",
            "条件を指定して検索 →",
            "条件別検索",
            "condition_card"
        )

    # --------------------------------------
    # その他の機能
    # --------------------------------------

    st.write("")
    st.divider()

    st.markdown(
        '<div class="menu-section">📚 その他の機能</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'レース情報や初心者向けコンテンツも利用できます。'
        '</div>',
        unsafe_allow_html=True
    )

    col5, col6 = st.columns(2, gap="large")

    with col5:
        with st.container(border=True):

            st.markdown("### 📅 開催予定レース")
            st.caption("これから開催されるレースの情報を確認")

            if st.button(
                "開催予定を見る →",
                key="btn_upcoming",
                use_container_width=True
            ):
                move_page("開催予定レース")

    with col6:
        with st.container(border=True):

            st.markdown("### 📖 競馬用語集")
            st.caption("初心者向けに競馬の基本用語を解説")

            if st.button(
                "用語集を見る →",
                key="btn_glossary",
                use_container_width=True
            ):
                move_page("用語集")

    # --------------------------------------
    # フッター
    # --------------------------------------

    footer_html = (
        '<div class="menu-footer">'
        'HORSE RACING ANALYTICS'
        '<br>'
        'Horse Racing Data Analysis Tool'
        '</div>'
    )

    st.markdown(footer_html, unsafe_allow_html=True)

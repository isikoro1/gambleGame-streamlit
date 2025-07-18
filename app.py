# app.py
import streamlit as st
import random

st.set_page_config(page_title="Gamble Game", page_icon="🎰")

st.title("🎰 Gamble Game")
st.write("コインの表と裏で賭けをします。**表**なら勝ち、**裏**なら負けです。")

# 初期化（セッション変数）
if "G" not in st.session_state:
    st.session_state.G = 1000
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.message = ""

# 結果の表示
st.metric(label="所持金 💰", value=f"{st.session_state.G} 円")
st.write(f"✅ 勝ち：{st.session_state.win} 回")
st.write(f"❌ 負け：{st.session_state.lose} 回")

# 掛け金の入力
bet = st.number_input("掛け金を入力してください（円）", min_value=1, max_value=st.session_state.G, step=1)

# ギャンブルボタン
if st.button("ギャンブル開始！"):
    if bet > st.session_state.G:
        st.warning("所持金以上は賭けられません！")
    else:
        coin = random.randint(0, 1)  # 0 = lose, 1 = win
        if coin == 0:
            st.session_state.G -= bet
            st.session_state.lose += 1
            st.session_state.message = f"😢 裏です。負けました... -{bet} 円"
        else:
            st.session_state.G += bet
            st.session_state.win += 1
            st.session_state.message = f"🎉 表です！勝ちました！ +{bet} 円"

# メッセージ表示
if st.session_state.message:
    st.subheader(st.session_state.message)

# 所持金ゼロで終了
if st.session_state.G <= 0:
    st.error("💸 所持金がなくなりました！ゲームオーバーです。")
    if st.button("リセットしてもう一度遊ぶ"):
        st.session_state.G = 1000
        st.session_state.win = 0
        st.session_state.lose = 0
        st.session_state.message = ""


import streamlit as st
import random
import time

st.set_page_config(page_title="Gamble Game", page_icon="🎰")
st.title("🎰 スロット風 Gamble Game")

# セッション変数の初期化
if "G" not in st.session_state:
    st.session_state.G = 1000
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.message = ""
    st.session_state.slot_result = ["❓", "❓", "❓"]
    st.session_state.bet = 0

# スロット絵柄
symbols = ["🤡", "🍉", "🍒", "7️⃣", "💎"]

# 💰 所持金・勝敗
st.metric(label="所持金", value=f"{st.session_state.G:,} G")
st.write(f"✅ 勝ち：{st.session_state.win} 回")
st.write(f"❌ 負け：{st.session_state.lose} 回")

# 🎯 掛け金の操作ボタン
st.write(f"🎯 掛け金: {st.session_state.bet} G")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
bet_options = [1, 5, 10, 100, 1000, 10000]

for i, col in enumerate([col1, col2, col3, col4, col5, col6]):
    amount = bet_options[i]
    if st.session_state.G >= st.session_state.bet + amount:
        if col.button(f"+{amount}G"):
            st.session_state.bet += amount

with col7:
    if st.button("リセット"):
        st.session_state.bet = 0

# 🎰 表示用スロット
slot_box = st.empty()
with slot_box.container():
    st.markdown(
        f"<h1 style='text-align:center; font-size: 5rem'>{' '.join(st.session_state.slot_result)}</h1>",
        unsafe_allow_html=True
    )

# 🎰 スロット開始ボタン
if st.button("スロットを回す！"):
    if st.session_state.bet <= 0:
        st.warning("掛け金を設定してください！")
    elif st.session_state.bet > st.session_state.G:
        st.warning("所持金が足りません！")
    else:
        # スロット演出
        for _ in range(20):
            reels = [random.choice(symbols) for _ in range(3)]
            with slot_box.container():
                st.markdown(
                    f"<h1 style='text-align:center; font-size: 5rem'>{' '.join(reels)}</h1>",
                    unsafe_allow_html=True
                )
            time.sleep(0.1)

        # 勝敗を50%の確率で決定
        is_win = random.randint(0, 1) == 1
        if is_win:
            chosen = random.choice(symbols)
            reels = [chosen] * 3
            st.session_state.G += st.session_state.bet
            st.session_state.win += 1
            st.session_state.message = f"🎉 あたり！ +{st.session_state.bet:,} G"
        else:
            reels = random.sample(symbols, 3)
            st.session_state.G -= st.session_state.bet
            st.session_state.lose += 1
            st.session_state.message = f"😢 はずれ！ -{st.session_state.bet:,} G"

        st.session_state.slot_result = reels
        st.session_state.bet = 0
        st.rerun()

# 🔊 結果メッセージ
if st.session_state.message:
    st.subheader(st.session_state.message)

# 💸 所持金ゼロで終了
if st.session_state.G <= 0:
    st.error("所持金がなくなりました！ゲームオーバーです。")
    if st.button("リセットしてもう一度遊ぶ"):
        st.session_state.G = 1000
        st.session_state.win = 0
        st.session_state.lose = 0
        st.session_state.message = ""
        st.session_state.slot_result = ["❓", "❓", "❓"]
        st.session_state.bet = 0

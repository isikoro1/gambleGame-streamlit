# app.py
import streamlit as st
import random
import time

st.set_page_config(page_title="Gamble Game", page_icon="🎰")

st.title("🎰 スロット風 Gamble Game")
st.write("スロットを回して、絵柄が3つ揃えば当たりです。（実際の勝敗は2分の1）")

# 初期化（セッション変数）
if "G" not in st.session_state:
    st.session_state.G = 1000
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.message = ""
    st.session_state.slot_result = ["❓", "❓", "❓"]

# 結果の表示
st.metric(label="所持金 💰", value=f"{st.session_state.G} $")
st.write(f"✅ 勝ち：{st.session_state.win} 回")
st.write(f"❌ 負け：{st.session_state.lose} 回")

# 掛け金の入力
bet = st.number_input("掛け金を入力してください（$）", min_value=1, max_value=st.session_state.G, step=1)

# 絵文字のスロット絵柄候補
symbols = ["🤡", "🍉", "🍒", "7️⃣", "💎"]

# 表示用スロット
slot_box = st.empty()

# スロットの状態表示（常に見える）
with slot_box.container():
    st.markdown(
        f"<h1 style='text-align:center'>{' '.join(st.session_state.slot_result)}</h1>",
        unsafe_allow_html=True
    )

if st.button("スロットを回す！"):
    if bet > st.session_state.G:
        st.warning("所持金以上は賭けられません！")
    else:
        # アニメーション演出
        for _ in range(20):
            reels = [random.choice(symbols) for _ in range(3)]
            with slot_box.container():
                st.markdown(
                    f"<h1 style='text-align:center'>{' '.join(reels)}</h1>",
                    unsafe_allow_html=True
                )
            time.sleep(0.1)

         # 実際の勝敗を2分の1で判定
        is_win = random.randint(0, 1) == 1

        if is_win:
            # 当たり：同じ絵柄3つにする（演出）
            chosen = random.choice(symbols)
            reels = [chosen] * 3
            st.session_state.G += bet
            st.session_state.win += 1
            st.session_state.message = f"🎉 あたり！ +{bet} 円"
        else:
            # はずれ：3つ違う絵柄（演出）
            reels = random.sample(symbols, 3)
            st.session_state.G -= bet
            st.session_state.lose += 1
            st.session_state.message = f"😢 はずれ！ -{bet} 円"

        # 表示を更新してリザルトを保存
        st.session_state.slot_result = reels
        st.rerun()

# 結果メッセージ
if st.session_state.message:
    st.subheader(st.session_state.message)

# ゲームオーバー時のリセット
if st.session_state.G <= 0:
    st.error("💸 所持金がなくなりました！ゲームオーバーです。")
    if st.button("リセットしてもう一度遊ぶ"):
        st.session_state.G = 1000
        st.session_state.win = 0
        st.session_state.lose = 0
        st.session_state.message = ""
        st.session_state.slot_result = ["❓", "❓", "❓"]


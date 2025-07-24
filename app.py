import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 🎵 効果音再生関数
def play_sound(file_path: str, volume: float = 1.0):
    components.html(f"""
        <audio autoplay>
            <source src="{file_path}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <script>
            const audio = document.querySelector("audio");
            if (audio) {{
                audio.volume = {volume};
            }}
        </script>
    """, height=0)


st.set_page_config(page_title="Gamble Game", page_icon="🎰")

# 🎚️ 音量調整スライダーの初期化
if "volume" not in st.session_state:
    st.session_state.volume = 1.0

# サイドバーにスライダー表示
st.sidebar.markdown("🎚️ **音量調整**")
st.session_state.volume = st.sidebar.slider("音量", 0.0, 1.0, st.session_state.volume, step=0.05)

st.title("🎰 スロット風 Gamble Game")

st.write(f"あたり確率は５０％")

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

# 🎯 掛け金の表示
st.write(f"🎯 掛け金: {st.session_state.bet} G")

# 掛け金入力ボタン行
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
bet_options = [1, 5, 10, 100, 1000, 10000]

# 金額追加ボタン
for i, col in enumerate([col1, col2, col3, col4, col5, col6]):
    amount = bet_options[i]
    if st.session_state.G >= st.session_state.bet + amount:
        if col.button(f"+{amount}G"):
            st.session_state.bet += amount
            play_sound("sounds/coin_insert.mp3", st.session_state.volume)
            st.rerun()  # ← 即時反映

# 倍プッシュボタン
last_bet = st.session_state.get("last_bet", 0)
double_bet = last_bet * 2
if last_bet > 0 and st.session_state.G >= st.session_state.bet + double_bet:
    with col7:
        if st.button(f"倍プッシュ +{double_bet}G"):
            st.session_state.bet += double_bet
            st.rerun()  # ← 即時反映

# リセットボタン
with col8:
    if st.button("リセット"):
        st.session_state.bet = 0
        st.rerun()  # ← 即時UIリセット

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
        # 🎵 スロットレバー効果音（ガシャコン）
        play_sound("sounds/lever_pull.mp3", st.session_state.volume)

        # 🎵 リール回転開始音（ルルル…）
        play_sound("sounds/reel_spin.mp3", st.session_state.volume)

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
            play_sound("sounds/jackpot.mp3", st.session_state.volume)
            st.session_state.last_bet = st.session_state.bet
        else:
            reels = random.sample(symbols, 3)
            st.session_state.G -= st.session_state.bet
            st.session_state.lose += 1
            st.session_state.message = f"😢 はずれ！ -{st.session_state.bet:,} G"
            st.session_state.last_bet = st.session_state.bet


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

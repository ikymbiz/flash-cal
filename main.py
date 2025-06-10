import streamlit as st
import random
import time
import operator

# ページ設定
st.set_page_config(page_title="フラッシュあんざん", layout="centered", initial_sidebar_state="collapsed")

# 四則演算関数
ops = {
    "+": operator.add,
    "-": operator.sub,
    "×": operator.mul,
    "÷": operator.truediv,
}


# 入力正規化
def normalize_input(s):
    return s.translate(str.maketrans("０１２３４５６７８９．", "0123456789."))


# スタイル
st.markdown("""
<style>
.problem-display {
    background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
    color: black;
    padding: 60px 40px;
    margin: 30px 0;
    border-radius: 20px;
    text-align: center;
    font-size: 96px;
    font-weight: bold;
    font-family: 'Arial', sans-serif;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# セッション初期化
for key, val in {
    "problems": [],
    "operator": "",
    "started": False,
    "start_time": 0.0,
    "correct_count": 0,
    "total_count": 0,
    "current_problem_index": 0,
    "showing_problem": False,
    "digit_input": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# 設定
with st.sidebar:
    st.header("⚙️ 設定")
    st.session_state.num_terms = st.number_input("項数", min_value=2, max_value=10, value=2)
    st.session_state.min_digits = st.selectbox("最小桁数", [1, 2, 3], index=0)
    st.session_state.max_digits = st.selectbox("最大桁数", [1, 2, 3], index=0)
    st.session_state.operator_choice = st.selectbox("演算子", ["+", "-", "×", "÷"])
    st.session_state.display_speed = st.slider("表示速度（秒）", 0.05, 2.0, 0.8, 0.05)

# タイトルとスタート
st.title("🧮 フラッシュあんざん")
if st.button("▶ スタート", use_container_width=True):
    digits = []
    for _ in range(st.session_state.num_terms):
        d = random.randint(st.session_state.min_digits, st.session_state.max_digits)
        digits.append(random.randint(10 ** (d - 1), 10 ** d - 1))

    if st.session_state.operator_choice == "÷":
        result = digits[0]
        for i in range(1, len(digits)):
            d = random.randint(st.session_state.min_digits, st.session_state.max_digits)
            divisor = random.randint(10 ** (d - 1), 10 ** d - 1)
            result *= divisor
            digits[i] = divisor
        digits[0] = result

    st.session_state.problems = digits
    st.session_state.operator = st.session_state.operator_choice
    st.session_state.started = True
    st.session_state.current_problem_index = 0
    st.session_state.showing_problem = True
    st.session_state.digit_input = ""
    st.rerun()

# ─── 数字ボタンを大きくするCSS ───
st.markdown("""
<style>
/* 全てのボタンを大きくする汎用的なアプローチ */
.stButton > button {
    height: 40px !important;
    font-size: 60px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    margin: 2px !important;
}

/* 数字パッド専用のスタイル */
.big-number-button {
    display: inline-block;
    width: 100%;
    margin: 2px;
}

.big-number-button button {
    width: 100% !important;
    height: 100px !important;
    font-size: 50px !important;
    font-weight: bold !important;
    border-radius: 15px !important;
    background-color: #4CAF50 !important;
    color: white !important;
    border: none !important;
    margin: 0 !important;
}

.big-number-button button:hover {
    background-color: #45a049 !important;
    transform: scale(1.02) !important;
}
</style>
""", unsafe_allow_html=True)

# 出題フェーズ（演算子も表示）
if st.session_state.started and st.session_state.showing_problem:
    max_index = len(st.session_state.problems) * 2 - 1
    idx = st.session_state.current_problem_index
    if idx < max_index:
        if idx % 2 == 0:
            # 数字表示
            display = str(st.session_state.problems[idx // 2])
        else:
            # 演算子表示
            display = st.session_state.operator

        st.markdown(f"<div class='problem-display'>{display}</div>", unsafe_allow_html=True)
        time.sleep(st.session_state.display_speed)
        st.session_state.current_problem_index += 1
        st.rerun()
    else:
        st.session_state.showing_problem = False
        st.session_state.started = False
        st.session_state.start_time = time.time()
        st.rerun()

# 入力フェーズ（大きな数字ボタン）
if not st.session_state.started and st.session_state.problems and not st.session_state.showing_problem:
    st.markdown("<div class='problem-display'>こたえは？</div>", unsafe_allow_html=True)
    st.subheader(f"🔢 にゅうりょく: `{st.session_state.digit_input or '　'}`")

    # 数字のグリッド（3x4 + 操作ボタン）

    # 1行目: 1, 2, 3
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("1", key="btn1", use_container_width=True):
            st.session_state.digit_input += "1"
            st.rerun()
    with col2:
        if st.button("2", key="btn2", use_container_width=True):
            st.session_state.digit_input += "2"
            st.rerun()
    with col3:
        if st.button("3", key="btn3", use_container_width=True):
            st.session_state.digit_input += "3"
            st.rerun()

    # 2行目: 4, 5, 6
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("4", key="btn4", use_container_width=True):
            st.session_state.digit_input += "4"
            st.rerun()
    with col5:
        if st.button("5", key="btn5", use_container_width=True):
            st.session_state.digit_input += "5"
            st.rerun()
    with col6:
        if st.button("6", key="btn6", use_container_width=True):
            st.session_state.digit_input += "6"
            st.rerun()

    # 3行目: 7, 8, 9
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("7", key="btn7", use_container_width=True):
            st.session_state.digit_input += "7"
            st.rerun()
    with col8:
        if st.button("8", key="btn8", use_container_width=True):
            st.session_state.digit_input += "8"
            st.rerun()
    with col9:
        if st.button("9", key="btn9", use_container_width=True):
            st.session_state.digit_input += "9"
            st.rerun()

    # 4行目: 0, ., 操作
    col0, colback,colbtnsubmit = st.columns(3)
    with col0:
        if st.button("0", key="btn0", use_container_width=True):
            st.session_state.digit_input += "0"
            st.rerun()
    with colback:
        if st.button("⌫", key="btnback", use_container_width=True):
            st.session_state.digit_input = st.session_state.digit_input[:-1]
            st.rerun()
    with colbtnsubmit:
        if st.button("こたえあわせ", key="btnsubmit", use_container_width=True):
            st.session_state.answer_final = normalize_input(st.session_state.digit_input)
            st.rerun()

# 判定フェーズ
if "answer_final" in st.session_state:
    answer = st.session_state.answer_final
    try:
        user_answer = float(answer)
        result = st.session_state.problems[0]
        for n in st.session_state.problems[1:]:
            try:
                result = ops[st.session_state.operator](result, n)
            except ZeroDivisionError:
                result = float("inf")
                break
        elapsed = round(time.time() - st.session_state.start_time, 2)
        st.session_state.total_count += 1
        correct = abs(user_answer - result) < 0.01
        if correct:
            st.session_state.correct_count += 1
            st.success(f"✅ せいかい！（{elapsed} びょう）")

        else:
            st.error(f"❌ まちがい！せいかい：{round(result, 2)}（{elapsed} びょう）")


        expr = f" {st.session_state.operator} ".join(map(str, st.session_state.problems))
        st.info(f"🧮 もんだい： {expr} = {round(result, 2)}")

    except ValueError:
        st.error("⚠️ 数字を正しく入力してください。")

    # 後片付け
    st.session_state.problems = []
    st.session_state.digit_input = ""
    del st.session_state["answer_final"]

    with st.sidebar:
        # total_count が 0 より大きい＝最低１回は回答済み
        if st.session_state.get("total_count", 0) > 0:
            acc = round(100 * st.session_state.correct_count / st.session_state.total_count, 1)
            st.metric(
                "最新の正解率",
                f"{acc}%",
                f"{st.session_state.correct_count}/{st.session_state.total_count}"
            )

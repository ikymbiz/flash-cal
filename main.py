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
} .items():
    if key not in st.session_state:
        st.session_state[key] = val

# 設定
with st.sidebar:
    st.header("⚙️ 設定")
    st.session_state.num_terms = st.number_input("項数", min_value=2, max_value=10, value=2)
    st.session_state.min_digits = st.selectbox("最小桁数", [1, 2, 3], index=0)
    st.session_state.max_digits = st.selectbox("最大桁数", [1, 2, 3], index=0)
    st.session_state.operator_choice = st.selectbox("演算子", ["+", "-", "×", "÷"])
    st.session_state.display_speed = st.slider("表示速度（秒）", 0.1, 2.0, 1.0, 0.1)

    if st.session_state.total_count > 0:
        acc = round(100 * st.session_state.correct_count / st.session_state.total_count, 1)
        st.metric("正解率", f"{acc}%", f"{st.session_state.correct_count}/{st.session_state.total_count}")

# タイトルとスタート
st.title("🧮 フラッシュあんざん")
if st.button("▶ スタート", use_container_width=True):
    digits = []
    for _ in range(st.session_state.num_terms):
        d = random.randint(st.session_state.min_digits, st.session_state.max_digits)
        digits.append(random.randint(10**(d-1), 10**d - 1))

    if st.session_state.operator_choice == "÷":
        result = digits[0]
        for i in range(1, len(digits)):
            d = random.randint(st.session_state.min_digits, st.session_state.max_digits)
            divisor = random.randint(10**(d-1), 10**d - 1)
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

# 表示フェーズ
if st.session_state.started and st.session_state.showing_problem:
    if st.session_state.current_problem_index < len(st.session_state.problems):
        num = st.session_state.problems[st.session_state.current_problem_index]
        st.markdown(f"<div class='problem-display'>{num}</div>", unsafe_allow_html=True)
        time.sleep(st.session_state.display_speed)
        st.session_state.current_problem_index += 1
        st.rerun()
    else:
        st.session_state.showing_problem = False
        st.session_state.started = False
        st.session_state.start_time = time.time()
        st.rerun()

# 入力フェーズ
if not st.session_state.started and st.session_state.problems and not st.session_state.showing_problem:
    st.markdown("<div class='problem-display'>こたえは？</div>", unsafe_allow_html=True)

    # 入力中の数値をリアルタイム表示
    st.subheader(f"🔢 入力中: `{st.session_state.digit_input or '　'}`")

    # 数字と . ボタン（横一列）
    num_row = st.columns(11)
    for i, label in enumerate(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]):
        if num_row[i].button(label):
            if label == "." and "." in st.session_state.digit_input:
                continue
            st.session_state.digit_input += label
            st.rerun()

    # 操作ボタン（⌫・C・こたえあわせ）
    op_cols = st.columns([1, 1, 2])
    if op_cols[0].button("⌫"):
        st.session_state.digit_input = st.session_state.digit_input[:-1]
        st.rerun()
    if op_cols[1].button("C"):
        st.session_state.digit_input = ""
        st.rerun()
    if op_cols[2].button("こたえあわせ"):
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
            st.error(f"❌ まちがい！せいかい：{round(result,2)}（{elapsed} びょう）")

        expr = f" {st.session_state.operator} ".join(map(str, st.session_state.problems))
        st.info(f"🧮 もんだい： {expr} = {round(result, 2)}")

    except ValueError:
        st.error("⚠️ 数字を正しく入力してください。")

    # 後片付け
    st.session_state.problems = []
    st.session_state.digit_input = ""
    del st.session_state["answer_final"]

import streamlit as st
import random

# --- 1. 初始化游戏数据（只在第一次运行网页时执行） ---
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 50)
    st.session_state.min_num = 1
    st.session_state.max_num = 50
    st.session_state.game_over = False
    st.session_state.logs = ["游戏开始！炸弹已埋好。"]

# --- 2. 网页界面设计 ---
st.title("🚀 Python 数字炸弹：网页对战版")
st.write(f"### 当前安全范围：`{st.session_state.min_num}` — `{st.session_state.max_num}`")

# --- 3. 玩家输入区域 ---
if not st.session_state.game_over:
    guess = st.number_input("输入你的猜测：", 
                            min_value=1, max_value=50, step=1)
    
    if st.button("提交猜测"):
        # 逻辑判定
        if guess < st.session_state.min_num or guess > st.session_state.max_num:
            st.warning(f"别乱猜！请输入 {st.session_state.min_num} 到 {st.session_state.max_num} 之间的数")
        elif guess == st.session_state.target:
            st.error(f"💥 砰！炸弹爆炸了！数字就是 {guess}")
            st.session_state.game_over = True
        else:
            # 更新范围
            if guess > st.session_state.target:
                st.session_state.max_num = guess - 1
                st.session_state.logs.append(f"玩家猜了 {guess}，太大了！")
            else:
                st.session_state.min_num = guess + 1
                st.session_state.logs.append(f"玩家猜了 {guess}，太小了！")
            
            # --- 模拟电脑回合 ---
            if not st.session_state.game_over:
                com_guess = random.randint(st.session_state.min_num, st.session_state.max_num)
                if com_guess == st.session_state.target:
                    st.error(f"🤖 电脑猜了 {com_guess}，炸弹炸了！电脑输了！")
                    st.session_state.game_over = True
                else:
                    if com_guess > st.session_state.target:
                        st.session_state.max_num = com_guess - 1
                        st.session_state.logs.append(f"电脑猜了 {com_guess}，太大了！")
                    else:
                        st.session_state.min_num = com_guess + 1
                        st.session_state.logs.append(f"电脑猜了 {com_guess}，太小了！")
            
            # 强制刷新页面显示新范围
            st.rerun()

# --- 4. 游戏日志和重置 ---
st.write("---")
for log in reversed(st.session_state.logs):
    st.text(log)

if st.session_state.game_over:
    if st.button("重新开始游戏"):
        st.session_state.clear()
        st.rerun()
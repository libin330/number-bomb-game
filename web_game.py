import streamlit as st
from streamlit_server_state import server_state, server_state_lock
import random

# --- 1. 初始化公共游戏状态 (所有人共享) ---
with server_state_lock["game_state"]: # 加锁防止多人同时改数据导致冲突
    if "target" not in server_state:
        server_state.target = random.randint(1, 50)
        server_state.min_num = 1
        server_state.max_num = 50
        server_state.game_over = False
        server_state.logs = ["联机对战开始！"]
        server_state.current_turn = "玩家1" # 增加回合控制

st.title("🌐 数字炸弹：异地实时联机版")

# --- 2. 显示当前状态 ---
st.write(f"### 当前安全范围：`{server_state.min_num}` — `{server_state.max_num}`")
st.info(f"📢 当前轮到：**{server_state.current_turn}**")

# --- 3. 玩家对战逻辑 ---
if not server_state.game_over:
    # 玩家需要先“认领”身份
    player_identity = st.radio("请选择你的身份：", ["玩家1", "玩家2"])
    
    guess = st.number_input("输入你的猜测：", 
                            min_value=1, max_value=50, step=1)
    
    if st.button("提交猜测"):
        # 检查是否轮到该玩家
        if player_identity != server_state.current_turn:
            st.warning(f"还没轮到你呢，请等待 {server_state.current_turn} 行动！")
        else:
            with server_state_lock["game_state"]:
                if guess < server_state.min_num or guess > server_state.max_num:
                    st.warning(f"输入无效！必须在 {server_state.min_num} 到 {server_state.max_num} 之间")
                elif guess == server_state.target:
                    server_state.game_over = True
                    server_state.logs.append(f"💥 {player_identity} 踩到了炸弹 ({guess})！游戏结束。")
                else:
                    # 更新范围
                    if guess > server_state.target:
                        server_state.max_num = guess - 1
                    else:
                        server_state.min_num = guess + 1
                    
                    server_state.logs.append(f"🚩 {player_identity} 猜了 {guess}，安全！")
                    # 切换回合
                    server_state.current_turn = "玩家2" if player_identity == "玩家1" else "玩家1"
            st.rerun()

# --- 4. 实时日志展示 ---
st.write("---")
for log in reversed(server_state.logs):
    st.text(log)

# --- 5. 管理员功能：重置游戏 ---
if st.sidebar.button("强制重置游戏"):
    with server_state_lock["game_state"]:
        server_state.target = random.randint(1, 50)
        server_state.min_num = 1
        server_state.max_num = 50
        server_state.game_over = False
        server_state.logs = ["管理员重置了游戏，新一轮开始！"]
        server_state.current_turn = "玩家1"
    st.rerun()
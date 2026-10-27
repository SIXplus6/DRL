import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime

st.set_page_config(
    page_title="ROBOAI | Intelligence Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: #080d19;
    color: #e5edf8;
}
[data-testid="stSidebar"] {
    background: #0e1627;
    border-right: 1px solid #243149;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #e5edf8 !important;
}
p, label {
    color: #aab8ce;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #141f33, #101827);
    border: 1px solid #293952;
    padding: 20px;
    border-radius: 15px;
}
[data-testid="stMetricValue"] {
    color: #38bdf8;
}
div.stButton > button {
    background: #0284c7;
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
}
div.stButton > button:hover {
    background: #0369a1;
    color: white;
}
.card {
    background: #111b2d;
    border: 1px solid #263750;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}
.small {
    color: #91a4bd;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("# 🤖 ROBOAI")
st.sidebar.caption("INTELLIGENT ROBOTICS PLATFORM")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Sensor Analytics",
        "Robot Control",
        "DRL Training",
        "System Information"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### ⚙️ Configuration")

robot_speed = st.sidebar.slider("Motor Speed (%)", 0, 100, 50)
safe_distance = st.sidebar.slider("Safety Distance (cm)", 10, 100, 25)

st.sidebar.caption("Simulation Mode • No physical robot connected")

# ---------- SENSOR SIMULATION ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "robot_running" not in st.session_state:
    st.session_state.robot_running = False

if "episode" not in st.session_state:
    st.session_state.episode = 0

if "rewards" not in st.session_state:
    st.session_state.rewards = []

temperature = round(random.uniform(28, 42), 1)
battery = random.randint(35, 100)
distance = random.randint(10, 150)

if distance < safe_distance:
    robot_status = "OBSTACLE DETECTED"
    suggested_action = "TURN LEFT"
elif not st.session_state.robot_running:
    robot_status = "STANDBY"
    suggested_action = "WAIT"
else:
    robot_status = "NAVIGATING"
    suggested_action = "MOVE FORWARD"

st.session_state.history.append({
    "Time": datetime.now().strftime("%H:%M:%S"),
    "Temperature": temperature,
    "Battery": battery,
    "Distance": distance
})
st.session_state.history = st.session_state.history[-30:]

# ---------- HEADER ----------
st.markdown(
    "<div class='small'>ROBOTICS / INTELLIGENCE CENTER / "
    + page.upper() + "</div>",
    unsafe_allow_html=True
)
st.title("Robot Intelligence Center")
st.caption("AI-powered sensor monitoring and navigation research dashboard")

c1, c2 = st.columns([5, 1])
with c2:
    if st.button("↻ Refresh Data", use_container_width=True):
        st.rerun()

# ---------- OVERVIEW ----------
if page == "Overview":

    st.markdown("### System Overview")

    a, b, c, d = st.columns(4)
    a.metric("🌡️ Temperature", f"{temperature} °C")
    b.metric("🔋 Battery", f"{battery}%")
    c.metric("📡 Distance", f"{distance} cm")
    d.metric("⚙️ Motor Speed", f"{robot_speed}%")

    st.markdown("### Live Monitoring")

    left, right = st.columns([2, 1])

    with left:
        df = pd.DataFrame(st.session_state.history)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(df))),
            y=df["Temperature"],
            name="Temperature °C",
            mode="lines+markers"
        ))
        fig.add_trace(go.Scatter(
            x=list(range(len(df))),
            y=df["Distance"],
            name="Distance cm",
            mode="lines+markers"
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111b2d",
            plot_bgcolor="#111b2d",
            height=350,
            margin=dict(l=20, r=20, t=35, b=20),
            legend=dict(orientation="h")
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### 🤖 Robot Status")
        st.markdown(
            f"<div class='card'><h3>{robot_status}</h3>"
            f"<p class='small'>Suggested action</p>"
            f"<h2>{suggested_action}</h2></div>",
            unsafe_allow_html=True
        )

        if battery < 40:
            st.warning("Battery is getting low.")
        elif distance < safe_distance:
            st.warning("Obstacle detected in simulation.")
        else:
            st.success("No immediate safety alert.")

        st.markdown("#### System Health")
        st.progress(battery / 100, text="Battery level")
        st.progress(max(0, min(1, temperature / 60)),
                    text="Temperature indicator")

    st.markdown("### Recent Sensor Readings")
    st.dataframe(
        pd.DataFrame(st.session_state.history).tail(8),
        use_container_width=True,
        hide_index=True
    )

# ---------- SENSOR ANALYTICS ----------
elif page == "Sensor Analytics":

    st.header("📊 Sensor Analytics")
    df = pd.DataFrame(st.session_state.history)

    sensor = st.selectbox(
        "Select sensor",
        ["Temperature", "Battery", "Distance"]
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df[sensor],
        mode="lines+markers",
        fill="tozeroy",
        name=sensor
    ))
    fig.update_layout(
        template="plotly_dark",
        title=f"{sensor} History",
        paper_bgcolor="#111b2d",
        plot_bgcolor="#111b2d",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download Sensor Data CSV",
        df.to_csv(index=False),
        file_name="roboai_sensor_data.csv",
        mime="text/csv"
    )

# ---------- ROBOT CONTROL ----------
elif page == "Robot Control":

    st.header("🎮 Robot Control Panel")
    st.info("Virtual simulation only. No real robot is connected.")

    st.metric("Configured Speed", f"{robot_speed}%")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Start Simulation", use_container_width=True):
            st.session_state.robot_running = True
            st.success("Simulation started.")
    with col2:
        if st.button("⏹ Stop Simulation", use_container_width=True):
            st.session_state.robot_running = False
            st.warning("Simulation stopped.")

    st.markdown("### Navigation Status")
    st.write("Running" if st.session_state.robot_running else "Stopped")
    st.write("Suggested action:", suggested_action)
    st.write("Obstacle distance:", f"{distance} cm")

# ---------- DRL TRAINING ----------
elif page == "DRL Training":

    st.header("🧠 Deep Reinforcement Learning")
    st.write(
        "This section will be used to train and evaluate "
        "a reinforcement learning agent."
    )

    st.warning(
        "The current dashboard does not yet contain a trained DRL agent. "
        "The metrics below are placeholders until training is implemented."
    )

    st.metric("Training Episodes", st.session_state.episode)
    st.metric("Saved Reward Records", len(st.session_state.rewards))

    if st.button("Reset Training Display"):
        st.session_state.episode = 0
        st.session_state.rewards = []
        st.rerun()

    if st.session_state.rewards:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=st.session_state.rewards,
            mode="lines+markers",
            name="Episode reward"
        ))
        fig.update_layout(
            template="plotly_dark",
            title="Training Reward History"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------- SYSTEM INFO ----------
elif page == "System Information":

    st.header("ℹ️ System Information")

    st.markdown("""
    **Project:** ROBOAI

    **Purpose:** Robot sensor monitoring and intelligent navigation.

    **Interface:** Streamlit web dashboard.

    **Visualization:** Plotly.

    **Current data source:** Simulated sensor readings.

    **DRL status:** Agent training integration is pending.

    **Hardware:** No physical sensors or robot are connected.
    """)

st.divider()
st.caption(
    "ROBOAI Academic Project | Simulation Environment | Version 2.0"
)
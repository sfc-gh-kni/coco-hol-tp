import streamlit as st

st.title("Workshop agenda")

AGENDA = [
    ("9:00 AM", "Arrival & Coffee", None, None),
    ("9:15 AM", "Welcome & Workshop Overview", None, None),
    ("9:30 AM", "Session 1: Data Prep", "30 min", "1"),
    ("10:00 AM", "Session 2: Cortex Analyst & Semantic Views", "40 min", "2"),
    ("10:40 AM", "Session 3: Cortex Search", "30 min", "3"),
    ("11:10 AM", ":orange-badge[BREAK]", None, None),
    ("11:20 AM", "Session 4: Cortex Agents", "35 min", "4"),
    ("11:55 AM", "Session 5: CoWork", "20 min", "5"),
    ("12:15 PM", "Session 6: Streamlit", "15 min (optional)", "6"),
]

for time, title, duration, session_num in AGENDA:
    if session_num:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f":material/play_circle: **{title}** :gray-badge[{duration}]")
    elif "BREAK" in title:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f"{title}")
    else:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f":gray[{title}]")

st.space("medium")

st.markdown("##### What you'll build by end of session")
st.markdown("""
| Object Type | Count | Examples |
|-------------|-------|---------|
| **Tables** | 10 | Trades, orders, market prices, incident logs, compliance reports |
| **Cortex Search Services** | 1 | TRADING_DOCS_SEARCH |
| **Semantic Views** | 1 | ENERGY_TRADING_VIEW with relationships, metrics, and AI instructions |
| **Cortex Agents** | 1 | TRADING_OPS_AGENT with Analyst + Search + custom tools |
| **Streamlit Apps** | 1 | Operations dashboard with AI chat |
""")

st.space("small")

st.markdown("##### Location")
with st.container(border=True):
    st.markdown("""
:material/location_on: **TMX Trayport, London, UK**

July 28, 2026 — 9:00 AM to 12:30 PM
""")

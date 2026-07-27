import streamlit as st

st.title("Workshop agenda")

# (title, duration, session_num, optional)
AGENDA = [
    ("Session 1: Data Prep", "20 min", "1", False),
    ("Session 2: Cortex Analyst & Semantic Views", "30 min", "2", False),
    ("Session 3: Cortex Search", "25 min", "3", True),
    ("Session 4: Cortex Agents", "25 min", "4", False),
    ("Session 5: CoWork", "20 min", "5", False),
    ("Session 6: Streamlit", "20 min", "6", True),
]

for title, duration, session_num, optional in AGENDA:
    opt = " :blue-badge[Optional]" if optional else ""
    st.markdown(f":material/play_circle: **{title}** :gray-badge[{duration}]{opt}")

st.space("medium")

st.markdown("##### What you'll build")
st.markdown("""
| Object Type | Count | Examples |
|-------------|-------|---------|
| **Tables** | 10 | Trades, orders, market prices, incident logs, compliance reports |
| **Semantic Views** | 1 | ENERGY_TRADING_VIEW with relationships, metrics, and AI instructions |
| **Cortex Agents** | 1 | TRADING_OPS_AGENT with a semantic view tool + Data to Chart |
| **Cortex Search Services** | 1 (optional) | TRADING_DOCS_SEARCH |
| **Streamlit Apps** | 1 (optional) | Operations dashboard with AI chat |
""")

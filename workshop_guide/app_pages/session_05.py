import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(5, "CoWork", "Collaborative AI analysis with CoWork")

render_technologies_used([
    {"name": "Snowflake CoWork", "description": "An AI-powered collaborative workspace inside Snowsight where you can analyze data, generate insights, and share findings.", "icon": "group"},
    {"name": "Data Analysis", "description": "CoWork can query your Snowflake data, generate visualizations, and provide insights without writing SQL.", "icon": "analytics"},
    {"name": "Sharing & Collaboration", "description": "CoWork sessions can be shared with team members for collaborative data exploration.", "icon": "share"},
])

st.markdown("---")

st.markdown("#### :material/open_in_new: Open CoWork")
with st.container(border=True):
    st.markdown("""
In Snowsight, click **CoWork** in the left navigation panel. Start a new conversation.

CoWork discovers your tables in `TRAYPORT_AI.TRADING` automatically. Paste each question below one at a time.
""")

st.space("small")

st.markdown("#### :material/chat: Questions to ask CoWork")
st.caption("Copy and paste each question into CoWork individually.")

questions = [
    ("Trading activity overview", "Give me an overview of trading activity in TRAYPORT_AI.TRADING - total notional, number of trades, and the breakdown by commodity."),
    ("Top counterparties", "Who are the top trading firms by total notional value, and which commodities do they trade most?"),
    ("Venue performance", "Which markets have the highest average volatility, and how does that compare to their traded volume?"),
    ("Platform reliability", "Show me average platform uptime and peak latency by market, and flag any markets below 99.5% uptime."),
    ("Incidents vs. activity", "Which markets had the most High-severity incidents, and were those also the busiest by notional value?")
]

for title, question in questions:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.code(question, language="text", wrap_lines=True)

st.space("small")

render_explanation("How CoWork works", """
**CoWork** is Snowflake's collaborative AI workspace — different from Cortex Code:

| Tool | Best for |
|------|----------|
| Cortex Code | Building infrastructure, creating objects, writing SQL |
| CoWork | Exploring data, generating insights, team collaboration |
| Cortex Agent | End-user Q&A interface (deployed as a product) |
""")

render_key_concepts([
    {"term": "CoWork", "definition": "Snowflake's collaborative AI workspace. Conversational interface that queries data, creates visualizations, and generates insights."},
    {"term": "Context Maintenance", "definition": "CoWork maintains conversation history so follow-up questions build on previous analysis."},
])

render_what_you_built([
    "Explored operations data through conversational AI",
    "Generated visualizations and cross-table analysis",
    "Demonstrated the CoWork collaborative analysis pattern",
])

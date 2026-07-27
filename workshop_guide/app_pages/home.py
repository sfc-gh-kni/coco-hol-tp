import streamlit as st

st.title("European Energy Trading AI Workshop")
st.markdown("TMX Trayport &times; Snowflake &mdash; building intelligence for Europe's wholesale power, natural gas & carbon markets with Cortex")

st.space("small")

col1, col2, col3 = st.columns(3)
col1.metric("Sections", "6", help="Hands-on lab sections")
col2.metric("Prompts", "16", help="Total prompts across all tools")
col3.metric("Duration", "3.5 hrs", help="Total workshop time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each section has **numbered prompts** that you copy and paste into the appropriate tool:

- **Cortex Code** — for building infrastructure, creating objects, and writing SQL/Python
- **Cortex Analyst** — for testing natural language queries against your semantic view
- **Snowflake CoWork** — for collaborative data exploration and analysis

All prompts build on each other sequentially — run them in order throughout the morning.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
TMX Trayport operates the electronic trading networks that connect traders, brokers, and exchanges across Europe's wholesale energy markets. In this workshop you'll build an AI-powered operations platform over a synthetic slice of that world &mdash; power, natural gas, and carbon (EUA/UKA) trading across venues like TTF, NBP, EEX, EPEX, Nord Pool and N2EX. You'll turn raw trades, orders, market prices and platform telemetry &mdash; plus unstructured incident, compliance and market-notice text &mdash; into natural-language analytics, hybrid search, and an orchestrating AI agent.

We'll build a complete AI platform covering:

| Data type | Examples |
|-----------|---------|
| **Structured** | Executed trades, order-book activity, instruments, venues, and counterparties |
| **Unstructured** | Platform incident logs, REMIT/MiFID II compliance reports, exchange market notices |
| **Time series** | Daily market prices & volatility, platform telemetry (latency, uptime, throughput) |
""")

st.space("small")

st.markdown("#### What we're building")

with st.container(border=True):
    st.markdown("""
In 3.5 hrs, we build a complete AI-powered operations platform:

**1. Data Foundation** — Load structured and unstructured operations data into Snowflake from pre-generated CSV files.

**2. Natural Language Analytics** — Create a Semantic View over operational tables and query them with plain English via Cortex Analyst.

**3. Intelligent Search** — Build a Cortex Search service over safety documents and inspection reports for hybrid semantic + keyword search.

**4. AI Agents** — Create a Cortex Agent that orchestrates structured data queries AND document search through a single conversational interface.

**5. Collaborative AI** — Use CoWork to collaboratively analyze data with AI assistance.

**6. Operations Dashboard** — Deploy a Streamlit app with live KPIs, charts, and an AI chat interface.
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Snowflake account with **ACCOUNTADMIN** role — see **Getting Started** in the sidebar to provision a free trial
- **Cortex Code** open in Snowsight and connected to your account
- Cross-region inference enabled (for Cortex LLM functions)
""")

st.space("medium")
st.caption("Built for the July 28, 2026 workshop  :material/location_on:  TMX Trayport, London, UK")

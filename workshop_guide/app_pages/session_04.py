import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(4, "Cortex Agents", "11:20 AM", "35 min", "A Cortex Agent built in the Snowsight UI, using your semantic view as a tool")

render_technologies_used([
    {"name": "Cortex Agent", "description": "A managed agentic object that reasons over a request, plans the work, calls tools, and generates a response - all within Snowflake's governed environment.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The agent routes each question to the right tool. Here it uses your semantic view (via Cortex Analyst) for structured data questions.", "icon": "route"},
    {"name": "Data to Chart", "description": "A built-in tool that turns query results into visualizations - great for rankings and category breakdowns.", "icon": "insert_chart"},
])

st.info("""
:material/info: **This session is done in the Snowsight UI, not Cortex Code.** We'll create a Cortex Agent and wire in the `ENERGY_TRADING_VIEW` semantic view from Session 2 as a tool. We keep it lean - one structured-data tool plus charting.
""")

st.markdown("---")

st.markdown("#### :material/add_circle: Step 1 - Create the agent")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, go to **AI & ML -> Agents** -> **Create agent**.
2. If prompted for a location, choose **`TRAYPORT_AI.TRADING`**.
3. **Agent object name**: `TRADING_OPS_AGENT`
4. **Display name**: `European Energy Trading Assistant`
5. Select **Create agent**, then open it and go to the **Configuration** tab.
""")

st.markdown("Everything below happens across the **Configuration** sub-tabs: **General -> Instructions -> Tools**. We skip **Skills** and **MCP**.")

st.space("small")

st.markdown("#### :material/badge: Configuration - General")
with st.container(border=True):
    st.markdown("**Description**:")
    st.code(
        "Trading operations assistant for the TRAYPORT_AI.TRADING schema. Uses the "
        "ENERGY_TRADING_VIEW semantic view via Cortex Analyst (tool trading_analyst, "
        "warehouse TRAYPORT_WH) to answer natural-language questions about trades, "
        "counterparties, venues and commodities - notional value, volume, prices and trade counts.",
        language="text", wrap_lines=True,
    )
    st.markdown("**Example questions** (add each, up to 15):")
    st.code("Which five trading firms have the highest total notional value?", language="text", wrap_lines=True)
    st.code("What is the total notional value traded by commodity?", language="text", wrap_lines=True)
    st.code("How many trades settled versus were cancelled, by clearing house?", language="text", wrap_lines=True)

st.markdown("#### :material/tune: Configuration - Instructions")
with st.container(border=True):
    st.markdown("**Orchestration model**: select `auto` (Cortex picks the best available model).")
    st.markdown("**Planning instructions** (how the agent chooses tools):")
    st.code(
        "Use the trading_analyst tool for every quantitative request - notional value, "
        "traded volume, prices, trade counts, and rankings of trading firms (counterparties) - "
        "broken down by commodity, venue, country, trade side, status, or clearing house. "
        "For 'top' or 'biggest' counterparties, rank trading firms by total notional value.",
        language="text", wrap_lines=True,
    )
    st.markdown("**Response instructions** (tone/format):")
    st.code(
        "Respond concisely and professionally for an energy-trading audience. Show figures "
        "with their currency and prefer a chart when comparing categories or showing a ranking.",
        language="text", wrap_lines=True,
    )

st.markdown("#### :material/build: Configuration - Tools")
with st.container(border=True):
    st.markdown("""
Add your semantic view as a structured-data tool:

1. Find **Query structured data** -> **+ Add semantic view**.
2. **Name**: `trading_analyst`
3. **Semantic view**: `TRAYPORT_AI.TRADING.ENERGY_TRADING_VIEW`
4. **Warehouse**: `TRAYPORT_WH`
5. **Query timeout (seconds)**: `60`
6. **Description** (this drives tool routing - be specific):
""")
    st.code(
        "Converts natural-language questions into SQL over energy TRADES joined to MARKETS and "
        "TRADERS. Use for anything quantitative: total/average notional value, traded volume, "
        "prices, trade counts, and rankings of trading firms (counterparties), broken down by "
        "commodity, venue, country, side, status, or clearing house. Not for free-text document lookups.",
        language="text", wrap_lines=True,
    )
    st.markdown("7. Select **Add**.")
    st.markdown("Then enable **Data to Chart** (no resources needed) so the agent can visualize rankings and commodity breakdowns.")

st.markdown("#### :material/skip_next: Skills & MCP")
with st.container(border=True):
    st.markdown("Skip both tabs for this workshop. Then select **Save**.")

st.markdown("#### :material/verified: Save & test")
with st.container(border=True):
    st.markdown("Open the **Preview** tab (playground) and run the example questions. Confirm the agent routes to `trading_analyst`, returns correct figures/SQL, and charts the commodity breakdown.")
    st.markdown("Verify the object in SQL:")
    st.code("DESCRIBE AGENT TRAYPORT_AI.TRADING.TRADING_OPS_AGENT;", language="sql", wrap_lines=True)

st.success("""
:material/lightbulb: **Optional - add document search.** If you completed Session 3 and have the `TRADING_DOCS_SEARCH` service, add a **Cortex Search** tool named `trading_docs_search` (mark `content` searchable and `doc_type` filterable). The agent can then answer qualitative questions about incidents, compliance findings, and market notices - and combine them with the numbers.
""")

render_explanation("How the agent decides which tool to use", """
A Cortex Agent runs a **plan -> use tools -> reflect** loop. It reads each tool's **description** to decide
where to route a question, so the description does the heavy lifting: state clearly *what the tool does,
which data it covers, and when NOT to use it*.

In this lab the agent has one structured-data tool (your semantic view via Cortex Analyst) plus Data to
Chart. Because the planning instructions and tool description both point quantitative questions at
`trading_analyst`, the agent reliably turns "top counterparties by notional" into governed SQL - and, with
Data to Chart enabled, visualizes the result.

If a question doesn't route as expected, tighten the tool **Description** first - that's almost always the fix.
""")

render_key_concepts([
    {"term": "Cortex Agent", "definition": "A schema-level object that bundles a model, tools, and orchestration instructions to answer multi-step questions over your governed data."},
    {"term": "Tool description", "definition": "The natural-language guidance the agent uses to route questions to a tool. Clear 'use for / not for' wording is the single biggest driver of correct routing."},
    {"term": "Data to Chart", "definition": "A built-in agent tool that generates visualizations from data returned by other tools. No resources required."},
])

render_what_you_built([
    "TRADING_OPS_AGENT Cortex Agent in TRAYPORT_AI.TRADING (built in the Snowsight UI)",
    "trading_analyst tool backed by the ENERGY_TRADING_VIEW semantic view",
    "Planning and response instructions with energy-trading domain context",
    "Data to Chart enabled and validated in the agent playground",
])

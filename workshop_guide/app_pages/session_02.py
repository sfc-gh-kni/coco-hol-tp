import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(2, "Cortex Analyst & Semantic Views", "10:00 AM", "40 min", "A semantic view over 3 tables, built with Autopilot in the Snowsight UI")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL using a semantic view to understand your data's business meaning.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics and synonyms.", "icon": "description"},
    {"name": "Semantic View Autopilot", "description": "An AI-assisted generator in Snowsight that builds a semantic view from your tables so you can refine it visually - no YAML required.", "icon": "auto_fix_high"},
])

st.info("""
:material/info: **This session is done in the Snowsight UI, not Cortex Code.** We'll use the **Semantic View Autopilot** to generate a view, then refine it in the visual editor. Keep a **3-table star schema** - it means only **two joins** to define.
""")

st.markdown("---")

st.markdown("#### The model we're building")
with st.container(border=True):
    st.markdown("""
| Role | Table | Used for |
|------|-------|---------|
| **Fact** | `TRADES` | quantity, price, notional value, side, status, clearing house |
| **Dimension** | `MARKETS` | venue, commodity, region, country, currency |
| **Dimension** | `TRADERS` | firm, participant type, country, tier |

**Two relationships:** `TRADES.market_id -> MARKETS.market_id` and `TRADES.trader_id -> TRADERS.trader_id`
""")

st.space("small")

st.markdown("#### :material/rocket_launch: Step 1 - Launch Autopilot")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, go to **AI & ML -> Cortex Analyst**.
2. At the top, select **Create new -> Create new Semantic View**.
3. **Location**: database `TRAYPORT_AI`, schema `TRADING`.
4. **Name**: `ENERGY_TRADING_VIEW`.
5. **Description**: *European energy trades by venue and counterparty - notional, volume and status across power, gas and carbon markets.*
6. Select **Next**.
""")

st.markdown("#### :material/skip_next: Step 2 - Skip the context step")
with st.container(border=True):
    st.markdown("""
On the context screen, **don't upload anything** - select **Next** to go straight to table selection.

:material/lightbulb: Providing example SQL here would help Autopilot infer joins automatically, but we're skipping it to keep the flow simple - so we'll add the two relationships ourselves in Step 4.
""")

st.markdown("#### :material/table_chart: Step 3 - Select tables & columns")
with st.container(border=True):
    st.markdown("""
1. **Select tables**: choose **`TRADES`, `MARKETS`, `TRADERS`** (three tables only). Select **Next**.
2. **Select columns**: keep all columns, and enable **Add sample values** and **Add AI-generated descriptions** (both improve accuracy).
3. Select **Create and save**, then **Save and run**. Generation takes a couple of minutes.
""")

st.markdown("#### :material/key: Step 4 - Primary keys & the two relationships")
with st.container(border=True):
    st.markdown("""
Open the generated view in the editor and confirm/add the following.

**Primary keys** (Edit the logical table -> Primary Key):
- `MARKETS` -> `market_id`
- `TRADERS` -> `trader_id`

**Relationships** (select **+** next to Relationships; Left = the fact table, Right = the dimension):

| Left Table (FK) | Right Table (PK) | Join columns |
|-----------------|------------------|--------------|
| `TRADES` | `MARKETS` | `market_id -> market_id` |
| `TRADES` | `TRADERS` | `trader_id -> trader_id` |

:material/info: You don't set join types in the UI - they're inferred from the primary keys.
""")

st.markdown("#### :material/functions: Step 5 - Add metrics")
with st.container(border=True):
    st.markdown("""
Under the **`TRADES`** table, select **+** next to **Metrics** and add (Name / Expression):

- `total_notional` = `SUM(notional_value)`
- `trade_count` = `COUNT(trade_id)`
- `avg_trade_price` = `AVG(price)`
- `total_volume` = `SUM(quantity)`
""")

st.markdown("#### :material/label: Step 6 - Synonyms & custom instructions")
with st.container(border=True):
    st.markdown("""
**Synonyms** - on the **`MARKETS`** table, add synonyms to **two fields** (Edit the field -> Synonyms):
- `market_name` -> `venue, hub, exchange`
- `commodity` -> `carbon, allowance, EUA`

**Custom Instructions** - paste into the Custom Instructions section:
""")
    st.code(
        "European wholesale energy trades across power, natural gas and carbon (EUA/UKA) "
        "markets. 'Notional' is the monetary value of a trade (notional_value). Commodities "
        "are Power, Natural Gas and Emissions; venues include TTF, NBP, EEX, EPEX, Nord Pool "
        "and N2EX. When asked for the 'biggest' or 'top' counterparties, rank trading firms "
        "by total notional_value.",
        language="text", wrap_lines=True,
    )
    st.markdown("Then select **Save**.")

st.markdown("#### :material/verified: Step 7 - Verify & test with natural language")
with st.container(border=True):
    st.markdown("Confirm the object in a worksheet:")
    st.code("DESCRIBE SEMANTIC VIEW TRAYPORT_AI.TRADING.ENERGY_TRADING_VIEW;", language="sql", wrap_lines=True)
    st.markdown("Then, in **AI & ML -> Cortex Analyst**, select your view and ask these questions one at a time:")
    st.code("Which five trading firms have the highest total notional value?", language="text", wrap_lines=True)
    st.code("What is the total notional value traded by commodity?", language="text", wrap_lines=True)
    st.code("How many trades settled versus were cancelled, by clearing house?", language="text", wrap_lines=True)
    st.caption("Watch the generated SQL alongside each answer - great for showing how the semantic view drives Cortex Analyst.")

render_explanation("Why a semantic view (and why only 3 tables)?", """
A **semantic view** is a first-class Snowflake object that maps physical tables to business concepts -
relationships, facts, dimensions, metrics and synonyms - so Cortex Analyst can turn plain English into
correct SQL.

Starting with a focused **star schema** (one fact + two dimensions) keeps the model easy to reason about
and gives higher accuracy than a large "do-it-all" model. You can always expand it later by adding more
tables (for example `ORDERS` or `MARKET_PRICES`) and their relationships.

- **Facts** are row-level numbers (`quantity`, `price`, `notional_value`).
- **Metrics** are aggregations (`SUM(notional_value)`) that resolve consistently across questions.
- **Dimensions** are the categorical attributes you slice by (commodity, firm, status).
- **Synonyms** and **custom instructions** give Analyst your business vocabulary.
""")

render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Converts natural language to SQL using a semantic view for context."},
    {"term": "Semantic View Autopilot", "definition": "An AI-assisted generator in Snowsight that creates a semantic view from selected tables (and optional example SQL), which you then refine in the visual editor."},
    {"term": "Star schema", "definition": "A central fact table joined to dimension tables. Simple, fast, and the recommended starting point for a semantic view."},
])

render_what_you_built([
    "ENERGY_TRADING_VIEW semantic view (TRADES + MARKETS + TRADERS) via Autopilot",
    "Two relationships, four TRADES metrics, and synonyms on the MARKETS table",
    "Custom instructions with energy-trading domain context",
    "Natural language queries validated in Cortex Analyst",
])

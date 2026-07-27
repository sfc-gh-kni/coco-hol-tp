import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(2, "Cortex Analyst & Semantic Views", "10:00 AM", "40 min", "Semantic view with relationships, metrics, and natural language queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries using a semantic view to understand your data's business meaning.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms.", "icon": "description"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL — providing domain context and disambiguation hints.", "icon": "auto_fix_high"},
])


PROMPT_2_1 = """/semantic_studio In TRAYPORT_AI.TRADING, create a semantic view called ENERGY_TRADING_VIEW for use with Cortex Analyst. It should cover these tables: TRADES, ORDERS, MARKET_PRICES, INSTRUMENTS, MARKETS, TRADERS.

Include:
- Relationships between the tables following these rules:
  - Do NOT specify join_type — omit it entirely (the proto enum doesn't accept string values like many_to_one)
  - Convention: left_table = fact/many side, right_table = dimension/one side (put the table with many rows as left_table)
  - Define primary_key.columns on dimension tables (MARKETS, TRADERS, INSTRUMENTS) so the engine knows the "one" side
  - Use this template for each relationship:
    relationships:
      - name: <descriptive_name>
        left_table: <FACT_TABLE>
        right_table: <DIMENSION_TABLE>
        relationship_columns:
          - left_column: <FK_COLUMN>
            right_column: <PK_COLUMN>
  - Relationships needed: TRADES.instrument_id -> INSTRUMENTS.instrument_id; TRADES.market_id -> MARKETS.market_id; TRADES.trader_id -> TRADERS.trader_id; ORDERS.instrument_id -> INSTRUMENTS.instrument_id; ORDERS.market_id -> MARKETS.market_id; ORDERS.trader_id -> TRADERS.trader_id; MARKET_PRICES.instrument_id -> INSTRUMENTS.instrument_id; MARKET_PRICES.market_id -> MARKETS.market_id; INSTRUMENTS.market_id -> MARKETS.market_id (INSTRUMENTS is the many/left side here)
- Facts for key numeric columns: TRADES.quantity, TRADES.price, TRADES.notional_value; ORDERS.quantity, ORDERS.limit_price, ORDERS.fill_rate; MARKET_PRICES.close_price, MARKET_PRICES.volume, MARKET_PRICES.volatility
- Dimensions for categorical columns: MARKETS.market_name, MARKETS.commodity, MARKETS.region, MARKETS.country, MARKETS.venue_type, MARKETS.currency; TRADERS.firm_name, TRADERS.participant_type, TRADERS.country, TRADERS.tier; INSTRUMENTS.instrument_name, INSTRUMENTS.contract_type, INSTRUMENTS.delivery_period; TRADES.side, TRADES.trade_status, TRADES.clearing_house; ORDERS.side, ORDERS.order_status
- Add useful SYNONYMS ('venue'/'hub'/'exchange' for market_name; 'counterparty'/'participant'/'firm' for firm_name; 'deal'/'transaction' for a trade; 'product'/'contract' for instrument_name; 'carbon'/'allowance'/'EUA' for the Emissions commodity; 'volume' for quantity)
- Metrics: total_notional = SUM(TRADES.notional_value); trade_count = COUNT(TRADES.trade_id); avg_trade_price = AVG(TRADES.price); total_volume = SUM(TRADES.quantity); avg_fill_rate = AVG(ORDERS.fill_rate); avg_volatility = AVG(MARKET_PRICES.volatility)
- An AI_SQL_GENERATION instruction with domain context: This data models European wholesale energy trading across power, natural gas and carbon (EUA/UKA) markets. 'Notional' means the monetary value of a trade (notional_value column). Commodities are Power, Natural Gas and Emissions. Venues include TTF, NBP, THE, PEG, EEX, EPEX, Nord Pool, N2EX and OMIE. Prices are in the venue's local currency (EUR or GBP). 'Baseload' and 'peakload' are power delivery profiles. When a user asks for the 'biggest' or 'top' counterparties, rank trading firms by total notional_value.

Execute the SQL and confirm with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 2.1", "Create the Semantic View", PROMPT_2_1)

render_explanation("What this prompt does", """
Creates a **semantic view** — a first-class Snowflake object that enables natural language to SQL.


Key concepts encoded in the semantic view:

- **Relationships** connect the fact tables (`TRADES`, `ORDERS`, `MARKET_PRICES`) to their
  dimensions (`INSTRUMENTS`, `MARKETS`, `TRADERS`) so Analyst can join correctly. The fact table
  is always the *left* (many) side and the dimension the *right* (one) side, with primary keys
  defined on the dimension tables.
- **Facts** are the numeric measures Analyst can aggregate: trade `notional_value`, `quantity`,
  `price`, order `fill_rate`, and price `volatility`.
- **Dimensions** are the categorical attributes to slice by: commodity, venue type, participant
  type, contract type, trade side and status.
- **Metrics** are reusable calculations (total notional, trade count, average price) so business
  questions resolve consistently.
- **AI instructions** give Cortex Analyst the domain vocabulary of energy trading so it maps
  words like "counterparty", "hub" and "carbon" to the right columns.

""")


PROMPT_2_2 = """Ask Cortex Analyst these questions using TRAYPORT_AI.TRADING.ENERGY_TRADING_VIEW:

1. What is the total notional value traded by commodity?
2. Which five trading firms have the highest total notional value?
3. What is the average price volatility by market?
4. How many trades settled versus were cancelled, broken down by clearing house?

Show the generated SQL and results for each."""

render_prompt("Prompt 2.2", "Test with Natural Language Queries", PROMPT_2_2)

st.info("""
:material/lightbulb: **You can also test these in the Cortex Analyst UI!**

In Snowsight, navigate to **AI & ML → Cortex Analyst** in the left sidebar. Select your `ENERGY_TRADING_VIEW` semantic view, and you'll see a playground where you can type natural language questions interactively.
""")

render_explanation("What this prompt does", """
Tests Cortex Analyst across different question types to validate the semantic view definitions.


- **Question 1** exercises a metric (total notional) grouped by a dimension reached through a
  relationship (`TRADES` -> `INSTRUMENTS`/`MARKETS` commodity).
- **Question 2** validates ranking trading firms by an aggregate across the `TRADES` -> `TRADERS`
  relationship.
- **Question 3** aggregates a fact (`volatility`) from the `MARKET_PRICES` table by venue.
- **Question 4** combines a count with two categorical dimensions (`trade_status`, `clearing_house`).

""")


PROMPT_2_3 = """Now expand our ENERGY_TRADING_VIEW in TRAYPORT_AI.TRADING:

Add two calculated metrics: (1) settlement_rate = the share of trades whose trade_status = 'Settled' out of all trades, and (2) avg_notional_per_trade = total_notional / trade_count. Also add the synonym 'clearing venue' for the clearing_house column and ensure INSTRUMENTS.commodity is available as a dimension.

Execute all SQL."""

render_prompt("Prompt 2.3", "Expand the Semantic View", PROMPT_2_3)

render_explanation("What this prompt does", """
Demonstrates iterative semantic view development — adding calculated metrics.


Adds a **settlement_rate** ratio metric and an **avg_notional_per_trade** derived metric,
showing how you iterate on a semantic view over time. Re-running the Analyst questions after the
expansion lets attendees see the new metrics used automatically.

""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Converts natural language to SQL using a semantic view for context."},
    {"term": "Semantic View", "definition": "A first-class Snowflake object mapping tables to business concepts. Contains relationships, facts, dimensions, metrics, synonyms, and AI instructions."},
    {"term": "AI_SQL_GENERATION", "definition": "Custom instructions guiding SQL generation. Essential for domain-specific terminology."},
])

render_what_you_built([
    "ENERGY_TRADING_VIEW semantic view with domain-specific metrics",
    "Natural language queries validated against the view",
    "Expanded view with calculated metrics",
])

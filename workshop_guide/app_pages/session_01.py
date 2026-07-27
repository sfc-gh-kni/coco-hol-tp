import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(1, "Data Prep", "Database, schema, warehouse, and 10 operational tables loaded from CSV")

render_technologies_used([
    {"name": "Database & Schema", "description": "Snowflake's organizational hierarchy for objects. A database contains schemas, and schemas contain tables, views, and other objects.", "icon": "database"},
    {"name": "CSV File Format", "description": "Snowflake can infer schema and load data directly from CSV files using file formats and COPY INTO commands.", "icon": "table_chart"},
    {"name": "Virtual Warehouse", "description": "Snowflake's compute engine. A warehouse provides the CPU and memory to execute queries and load data.", "icon": "memory"},
])


PROMPT_1_1 = """Create the following Snowflake objects for our European Energy Trading AI workshop:

1. A database called TRAYPORT_AI
2. A schema called TRADING inside that database
3. A stage called DATA in the schema TRADING with a directory table and server side encryption
3. A warehouse called TRAYPORT_WH (size MEDIUM, auto-suspend after 60 seconds, auto-resume enabled)
4. Set the session context to use these objects

Execute all SQL and confirm each object was created."""

render_prompt("Prompt 1.1", "Create Database, Schema & Warehouse", PROMPT_1_1)

render_explanation("What this prompt does", """
Creates the foundational Snowflake objects:

```sql
CREATE DATABASE TRAYPORT_AI;
CREATE SCHEMA TRAYPORT_AI.TRADING;
CREATE WAREHOUSE TRAYPORT_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

USE DATABASE TRAYPORT_AI;
USE SCHEMA TRADING;
USE WAREHOUSE TRAYPORT_WH;
```
""")


PROMPT_1_2 = """In TRAYPORT_AI.TRADING, the 10 CSV files have been uploaded to an internal stage called DATA.

For all 10 tables (MARKETS, TRADERS, INSTRUMENTS, TRADES, ORDERS, MARKET_PRICES, PLATFORM_METRICS, INCIDENT_LOGS, COMPLIANCE_REPORTS, MARKET_NOTICES):

1. Create a file format (CSV with PARSE_HEADER=TRUE, FIELD_OPTIONALLY_ENCLOSED_BY='"')
2. Create the tables with appropriate column types inferred from the data. Ensure to convert the column names to uppercase.
3. Load the data

Use CREATE TABLE with INFER_SCHEMA from a stage and then COPY INTO them. The key requirement is that all 10 tables are created and populated.

Execute all SQL."""

st.markdown("""
**Before running the prompt below, download the CSV files and upload them to the `DATA` stage:**

1. Download the zip file containing all CSVs: [trayport_data.zip](https://github.com/sfc-gh-kni/coco-hol-tp/raw/main/workshop_guide/data/trayport_data.zip)
2. Unzip the file on your computer to get the individual CSV files.
3. Using Snowsight, use the Horizon Catalog to browse to the `TRAYPORT_AI.TRADING.DATA` stage and upload all CSV files.
4. Then copy the prompt below into Cortex Code and execute.
""")

render_prompt("Prompt 1.2", "Load and Create Tables from CSV", PROMPT_1_2)

render_explanation("What this prompt does", """
Loads all operational data tables from CSV files uploaded to the internal stage `DATA`:

```sql
CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE OR REPLACE TABLE TRADES
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(INFER_SCHEMA(
      LOCATION => '@TRAYPORT_AI.TRADING.DATA/trades.csv',
      FILE_FORMAT => 'csv_format'
    ))
  );

COPY INTO TRADES
  FROM @TRAYPORT_AI.TRADING.DATA/trades.csv
  FILE_FORMAT = csv_format;
```

**The tables**:

| Table | Rows | Description |
|-------|------|-------------|
| **MARKETS** | 12 | European trading venues/hubs (TTF, NBP, EEX, EPEX, Nord Pool, EUA...) by commodity, region, currency |
| **TRADERS** | 20 | Market participants &mdash; utilities, trading houses, banks, brokers |
| **INSTRUMENTS** | 24 | Tradeable products (spot, forward, future, option) with delivery period and unit |
| **TRADES** | 300 | Executed trades with price, quantity, notional, status and clearing house |
| **ORDERS** | 300 | Order-book activity with side, limit price, status and fill rate |
| **MARKET_PRICES** | 400 | Weekly OHLC prices, volume and volatility per instrument |
| **PLATFORM_METRICS** | 360 | Daily platform telemetry &mdash; messages, latency, uptime, active users, throughput |
| **INCIDENT_LOGS** | 41 | Platform/trading incident write-ups with severity, category and resolution |
| **COMPLIANCE_REPORTS** | 25 | REMIT / MiFID II / EMIR / market-abuse surveillance findings |
| **MARKET_NOTICES** | 20 | Exchange notices &mdash; listings, hours, tick size, clearing, regulatory |

""")


PROMPT_1_3 = """Run a query in TRAYPORT_AI.TRADING that shows every table name and its row count, ordered by row count descending. Format it nicely."""

render_prompt("Prompt 1.3", "Verify All Data Tables", PROMPT_1_3)

render_explanation("What this prompt does", """
A quick verification query. You should see approximately **1,500 total rows** across 10 tables.
""")


render_key_concepts([
    {"term": "Internal Stage", "definition": "A named Snowflake stage that stores files within Snowflake's managed storage. Files are uploaded via Snowsight UI or PUT command."},
    {"term": "INFER_SCHEMA", "definition": "A Snowflake table function that automatically detects column names and types from files in a stage."},
    {"term": "File Format", "definition": "A named object specifying how to parse files (CSV delimiters, headers, quoting). Created once and reused across multiple COPY INTO operations."},
])

render_what_you_built([
    "TRAYPORT_AI database and TRADING schema",
    "TRAYPORT_WH warehouse (Medium, auto-suspend 60s)",
    "10 operational data tables loaded from CSV (~1,500 total rows)",
])

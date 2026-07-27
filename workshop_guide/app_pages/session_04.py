import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(4, "Cortex Agents", "11:20 AM", "35 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools, executes them, reflects on results, and generates responses.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for documents, custom UDFs for logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities with custom business logic.", "icon": "build"},
])


PROMPT_4_1 = """In TRAYPORT_AI.TRADING, create a Cortex Agent called TRADING_OPS_AGENT.

It should:
- Use auto as the orchestration model
- Have two tools: the ENERGY_TRADING_VIEW semantic view (for structured data queries) and the TRADING_DOCS_SEARCH Cortex Search service (for unstructured document search)
- Include instructions defining it as the European Energy Trading Operations Assistant, guiding it to use structured data for trade volumes, notional values, counterparty rankings, prices, volatility and order fill rates and search for platform incidents, compliance and market-surveillance findings, and exchange market notices
- Mention domain context: European wholesale energy markets &mdash; power, natural gas and carbon (EUA/UKA) &mdash; traded across venues such as TTF, NBP, EEX, EPEX, Nord Pool and N2EX, connecting utilities, trading houses, banks and brokers.
- Include 3-4 sample questions spanning both tools

Execute and show confirmation."""

render_prompt("Prompt 4.1", "Create the Cortex Agent", PROMPT_4_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** combining structured analytics with document search:

- **Structured questions** → routed to Cortex Analyst via the semantic view
- **Unstructured questions** → routed to Cortex Search
- **Mixed questions** → Agent uses both tools and synthesizes
""")


PROMPT_4_2 = """Test our TRADING_OPS_AGENT with these queries:

1. (Structured) Which trading firms have the highest total notional value, and in which commodities?
2. (Unstructured) Summarise the most severe connectivity incidents and how they were resolved.
3. (Mixed) For the market with the most High-severity incidents, what was its total traded notional value?

Show the responses and note which tools the agent selected."""

render_prompt("Prompt 4.2", "Test the Agent", PROMPT_4_2)

render_explanation("What this prompt does", """
Tests the agent with structured, unstructured, and mixed queries to validate tool routing.
""")


PROMPT_4_3 = """In TRAYPORT_AI.TRADING, add a custom tool to the agent:

1. Create a UDF:

CREATE OR REPLACE FUNCTION TRAYPORT_AI.TRADING.CALCULATE_MARGIN_REQUIREMENT(NOTIONAL_VALUE FLOAT, VOLATILITY_PCT FLOAT)
RETURNS FLOAT
LANGUAGE SQL
COMMENT = 'Estimates initial margin for a cleared trade using a 2-day, 99% confidence parametric approach: notional * (volatility%/100) * 2.33 * sqrt(2).'
AS
$$
  ROUND(NOTIONAL_VALUE * (VOLATILITY_PCT / 100) * 2.33 * SQRT(2), 2)
$$;

2. Recreate TRADING_OPS_AGENT with CALCULATE_MARGIN_REQUIREMENT as an additional tool.

3. Test with: "What is the estimated initial margin for a trade with a notional value of 5,000,000 and volatility of 18%?"

Execute all SQL."""

render_prompt("Prompt 4.3", "Agent with Custom Tool", PROMPT_4_3)

render_explanation("What this prompt does", """
Adds a **custom UDF tool** for domain-specific calculations. The Agent can now query data, search documents, AND run custom business logic.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A Snowflake object that orchestrates LLMs, Analyst, Search, and custom tools to answer complex questions."},
    {"term": "Tool Routing", "definition": "The Agent selects the right tool for each question based on the question type and tool descriptions."},
    {"term": "Custom Tools", "definition": "SQL UDFs registered as Agent tools. Enable domain-specific calculations and business logic."},
])

render_what_you_built([
    "TRADING_OPS_AGENT — Cortex Agent with Analyst + Search tools",
    "Tested structured, unstructured, and mixed queries",
    "CALCULATE_MARGIN_REQUIREMENT as a custom tool",
    "Enhanced agent with three tool types",
])

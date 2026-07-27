import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(3, "Cortex Search", "Knowledge base view, a Cortex Search service built in the Snowsight UI, and search testing in the Playground")

st.warning("""
:material/info: **This section is optional.** The core AI platform (Semantic View + Agent) is complete without it. This session adds hybrid search over the unstructured incident, compliance, and market-notice text — and enables the optional document-search tool on the agent in Session 4.
""")

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine combining vector (semantic) and keyword search with automatic reranking and refreshes. Created from the Snowsight UI or a single SQL statement.", "icon": "search"},
    {"name": "Hybrid Search", "description": "Combines vector search (semantic similarity) with keyword search (exact matching), then reranks - better recall than either alone.", "icon": "hub"},
    {"name": "Search Playground", "description": "A built-in Snowsight UI for testing a search service interactively - type a query, apply filters, and inspect ranked results.", "icon": "preview"},
])

st.info("""
:material/info: **Mostly UI, one SQL step.** The Cortex Search creation wizard reads from a **single table or view**, so we first build one unified knowledge-base **view** that combines the three text tables (this needs a short worksheet query). Everything after that - creating the service and testing it - is done in the Snowsight UI.
""")

st.markdown("---")

st.markdown("#### :material/merge: Step 1 - Build the knowledge-base view (worksheet)")
with st.container(border=True):
    st.markdown("Run this once in a SQL worksheet to combine incidents, compliance findings, and market notices into one searchable view with a common shape:")
    st.code(
        "CREATE OR REPLACE VIEW TRAYPORT_AI.TRADING.TRADING_KNOWLEDGE_BASE AS\n"
        "SELECT incident_id AS doc_id, 'INCIDENT' AS doc_type,\n"
        "       category || ': ' || description || ' Resolution: ' || resolution AS content,\n"
        "       category AS metadata_category, severity AS metadata_priority, incident_date AS doc_date\n"
        "FROM TRAYPORT_AI.TRADING.INCIDENT_LOGS\n"
        "UNION ALL\n"
        "SELECT report_id, 'COMPLIANCE',\n"
        "       regulation || ' - ' || description,\n"
        "       regulation, status, report_date\n"
        "FROM TRAYPORT_AI.TRADING.COMPLIANCE_REPORTS\n"
        "UNION ALL\n"
        "SELECT notice_id, 'NOTICE',\n"
        "       title || '. ' || description,\n"
        "       notice_type, 'Info', notice_date\n"
        "FROM TRAYPORT_AI.TRADING.MARKET_NOTICES;",
        language="sql", wrap_lines=True,
    )

st.markdown("#### :material/search: Step 2 - Create the search service (Snowsight UI)")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, go to **AI & ML -> Cortex Search** -> **Create**.
2. Select a **role** (must have the `SNOWFLAKE.CORTEX_USER` database role) and the **`TRAYPORT_WH`** warehouse.
3. Select **database `TRAYPORT_AI`** and **schema `TRADING`**.
4. **Name**: `TRADING_DOCS_SEARCH`, then **Next**.
5. Choose **Table or view** and select **`TRADING_KNOWLEDGE_BASE`**, then **Next**.
6. **Columns to include** in results: select all - `doc_id`, `doc_type`, `content`, `metadata_category`, `metadata_priority`, `doc_date`. **Next**.
7. **Column to search**: select **`content`**. **Next**.
8. **Filter columns**: select **`doc_type`**, **`metadata_category`**, **`metadata_priority`**. **Next**.
9. **Target lag**: `1 hour`. Select **Create**.
""")
    st.caption("Snowflake auto-enables change tracking on the base tables and builds the index as part of creation - this can take a minute or two.")

st.markdown("#### :material/manage_search: Step 3 - Test in the Search Playground (UI)")
with st.container(border=True):
    st.markdown("Open the new `TRADING_DOCS_SEARCH` service and use the **Playground** to run these queries. Try the `doc_type` filter to scope results:")
    st.code("latency spikes during volatile trading", language="text", wrap_lines=True)
    st.caption("Filter doc_type = INCIDENT")
    st.code("wash trades, spoofing and layering surveillance", language="text", wrap_lines=True)
    st.caption("Filter doc_type = COMPLIANCE")
    st.code("clearing house margin parameter changes", language="text", wrap_lines=True)
    st.code("connectivity outage affecting a natural gas venue", language="text", wrap_lines=True)

st.success("""
:material/lightbulb: **This powers the agent.** In Session 4 (optional), add `TRADING_DOCS_SEARCH` as a Cortex Search tool on `TRADING_OPS_AGENT`. The agent then handles qualitative questions ("summarize the connectivity incidents") and combines them with the structured numbers - the RAG pattern, orchestrated for you.
""")

render_explanation("How Cortex Search works", """
Cortex Search builds a **hybrid** index over your text: it embeds each `content` value for **vector
(semantic)** search, keeps a **keyword** index for exact matches, and applies **semantic reranking** to
order results - no tuning required. It auto-refreshes as the base data changes (governed by the target lag).

Because the wizard reads a single source, we first shaped the three document types into one
`TRADING_KNOWLEDGE_BASE` view with a common schema (`doc_id`, `doc_type`, `content`, plus filter columns).
The filter columns (`doc_type`, `metadata_category`, `metadata_priority`) let you scope searches - e.g. only
compliance findings, or only High-severity incidents.
""")

render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed hybrid search engine created in the UI or with one SQL statement. Handles embedding, indexing, reranking, and auto-refresh automatically."},
    {"term": "Hybrid Search", "definition": "Combining vector search (semantic similarity) with keyword search (exact matching), plus reranking. Better than either alone."},
    {"term": "RAG", "definition": "Retrieval Augmented Generation: retrieve relevant documents, then have an LLM generate a grounded answer. Here the Session 4 agent orchestrates this for you."},
])

render_what_you_built([
    "TRADING_KNOWLEDGE_BASE - unified view over incidents, compliance findings, and market notices",
    "TRADING_DOCS_SEARCH - a Cortex Search service built in the Snowsight UI",
    "Hybrid search validated in the Search Playground with document-type filters",
    "A retrieval layer ready to plug into the Session 4 agent",
])

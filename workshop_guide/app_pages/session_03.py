import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(3, "Cortex Search", "10:40 AM", "30 min", "Knowledge base, Cortex Search service, and RAG query pattern")

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine combining vector (semantic) and keyword search with automatic reranking. Created with a single SQL statement.", "icon": "search"},
    {"name": "RAG (Retrieval Augmented Generation)", "description": "A pattern that retrieves relevant documents first, then passes them as context to an LLM for grounded answer generation.", "icon": "hub"},
    {"name": "SEARCH_PREVIEW", "description": "SQL function to query a Cortex Search Service. Supports text queries, column selection, filtering, and result limits.", "icon": "preview"},
])


PROMPT_3_1 = """In TRAYPORT_AI.TRADING:

1. First, create a unified text table for search called TRADING_KNOWLEDGE_BASE that combines:
   - From INCIDENT_LOGS: doc_id = incident_id, doc_type = 'INCIDENT', content = category || ': ' || description || ' Resolution: ' || resolution, metadata_category = category, metadata_priority = severity, doc_date = incident_date
   - From COMPLIANCE_REPORTS: doc_id = report_id, doc_type = 'COMPLIANCE', content = regulation || ' - ' || description, metadata_category = regulation, metadata_priority = status, doc_date = report_date
   - From MARKET_NOTICES: doc_id = notice_id, doc_type = 'NOTICE', content = title || '. ' || description, metadata_category = notice_type, metadata_priority = 'Info', doc_date = notice_date

2. Then create a Cortex Search Service:
   CREATE OR REPLACE CORTEX SEARCH SERVICE TRADING_DOCS_SEARCH
     ON content
     ATTRIBUTES metadata_category, metadata_priority, doc_type
     WAREHOUSE = TRAYPORT_WH
     TARGET_LAG = '1 hour'
     EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
     AS (
       SELECT doc_id, doc_type, content, metadata_category, metadata_priority, doc_date
       FROM TRADING_KNOWLEDGE_BASE
     );

Execute all SQL. Then verify with SHOW CORTEX SEARCH SERVICES."""

render_prompt("Prompt 3.1", "Create Cortex Search Service", PROMPT_3_1)

render_explanation("What this prompt does", """
Builds a unified knowledge base from unstructured text sources and creates a hybrid search service.

The search service automatically embeds, indexes, and serves results with auto-refresh when source data changes.
""")


PROMPT_3_2 = """In TRAYPORT_AI.TRADING, query our TRADING_DOCS_SEARCH service using SEARCH_PREVIEW:

1. "latency spikes during volatile trading" (filter doc_type = 'INCIDENT')
2. "wash trades, spoofing and layering surveillance" (filter doc_type = 'COMPLIANCE')
3. "clearing house margin parameter changes"
4. "connectivity outage affecting a natural gas venue" 

Execute all searches and show results."""

render_prompt("Prompt 3.2", "Query the Search Service", PROMPT_3_2)

render_explanation("What this prompt does", """
Tests different search capabilities across the document corpus:


- **Query 1** shows semantic matching on operational incident text, narrowed to incidents only.
- **Query 2** finds market-surveillance findings using domain terms (wash trades, spoofing, layering).
- **Query 3** demonstrates keyword + semantic hybrid recall across clearing-related notices/incidents.
- **Query 4** retrieves across document types for a specific commodity/venue theme.

""")


PROMPT_3_3 = """In TRAYPORT_AI.TRADING, implement a RAG pattern:

1. Question: "What are the most common platform incident types affecting our trading venues, and which measures have proven effective at resolving them?"

2. Retrieve top 5 documents from TRADING_DOCS_SEARCH, then pass to SNOWFLAKE.CORTEX.COMPLETE() with instructions to answer ONLY from the provided documents, cite doc_ids, and structure the answer with: 1) Common incident types, 2) Root causes, 3) Effective measures, 4) Recommendations.

Use claude-sonnet-4-6 as the model. Execute and show the RAG response."""

render_prompt("Prompt 3.3", "RAG Pattern: Search + Generate", PROMPT_3_3)

render_explanation("What this prompt does", """
Implements the full **RAG** pattern: retrieve relevant documents, then generate a grounded answer with citations.
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed hybrid search engine created with SQL. Handles embedding, indexing, reranking, and auto-refresh automatically."},
    {"term": "RAG", "definition": "Retrieval Augmented Generation: retrieve documents, include as context in LLM prompt, generate grounded answer."},
    {"term": "Hybrid Search", "definition": "Combining vector search (semantic similarity) with keyword search (exact matching). Better than either alone."},
])

render_what_you_built([
    "TRADING_KNOWLEDGE_BASE — unified document table",
    "TRADING_DOCS_SEARCH — Cortex Search service with hybrid search",
    "Search queries across multiple document types",
    "Full RAG pipeline for grounded Q&A",
])

"""
Streamlit UI for AI Market Analyst Agent (Bonus Feature 4).
"""
import streamlit as st
import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="AI Market Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 AI Market Analyst Agent</div>', unsafe_allow_html=True)
st.markdown("**Analyze market research documents with AI-powered insights**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check API health
    try:
        health_response = requests.get(f"{API_BASE_URL}/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ API Status: Healthy")
            
            with st.expander("📋 System Info"):
                st.write(f"**Vector Store:** {health_data['vector_store']['total_documents']} documents")
                st.write(f"**Embedding Model:** {health_data['embedding_model']}")
                st.write(f"**Generation Model:** {health_data['generation_model']}")
        else:
            st.error("❌ API Status: Unhealthy")
    except Exception as e:
        st.error(f"❌ Cannot connect to API: {str(e)}")
    
    st.markdown("---")
    
    st.header("ℹ️ About")
    st.info("""
    This AI agent analyzes the Innovate Inc. market research document using:
    - **RAG** for contextual Q&A
    - **Summarization** for insights
    - **Extraction** for structured data
    - **Autonomous Routing** for smart tool selection
    """)

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 Auto Query (Smart)",
    "❓ Q&A",
    "📝 Summarize",
    "📊 Extract Data",
    "📖 About"
])

# ==================== Tab 1: Auto Query (Bonus Feature 1) ====================
with tab1:
    st.header("🤖 Autonomous Query Routing")
    st.markdown("""
    Ask any question in natural language, and the AI will automatically choose 
    the best tool (Q&A, Summarization, or Data Extraction) to answer it.
    """)
    
    auto_query = st.text_input(
        "Enter your query:",
        placeholder="e.g., What is Innovate Inc's market share? or Summarize the SWOT analysis",
        key="auto_query"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        auto_button = st.button("🚀 Submit", key="auto_submit", type="primary")
    
    if auto_button and auto_query:
        with st.spinner("Processing your query..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/auto",
                    json={"query": auto_query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Show routing decision
                    routing = data['routing']
                    st.markdown("### 🎯 Routing Decision")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Selected Tool", routing['tool'].upper())
                    with col2:
                        st.metric("Confidence", f"{routing['confidence']:.0%}")
                    with col3:
                        st.info(f"**Reasoning:** {routing['reasoning']}")
                    
                    st.markdown("---")
                    
                    # Show result
                    result = data['result']
                    st.markdown("### 📋 Result")
                    
                    if routing['tool'] == 'qa':
                        st.markdown(f"**Answer:** {result['answer']}")
                        
                        with st.expander("📚 View Sources"):
                            for i, source in enumerate(result['sources'], 1):
                                st.text_area(f"Source {i}", source, height=100, disabled=True)
                    
                    elif routing['tool'] == 'summarize':
                        st.markdown(result['summary'])
                        st.caption(f"Word count: {result['word_count']}")
                    
                    elif routing['tool'] == 'extract':
                        if result['success']:
                            st.json(result['data'])
                        else:
                            st.error(f"Extraction failed: {result.get('error', 'Unknown error')}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ==================== Tab 2: Q&A ====================
with tab2:
    st.header("❓ Question Answering")
    st.markdown("Ask specific questions about the Innovate Inc. market research report.")
    
    question = st.text_area(
        "Your Question:",
        placeholder="e.g., What are the main competitors of Innovate Inc.?",
        height=100,
        key="qa_question"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        top_k = st.number_input("Top K", min_value=1, max_value=10, value=5, key="qa_top_k")
    
    qa_button = st.button("🔍 Get Answer", key="qa_submit", type="primary")
    
    if qa_button and question:
        with st.spinner("Searching for answer..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/qa",
                    json={"question": question, "top_k": top_k}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Show answer
                    st.markdown("### 💡 Answer")
                    st.success(data['answer'])
                    
                    # Show confidence
                    st.metric("Confidence", f"{data['confidence']:.0%}")
                    
                    # Show sources
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(data['sources'], 1):
                            st.markdown(f"**Source {i}:**")
                            st.text_area(f"source_{i}", source, height=150, disabled=True, label_visibility="collapsed")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ==================== Tab 3: Summarize ====================
with tab3:
    st.header("📝 Document Summarization")
    st.markdown("Generate summaries of the market research report.")
    
    col1, col2 = st.columns(2)
    with col1:
        summary_type = st.selectbox(
            "Summary Type:",
            ["comprehensive", "executive", "key_findings"],
            key="summary_type"
        )
    with col2:
        max_words = st.slider("Max Words:", 50, 500, 200, step=50, key="max_words")
    
    summarize_button = st.button("📝 Generate Summary", key="summarize_submit", type="primary")
    
    if summarize_button:
        with st.spinner("Generating summary..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/summarize",
                    json={"summary_type": summary_type, "max_words": max_words}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.markdown("### 📄 Summary")
                    st.markdown(data['summary'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Word Count", data['word_count'])
                    with col2:
                        st.metric("Type", data['summary_type'])
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ==================== Tab 4: Extract ====================
with tab4:
    st.header("📊 Structured Data Extraction")
    st.markdown("Extract structured data from the document as JSON.")
    
    extract_button = st.button("🔎 Extract Data", key="extract_submit", type="primary")
    
    if extract_button:
        with st.spinner("Extracting data..."):
            try:
                response = requests.post(f"{API_BASE_URL}/extract", json={})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['success']:
                        st.markdown("### 📊 Extracted Data")
                        
                        # Display as formatted JSON
                        st.json(data['data'])
                        
                        # Download button
                        json_str = json.dumps(data['data'], indent=2)
                        st.download_button(
                            label="💾 Download JSON",
                            data=json_str,
                            file_name="extracted_data.json",
                            mime="application/json"
                        )
                    else:
                        st.error(f"Extraction failed: {data.get('error', 'Unknown error')}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ==================== Tab 5: About ====================
with tab5:
    st.header("📖 About This Application")
    
    st.markdown("""
    ## 🎯 AI Market Analyst Agent
    
    This application is built for the VAIA Agentic AI Residency Program take-home assignment.
    It demonstrates a multi-functional AI agent capable of analyzing market research documents.
    
    ### 🚀 Features
    
    1. **Question Answering (Q&A)**: 
       - Uses RAG (Retrieval-Augmented Generation)
       - Retrieves relevant document chunks
       - Generates contextual answers with source citations
    
    2. **Summarization**:
       - Three types: Comprehensive, Executive, Key Findings
       - Customizable length
       - Extracts strategic insights
    
    3. **Data Extraction**:
       - Extracts structured data as JSON
       - Includes company metrics, competitors, SWOT analysis
       - Downloadable format
    
    4. **Autonomous Routing** (Bonus ⭐):
       - Automatically selects the best tool for your query
       - Smart intent classification
       - Natural language understanding
    
    ### 🛠️ Technical Stack
    
    - **LLM**: Google Gemini (gemini-2.0-flash-exp)
    - **Embeddings**: text-embedding-004 (768 dimensions)
    - **Vector Store**: ChromaDB (cosine similarity)
    - **Framework**: FastAPI + Streamlit
    - **RAG**: Custom implementation with LangChain
    
    ### 📊 Design Decisions
    
    **Chunking Strategy:**
    - Chunk Size: 1000 characters
    - Overlap: 200 characters (20%)
    - Rationale: Balances context preservation with retrieval precision
    
    **Embedding Model:**
    - Model: text-embedding-004
    - Rationale: Free tier, excellent quality, 768 dimensions
    
    **Vector Database:**
    - Database: ChromaDB
    - Rationale: Lightweight, persistent, no separate server needed
    
    **Structured Extraction:**
    - Temperature: 0.1 (deterministic)
    - JSON validation and type casting
    - Clear schema definition in prompt
    
    ### 👨‍💻 Developer
    
    Built for VAIA Agentic AI Residency Program
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("API Endpoints", "5")
    with col2:
        st.metric("Bonus Features", "4/4")
    with col3:
        st.metric("Tech Stack", "7+ tools")

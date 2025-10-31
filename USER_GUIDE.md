# AI Market Analyst - Complete User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Understanding the Interface](#understanding-the-interface)
3. [Tab 1: Auto Query (Smart Routing)](#tab-1-auto-query-smart-routing)
4. [Tab 2: Question Answering (Q&A)](#tab-2-question-answering-qa)
5. [Tab 3: Document Summarization](#tab-3-document-summarization)
6. [Tab 4: Data Extraction](#tab-4-data-extraction)
7. [Tab 5: About](#tab-5-about)
8. [Sidebar Features](#sidebar-features)
9. [Understanding Key Concepts](#understanding-key-concepts)
10. [Example Queries](#example-queries)

---

## Getting Started

### Accessing the Application

1. **Start the backend API** (Docker container on port 8000)
2. **Open the Streamlit UI** in your browser: `http://localhost:8501`
3. **Check the sidebar** to ensure the API status shows "✅ API Status: Healthy"

### First Look

When you open the application, you'll see:
- **Top Header**: "📊 AI Market Analyst Agent" - the main title
- **Five Tabs**: Different ways to interact with the AI
- **Sidebar (Left)**: System configuration and health status

---

## Understanding the Interface

### Main Layout

```
┌─────────────────────────────────────────────────────────┐
│          📊 AI Market Analyst Agent                     │
│   Analyze market research documents with AI insights    │
├─────────────────────────────────────────────────────────┤
│  🤖 Auto Query │ ❓ Q&A │ 📝 Summarize │ 📊 Extract │...│
├─────────────────────────────────────────────────────────┤
│                                                          │
│              [Active Tab Content Here]                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Color Coding

- **Green boxes** = Success messages, answers
- **Blue boxes** = Information, tips
- **Red boxes** = Errors (rare if API is healthy)
- **Gray boxes** = Source documents, metadata

---

## Auto Query (Smart Routing)

### What It Does

This is the **smartest** tab! You type any question naturally, and the AI automatically:
1. **Understands** what you're asking
2. **Chooses** the right tool (Q&A, Summarize, or Extract)
3. **Shows you** why it made that choice
4. **Returns** the answer using the selected tool

### How to Use

1. **Type your question** in the text box
   - Use natural language - no special format needed
   - Examples below

2. **Click "🚀 Submit"**

3. **Review the routing decision**:
   - **Selected Tool**: Which tool the AI chose
   - **Confidence**: How sure it is (0-100%)
   - **Reasoning**: Why it made this choice

4. **Read the result**: Based on the tool selected

### Example Questions and Expected Routing

| Your Question | Tool Selected | Why |
|--------------|---------------|-----|
| "What is Innovate Inc's market share?" | **Q&A** | Specific factual question |
| "Summarize the SWOT analysis" | **Summarize** | Asking for condensed overview |
| "Give me all the financial data" | **Extract** | Requesting structured information |
| "Who are the competitors?" | **Q&A** | Specific list/fact question |
| "What are the key findings?" | **Summarize** | Broad insights request |

### Understanding Confidence

**Confidence Score** shows how certain the AI is about which tool to use:

- **90-100%**: Very confident - clear intent
  - Example: "What is the market share?" → Q&A (98%)

- **70-89%**: Confident - likely correct
  - Example: "Tell me about competitors" → Could be Q&A or Summarize (85%)

- **50-69%**: Moderate - best guess
  - Example: "What's important here?" → Summarize (65%)

**Note**: Even at 60% confidence, the AI usually picks the right tool based on keyword analysis.

### How Routing Works (Behind the Scenes)

The AI analyzes your question for:
1. **Keywords**: "summarize", "extract", "what is", "who are"
2. **Question type**: Factual vs. broad vs. data-focused
3. **Intent**: Information retrieval vs. overview vs. structured data

**Routing Logic**:
```
Question contains "summarize/overview/key findings" → Summarize (High confidence)
Question asks "what/who/when/where" + specific topic → Q&A (High confidence)
Question asks for "data/metrics/all X" → Extract (High confidence)
Default → Q&A (Medium confidence)
```

---

## Question Answering (Q&A)

### What It Does

This tab answers **specific questions** about the Innovate Inc. market research document using RAG (Retrieval-Augmented Generation).

### How to Use

1. **Enter your question** in the text area
2. **Set Top K** (optional) - explained below
3. **Click "🔍 Get Answer"**
4. **Read the answer** (green success box)
5. **Check confidence score**
6. **Expand sources** to see where the answer came from

### What is "Top K"?

**Top K** = Number of document chunks to retrieve before answering

**How it works**:
1. Your question is converted to a vector (embedding)
2. The system searches for the **K most similar** document chunks
3. These chunks are sent to the AI as context
4. The AI generates an answer based on these chunks

**Choosing the Right Top K**:

| Top K | Use When | Pros | Cons |
|-------|----------|------|------|
| **1-3** | Very specific question with one clear answer | Fast, focused | May miss context |
| **5** (default) | Most questions | Balanced | Best for general use |
| **7-10** | Broad question needing multiple sources | Comprehensive | Slower, may add noise |

**Example**:
- Question: "What is Innovate Inc's market share?"
- Top K = 3 → Retrieves 3 chunks mentioning "market share"
- Answer: "12%" with sources showing where this was found

### Understanding Confidence in Q&A

**Confidence Score** (0-100%) indicates answer quality:

**How it's calculated**:
```
Confidence = Average of:
1. Similarity scores of retrieved chunks (how relevant they are)
2. Keyword overlap between question and sources
3. Presence of numerical/factual data (higher confidence)
```

**What different levels mean**:
- **85-100%**: Exact answer found in sources
  - Example: "Market share is 12%" → Direct quote found

- **70-84%**: Strong answer, good sources
  - Example: "Competitors include X, Y, Z" → List found across sources

- **60-69%**: Reasonable answer, some inference
  - Example: "Growth strategy focuses on..." → Synthesized from context

- **Below 60%**: Uncertain, may be inferred
  - Consider rephrasing your question or increasing Top K

### Viewing Sources

Click **"📚 View Sources"** to see the exact document chunks used:
- Each source is a 1000-character chunk from the original document
- Sources are ranked by relevance (most relevant first)
- Use sources to verify the answer or read more context

---

## Document Summarization

### What It Does

Generates condensed summaries of the Innovate Inc. market research report in different styles.

### How to Use

1. **Choose Summary Type**:
   - **Comprehensive**: Detailed overview covering all major points
   - **Executive**: High-level summary for decision-makers
   - **Key Findings**: Bullet points of most important insights

2. **Set Max Words** (50-500):
   - Controls the length of the summary
   - Slider adjusts in 50-word increments

3. **Click "📝 Generate Summary"**

4. **Read the summary** formatted with markdown
   - Word count shown below
   - Summary type confirmed

### Summary Types Explained

#### 1. **Comprehensive** (Recommended: 200-300 words)

**Best for**: Deep understanding, reports, documentation

**What it includes**:
- Company overview
- Market position and competitors
- SWOT analysis points
- Strategic initiatives
- Future outlook

**Example output**:
```
Innovate Inc. is a technology company specializing in AI solutions
with a 12% market share in the enterprise AI market. The company
faces competition from TechCorp (25% market share) and SmartAI
(18% market share)...

[Continues with detailed coverage of all major topics]

Word Count: 287
```

#### 2. **Executive** (Recommended: 100-150 words)

**Best for**: Quick briefing, presentations, stakeholder updates

**What it includes**:
- Core value proposition
- Key metrics (market share, growth)
- Critical challenges and opportunities
- Strategic direction

**Focus**: High-impact information only

**Example output**:
```
Innovate Inc. (12% market share) competes in the enterprise AI
market against larger players. Key strengths include innovative
technology and customer relationships, but faces challenges from
limited brand recognition and resource constraints...

[Focuses on actionable insights]

Word Count: 94
```

#### 3. **Key Findings** (Recommended: 100-200 words)

**Best for**: Meeting notes, highlights, decision points

**What it includes**:
- Bullet-pointed main insights
- Critical facts and figures
- Action items or recommendations
- Standout observations

**Format**: Structured list for easy scanning

**Example output**:
```
KEY FINDINGS:

• Market Position: 12% share, 3rd place behind TechCorp (25%)
• Core Strength: Proprietary AI technology and agile development
• Major Weakness: Limited marketing budget and brand recognition
• Primary Opportunity: Emerging markets showing 35% growth
• Key Threat: Increasing competition from well-funded startups

Word Count: 156
```

### Choosing Max Words

**Guidelines**:

| Max Words | Use Case | Reading Time |
|-----------|----------|--------------|
| **50-100** | Ultra-brief, email summary | 30 seconds |
| **100-200** | Standard brief, executive review | 1 minute |
| **200-300** | Detailed overview, reports | 2 minutes |
| **300-500** | Comprehensive analysis, deep dive | 3-4 minutes |

**Important**: The AI targets your max word count but may go slightly over/under to complete thoughts naturally.

### When to Use Each Type

**Use Comprehensive when**:
- Writing a report or documentation
- Need to understand all aspects
- Sharing with team members who need context
- First time reading about the company

**Use Executive when**:
- Presenting to leadership
- Time is limited
- Need decision-ready insights
- Audience is already familiar with context

**Use Key Findings when**:
- Creating meeting notes
- Need quick reference
- Highlighting action items
- Comparing multiple companies/reports

---

## Data Extraction

### What It Does

Extracts **structured data** from the document in JSON format - perfect for:
- Importing into spreadsheets
- Feeding into other systems
- Creating dashboards
- Data analysis

### How to Use

1. **Click "🔎 Extract Data"**
   - No parameters needed!
   - Extraction is deterministic (same result every time)

2. **Review the JSON data**
   - Displayed in formatted, collapsible view
   - Organized into logical sections

3. **Download the data**:
   - Click "💾 Download JSON"
   - Saves as `extracted_data.json`
   - Can open in any text editor or import into tools

### What Data is Extracted

The system extracts this **exact structure**:

```json
{
  "company_name": "Innovate Inc.",
  "industry": "Artificial Intelligence Solutions",
  "market_share": "12%",
  "competitors": [
    {
      "name": "TechCorp",
      "market_share": "25%",
      "key_strength": "..."
    },
    {
      "name": "SmartAI",
      "market_share": "18%",
      "key_strength": "..."
    }
  ],
  "swot_analysis": {
    "strengths": [
      "Proprietary AI technology",
      "Strong customer relationships",
      ...
    ],
    "weaknesses": [
      "Limited brand recognition",
      "Resource constraints",
      ...
    ],
    "opportunities": [
      "Emerging markets",
      "Strategic partnerships",
      ...
    ],
    "threats": [
      "Intense competition",
      "Rapid technological changes",
      ...
    ]
  },
  "target_market": "Enterprise clients in financial services, healthcare, and retail",
  "key_products": [
    "AI-powered analytics platform",
    "Predictive modeling tools",
    ...
  ],
  "financial_metrics": {
    "annual_revenue": "$50M",
    "growth_rate": "25% YoY",
    "profit_margin": "15%"
  }
}
```

### Understanding the JSON Structure

**Top-Level Fields**:
- `company_name`: Official company name
- `industry`: Business sector/domain
- `market_share`: Percentage (string format)
- `target_market`: Customer segments

**Complex Objects**:

1. **competitors** (Array):
   - Each competitor is an object with name, market share, and strength
   - Sorted by market share (highest first)

2. **swot_analysis** (Object):
   - Four arrays: strengths, weaknesses, opportunities, threats
   - Each item is a string description
   - Typically 3-5 items per category

3. **key_products** (Array):
   - List of main product offerings
   - Strings describing each product

4. **financial_metrics** (Object):
   - Structured financial data
   - Includes revenue, growth, margins
   - All values are strings (may include units like "$" or "%")

### Using the Extracted Data

**In Excel/Google Sheets**:
1. Download the JSON file
2. Use Data → Import → JSON
3. Creates structured table automatically

**In Python**:
```python
import json

with open('extracted_data.json', 'r') as f:
    data = json.load(f)

market_share = data['market_share']
competitors = data['competitors']
```

**In JavaScript**:
```javascript
fetch('extracted_data.json')
  .then(response => response.json())
  .then(data => {
    console.log(data.company_name);
  });
```

### Why Extraction is Useful

**Advantages over Copy-Paste**:
- ✅ **Structured**: Consistent format every time
- ✅ **Machine-readable**: Easy to process programmatically
- ✅ **Complete**: Captures all key data points
- ✅ **Validated**: JSON format ensures data integrity
- ✅ **Reusable**: Import into any tool that reads JSON

**Use Cases**:
- Creating comparison dashboards (multiple companies)
- Populating databases
- Generating reports automatically
- Feeding into ML models
- Building visualizations (charts, graphs)

---

## Example Queries

### For Auto Query Tab

**Factual Questions** (→ Q&A):
- "What is Innovate Inc's market share?"
- "Who are the competitors?"
- "What is the target market?"
- "What are the key products?"

**Summary Requests** (→ Summarize):
- "Summarize the SWOT analysis"
- "Give me an overview of the company"
- "What are the key findings?"
- "Summarize the competitive landscape"

**Data Requests** (→ Extract):
- "Extract all the financial data"
- "Give me structured data about the company"
- "Export the SWOT analysis as JSON"
- "Show me all metrics in data format"

### For Q&A Tab

**Company Information**:
- "What industry does Innovate Inc. operate in?"
- "What is Innovate Inc's primary business?"
- "When was the company founded?"

**Market Analysis**:
- "What is Innovate Inc's market position?"
- "How does Innovate Inc. compare to competitors?"
- "What is the market share of TechCorp?"

**Strategic Elements**:
- "What are Innovate Inc's main strengths?"
- "What weaknesses does the company face?"
- "What opportunities are mentioned?"
- "What threats does Innovate Inc. face?"

**Products & Customers**:
- "Who is the target market?"
- "What products does Innovate Inc. offer?"
- "What customer segments are mentioned?"

**Financial**:
- "What is the annual revenue?"
- "What is the growth rate?"
- "What is the profit margin?"

### For Summarize Tab

**Comprehensive** (200-300 words):
- Use for: First-time readers, comprehensive reports
- Goal: Understand everything important

**Executive** (100-150 words):
- Use for: Quick briefing, decision-makers
- Goal: High-level strategic insights only

**Key Findings** (100-200 words):
- Use for: Action items, meeting notes
- Goal: Bulleted highlights and metrics

### For Extract Tab

**No input needed** - just click extract!

**Best used when**:
- Need to compare multiple companies (extract from each)
- Building a database or spreadsheet
- Creating visualizations
- Automating workflows
- Sharing data with other systems

---

## Summary

This AI Market Analyst Agent provides:
- ✅ **Flexible interaction**: 5 different ways to get insights
- ✅ **Transparent**: Shows sources, confidence, reasoning
- ✅ **Accurate**: Grounded in document facts via RAG
- ✅ **Versatile**: Q&A, summaries, structured data
- ✅ **Smart**: Autonomous routing picks the right tool
- ✅ **Export-ready**: Download JSON data for other tools

**Start with** Auto Query to explore, then use specialized tabs for focused tasks!

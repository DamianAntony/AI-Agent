# AI Research Chatbot - Complete Project Walkthrough

## 📋 Project Overview

This is an **AI-Powered Research Assistant Chatbot** built with LangChain and Google's Generative AI (Gemini). The application takes user research queries and returns structured research information including topic, summary, sources, and tools used.

**Purpose**: Automate research tasks by querying web search and Wikipedia to provide comprehensive research summaries.

---

## 🏗️ Project Architecture

```
AI Agent Project/
├── main.py                 # Main application logic
├── tool.py                 # Tool definitions (search & wiki)
├── requirements.txt        # Project dependencies
├── check_versions.py       # Utility to check installed packages
├── .env                    # Environment variables (API keys)
└── venv/                   # Virtual environment
```

---

## 📦 Project Dependencies

### Core Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| `langchain` | >=0.0.280 | Framework for building LLM applications |
| `langchain-core` | - | Core abstractions for LangChain |
| `langchain-community` | - | Community integrations & tools |
| `langchain-google-genai` | >=0.0.11 | Google Generative AI integration |
| `python-dotenv` | 1.0.1 | Load environment variables from .env |
| `pydantic` | 2.7.1 | Data validation and parsing |
| `duckduckgo-search` | 6.3.5 | Web search functionality |
| `wikipedia` | 1.4.0 | Wikipedia content access |

---

## 🔧 Component Breakdown

### 1. **main.py** - Main Application

#### Imports
```python
from dotenv import load_dotenv              # Load API keys from .env
from pydantic import BaseModel              # Data validation
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM
from langchain_core.prompts import ChatPromptTemplate  # Prompt structure
from langchain_core.output_parsers import PydanticOutputParser  # JSON parsing
```

#### Key Components

**a) ResearchResponse Model**
```python
class ResearchResponse(BaseModel):
  topic: str              # Research topic
  summary: str            # Research summary
  sources: str            # Information sources
  tools_used: str         # Tools that were used
```
- Defines the structure of output data
- Ensures consistent JSON responses

**b) LLM Configuration**
```python
llm = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash",
  temperature=0.7,
  convert_system_message_to_human=True
)
```
- **Model**: Gemini 2.5 Flash (fast and efficient)
- **Temperature**: 0.7 (balanced creativity)
- **convert_system_message_to_human**: Required for Google API compatibility

**c) Prompt Template**
```python
prompt = ChatPromptTemplate.from_messages([
  ("system", "You are a research assistant..."),
  ("placeholder", "{chat_history}"),
  ("human", "{query}"),
  ("placeholder", "{agent_scratchpad}")
])
```
- Instructs the LLM to output only JSON
- Prevents tool calls from failing
- Handles chat history and working memory

**d) Processing Chain**
```python
chain = prompt | llm | parser
```
- **Pipeline**: Prompt → LLM → Pydantic Parser
- Converts user input → structured JSON output
- No tool calling agent (for compatibility)

**e) Main Execution Flow**
```python
1. Load environment variables
2. Get user input: "What can I help you In Research "
3. Invoke chain with query + empty chat_history + empty agent_scratchpad
4. Parse and validate output
5. Display structured ResearchResponse
```

---

### 2. **tool.py** - Tool Definitions

#### Web Search Tool
```python
search = DuckDuckGoSearchRun()
search_tool = Tool(
  name="search_web",
  func=search.run,
  description="search web for information"
)
```
- **Purpose**: Search the internet for current information
- **Source**: DuckDuckGo (privacy-friendly)
- **Output**: Relevant web results

#### Wikipedia Tool
```python
api_wrapper = WikipediaAPIWrapper(
  top_k_results=2,           # Return top 2 results
  doc_content_chars_max=200  # Limit content to 200 chars
)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
```
- **Purpose**: Access Wikipedia for reference information
- **Features**: 
  - Limits to top 2 results for relevance
  - Truncates content to 200 characters for efficiency

---

### 3. **check_versions.py** - Diagnostic Utility

Checks installed package versions:
```python
import langchain
import langchain_core
import langchain_community
import langchain_google_genai
import duckduckgo_search
```

**Usage**: Verify all dependencies are installed correctly
```bash
python check_versions.py
```

---

## 🚀 How It Works - Step by Step

### Execution Flow

```
┌─────────────────────────────────────┐
│   User runs: python main.py         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Load environment variables         │
│  (Google API key from .env)         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Prompt user:                       │
│  "What can I help you In Research " │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  User enters query                  │
│  e.g., "latest efootball updates"   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Chain Processing:                  │
│  1. Format prompt with user input   │
│  2. Send to Gemini LLM              │
│  3. LLM generates JSON response     │
│  4. Parser validates & structures   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Error Handling:                    │
│  - If parsing fails → Use defaults  │
│  - Return partial response          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Display Output:                    │
│  ✅ Structured Output               │
│  - topic                            │
│  - summary                          │
│  - sources                          │
│  - tools_used                       │
└─────────────────────────────────────┘
```

---

## 🔑 Setup & Configuration

### Prerequisites
- Python 3.8+
- Google API Key (from Google Cloud)

### Installation Steps

1. **Clone/Download the project**
```bash
cd "C:\Users\We Store\OneDrive\Desktop\Python ChatBot\AI Agent"
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
.\venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Create .env file**
```bash
# In the project root directory
echo GOOGLE_API_KEY=your_api_key_here > .env
```

6. **Run the application**
```bash
python main.py
```

---

## 📊 Data Flow Example

### Example Query: "latest efootball updates"

**Input:**
```
What can I help you In Research latest efootball updates?
```

**Processing:**
1. Prompt formatted with query
2. Sent to Gemini 2.5 Flash
3. LLM generates research structure
4. Pydantic parser validates JSON

**Expected Output:**
```json
{
  "topic": "eFootball Latest Updates",
  "summary": "Latest information about eFootball game updates...",
  "sources": "Wikipedia, Web Search",
  "tools_used": "Browser, Wikipedia"
}
```

---

## ⚠️ Error Handling

The application includes comprehensive error handling:

### 1. **Parsing Errors**
```python
try:
    structured_output = chain.invoke({...})
except OutputParserException as e:
    # Falls back to default ResearchResponse
    structured_output = ResearchResponse(
        topic=user_input,
        summary="Unable to parse structured response",
        sources="None",
        tools_used="Web_Search, Wikipedia"
    )
```

### 2. **Common Issues & Fixes**

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'dotenv'` | Missing dependency | Run `pip install -r requirements.txt` |
| `ValueError: SystemMessages not supported` | Google API config | Add `convert_system_message_to_human=True` |
| `AttributeError: 'int' object has no attribute 'name'` | Version mismatch | Update langchain-google-genai |
| `No module named 'langchain_core.pydantic_v1'` | Incompatible versions | Use compatible package versions |

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_generative_ai_api_key_here
```

**Getting the API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy and paste into .env file

---

## 🧪 Testing

### Test the installation
```bash
python check_versions.py
```

### Test the chatbot
```bash
python main.py
# Enter a research query when prompted
```

---

## 📝 Code Quality

### Current Features
✅ Error handling with fallbacks
✅ Type validation with Pydantic
✅ Environment variable management
✅ Clean separation of concerns
✅ Structured JSON output

### Potential Improvements
- Add chat history persistence
- Implement caching for repeated queries
- Add rate limiting
- Implement logging system
- Add more search tools
- Create web interface (Flask/Streamlit)

---

## 🎯 Use Cases

1. **Academic Research**: Gather information on research topics
2. **News Monitoring**: Get latest updates on trending topics
3. **Data Collection**: Automated information gathering
4. **Learning Assistant**: Educational information retrieval
5. **Business Intelligence**: Market research automation

---

## 📚 Dependencies Explanation

### LangChain Ecosystem
- **langchain**: Core framework for building LLM applications
- **langchain-core**: Base classes and interfaces
- **langchain-community**: Community tools (search, Wikipedia, etc.)
- **langchain-google-genai**: Google Generative AI integration

### External APIs
- **duckduckgo-search**: Privacy-focused web search
- **wikipedia**: Wikipedia content API

### Utilities
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation and settings management

---

## 🔄 Version History

### v1.0 (Current)
- Initial implementation
- Basic research assistant chatbot
- Google Gemini 2.5 Flash integration
- Web search + Wikipedia tools
- Structured JSON output

### Fixed Issues
1. ✅ Typo in variable names (`agent_executer` → `agent_executor`)
2. ✅ Invalid Python syntax in comments (`&&` → `and`)
3. ✅ Missing chat_history in invoke call
4. ✅ agent_scratchpad type error (string → list)
5. ✅ SystemMessage compatibility with Google API
6. ✅ Package version conflicts resolved

---

## 📞 Support

### Common Questions

**Q: Why is the output empty?**
A: Check your Google API key in .env file. Ensure it's valid and has proper permissions.

**Q: How do I change the model?**
A: Edit line 26 in main.py:
```python
model="gemini-2.5-flash"  # Change to another model
```

**Q: Can I use different search engines?**
A: Yes, modify tool.py to add other search tools from langchain-community.

---

## 📄 Files Summary

| File | Lines | Purpose |
|------|-------|---------|
| main.py | 97 | Main application logic |
| tool.py | 17 | Tool definitions |
| check_versions.py | 31 | Diagnostic utility |
| requirements.txt | 8 | Dependencies |
| .env | - | API keys (not in repo) |

---

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [DuckDuckGo Search](https://github.com/debanjo01/duckduckgo-search)

---

**Project Created**: February 3, 2026
**Status**: ✅ Functional
**Last Updated**: February 3, 2026

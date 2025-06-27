# 📚 Grimoire Guardian

An ancient and mystical archivist that helps you explore and query documents using advanced AI-powered retrieval and reasoning.

![](./grimoire-guardian.jpg)

## 🎭 About

The Grimoire Guardian is an AI-powered document assistant that acts as an ancient archivist machine. It processes documents, creates intelligent indexes, and answers questions about the content using a combination of semantic search and large language models. Perfect for exploring books, research papers, or any text-based documents!

## ✨ Features

- **🔍 Intelligent Document Search**: Uses FAISS vector search with HuggingFace embeddings
- **🤖 AI-Powered Q&A**: Leverages Databricks OpenAI models for natural language responses
- **📖 Document Processing**: Supports PDF documents with smart text chunking
- **🎨 Interactive Interface**: Streamlit web app for easy document exploration
- **🧙 Mystical Personality**: Responds as an ancient archivist with magical flair
- **🔗 LangGraph Integration**: Uses advanced agent workflows for complex reasoning

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Databricks workspace access
- OpenAI API access through Databricks

### Installation

1. **Clone and navigate to the project:**

   ```bash
   cd grimoire-guardian
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Configure Databricks authentication:**
   ```bash
   export DATABRICKS_HOST=<your-databricks-host>
   export DATABRICKS_TOKEN=<your-databricks-token>
   export OPEN_AI_API_KEY=$DATABRICKS_TOKEN
   ```

### Usage

#### 🖥️ Streamlit Web Interface

Launch the interactive web application:

```bash
uv run streamlit run src/grimoire_guardian/app.py
```

This will:

- Start a local web server (usually at `http://localhost:8501`)
- Automatically index the Harry Potter book
- Provide a chat interface for asking questions

#### 📟 Command Line Interface

Run a quick query from the terminal:

```bash
uv run grimoire-guardian
```

This runs the default example query: _"What happened to Harry's parents?"_

#### 🐍 Python API

Use the Grimoire Guardian programmatically:

```python
from grimoire_guardian import create_index, graph

# Create document index
idx = create_index("your-document.pdf")

# Create the AI agent graph
g = graph(idx)

# Ask questions
result = g.invoke({"query": "Your question here"})
print(result)
```

## 🛠️ Technical Architecture

### Components

```
Document → Chunking → Vector Embeddings → FAISS Index
                                              ↓
User Query → LangGraph Agent → Search Tool → LLM Response
```

### Key Technologies

- **🔍 Vector Search**: FAISS with sentence-transformers embeddings
- **🤖 Language Model**: Databricks OpenAI GPT-4o
- **🧠 Agent Framework**: LangGraph for workflow orchestration
- **📄 Document Processing**: Unstructured for PDF parsing
- **🎨 Web Interface**: Streamlit for interactive UI

### Agent Workflow

1. **System Prompt**: Initializes the mystical archivist persona
2. **Query Processing**: Analyzes user questions
3. **Document Search**: Retrieves relevant text chunks using semantic similarity
4. **Answer Generation**: Synthesizes responses based on found information
5. **Tool Integration**: Seamlessly combines search results with AI reasoning

## 📁 Project Structure

```
grimoire-guardian/
├── src/grimoire_guardian/
│   ├── __init__.py          # Core logic and agent setup
│   ├── app.py              # Streamlit web interface
│   └── sysprompt.txt       # System prompt for the agent
├── harry-potter-and-the-sorcerers-stone.pdf  # Example document
├── grimoire-guardian.jpg   # Project logo
├── pyproject.toml         # Project configuration
├── uv.lock               # Dependency lock file
└── README.md            # This file
```

## 🔧 Configuration

### Model Settings

Edit the constants in `__init__.py` to customize:

```python
MODEL = "data-science-gpt-4o"  # Databricks model name
MODEL_EMB = "sentence-transformers/all-MiniLM-L6-v2"  # Embedding model
DOC = "your-document.pdf"  # Document to index
```

### System Prompt

Customize the agent's personality by editing `sysprompt.txt`:

```
You are the Grimoire Guardian, an ancient and mystical archivist...
```

### Search Parameters

Adjust search behavior in the `search_index` function:

```python
def search_index(idx, q: str, topk: int = 50):  # Number of chunks to retrieve
```

## 📖 Example Queries

Try asking the Grimoire Guardian questions like:

- _"What happened to Harry's parents?"_
- _"Who is Professor McGonagall?"_
- _"Describe the Sorting Hat ceremony"_
- _"What is Quidditch?"_
- _"Tell me about Hagrid"_

## 🔧 Development

### Adding New Documents

1. Place your PDF in the project directory
2. Update the `DOC` constant in `__init__.py`
3. Restart the application to reindex

### Extending Functionality

The LangGraph architecture makes it easy to add new capabilities:

1. **Add new tools** to the agent for different data sources
2. **Modify the workflow** by editing the graph structure
3. **Enhance search** with different embedding models or retrieval strategies

### Custom Embeddings

To use different embedding models:

```python
embedder = HuggingFaceEmbeddings(
    model_name="your-preferred-model",
    model_kwargs={"torch_dtype": torch.float16},
    encode_kwargs={"normalize_embeddings": True}
)
```

## 🚨 Troubleshooting

### Common Issues

**Document indexing fails:**

- Ensure PDF is not password-protected
- Check file permissions and path
- Verify unstructured package is properly installed

**Databricks authentication errors:**

- Verify environment variables are set correctly
- Check workspace access permissions
- Ensure model serving endpoint is accessible

**Out of memory errors:**

- Reduce batch size in embedding configuration
- Use CPU instead of GPU for embeddings
- Process smaller document chunks

**Streamlit app not loading:**

- Check if port 8501 is available
- Verify all dependencies are installed
- Clear Streamlit cache: `streamlit cache clear`

### Performance Tips

- **Faster indexing**: Use GPU acceleration if available
- **Reduce memory usage**: Lower embedding batch size
- **Better search**: Increase `topk` parameter for more comprehensive results
- **Faster responses**: Use smaller embedding models

### Development Setup

```bash
# Install with development dependencies
uv sync --group dev

# Run the application
uv run streamlit run src/grimoire_guardian/app.py

# Test with different documents
uv run grimoire-guardian
```

---

_Seek knowledge, and the Grimoire Guardian shall reveal the secrets hidden within the ancient scrolls..._ ✨

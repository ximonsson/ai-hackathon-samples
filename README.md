# 🚀 AI Hackathon Samples

A collection of AI agent examples showcasing different approaches to building intelligent applications for the AI Agent Hackathon. These samples demonstrate various frameworks, use cases, and integration patterns to inspire your own AI agent projects.

## 🎯 Overview

This repository contains three distinct AI agent examples, each highlighting different technologies and use cases:

1. **🌦️ Stormy McWeatherface** - Weather forecasting agent with location intelligence
2. **📚 Grimoire Guardian** - Document Q&A assistant with RAG capabilities  
3. **🫠 Git Happens** - GitHub repository management through natural language

Each project is designed to be a starting point for hackathon participants, showcasing best practices for AI agent development, integration patterns, and user interface design.

## 🤖 Project Examples

### 🌦️ Stormy McWeatherface
> *An AI-powered weather assistant with intelligent location lookup*

<img src="./stormy-mcweatherface/7ebbb3e9-ed6e-4a66-a13d-f8a00ced3b8c.jpg" alt="Stormy McWeatherface" width="300">

**Key Technologies:**
- MLflow ResponsesAgent with Databricks model serving
- Nominatim API for geocoding
- Met.no API for weather data
- Gradio web interface + CLI

**What You'll Learn:**
- Building conversational agents with tool calling
- API integration and data processing
- Multiple interface patterns (CLI + Web)
- MLflow agent deployment

**Perfect For:** Location-based services, API integration, conversational interfaces

[→ Explore Stormy McWeatherface](./stormy-mcweatherface/)

---

### 📚 Grimoire Guardian
> *Ancient document archivist powered by modern RAG technology*

<img src="./grimoire-guardian/grimoire-guardian.jpg" alt="Grimoire Guardian" width="300">

**Key Technologies:**
- LangGraph for agent workflows
- FAISS vector search with HuggingFace embeddings
- Unstructured for document processing
- Streamlit interface with mystical personality

**What You'll Learn:**
- Retrieval-Augmented Generation (RAG) implementation
- Vector embeddings and semantic search
- Document processing and chunking strategies
- LangGraph agent orchestration

**Perfect For:** Document analysis, knowledge bases, research assistance

[→ Explore Grimoire Guardian](./grimoire-guardian/)

---

### 🫠 Git Happens
> *GitHub assistant that makes repository management conversational*

<img src="./git-happens/e35c80d6-28a3-4c71-83dd-5d197bf1dc83.jpg" alt="Git Happens" width="300">

**Key Technologies:**
- Smolagents framework
- Model Control Protocol (MCP)
- Docker containerization
- GitHub API integration

**What You'll Learn:**
- Modern agent frameworks (Smolagents)
- MCP protocol for tool integration
- Containerized service architecture
- GitHub API automation

**Perfect For:** DevOps automation, project management, API orchestration

[→ Explore Git Happens](./git-happens/)

## 🛠️ Common Technologies

All projects share these foundational technologies:

- **🏗️ Databricks**: Model serving and AI infrastructure
- **🐍 Python 3.11+**: Modern Python development
- **📦 uv**: Fast, reliable Python package management
- **🎨 Web Interfaces**: Gradio/Streamlit for user interaction
- **🔧 Agent Frameworks**: Various approaches to AI agent architecture

## 🚀 Getting Started

### Prerequisites

Before diving into any project, ensure you have:

- Python 3.11 or higher
- [uv package manager](https://docs.astral.sh/uv/)
- Databricks workspace access
- Docker (for Git Happens)

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-hackathon-samples
   ```

2. **Choose your starting point:**
   ```bash
   cd stormy-mcweatherface  # Weather agent
   cd grimoire-guardian     # Document Q&A
   cd git-happens          # GitHub assistant
   ```

3. **Follow individual project READMEs** for specific setup instructions

### Environment Setup

All projects require Databricks authentication:

```bash
export DATABRICKS_HOST=<your-databricks-host>
export DATABRICKS_TOKEN=<your-databricks-token>
```

Additional requirements vary by project (GitHub tokens, etc.).

## 🎓 Learning Paths

### For Beginners
**Start with:** 🌦️ **Stormy McWeatherface**
- Simple API integrations
- Clear tool calling patterns
- Multiple interface options
- Well-documented workflows

### For Document AI Enthusiasts
**Start with:** 📚 **Grimoire Guardian**
- Advanced RAG implementation
- Vector search fundamentals
- Document processing pipelines
- LangGraph orchestration

### For DevOps/Integration Focused
**Start with:** 🫠 **Git Happens**
- Modern agent frameworks
- MCP protocol exploration
- Container orchestration
- API automation patterns

## 💡 Hackathon Ideas

Use these examples as inspiration for your own projects:

### Extending the Examples
- **Stormy+**: Add weather alerts, historical data, or climate analysis
- **Grimoire+**: Multi-document support, advanced filters, or domain-specific knowledge
- **Git+**: Add CI/CD integration, code analysis, or team analytics


## 🏗️ Architecture Patterns

### Tool-Calling Agents
- **Example**: Stormy McWeatherface
- **Pattern**: LLM + defined tools + structured responses
- **Best For**: API integrations, clear task boundaries

### RAG Agents
- **Example**: Grimoire Guardian
- **Pattern**: Vector search + context injection + generation
- **Best For**: Knowledge bases, document analysis

### Workflow Agents
- **Example**: Git Happens (MCP pattern)
- **Pattern**: Multi-step processes + external services
- **Best For**: Complex automations, enterprise integrations

## 🔧 Development Tips

### Best Practices
- **Start Simple**: Begin with basic functionality, then add complexity
- **Test Early**: Validate APIs and integrations before building full workflows
- **User Experience**: Focus on intuitive interfaces and clear error handling
- **Documentation**: Keep track of what works and what doesn't

### Common Patterns
- **Environment Management**: Use `.env` files for local development
- **Error Handling**: Graceful failures with helpful error messages
- **Logging**: Track agent decisions and API calls
- **Testing**: Validate tool functions independently

### Resource Management
- **API Limits**: Implement rate limiting and caching
- **Memory Usage**: Optimize vector operations and document processing
- **Response Times**: Balance accuracy with speed


## 📚 Additional Resources

### Learning Materials
- [Databricks ML Documentation](https://docs.databricks.com/machine-learning/)
- [LangChain Documentation](https://python.langchain.com/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Ready to build amazing AI agents? Pick your starting point and let's get hacking!** 🚀✨

*Remember: The best agent is the one that solves a real problem for real people.*

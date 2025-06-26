# 🫠 Git Happens!

An AI-powered GitHub assistant that helps you manage repositories, issues, pull requests, and more through natural language commands. Sometimes things don't go as planned... but that's where Git Happens comes in!

![](./e35c80d6-28a3-4c71-83dd-5d197bf1dc83.jpg)

## 🎯 About

Git Happens is a conversational AI agent that connects to GitHub through the Model Control Protocol (MCP) to provide a natural language interface for repository management. Whether you're creating issues, managing pull requests, or exploring repository data, this assistant makes GitHub operations more intuitive and accessible.

## ✨ Features

- **🤖 Conversational GitHub Interface**: Chat with your repositories using natural language
- **🔧 Repository Management**: Create, update, and manage repositories
- **🐛 Issue Tracking**: Create, assign, and track issues effortlessly  
- **🔀 Pull Request Workflow**: Manage PRs, reviews, and merges
- **📊 Repository Analytics**: Get insights about commits, contributors, and activity
- **🎨 Gradio Web Interface**: User-friendly web UI for interactions
- **🐳 Docker Integration**: Uses GitHub MCP server in a containerized environment
- **🔗 MCP Protocol**: Modern tool integration using Model Control Protocol

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (for GitHub MCP server)
- Databricks workspace access
- GitHub Personal Access Token

### Installation

1. **Navigate to the project:**
   ```bash
   cd git-happens
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up authentication:**
   ```bash
   # Databricks credentials
   export DATABRICKS_HOST=<your-databricks-host>
   export DATABRICKS_TOKEN=<your-databricks-token>
   
   # GitHub Personal Access Token
   export GITHUB_PERSONAL_ACCESS_TOKEN=<your-github-token>
   ```

4. **Ensure Docker is running:**
   ```bash
   docker --version  # Verify Docker is installed and running
   ```

### Usage

#### 🖥️ Web Interface

Launch the Gradio web application:

```bash
uv run git-happens
```

This will:
- Start the GitHub MCP server in a Docker container
- Initialize the Smolagents AI agent
- Launch a web interface (usually at `http://127.0.0.1:7860`)
- Provide file upload capabilities for repository operations

#### 💬 Example Conversations

Try asking Git Happens questions like:

- *"Show me the latest issues in my repository"*
- *"Create a new issue for fixing the login bug"*
- *"List all open pull requests"*
- *"What commits were made this week?"*
- *"Create a new repository called 'my-awesome-project'"*
- *"Assign issue #123 to john-doe"*

## 🛠️ Technical Architecture

### Components

```
User Input → Gradio UI → Smolagents Agent → MCP Protocol → GitHub API
                              ↓                    ↓
                         Databricks LLM    Docker Container
```

### Key Technologies

- **🤖 Smolagents**: Modern agent framework for tool integration
- **🔗 MCP (Model Control Protocol)**: Standardized tool communication
- **🐳 Docker**: Containerized GitHub MCP server
- **🎨 Gradio**: Interactive web interface
- **🏗️ Databricks**: AI model serving platform
- **📡 GitHub API**: Repository and project management

### Agent Workflow

1. **User Input**: Natural language commands through web interface
2. **Intent Analysis**: AI agent processes and understands the request
3. **Tool Selection**: Determines appropriate GitHub operations
4. **MCP Communication**: Sends structured commands to GitHub MCP server
5. **API Execution**: Docker container executes GitHub API calls
6. **Response Processing**: Results are formatted and returned to user

## 📁 Project Structure

```
git-happens/
├── src/git_happens/
│   └── __init__.py              # Main agent and UI setup
├── e35c80d6-28a3-4c71-83dd-5d197bf1dc83.jpg  # Project logo
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependency lock file
└── README.md                  # This file
```

## 🔧 Configuration

### Model Settings

The agent uses Databricks model serving. Configure in `__init__.py`:

```python
MODEL = "data-science-gpt-4o"  # Databricks model name
```

### GitHub MCP Server

The Docker container runs the official GitHub MCP server:

```python
params = mcp.StdioServerParameters(
    command="docker",
    args=[
        "run", "-i", "--rm", "-e",
        f"GITHUB_PERSONAL_ACCESS_TOKEN={os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']}",
        "ghcr.io/github/github-mcp-server",
    ],
)
```

### Authentication

Required environment variables:

- `DATABRICKS_HOST`: Your Databricks workspace URL
- `DATABRICKS_TOKEN`: Databricks access token
- `GITHUB_PERSONAL_ACCESS_TOKEN`: GitHub token with appropriate permissions

## 🔑 GitHub Token Permissions

Your GitHub Personal Access Token should include:

- **Repository access**: `repo` (for private repos) or `public_repo` (for public only)
- **Issue management**: `repo` scope covers this
- **Pull request management**: `repo` scope covers this
- **Organization access**: `read:org` (if working with org repositories)

## 💡 Usage Examples

### Repository Management

```
User: "Create a new repository called 'awesome-project' with a description"
Agent: Creates repository with specified name and description

User: "List all my repositories"
Agent: Shows all repositories with details like stars, forks, and activity
```

### Issue Management

```
User: "Create an issue about fixing the authentication bug"
Agent: Creates new issue with title and description

User: "Show me all open issues assigned to me"
Agent: Lists issues with filtering and details
```

### Pull Request Workflow

```
User: "Show me open pull requests that need review"
Agent: Lists PRs awaiting review with status information

User: "Merge pull request #42"
Agent: Merges the specified PR (with safety checks)
```

## 🚨 Troubleshooting

### Common Issues

**Docker not found:**
```bash
# Install Docker Desktop or Docker Engine
# Verify installation:
docker --version
```

**GitHub authentication failed:**
```bash
# Check token is set and valid:
echo $GITHUB_PERSONAL_ACCESS_TOKEN
# Verify token permissions on GitHub.com
```

**MCP server connection issues:**
```bash
# Ensure Docker can pull the image:
docker pull ghcr.io/github/github-mcp-server
```

**Databricks authentication errors:**
```bash
# Verify environment variables:
echo $DATABRICKS_HOST
echo $DATABRICKS_TOKEN
```

**Web interface not loading:**
- Check if port 7860 is available
- Verify all dependencies are installed with `uv sync`
- Check terminal for error messages

### Performance Tips

- **Faster responses**: Use specific repository names in queries
- **Better results**: Be explicit about what you want to accomplish
- **Efficient operations**: Batch related GitHub operations when possible

## 🔒 Security Considerations

- **Token Security**: Never commit GitHub tokens to version control
- **Permissions**: Use tokens with minimal required permissions
- **Docker Security**: The MCP server runs in an isolated container
- **Network Access**: Ensure proper firewall configuration for Docker

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Test with your GitHub repositories (use test repos!)
4. Submit a pull request

### Development Setup

```bash
# Install with development dependencies
uv sync --group dev

# Run the application
uv run git-happens

# Test with different GitHub operations
```

## 📚 Related Projects

- **Smolagents**: [Agent framework](https://github.com/huggingfaceh4/smolagents)
- **MCP Protocol**: [Model Control Protocol](https://modelcontextprotocol.io/)
- **GitHub MCP Server**: [Official GitHub MCP implementation](https://github.com/github/github-mcp-server)

## 📄 License

This project is licensed under the MIT License.

## 🚀 Future Enhancements

- **GitHub Actions**: Trigger and monitor workflows
- **Advanced Analytics**: Repository insights and metrics
- **Team Management**: Organization and team operations
- **Code Analysis**: AI-powered code review suggestions
- **Integration Webhooks**: Real-time repository event handling
- **Multi-Repository Operations**: Bulk operations across repositories

---

*When Git happens, make it happen better with AI! 🤖✨*

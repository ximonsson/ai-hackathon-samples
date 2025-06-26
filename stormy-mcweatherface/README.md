# 🌦️ Stormy McWeatherface

An AI-powered weather assistant that helps you get weather information for any location using intelligent location lookup and real-time weather forecasting.

![](7ebbb3e9-ed6e-4a66-a13d-f8a00ced3b8c.jpg)

## 🚀 Features

- **🤖 AI-Powered Agent**: Uses MLflow ResponsesAgent with Databricks model serving
- **📍 Smart Location Lookup**: Converts location names/addresses to GPS coordinates using Nominatim API
- **🌡️ Real-time Weather**: Fetches current weather data from the Met.no API
- **💬 Conversational Interface**: Natural language responses with activity suggestions
- **🖥️ Multiple Interfaces**: Command line tool and web interface

## 📦 Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Databricks workspace access
- OpenAI API access through Databricks

### Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd stormy-mcweatherface
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Configure Databricks authentication:**
   ```bash
   # Set up your Databricks credentials
   export DATABRICKS_HOST=<your-databricks-host>
   export DATABRICKS_TOKEN=<your-databricks-token>
   ```

## 🎯 Usage

Stormy McWeatherface can be used in two ways: through the command line or via a web interface.

### 📟 Command Line Interface

The command line tool allows you to quickly get weather information from your terminal.

#### Basic Usage

```bash
# Use default location (Biskop Gunnerus gate 14)
uv run stormy-mcweatherface

# Specify a custom location
uv run stormy-mcweatherface "Oslo, Norway"

# Multiple word locations (automatically joined)
uv run stormy-mcweatherface Oslo Norway

# Specific addresses
uv run stormy-mcweatherface "Youngstorget 3, Oslo"
```

### 🌐 Web Interface (Gradio App)

The web interface provides a user-friendly GUI with additional features like progress tracking and request cancellation.

#### Launch the Web App

```bash
# Start the Gradio web interface
uv run stormy-gradio
```

This will:

- Start a local web server (usually at `http://127.0.0.1:7860`)
- Provide a shareable public link
- Open your default browser automatically

#### Web Interface Features

- **📍 Location Input**: Text field for entering any location
- **🔍 Submit Button**: Process weather requests
- **📊 Progress Tracking**: Visual progress with status updates
- **🎯 Example Buttons**: Quick-select common locations
- **⌨️ Keyboard Support**: Press Enter to submit

## 🛠️ Technical Details

### Architecture

```
User Input → Location Geocoding → Weather API → AI Response Generation
     ↓              ↓                  ↓              ↓
  Location     GPS Coords        Weather Data    Formatted Response
```

### APIs Used

- **Nominatim API**: For geocoding location names to GPS coordinates
- **Met.no API**: For fetching weather forecast data
- **Databricks OpenAI**: For generating conversational responses

### Agent Tools

The AI agent has access to two main tools:

1. **`get_geocode_location`**: Converts location names to GPS coordinates
2. **`get_weather`**: Fetches weather data for given coordinates

## 🔧 Development

### Project Structure

```
stormy-mcweatherface/
├── src/stormy_mcweatherface/
│   ├── __init__.py          # Main CLI entry point
│   ├── stormy.py            # Agent creation and core logic
│   └── gradio_app.py        # Web interface
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
└── README.md               # This file
```

### Adding New Features

The agent architecture makes it easy to add new tools:

1. Define your tool function in `stormy.py`
2. Add it to the `tools` list with proper OpenAI function spec
3. Update the system prompt to describe how to use the new tool

## 🆘 Troubleshooting

### Common Issues

**"Module not found" errors:**

```bash
uv sync  # Reinstall dependencies
```

**Databricks authentication issues:**

```bash
# Check your environment variables
echo $DATABRICKS_HOST
echo $DATABRICKS_TOKEN
```

**Web interface not loading:**

- Check if port 7860 is available
- Try accessing `http://127.0.0.1:7860` directly
- Check firewall settings

**Timeout errors:**

- Use the cancel button in web interface
- Try simpler location names
- Check your internet connection

### Getting Help

If you encounter issues:

1. Check the error messages in the terminal
2. Verify your Databricks and API configurations
3. Try with simpler location names first
4. Check the project issues on GitHub

---

_Made with ❤️ for better weather forecasting_

# Currency Exchange Service

A currency exchange service that provides real-time exchange rates and lists supported currencies.

## Features

- Get current exchange rates between any two supported currencies
- List all supported currencies
- Docker support for easy deployment
- SSE (Server-Sent Events) based communication

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- Git
- Exchange Rate API key (get it from https://www.exchangerate-api.com/)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file as instructed in `.env.example` in the project root:
```bash
# Get your API key from https://www.exchangerate-api.com/
- `EXCHANGE_RATE_API_KEY`: Your Exchange Rate API key
- `GROQ_API_KEY`: Your GROQ API key
```

3. Build and start the Docker container:
```bash
docker compose up -d
```

### Using Python directly

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file in the project root:
```bash
# Get your API key from https://www.exchangerate-api.com/
EXCHANGE_RATE_API_KEY=your_api_key_here
```

3. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r mcpserver/requirements.txt
```

## Usage

### Using the Python Client

Run the client script to interact with the service:
```bash
python mcpserver/client-sse.py
```

This will:
- List all available tools
- Show an example exchange rate (INR to USD)
- Display a list of supported currencies

## API Documentation

The service provides two main tools:

1. `get_exchange_rate(from_currency, to_currency)`
   - Returns the current exchange rate between two currencies
   - Example: Get USD to EUR rate

2. `list_supported_currencies()`
   - Returns a list of all supported currencies
   - Includes currency codes and names

## Development

To modify the service:

1. Make changes to `mcpserver/server.py`
2. Test using the client script
3. Rebuild the Docker container if using Docker:
```bash
docker compose build --no-cache
docker compose up -d
```

## Getting an API Key

1. Visit https://www.exchangerate-api.com/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file as shown in the installation steps


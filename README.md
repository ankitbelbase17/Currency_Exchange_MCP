# Currency_Exchange_MCP

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

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Build and start the Docker container:
```bash
docker compose up -d
```

### Using Python directly

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
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

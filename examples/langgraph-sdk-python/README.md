# Infobip MCP LangGraph SDK Demo

This demo application showcases the integration of Infobip's MCP Server with [LangGraph SDK](https://langchain-ai.github.io/langgraph/) to build a conversational AI agent. The application demonstrates the capabilities of the Infobip SMS MCP server and can be easily adapted to work with other Infobip MCP servers.

## Setup and Installation (Linux/MacOS)
### 1. Set up uv and virtual environment

```bash
uv venv
source .venv/bin/activate
```

**Note:** For more information about `uv` and platform-specific instructions, visit the [uv documentation](https://docs.astral.sh/uv/).

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file based on the provided `.env.example` and configure the following required environment variables:

- `AWS_REGION` - AWS region to use (e.g., `us-east-1`)
- `AWS_ACCESS_KEY` - Your AWS access key
- `AWS_SECRET_KEY` - Your AWS secret key
- `AWS_MODEL_ID` - The model ID to use. You can use the [Supported models and model features](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-supported-models-features.html)
- `INFOBIP_API_KEY` - Your Infobip [API key](https://www.infobip.com/docs/essentials/api-essentials/api-authentication#api-key-header) (see [Scopes](#scopes) section below for details)

### 4. Run the application

```bash
uv run main.py
```

## Scopes

To successfully run the demo, you need the correct [scopes](https://www.infobip.com/docs/essentials/api-essentials/api-authorization#api-scopes) assigned to your Infobip API key.

To use the Infobip SMS MCP server to its full capacity, ensure you have the `sms:manage` scope assigned.

The scopes for a particular MCP server can be found under `scopes_supported` in the authorization server metadata at:

```
{mcp-server-url}/.well-known/oauth-authorization-server
```

For example, the scopes for the Infobip SMS MCP server are available at:
https://mcp.infobip.com/sms/.well-known/oauth-authorization-server

## Usage

### Interacting with the Agent

You can interact with the agent through the command line interface (CLI).

Enjoy the conversation!

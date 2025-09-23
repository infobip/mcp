# Infobip MCP OpenAI agents SDK Demo

This demo application showcases the integration of Infobip's MCP Server with [OpenAI agents](https://github.com/openai/openai-agents-js) to build a conversational AI agent. The application demonstrates the capabilities of the Infobip SMS MCP server and can be easily adapted to work with other Infobip MCP servers.

## Setup and Installation (Linux/MacOS)

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment variables

Create a `.env` file based on the provided `.env.example` and configure the following required environment variables:

- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- `AZURE_OPENAI_API_VERSION` - Azure OpenAI API version (e.g., "2025-03-01-preview")
- `AZURE_OPENAI_MODEL_NAME` - Your Azure OpenAI model name (e.g., "gpt-4o")
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key
- `INFOBIP_API_KEY` - Your Infobip [API key](https://www.infobip.com/docs/essentials/api-essentials/api-authentication#api-key-header) (see [Scopes](#scopes) section below for details)

### 3. Run the application

```bash
node --env-file=.env index.js
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

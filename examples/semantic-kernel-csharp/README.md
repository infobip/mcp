# Infobip MCP Semantic Kernel Demo (C#)

This demo application showcases the integration of Infobip's MCP Server with [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/overview/) to build a conversational AI agent. The application demonstrates the capabilities of the Infobip SMS MCP server using C# and .NET 9.0, and can be easily adapted to work with other Infobip MCP servers.

## Prerequisites

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later
- Visual Studio Code or Visual Studio (recommended)
- An Infobip account with SMS API access
- An Azure OpenAI account

## Setup and Installation

### 1. Configure environment variables

Create a `.env` file in the root directory based on provided `.env.example` file.

**Environment Variable Descriptions:**
- `AzureOpenAIBaseUrl` - Your Azure OpenAI endpoint URL
- `AzureOpenAIApiKey` - Your Azure OpenAI API key
- `AzureDeploymentName` - Your Azure OpenAI model deployment name (e.g., "gpt-4o")
- `ApiKey` - Your Infobip [API key](https://www.infobip.com/docs/essentials/api-essentials/api-authentication#api-key-header) (see [Scopes](#scopes) section below for details)
- `ApiBaseUrl` - The Infobip MCP server endpoint for SMS

### 2. Run the application

```bash
dotnet run
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
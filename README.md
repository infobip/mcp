# Infobip MCP Servers

<img src="https://cdn-web.infobip.com/uploads/2025/05/infobip-logo-horizontal-orange.png" alt="Infobip Logo" height="48" style="display:inline;vertical-align:middle;">

[Infobip MCP Servers](https://www.infobip.com/docs/mcp?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp) let you build AI agents to interact with the Infobip platform through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs).
Connect to Infobip and enable your agents to perform actions, such as sending messages over channels like SMS, WhatsApp, or Viber, or managing customer data in a controlled, production-grade environment.

No more complex integrations or digging through endless documentation. Just plug in and let your AI do the talking.


## 🛠️ Features

- ✉️ Send messages using channels like SMS, WhatsApp, Viber, or RCS (more coming soon)
- 📱 Set up and run 2FA flows
- 🧑‍💼 Store & activate your customer information
- 👤 Manage Infobip user accounts

## 🌐 Available Remote MCP Servers

Infobip remote MCP servers support [streamable HTTP transport](https://modelcontextprotocol.io/docs/learn/architecture#transport-layer).
Below is a list of available remote MCP servers.

**Base URL:** `https://mcp.infobip.com`

| Server                               | Endpoint                                     |
|--------------------------------------|----------------------------------------------|
| **SMS**                              | `https://mcp.infobip.com/sms`                |
| **WhatsApp**                         | `https://mcp.infobip.com/whatsapp`           |
| **Viber**                            | `https://mcp.infobip.com/viber`              |
| **RCS**                              | `https://mcp.infobip.com/rcs`                |
| **2FA**                              | `https://mcp.infobip.com/2fa`                |
| **People**                           | `https://mcp.infobip.com/people`             |
| **Account Management**               | `https://mcp.infobip.com/account-management` |
| **CPaaSX Applications and Entities** | `https://mcp.infobip.com/application-entity` |
| **Infobip Documentation**            | `https://mcp.infobip.com/search`             |

For more details on supported endpoints, see the [Infobip MCP documentation](https://www.infobip.com/docs/mcp?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp).

Examples of using Infobip MCP servers with different frameworks can be found in the [examples](./examples) directory.

> If you need SSE transport support, append `/sse` to the endpoint URL (e.g., `https://mcp.infobip.com/sms/sse`).

### Using an HTTP Transport Option

Use the `HTTP` transport method to connect directly to an Infobip MCP Server:

```json
{
 "mcpServers": {
   "ib-sms": {
     "type": "http",
     "url": "https://mcp.infobip.com/sms",
     "headers": {
       "Authorization": "App ${INFOBIP_API_KEY}"
     }
   }
 }
}
```

### Using a STDIO Transport Bridge

If your agent does not support remote MCP servers, you can use a bridge like [mcp-remote](https://github.com/geelen/mcp-remote).

```json
{
  "mcpServers": {
    "infobip-sms": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.infobip.com/sms",
        "--header",
        "Authorization: App ${INFOBIP_API_KEY}"
      ],
      "env": {
        "INFOBIP_API_KEY": "<Your Infobip API Key here>"
      }
    }
  }
}
```

## 🔐 Authentication and Authorization

To use Infobip MCP servers, you need an Infobip account.
If you don't have one, [create an Infobip account with a free trial](https://infobip.com/signup?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp).

### Using an API Key

If your MCP client supports adding additional headers through configuration or environment variables, you can use your [Infobip API key](https://www.infobip.com/docs/essentials/api-essentials/api-authentication?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp#api-key-header) and provide it in the `Authorization` header using the following format: `App ${INFOBIP_API_KEY}`.
See the `mcp-remote` [example](#using-a-stdio-transport-bridge) above for setup details.

### Using OAuth 2.1

Infobip MCP servers support OAuth 2.1 authentication.
To use OAuth 2.1, your MCP client must support OAuth 2.1 authentication and dynamic OAuth authorization server [metadata discovery](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#server-metadata-discovery).
To start the OAuth flow, configure your MCP client to connect to the Infobip MCP server without providing authentication credentials.
Your MCP client should initiate the OAuth flow automatically, redirecting you to the Infobip OAuth server for authentication.

#### Discovering Supported Scopes

Some MCP clients may not support automatic `scopes_supported` discovery.
In this case, you must manually configure the scopes in your MCP client configuration.
The scopes for a particular MCP server can be found in the authorization server metadata at `{server-url}/.well-known/oauth-authorization-server`.

For example, for the Infobip SMS MCP server, the scopes are available at:
https://mcp.infobip.com/sms/.well-known/oauth-authorization-server

Example configuration for Claude Desktop:

```json
{
  "mcpServers": {
    "infobip-sms": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.infobip.com/sms",
        "--debug",
        "--static-oauth-client-metadata",
        "{\"scope\":\"sms:manage profile\"}"
      ]
    }
  }
}
```

## Agent Permission and Access Control

Effective AI agent governance requires implementing granular permission controls, especially for high-impact operations like message sending. Unrestricted access privileges pose substantial security vulnerabilities and operational hazards that can compromise system integrity and user trust.

Make sure to follow official [MCP implementation guidelines](https://modelcontextprotocol.io/specification/draft/server/prompts#implementation-considerations).

## 🛠️ Troubleshooting

**Authentication and Authorization Issues**
- Ensure you have a valid Infobip account and an [API key with a correct scope](https://www.infobip.com/docs/essentials/api-essentials/api-authentication?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp#api-scopes-on-basic-auth-basic).
- If using OAuth 2.1, verify your MCP client supports dynamic metadata discovery.
- Confirm that required scopes are correctly configured in your MCP client.

**Message Delivery Issues**
- Make sure the recipient phone number is valid and reachable.

**Other Issues**
- For HTTP status codes and error details, see the [troubleshooting guide](https://www.infobip.com/docs/essentials/api-essentials/response-status-and-error-codes?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp#http-status-codes).

## 🤝 Contributing

If you have suggestions for improvements, please contact [devrel@infobip.com](mailto:devrel@infobip.com).

## 📄 License

This document is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

**Happy building with Infobip MCP! 🚀**

# Infobip MCP Servers

<img src="https://cdn-web.infobip.com/uploads/2025/05/infobip-logo-horizontal-orange.png" alt="Infobip Logo" height="48" style="display:inline;vertical-align:middle;">

[Infobip MCP Servers](https://www.infobip.com/docs/mcp?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp) let you build AI agents to interact with the Infobip platform through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs).
Connect to Infobip and enable your agents to perform actions, such as sending messages over channels like SMS, WhatsApp, or Viber, or managing customer data in a controlled, production-grade environment.

No more complex integrations or digging through endless documentation. Just plug in and let your AI do the talking.

## 🛠️ Features

- ✉️ Send messages using channels like SMS, WhatsApp, RCS, Viber, Voice, Mobile push
- 📱 Set up and run 2FA flows
- 📱 Use Telco network capabilities to improve authentication methods and enhance the security of online transactions
- 👤 Store & activate your customer information
- 👤 Manage Infobip user accounts
- 👤 Orchestrate multi-tenant workflows with CPaaS X
- 🔍 Explore Infobip documentation
- 🔍 Let deep research models search and retrieve Infobip documentation as a data source

## 📋 Prerequisites

- [Infobip account](https://infobip.com/signup?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp) - free trial available
- AI agent or application with MCP client support
---  
  ### Table of Contents
  - [🌐 Available Remote MCP Servers](#-available-remote-mcp-servers)
  - [🔌 HTTP Transport](#-http-transport)
  - [🔐 Authentication and Authorization](#-authentication-and-authorization)
    - [Using OAuth 2.1](#using-oauth-21)
    - [Using an API Key](#using-an-api-key)
  - [🤖 Agent Permission and Access Control](#-agent-permission-and-access-control)
  - [🛠️ Troubleshooting](#️-troubleshooting)
  - [🚀 Infobip MCP Servers in Use](#-infobip-mcp-servers-in-use)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
---

## 🌐 Available Remote MCP Servers

Infobip remote MCP servers support [streamable HTTP transport](https://modelcontextprotocol.io/docs/learn/architecture#transport-layer).
Below is a list of available remote MCP servers.

**Base URL:** `https://mcp.infobip.com`

### ✉️ Messaging channels

| Server | Endpoint | Features |
|---|---|---|
| **SMS** | `https://mcp.infobip.com/sms` | Send and preview messages, schedule and reschedule, bulk sending, multilingual support (transliteration, character sets), delivery reports, message logs, URL tracking |
| **WhatsApp** | `https://mcp.infobip.com/whatsapp` | Send template messages, send text/media (text, document, image, audio, video, sticker), send location/contact messages, template management (create, edit, delete, retrieve), delivery reports, message logs, SMS failover |
| **WhatsApp Flow** | `https://mcp.infobip.com/whatsapp-flow` | Create and manage static/dynamic flows, generate flow structure, manage flow JSON, send interactive flows, preview flows, add and manage interactive components (forms, buttons, checkboxes) |
| **Viber** | `https://mcp.infobip.com/viber` | Send messages with rich media (images, videos, files, URLs), delivery reports, message logs, scheduling, SMS failover, URL tracking |
| **RCS** | `https://mcp.infobip.com/rcs` | Send rich messages (multimedia, suggested replies, carousels, barcodes), delivery reports, message logs, capability check, SMS/MMS failover |
| **Voice** | `https://mcp.infobip.com/voice` | Single and multi-recipient voice calls, text-to-speech, pre-recorded audio, call management, conference calls, voice list management, delivery reports, call logs |
| **Mobile App Messaging** | `https://mcp.infobip.com/mobile-app-messaging` | Send push notifications, delivery reports, message logs, push statistics, push application management, inbox message management |

### 📱 Authentication and verification

| Server | Endpoint | Features |
|---|---|---|
| **2FA** | `https://mcp.infobip.com/2fa` | Application management, message templates (SMS/Email), send PIN (SMS/Voice/Email), resend and verify PIN, PIN verification status |
| **CAMARA** | `https://mcp.infobip.com/camara` | Number verification authorization, verify number, device location verification, SIM swap check, SIM swap date retrieval, KYC match |

### 👤 Customer data and platform management

| Server | Endpoint | Features |
|---|---|---|
| **People** | `https://mcp.infobip.com/people` | Manage Person profiles, add and manage company profiles, tags, custom attributes and lists, track and export events, audience segmentation |
| **Account Management** | `https://mcp.infobip.com/account-management` | Account balance, free messages count, total balance, manage and update account details, audit logs |
| **CPaaSX Applications and Entities** | `https://mcp.infobip.com/application-entity` | Create and manage applications and entities, resource associations, inbound message configuration, list resources, coverage lookup, resource request submission and tracking |

### 🔍 Developer resources

| Server | Endpoint | Features |
|---|---|---|
| **Infobip Documentation** | `https://mcp.infobip.com/search` | Documentation search, API reference, use cases, product guides |
| **Infobip Deep Research** | `https://mcp.infobip.com/deep-research` | Deep search across API documentation, fetch detailed content |

For more details on supported endpoints, see the [Infobip MCP documentation](https://www.infobip.com/docs/mcp?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp).

Examples of using Infobip MCP servers with different frameworks can be found in the [examples](./examples) directory.

> If you need SSE transport support, append `/sse` to the endpoint URL (e.g., `https://mcp.infobip.com/sms/sse`).

## 🔌 HTTP Transport

Infobip MCP servers support [streamable HTTP transport](https://modelcontextprotocol.io/docs/learn/architecture#transport-layer). Connect your MCP client directly to any Infobip MCP server endpoint:

```json
{
  "mcpServers": {
    "infobip-sms": {
      "type": "http",
      "url": "https://mcp.infobip.com/sms"
    }
  }
}
```

> If your MCP client supports OAuth 2.1, the authorization flow will be triggered automatically on first connection. See [Authentication and Authorization](#-authentication-and-authorization) below.

## 🔐 Authentication and Authorization

To use Infobip MCP servers, you need an Infobip account. If you don't have one, [create an Infobip account with a free trial](https://infobip.com/signup?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp).

### Using OAuth 2.1

Infobip MCP servers support OAuth 2.1 authentication.
To use OAuth 2.1, your MCP client must support OAuth 2.1 authentication and [Authorization Server Discovery](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization#authorization-server-discovery).
Configure your MCP client to connect to the Infobip MCP server without providing authentication credentials — the OAuth flow will be triggered automatically, redirecting you to the Infobip OAuth server for authentication.

#### Discovering Supported Scopes

Some MCP clients may not support automatic `scopes_supported` discovery.
In this case, you must manually configure the scopes in your MCP client configuration.
The scopes for a particular MCP server can be found in the authorization server metadata at `{server-url}/.well-known/oauth-authorization-server`.

For example, for the Infobip SMS MCP server, the scopes are available at:
https://mcp.infobip.com/sms/.well-known/oauth-authorization-server

### Using an API Key

You can authenticate using your [Infobip API key](https://www.infobip.com/docs/essentials/api-essentials/api-authentication?utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp#api-key-header) by providing it in the `Authorization` header using the format `App ${INFOBIP_API_KEY}`:

```json
{
  "mcpServers": {
    "infobip-sms": {
      "type": "http",
      "url": "https://mcp.infobip.com/sms",
      "headers": {
        "Authorization": "App ${INFOBIP_API_KEY}"
      }
    }
  }
}
```

## 🤖 Agent Permission and Access Control

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

## 🚀 Infobip MCP Servers in Use

Learn how to build, configure, and integrate various Infobip MCP servers with our [hands-on MCP tutorials](https://www.infobip.com/docs/tutorials?page=1&filter=%26products%3Dinfobip-mcp&utm_source=infobip-mcp-github&utm_medium=referral&utm_campaign=mcp).

## 🤝 Contributing

If you have suggestions for improvements, please contact [devrel@infobip.com](mailto:devrel@infobip.com).

## 📄 License

This document is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

**Happy building with Infobip MCP! 🚀**

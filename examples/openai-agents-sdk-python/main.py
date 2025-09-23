import asyncio
import logging
import os

from agents import (
    Agent,
    ModelSettings,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents.mcp import MCPServerStreamableHttp
from dotenv import load_dotenv
from openai.lib.azure import AsyncAzureOpenAI

log = logging.getLogger("Infobip-MCP-Chat")

load_dotenv()

client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("responses")
set_tracing_disabled(disabled=True)

ib_sms_mcp_server = MCPServerStreamableHttp(
    name="InfobipSMS",
    params={
        "url": "https://mcp.infobip.com/sms",
        "headers": {"Authorization": f"App {os.getenv("INFOBIP_API_KEY")}"},
    },
    client_session_timeout_seconds=30,
)


async def main():
    async with ib_sms_mcp_server:
        sms_agent = Agent(
            name="Infobip SMS Agent",
            model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
            mcp_servers=[ib_sms_mcp_server],
            model_settings=ModelSettings(tool_choice="required", store=True),
        )
        log.info("Chat session started.")

        reply = await Runner.run(
            sms_agent,
            """
            You are a helpful assistant specialized in SMS messaging services.
            You can help users send SMS messages through the Infobip platform.
            Please introduce yourself at a start of each session.
            Briefly explain your capabilities and welcome the user to interact with you.
            Be professional, friendly, and provide clear guidance on how you can assist with SMS-related tasks.
            """,
        )
        print("Assistant: ", reply.final_output)

        while True:
            print()
            user = input("You: ").strip()
            if user.lower() in {"exit", "quit", "bye", "goodbye"}:
                log.info("Chat session ended by user.")
                break
            if not user:
                continue

            reply = await Runner.run(
                sms_agent,
                input=user,
                previous_response_id=reply.last_response_id,
            )
            print()
            print("Assistant: ", reply.final_output)


if __name__ == "__main__":
    asyncio.run(main())

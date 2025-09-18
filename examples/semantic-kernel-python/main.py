#!/usr/bin/env python3

import asyncio
import logging
import os

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.contents import ChatHistory

log = logging.getLogger("Infobip-MCP-Chat")

load_dotenv()

chat_service = AzureChatCompletion(
    deployment_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

kernel = Kernel()
kernel.add_service(chat_service)

settings = AzureChatPromptExecutionSettings()
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()


async def main() -> None:
    async with MCPStreamableHttpPlugin(
            name="InfobipSMS",
            description="Infobip SMS Plugin - Enables sending SMS messages through the Infobip platform.",
            url="https://mcp.infobip.com/sms",
            headers={
                "Authorization": f"App {os.getenv('INFOBIP_API_KEY')}"
            }
    ) as infobip_plugin:
        kernel.add_plugin(infobip_plugin)

        history = ChatHistory(system_message="""
        You are a helpful assistant specialized in SMS messaging services.
        You can help users send SMS messages through the Infobip platform.
        Please introduce yourself at a start of each session.
        Briefly explain your capabilities and welcome the user to interact with you.
        Be professional, friendly, and provide clear guidance on how you can assist with SMS-related tasks.
        """)

        log.info("Chat session started.")

        reply = await chat_service.get_chat_message_content(history, settings, kernel=kernel)
        print("Assistant:", reply.content)
        history.add_assistant_message(reply.content)

        while True:
            print()
            user = input("You: ").strip()
            if user.lower() in {"exit", "quit", "bye", "goodbye"}:
                log.info("Chat session ended by user.")
                break
            if not user:
                continue

            history.add_user_message(user)
            reply = await chat_service.get_chat_message_content(history, settings, kernel=kernel)
            print()
            print("Assistant:", reply.content)
            history.add_assistant_message(reply.content)


if __name__ == "__main__":
    asyncio.run(main())

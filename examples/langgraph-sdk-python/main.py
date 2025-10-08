import asyncio
import logging
import os

from dotenv import load_dotenv
from langchain_aws.chat_models import ChatBedrock
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode

log = logging.getLogger("Infobip-MCP-Chat")

load_dotenv()

client = MultiServerMCPClient(
    {
        "infobip-sms": {
            "url": "https://mcp.infobip.com/sms",
            "transport": "streamable_http",
            "headers": {"Authorization": f"App {os.getenv('INFOBIP_API_KEY')}"},
        }
    }
)

llm = ChatBedrock(
    model=os.getenv("AWS_MODEL_ID"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region=os.getenv("AWS_REGION")
)


async def run_agent():
    tools = await client.get_tools()
    tool_node = ToolNode(tools)
    llm_with_tools = llm.bind_tools(tools)

    def should_continue(state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    async def call_model(state: MessagesState):
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", should_continue)
    builder.add_edge("tools", "call_model")

    graph = builder.compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "chat_session_1"}}

    reply = await graph.ainvoke(
        {
            "messages": [
                ("system", """
                    You are a helpful assistant specialized in SMS messaging services.
                    You can help users send SMS messages through the Infobip platform.
                    Please introduce yourself at a start of each session.
                    Briefly explain your capabilities and welcome the user to interact with you.
                    Be professional, friendly, and provide clear guidance on how you can assist with SMS-related tasks.
                    """),
                ("user", "Hello"),
            ]
        },
        config=config,
    )
    print(f"Assistant: {reply['messages'][-1].content}")

    while True:
        print()
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit", "bye", "goodbye"}:
            print("Chat session ended by user.")
            break
        if not user:
            continue

        reply = await graph.ainvoke({"messages": [("user", user)]}, config=config)
        print()
        print(f"Assistant: {reply['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(run_agent())


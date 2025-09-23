import {
  Agent,
  MCPServerStreamableHttp,
  run,
  setDefaultOpenAIClient,
  setTracingDisabled,
} from "@openai/agents";
import readline from "node:readline";
import { AzureOpenAI } from "openai";

const client = new AzureOpenAI({
  apiKey: process.env.AZURE_OPENAI_API_KEY,
  endpoint: process.env.AZURE_OPENAI_ENDPOINT,
  apiVersion: process.env.AZURE_OPENAI_API_VERSION,
});

setDefaultOpenAIClient(client);
setTracingDisabled(true);

const ibSmsMcpServer = new MCPServerStreamableHttp({
  name: "InfobipSMS",
  url: "https://mcp.infobip.com/sms",
  fetch: async (url, init) =>
    fetch(url, {
      ...init,
      headers: {
        ...init?.headers,
        "Content-Type": "application/json",
        Accept: "application/json, text/event-stream",
        Authorization: `App ${process.env.INFOBIP_API_KEY}`,
      },
    }),
});

await ibSmsMcpServer.connect();

try {
  const smsAgent = new Agent({
    name: "Infobip SMS Agent",
    model: process.env.AZURE_OPENAI_MODEL_NAME,
    mcpServers: [ibSmsMcpServer],
    modelSettings: {
      toolChoice: "required",
      store: true,
    },
  });

  let reply = await run(
    smsAgent,
    `
  You are a helpful assistant specialized in SMS messaging services.
  You can help users send SMS messages through the Infobip platform.
  Please introduce yourself at a start of each session.
  Briefly explain your capabilities and welcome the user to interact with you.
  Be professional, friendly, and provide clear guidance on how you can assist with SMS-related tasks.
  `,
  );

  console.log("Assistant: ", reply.finalOutput);

  while (true) {
    console.log();
    const user = await readInput();
    if (!user) {
      continue;
    }
    if (["exit", "quit", "bye", "goodbye"].includes(user.toLowerCase())) {
      break;
    }

    reply = await run(smsAgent, user, { previousResponseId: reply.id });
    console.log();
    console.log("Assistant: ", reply.finalOutput);
  }
} finally {
  await ibSmsMcpServer.close();
}

async function readInput() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: true,
  });
  return new Promise((resolve) =>
    rl.question("You: ", (input) => {
      rl.close();
      resolve(input.trim());
    }),
  );
}

using System.Text.Json;
using Azure.Identity;
using DotNetEnv;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;
using Microsoft.SemanticKernel;
using ModelContextProtocol.Client;
using Spectre.Console;
using Microsoft.SemanticKernel.ChatCompletion;

Env.Load();

static string GetRequiredEnvironmentVariable(string variableName)
{
    var value = Environment.GetEnvironmentVariable(variableName);
    ArgumentException.ThrowIfNullOrEmpty(value, variableName);
    return value;
}

string apiKey = GetRequiredEnvironmentVariable("ApiKey");
string apiBaseUrl = GetRequiredEnvironmentVariable("ApiBaseUrl");
string azureOpenAIBaseUrl = GetRequiredEnvironmentVariable("AzureOpenAIBaseUrl");
string azureOpenAIApiKey = GetRequiredEnvironmentVariable("AzureOpenAIApiKey");
string azureDeploymentName = GetRequiredEnvironmentVariable("AzureDeploymentName");


string smsSendToolName = "SmsSendTool";
var transport = new SseClientTransport(new SseClientTransportOptions
{
    Name = smsSendToolName,
    Endpoint = new Uri(apiBaseUrl),
    AdditionalHeaders =
        new Dictionary<string, string>
        {
            { "Authorization", $"App {apiKey}" }
        }
});

var mcpClient = await McpClientFactory.CreateAsync(transport);
var tools = await mcpClient.ListToolsAsync(JsonSerializerOptions.Default);

var builder = Kernel.CreateBuilder();
var defaultAzureCreds = new DefaultAzureCredential(
    new DefaultAzureCredentialOptions
    {
        ExcludeAzureCliCredential = false,
        ExcludeEnvironmentCredential = true,
        ExcludeManagedIdentityCredential = true,
        ExcludeVisualStudioCredential = true
    });
builder.AddAzureOpenAIChatCompletion(azureDeploymentName, azureOpenAIBaseUrl, azureOpenAIApiKey);

var kernel = builder.Build();
var kernelFunctions = tools.Select(tool => tool.AsKernelFunction());

kernel.Plugins.AddFromFunctions(smsSendToolName, kernelFunctions);
var executionSettings = new AzureOpenAIPromptExecutionSettings
{
    Temperature = 0,
    FunctionChoiceBehavior = FunctionChoiceBehavior.Auto(),
};

var chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

ChatHistory history = [];
history.AddSystemMessage("You are a helpful assistant specialized in SMS messaging services." +
        "You can help users send SMS messages through the Infobip platform." +
        "Please introduce yourself at a start of each session." +
        "Briefly explain your capabilities and welcome the user to interact with you." +
        "Be professional, friendly, and provide clear guidance on how you can assist with SMS-related tasks.");

var initialReply = await chatCompletionService.GetChatMessageContentAsync(history, kernel: kernel, executionSettings: executionSettings);
AnsiConsole.WriteLine("Assistant: " + initialReply.Content);
history.AddAssistantMessage(initialReply.Content ?? "");

while (true)
{
    AnsiConsole.WriteLine();
    string user = AnsiConsole.Ask<string>("You: ").Trim().ToLower();
    if (new[] { "exit", "quit", "bye", "goodbye" }.Contains(user))
    {
        break;
    }
    if (user.Length == 0)
    {
        continue;
    }

    history.AddUserMessage(user);
    var reply = await chatCompletionService.GetChatMessageContentAsync(history, kernel: kernel, executionSettings: executionSettings);
    AnsiConsole.WriteLine();
    AnsiConsole.WriteLine("Assistant: " + reply.Content);
    history.AddAssistantMessage(reply.Content ?? "");
}

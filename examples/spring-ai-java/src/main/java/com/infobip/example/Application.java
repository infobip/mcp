package com.infobip.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.Set;

@SpringBootApplication
public class Application implements CommandLineRunner {

    private final static Logger log = LoggerFactory.getLogger(Application.class);

    public static void main(String[] args) {
        var springApp = new SpringApplication(Application.class);
        springApp.setWebApplicationType(WebApplicationType.NONE);
        springApp.run(args);
    }

    private final ChatClient chatClient;

    public Application(
            ChatClient.Builder chatClientBuilder,
            ChatMemory chatMemory,
            ToolCallbackProvider toolsProvider
    ) {
        chatClient = chatClientBuilder
                .defaultToolCallbacks(toolsProvider)
                .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())
                .defaultSystem("""
                        You are a helpful assistant specialized in SMS messaging services.
                        You can help users send SMS messages through the Infobip platform.
                        Please introduce yourself at a start of each session.
                        Briefly explain your capabilities and welcome the user to interact with you.
                        Be professional, friendly, and provide clear guidance on how you can assist with SMS-related tasks."""
                ).build();
    }

    @Override
    public void run(String... args) throws Exception {
        log.info("Chat session started.");

        var initialReply = chatClient.prompt("Introduce yourself").call().content();
        System.out.println("Assistant: " + initialReply);

        while (true) {
            System.out.println();
            System.out.print("You: ");
            var user = System.console().readLine();
            if (user == null || user.isBlank()) {
                continue;
            } else if (Set.of("exit", "quit", "bye", "goodbye").contains(user.toLowerCase().trim())) {
                break;
            }

            var reply = chatClient.prompt(user).call().content();
            System.out.println();
            System.out.println("Assistant: " + reply);
        }
    }
}

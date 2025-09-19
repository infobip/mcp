package com.infobip.example;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {
    @Bean
    WebClient.Builder apiKeyInjectingWebClientBuilder(
            @Value("${infobip.api.key}") String infobipApiKey
    ) {
        return WebClient.builder().apply(builder -> builder
                .defaultHeader(HttpHeaders.AUTHORIZATION, "App " + infobipApiKey)
        );
    }
}

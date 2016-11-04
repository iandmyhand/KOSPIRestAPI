package com.blackvelvet;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class KospiApiController {

    @RequestMapping("/")
    public String index() {
        return "Hello! This is KOSPI REST API!";
    }

    @RequestMapping("/ping")
    public String ping() {
        return "OK";
    }

}

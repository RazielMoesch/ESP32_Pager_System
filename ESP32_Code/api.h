#pragma once

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

class API {

public:
    API(const String& url, const String& pid);
    bool request_setup(const String& tempkey);
    bool finish_setup(const String& tempkey);
    bool load(const String& pid, const String& akey, int g);
    bool get_messages(JsonDocument& doc);
    bool is_ready() const { return authkey.length() > 0 && grade >= 0; }
    String get_authkey() const { return authkey; }
    int get_grade()   const { return grade; }

private:
    String api_url;
    String pager_id;
    String authkey;
    int grade = -1;

    WiFiClientSecure client;
    HTTPClient http;

    String post_request(const String& endpoint, const String& body);
};
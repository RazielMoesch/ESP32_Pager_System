

#include "API.h"

API::API(const String& url, const String& pid)
    : api_url(url), pager_id(pid), grade(-1) {
    client.setInsecure();
    client.setTimeout(10000);
}

bool API::load(const String& pid, const String& akey, int g) {
    pager_id = pid;
    authkey = akey;
    grade = g;
    return is_ready();
}

String API::post_request(const String& endpoint, const String& body) {
    String full_url = api_url + endpoint;

    Serial.println("POST to: " + full_url);
    Serial.println("Body: " + body);

    WiFiClientSecure fresh_client;
    fresh_client.setInsecure();
    fresh_client.setTimeout(10000);

    HTTPClient http;
    http.begin(fresh_client, full_url);
    http.addHeader("Content-Type", "application/json");
    http.setTimeout(10000);

    int code = http.POST(body);
    Serial.println("HTTP code: " + String(code));

    if (code <= 0) {
        http.end();
        return "";
    }

    String response = http.getString();
    Serial.println("Response: " + response);
    http.end();
    return response;
}

bool API::request_setup(const String& tempkey) {
    JsonDocument req;
    req["pagerid"] = pager_id;
    req["tempkey"] = tempkey;

    String body;
    serializeJson(req, body);

    String response = post_request("/pager/request_setup", body);
    if (response.length() == 0) return false;

    JsonDocument res;
    DeserializationError err = deserializeJson(res, response);
    if (err) return false;

    return String(res["status"].as<const char*>()) == "success";
}

bool API::finish_setup(const String& tempkey) {
    JsonDocument req;
    req["pagerid"] = pager_id;
    req["tempkey"] = tempkey;

    String body;
    serializeJson(req, body);

    String response = post_request("/pager/finish_setup", body);
    if (response.length() == 0) return false;

    JsonDocument res;
    DeserializationError err = deserializeJson(res, response);
    if (err) return false;

    if (String(res["status"].as<const char*>()) != "success") return false;

    authkey = res["authkey"].as<const char*>();
    grade    = res["grade"].as<int>();
    pager_id = res["pagerid"].as<const char*>();

    return is_ready();
}

bool API::get_messages(JsonDocument& doc) {
    JsonDocument req;
    req["pagerid"] = pager_id;
    req["authkey"] = authkey;
    req["grade"]   = grade;

    String body;
    serializeJson(req, body);

    String response = post_request("/pager/get_messages", body);
    if (response.length() == 0) return false;

    DeserializationError err = deserializeJson(doc, response);
    if (err) return false;

    return String(doc["status"].as<const char*>()) == "success";
}











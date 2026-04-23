#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_ILI9341.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include "display.h"
#include "API.h"

// const char* SSID     = "Fios-qWM6v";
// const char* PASSWORD = "cham33box4368gas";
const char* SSID     = "";
const char* PASSWORD = "";
const String API_URL  = "";
const String PAGER_ID = "RKYHSPager0";

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST, TFT_MISO);
EventLoop* loop_ptr  = nullptr;
API* api             = nullptr;
Preferences prefs;

enum class Screen { WIFI_ERROR, SETUP, MESSAGES };
Screen current_screen = Screen::WIFI_ERROR;

JsonDocument messages_doc;
std::vector<String> message_list;
int msg_index = 0;
String tempkey_input = "abc123";

void show_setup_screen();
void show_messages_screen();
void show_wifi_error_screen();
void try_connect_wifi();
void do_request_setup();
void do_finish_setup();
void show_message_at(int index);
void clear_all();

bool connect_wifi() {
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(1000);
    WiFi.begin(SSID, PASSWORD);
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        attempts++;
    }
    return WiFi.status() == WL_CONNECTED;
}

void clear_all() {
    loop_ptr->remove_button("btn_request");
    loop_ptr->remove_button("btn_finish");
    loop_ptr->remove_button("btn_prev");
    loop_ptr->remove_button("btn_next");
    loop_ptr->remove_button("btn_retry");
    loop_ptr->remove_button("btn_reload");
    loop_ptr->remove_text("lbl_title");
    loop_ptr->remove_text("lbl_title2");
    loop_ptr->remove_text("lbl_status");
    loop_ptr->remove_text("lbl_msg");
    loop_ptr->remove_text("lbl_counter");
    loop_ptr->remove_text("lbl_wifi_title");
    loop_ptr->remove_text("lbl_wifi_status");
    loop_ptr->tft->fillScreen(ILI9341_WHITE);
}

void try_connect_wifi() {
    loop_ptr->update_text("lbl_wifi_status", "Connecting...        ");
    if (connect_wifi()) {
        prefs.begin("pager", true);
        String stored_pid   = prefs.getString("pid",     "");
        String stored_akey  = prefs.getString("authkey", "");
        int    stored_grade = prefs.getInt("grade",      -1);
        prefs.end();
        if (stored_pid.length() > 0 && stored_akey.length() > 0 && stored_grade >= 0) {
            api->load(stored_pid, stored_akey, stored_grade);
            show_messages_screen();
        } else {
            show_setup_screen();
        }
    } else {
        loop_ptr->update_text("lbl_wifi_status", "Failed. Try again.   ");
    }
}

void show_wifi_error_screen() {
    current_screen = Screen::WIFI_ERROR;
    clear_all();
    text(loop_ptr, "lbl_wifi_title",  "No WiFi", 70, 80, 2, ILI9341_RED);
    text(loop_ptr, "lbl_wifi_status", "Cannot connect.", 10, 140, 1, ILI9341_DARKGREY);
    button(loop_ptr, "btn_retry", "Retry", 70, 180, 100, 40, try_connect_wifi, 1, ILI9341_WHITE, ILI9341_NAVY, ILI9341_NAVY);
}

void setup() {
    Serial.begin(115200);
    loop_ptr = new EventLoop(&tft, 2, ILI9341_WHITE);
    api      = new API(API_URL, PAGER_ID);
    loop_ptr->tft->setTextColor(ILI9341_BLACK);
    loop_ptr->tft->setTextSize(1);
    loop_ptr->tft->setCursor(10, 10);
    loop_ptr->tft->print("Connecting to WiFi...");
    if (connect_wifi()) {
        prefs.begin("pager", true);
        String stored_pid   = prefs.getString("pid",     "");
        String stored_akey  = prefs.getString("authkey", "");
        int    stored_grade = prefs.getInt("grade",      -1);
        prefs.end();
        if (stored_pid.length() > 0 && stored_akey.length() > 0 && stored_grade >= 0) {
            api->load(stored_pid, stored_akey, stored_grade);
            show_messages_screen();
        } else {
            show_setup_screen();
        }
    } else {
        show_wifi_error_screen();
    }
}

void loop() {
    loop_ptr->check();
}

void show_setup_screen() {
    current_screen = Screen::SETUP;
    clear_all();
    text(loop_ptr, "lbl_title", "Pager Setup: RKYHSPager5", 50, 30, 2, ILI9341_BLACK);
    button(loop_ptr, "btn_request", "Request Setup", 20, 100, 200, 44, do_request_setup, 1, ILI9341_WHITE, ILI9341_NAVY, ILI9341_NAVY);
    button(loop_ptr, "btn_finish", "Finish Setup", 20, 170, 200, 44, do_finish_setup, 1, ILI9341_WHITE, ILI9341_DARKGREEN, ILI9341_DARKGREEN);
    text(loop_ptr, "lbl_status", "Press Request Setup first.", 10, 240, 1, ILI9341_DARKGREY);
}

void do_request_setup() {
    loop_ptr->update_text("lbl_status", "Requesting...            ");
    bool ok = api->request_setup(tempkey_input);
    loop_ptr->update_text("lbl_status", ok ? "Done! Now press Finish.  " : "Request failed.          ");
}

void do_finish_setup() {
    loop_ptr->update_text("lbl_status", "Finishing setup...       ");
    bool ok = api->finish_setup(tempkey_input);
    if (ok) {
        prefs.begin("pager", false);
        prefs.putString("pid",     PAGER_ID);
        prefs.putString("authkey", api->get_authkey());
        prefs.putInt("grade",      api->get_grade());
        prefs.end();
        show_messages_screen();
    } else {
        loop_ptr->update_text("lbl_status", "Finish failed.           ");
    }
}

void show_messages_screen() {
    current_screen = Screen::MESSAGES;
    clear_all();
    text(loop_ptr, "lbl_title2", "Messages", 60, 10, 2, ILI9341_BLACK);
    button(loop_ptr, "btn_reload", "Reload", 160, 10, 70, 25, []() { show_messages_screen(); }, 1, ILI9341_WHITE, ILI9341_BLUE, ILI9341_BLUE);
    message_list.clear();
    msg_index = 0;
    if (api->get_messages(messages_doc)) {
        JsonArray arr = messages_doc["messages"].as<JsonArray>();
        for (JsonVariant v : arr) {
            message_list.push_back(v[3].as<const char*>());
        }
    }
    if (message_list.empty()) {
        text(loop_ptr, "lbl_msg",     "No messages.", 10, 140, 1, ILI9341_DARKGREY);
        text(loop_ptr, "lbl_counter", "0 / 0", 100, 290, 1, ILI9341_BLACK);
    } else {
        text(loop_ptr, "lbl_msg",     message_list[0], 10, 60, 1, ILI9341_BLACK);
        text(loop_ptr, "lbl_counter", "1 / " + String(message_list.size()), 100, 290, 1, ILI9341_BLACK);
    }
    button(loop_ptr, "btn_prev", "< Prev", 10, 285, 90, 28, []() {
        if (message_list.empty()) return;
        msg_index = (msg_index - 1 + message_list.size()) % message_list.size();
        show_message_at(msg_index);
    }, 1, ILI9341_BLACK, ILI9341_BLACK, ILI9341_LIGHTGREY);
    button(loop_ptr, "btn_next", "Next >", 140, 285, 90, 28, []() {
        if (message_list.empty()) return;
        msg_index = (msg_index + 1) % message_list.size();
        show_message_at(msg_index);
    }, 1, ILI9341_BLACK, ILI9341_BLACK, ILI9341_LIGHTGREY);
}

void show_message_at(int index) {
    loop_ptr->update_text("lbl_msg", message_list[index]);
    loop_ptr->update_text("lbl_counter", String(index + 1) + " / " + String(message_list.size()));
}
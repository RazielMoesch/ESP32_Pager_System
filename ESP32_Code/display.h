
#pragma once

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <XPT2046_Touchscreen.h>
#include <vector>


#define TFT_CS   10
#define TFT_DC   9
#define TFT_RST  8 
#define TFT_MOSI 17
#define TFT_SCLK 18
#define TFT_MISO 16

#define TOUCH_CS  7
#define TOUCH_CLK 5
#define TOUCH_DIN 4
#define TOUCH_DO  11


using callback_fn = std::function<void()>;

class EventLoop {

public:

  EventLoop( Adafruit_ILI9341* display, int rotation = 1, uint16_t bg = ILI9341_WHITE);
  void remove_text(const String& id);
  void remove_button(const String& id);
  void add_touch_area(const String& id, int x, int y, callback_fn callback, int w = 20, int h = 10);
  void add_text_area(const String& id, int x, int y, int w, int h, const String& text, int text_size, uint16_t color);
  void update_text( const String& id, const String& text);
  void check();

  Adafruit_ILI9341* tft;

private: 

  struct TouchButton {
    String id;
    int x, y, w, h;
    callback_fn callback;
  };

  struct TextArea {
    String id;
    int x, y, w, h, text_size;
    uint16_t color;
    String current_text;
  };

  SPIClass* touchSPI = nullptr;
  XPT2046_Touchscreen* ts = nullptr;
  std::vector<TouchButton> buttons;
  std::vector<TextArea> texts;
  uint16_t bg;
};

int get_char_w(int text_size);
int get_char_h(int text_size);

void button(
  EventLoop* loop,
  String id,
  String label,
  int x,
  int y,
  int w,
  int h,
  callback_fn fn,
  int text_size = 1,
  uint16_t text_color = ILI9341_BLACK,
  uint16_t box_color = ILI9341_BLACK,
  uint16_t fill_color = ILI9341_WHITE
);

void text(
  EventLoop* loop,
  String id,
  String text,
  int x,
  int y,
  int text_size = 1,
  uint16_t text_color = ILI9341_BLACK
);




void basic_button(
  EventLoop* loop,
  String id,
  String label,
  int x,
  int y,
  callback_fn fn
);

void basic_text(
  EventLoop* loop,
  String id,
  String txt,
  int x, 
  int y
);















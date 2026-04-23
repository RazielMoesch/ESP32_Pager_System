

#include "display.h"



int get_char_w(int text_size) { return 6 * text_size; }
int get_char_h(int text_size) { return 8 * text_size; }

EventLoop::EventLoop( Adafruit_ILI9341* display, int rotation, uint16_t bg_color ) {

  bg = bg_color;
  tft = display;
  tft->begin();
  tft->setRotation(rotation);
  tft->fillScreen(ILI9341_WHITE);

  touchSPI = new SPIClass(HSPI);
  touchSPI->begin(TOUCH_CLK, TOUCH_DO, TOUCH_DIN, TOUCH_CS);
  ts = new XPT2046_Touchscreen(TOUCH_CS);
  ts->begin(*touchSPI);
  ts->setRotation(rotation);

}


void EventLoop::add_touch_area(const String& id, int x, int y, callback_fn callback, int w, int h) {
  buttons.push_back({ id, x, y, w, h, callback });
}


void EventLoop::add_text_area(const String& id, int x, int y, int w, int h, const String& text, int text_size, uint16_t color) {
  texts.push_back({ id, x, y, w, h, text_size, color, text });
}

void EventLoop::remove_button(const String& id) {

  buttons.erase(
    std::remove_if(buttons.begin(), buttons.end(), 
      [&id](const TouchButton& b) { return b.id == id; }),
    buttons.end()
    );

}


void EventLoop::remove_text(const String& id) {
    texts.erase(
        std::remove_if(texts.begin(), texts.end(),
            [&id](const TextArea& t) { return t.id == id; }),
        texts.end()
    );
}





void EventLoop::update_text( const String& id, const String& text ) {

  for ( auto& t : texts ) {

    if ( t.id == id ) {
      tft->fillRect(t.x, t.y, t.w, t.h, bg);
      tft->setTextSize(t.text_size);
      tft->setTextColor(t.color);
      tft->setCursor(t.x, t.y);
      tft->print(text);

      t.current_text = text;
      break;
    }

  }

}


void EventLoop::check() {

  if (!ts->touched()) return;

  TS_Point p = ts->getPoint();

  int screen_x = map(p.x, 200, 3900, 240, 0);
  int screen_y = map(p.y, 200, 3900, 320, 0);

  for ( auto& b : buttons ) {

    if ( screen_x >= b.x && screen_x <= b.x + b.w && screen_y >= b.y && screen_y <= b.y + b.h ) {

      b.callback();
      delay(200);
      break;

    }

  }

}


void button(
  EventLoop* loop,
  String id,
  String label,
  int x,
  int y,
  int w,
  int h,
  callback_fn fn,
  int text_size,
  uint16_t text_color,
  uint16_t box_color,
  uint16_t fill_color
) {

  loop->tft->fillRect(x, y, w, h, fill_color);
  loop->tft->drawRect(x, y, w, h, box_color);
  
  int text_x = x + (w - label.length() * get_char_w(text_size)) / 2;
  int text_y = y + (h - get_char_h(text_size)) / 2;

  loop->tft->setTextSize(text_size);
  loop->tft->setTextColor(text_color);
  loop->tft->setCursor(text_x, text_y);
  loop->tft->print(label);

  loop->add_touch_area(id, x, y, fn, w, h);

}

void text(
  EventLoop* loop,
  String id,
  String txt,
  int x,
  int y,
  int text_size, 
  uint16_t color
) {

  int w = txt.length() * get_char_w(text_size);
  int h = get_char_h(text_size);

  loop->tft->setTextSize(text_size);
  loop->tft->setTextColor(color);
  loop->tft->setCursor(x, y);
  loop->tft->print(txt);

  loop->add_text_area(id, x, y, w, h, txt, text_size, color);

}

void basic_button(
  EventLoop* loop,
  String id,
  String label,
  int x,
  int y,
  callback_fn fn
) {
  int w = label.length() * get_char_w(1) + 10;
  int h = get_char_h(1) + 8;
  button(loop, id, label, x, y, w, h, fn);
}

void basic_text(
  EventLoop* loop,
  String id,
  String txt,
  int x,
  int y
) {
  text(loop, id, txt, x, y);
}






























































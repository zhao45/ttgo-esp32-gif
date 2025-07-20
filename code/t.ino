#include <TFT_eSPI.h>
#include <SPI.h>
#include "image_arrays.c"  // ← 你從 Python 轉出的圖片資料陣列

#define FRAME_COUNT 16
#define IMG_WIDTH  135    // 根據實際圖片大小修改
#define IMG_HEIGHT 218
#define FRAME_DELAY 300   // 每張圖顯示時間（毫秒）

TFT_eSPI tft = TFT_eSPI();
int frame_index = 0;

const uint16_t* frames[FRAME_COUNT] = {
  f1, f2, f3, f4,
  f5, f6, f7, f8,
  f9, f10, f11, f12,
  f13, f14, f15, f16
};


void setup() {
  tft.init();
  tft.setRotation(0);  // 根據需要調整旋轉方向
  tft.setSwapBytes(true);
  tft.fillScreen(TFT_BLACK);
}

void loop() {
  tft.pushImage(0, 0, IMG_WIDTH, IMG_HEIGHT, frames[frame_index]);
  frame_index = (frame_index + 1) % FRAME_COUNT;
  delay(FRAME_DELAY);
  
}

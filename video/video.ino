#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include "esp_camera.h"
#include "SPIFFS.h"

const char *ssid = "eee";
const char *password = "11111111";

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);

  // Kết nối tới mạng WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Khởi tạo camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sscb_sda = 26;
  config.pin_sscb_scl = 27;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // Phục vụ trang web
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/index.html");
  });

  // Phục vụ video stream
  server.on(
    "/stream", HTTP_GET, [](AsyncWebServerRequest *request) {
      request->send_P(200, "video/mp4", (const char *)NULL, 0);
    },
    [](AsyncWebServerRequest *request, String filename, size_t index, uint8_t data, size_t len, bool final) {
      if (!index) {
        // Gửi header cho video stream
        request->header("Access-Control-Allow-Origin");
        request->header("Content-Disposition", "inline; filename=stream.mp4");
        request->header("Content-Type", "video/mp4");
      }
      if (len) {
        // Gửi dữ liệu cho video stream
        request->send_P((const char *)data, len);
      }
    });

  // Bật server
  server.begin();
}

void loop() {
}

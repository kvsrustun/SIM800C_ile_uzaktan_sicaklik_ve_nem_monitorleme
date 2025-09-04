#include <Wire.h>
#include <Deneyap_SicaklikNemOlcer.h>
#include <SoftwareSerial.h>

TempHum sensor;
SoftwareSerial sim800(D8, D14); // RX, TX

const char* baseURL = "http://nazmiaras.com/kevser.php";

void setup() {
  Serial.begin(9600);
  sim800.begin(9600);
  sensor.begin();

  Serial.println("SIM800 başlatılıyor...");

  sendAT("AT", 1000);
  sendAT("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"", 1000);
  sendAT("AT+SAPBR=3,1,\"APN\",\"vodafone\"", 1000); // APN: operatöre göre değişir
  sendAT("AT+SAPBR=1,1", 3000);

  // GPRS bağlantı kontrol
  sim800.println("AT+SAPBR=2,1");
  delay(1000);

  String gprsResponse = readResponse();
  Serial.println("GPRS Bağlantı Durumu:");
  Serial.println(gprsResponse);

  if (gprsResponse.indexOf("+SAPBR: 1,1") != -1) {
    Serial.println("✅ GPRS bağlantısı BAŞARILI!");
  } else {
    Serial.println("❌ GPRS bağlantısı YOK!");
  }
}

void loop() {
  float sicaklik = sensor.getTempValue();
  float nem = sensor.getHumValue();

  // GET URL oluştur
  char fullUrl[200];
  sprintf(fullUrl, "%s?sicaklik=%.2f&nem=%.2f", baseURL, sicaklik, nem);

  // HTTP Başlatma
  sendAT("AT+HTTPINIT", 500);
  sendAT("AT+HTTPPARA=\"CID\",1", 500);
  sendAT("AT+HTTPPARA=\"UA\",\"Mozilla/5.0\"", 500); // User-Agent ekle

  // URL'yi gönder
  char atURL[250];
  sprintf(atURL, "AT+HTTPPARA=\"URL\",\"%s\"", fullUrl);
  sendAT(atURL, 1000);

  // GET isteği gönder
  Serial.println("GET isteği gönderiliyor...");
  sim800.println("AT+HTTPACTION=0");
  delay(5000);

  // HTTPACTION cevabını oku
  String response = readResponse();
  Serial.println("Modül cevabı:");
  Serial.println(response);

  if (response.indexOf("+HTTPACTION: 0,200") != -1) {
    Serial.println("✅ İstek başarılı! (200 OK)");
  } else {
    Serial.println("❌ İstek başarısız!");
  }

  sendAT("AT+HTTPTERM", 500);
  Serial.print("Veri gönderildi: ");
  Serial.println(fullUrl);
  delay(10000);
}

// AT komutu gönderici
void sendAT(const char* cmd, int delayTime) {
  sim800.println(cmd);
  delay(delayTime);
  while (sim800.available()) {
    Serial.write(sim800.read());
  }
}

// Modülden gelen cevabı okur
String readResponse() {
  String response = "";
  unsigned long timeout = millis() + 3000;
  while (millis() < timeout) {
    if (sim800.available()) {
      char c = sim800.read();
      response += c;
    }
  }
  return response;
}

"""
YKI - Yer Kontrol İstasyonu
Ana Program Dosyası
"""

# Sistem modülleri
import sys
import os
import cv2
import time

# Proje modülleri
from map_manager import MapManager
from uav import UAVObject
from hss_fetcher import HSSFetcher
from camera_stream import CameraStream
from api_client import ApiClient


# ----------------------------------------------------------
# Kamera fonksiyonu (isteğe bağlı)
# ----------------------------------------------------------
def camera():
    cam = CameraStream()
    cam.start()

    try:
        while True:
            frame = cam.read()
            if frame is not None:
                cv2.imshow("Camera Test", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.stop()
        cv2.destroyAllWindows()


# ----------------------------------------------------------
# HSS test fonksiyonu
# ----------------------------------------------------------
def hss():
    manager = MapManager()

    manager.add_uav(UAVObject(1, 41.5100, 36.1180))
    manager.add_uav(UAVObject(2, 41.5120, 36.1190))

    hss_fetch = HSSFetcher()
    zones = hss_fetch.fetch()
    manager.set_hss_zones(zones)

    manager.update_uav(1, 41.5105, 36.1185)
    manager.update_uav(2, 41.5125, 36.1195)

    output = manager.render("test_map.png")
    print("Map saved to:", output)


# ----------------------------------------------------------
# 🔥 LOCK GÖNDEREN FONKSİYON
# ----------------------------------------------------------
def trigger_lock(api_client):
    print("\n🔵 YKI → WebSocket event dinleyicileri ayarlanıyor...\n")

    # lock_response geldiğinde
    def on_response(data):
        print("🟢 Mock Sunucu lock_response:", data)

    # lock_success geldiğinde
    def on_success(data):
        print("🟣 Mock Sunucu lock_success:", data)
        # Buraya birazdan lock_packet gönderme kodunu ekleyeceğiz 😉

    # Event'leri kaydet
    api_client.ws.on("lock_response", on_response)
    api_client.ws.on("lock_success", on_success)

    # İlk lock_attempt'i gönder
    print("🔵 YKI → WebSocket lock_attempt gönderiliyor...")
    api_client.send_lock_attempt(
        uav_id="bizim_iha",
        target_lat=38.76520,
        target_lon=30.52430
    )



# ----------------------------------------------------------
# Ana fonksiyon
# ----------------------------------------------------------
def main():
    print("YKİ başlatılıyor...")

    # WebSocket istemcisi oluştur
    api_client = ApiClient()

    # Lock testi
    trigger_lock(api_client)

    # Eğer program hemen kapanmasın istiyorsan buraya küçük bir wait koyabiliriz:
    while True:
        time.sleep(1)


# ----------------------------------------------------------
if __name__ == "__main__":
    main()

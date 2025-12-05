# api_client.py

import socketio

class ApiClient:
    """YKİ → Mock Sunucu WebSocket istemcisi"""

    def __init__(self, url="http://127.0.0.1:8000"):
        self.ws = socketio.Client()

        # Bağlantı başarılı olduğunda
        @self.ws.event
        def connect():
            print("🔗 [WS] Mock sunucuya bağlanıldı.")

        # Bağlantı hatası
        @self.ws.event
        def connect_error(err):
            print("❌ [WS] Bağlantı hatası:", err)

        # Bağlantı koptuğunda
        @self.ws.event
        def disconnect():
            print("🔌 [WS] Bağlantı kesildi.")

        # lock_response event'ini dışarıdan set edeceğiz
        # (main.py içinde api_client.ws.on("lock_response", handler) ile)
        
        print(f"🌐 WebSocket bağlanıyor → {url}")
        self.ws.connect(url)

    # ----------------------------------------------------------
    # LOCK ATTEMPT
    # ----------------------------------------------------------
    def send_lock_attempt(self, uav_id, target_lat, target_lon):
        """Mock sunucuya lock_attempt gönderir."""
        payload = {
            "id": uav_id,
            "target_lat": target_lat,
            "target_lon": target_lon
        }

        print(f"🔵 [WS] lock_attempt gönderiliyor → {payload}")
        self.ws.emit("lock_attempt", payload)

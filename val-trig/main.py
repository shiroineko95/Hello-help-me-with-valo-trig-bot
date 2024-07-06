import ctypes
import time
import signal
import sys
from modules import loadConfig, getVar, keylistener_function1 as keyPressed, beepSound, findEnemyTrigger

class ucPasteTrigger:
    def __init__(self):
        """Sınıf oluşturulurken konfigürasyonu yükler ve tetikleme işlemini başlatır."""
        self.loadConfig()

    def loadConfig(self):
        """Konfigürasyon dosyasını yükler ve ayarları alır."""
        self.config = loadConfig()
        print("Configuration loaded successfully.")

    def start_trigger(self):
        """Tetikleme işlemini başlatır ve belirli tuşların basılıp basılmadığını kontrol eder."""
        clicked = False

        def signal_handler(sig, frame):
            """Ctrl+C sinyali alındığında programı sonlandırır."""
            print("Exiting program...")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C ile çıkışı yönetir

        while True:
            try:
                # Konfigürasyon dosyasından ayarları al
                key = getVar("key", "TRIGGER")
                fovX = getVar("fovx", "TRIGGER")
                fovY = getVar("fovy", "TRIGGER")
                mode = getVar("mode", "TRIGGER")
                delay = int(getVar("shootdelay", "TRIGGER"))

                print(f"Current settings: key={key}, fovx={fovX}, fovy={fovY}, mode={mode}, shootdelay={delay}")

                # Tetikleme moduna göre tetikleme işlemi yap
                if mode == "Toggle" and keyPressed(key):
                    clicked = not clicked

                    if clicked:
                        beepSound(440, 75)
                        beepSound(700, 100)
                        print("Toggled ON")
                    else:
                        beepSound(440, 75)
                        beepSound(200, 100)
                        print("Toggled OFF")

                    # Tuşa basılma durumunu bekle
                    while keyPressed(key):
                        pass

                elif ((mode == "Toggle" and clicked) or (mode == "Holding" and keyPressed(key))) and not any([keyPressed("W"), keyPressed("A"), keyPressed("S"), keyPressed("D")]):
                    # Düşmanı bul ve tetikleme işlemini yap
                    enemy = findEnemyTrigger(int(fovX), int(fovY))
                    if enemy:
                        self.shoot()
                        time.sleep(200 * delay / 1000)  # Belirlenen gecikme süresine göre bekle

                time.sleep(0.005)  # CPU kullanımını azaltmak için kısa bir süre bekle
            except Exception as e:
                print(f"An error occurred: {e}")  # Hata mesajını yazdır

    @staticmethod
    def shoot():
        """Tetikleme işlemini gerçekleştirir (fare tıklaması)."""
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # Sol fare tuşuna bas
        time.sleep(0.01)  # Kısa bir süre bekle
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # Sol fare tuşunu bırak

if __name__ == "__main__":
    trigger = ucPasteTrigger()
    trigger.start_trigger()

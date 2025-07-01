import cv2
import mediapipe as mp
from controller import Controller
import numpy as np

def main():
    """Ana uygulama fonksiyonu"""
    print("🖐️ El Kontrolü ile Fare Uygulaması")
    print("=" * 40)
    print("Kontroller:")
    print("👆 İmleci Hareket Ettir: Elin pozisyonunu değiştir")
    print("✋ İmleci Dondur: Tüm parmaklar yukarı + başparmak aşağı")
    print("👆 Sol Tık: Başparmak + işaret parmağı birleştir")
    print("👆 Sağ Tık: Başparmak + orta parmak birleştir")
    print("👆 Çift Tık: Başparmak + yüzük parmağı birleştir")
    print("✋ Sürükle: Tüm parmakları aşağı indir")
    print("📜 Yukarı Kaydır: Sadece işaret parmağı yukarı")
    print("📜 Aşağı Kaydır: Sadece küçük parmak yukarı")
    print("🔍 Zoom: İşaret ve orta parmak yukarı, mesafeyi değiştir")
    print("⌨️ ESC: Başparmak + küçük parmak birleştir")
    print("🚪 Çıkış: ESC tuşu veya 'q' tuşu")
    print("=" * 40)
    
    # Kamera başlat
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Kamera açılamadı!")
        print("💡 Çözüm önerileri:")
        print("   - Başka uygulamaların kamerayı kullanmadığından emin olun")
        print("   - Kamera sürücülerini kontrol edin")
        print("   - Windows Ayarlar > Gizlilik > Kamera izinlerini kontrol edin")
        return
    
    print("✅ Kamera başarıyla açıldı!")
    
    # Kamera çözünürlüğü ayarla
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # MediaPipe el algılama
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    mp_draw_styles = mp.solutions.drawing_styles
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,  # Tek el algıla
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    # FPS hesaplama için değişkenleri başlat
    fps_counter = 0
    fps_timer = cv2.getTickCount()
    fps = 0.0  # FPS'i başlat
    
    print("✅ Uygulama hazır. Kameraya elinizi gösterin.")
    print("🚪 Çıkmak için kamera penceresinde ESC veya Q tuşuna basın")
    
    try:
        while True:
            success, img = cap.read()
            if not success:
                print("❌ Kamera görüntüsü alınamadı!")
                break
            
            # Görüntüyü yatay olarak çevir (ayna etkisi)
            img = cv2.flip(img, 1)
            h, w, _ = img.shape
            
            # RGB'ye çevir (MediaPipe için)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            
            # FPS hesapla
            fps_counter += 1
            if fps_counter % 30 == 0:
                current_time = cv2.getTickCount()
                fps = 30 / ((current_time - fps_timer) / cv2.getTickFrequency())
                fps_timer = current_time
            
            # El algılandıysa
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # El landmark'larını çiz
                    mp_draw.draw_landmarks(
                        img, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS,
                        mp_draw_styles.get_default_hand_landmarks_style(),
                        mp_draw_styles.get_default_hand_connections_style()
                    )
                    
                    # Controller'a landmark'ları aktar
                    Controller.hand_landmarks = hand_landmarks
                    
                    # Kontrol işlemlerini çalıştır
                    Controller.update_fingers_status()
                    Controller.cursor_moving()
                    Controller.detect_scrolling()
                    Controller.detect_zooming()
                    Controller.detect_clicking()
                    Controller.detect_dragging()
                    Controller.detect_special_gestures()
                    
                    # Parmak durumlarını ekranda göster
                    draw_finger_status(img, w, h)
                    
                # El algılandı göstergesi
                cv2.putText(img, "El Algilandi", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # El algılanmadı
                cv2.putText(img, "El Algilanmiyor", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                Controller.hand_landmarks = None
            
            # FPS göster
            cv2.putText(img, f"FPS: {fps:.1f}", (w - 150, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Kontrol bilgilerini göster
            cv2.putText(img, "ESC veya Q: Cikis", (10, h - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Görüntüyü göster
            cv2.imshow('El Kontrolu ile Fare', img)
            
            # Çıkış kontrolü
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # ESC veya Q tuşu
                print("👋 Kullanıcı çıkış yaptı.")
                break
                
    except KeyboardInterrupt:
        print("\n⚠️ Kullanıcı tarafından durduruldu.")
    
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Temizlik
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("👋 Uygulama kapatıldı.")

def draw_finger_status(img, w, h):
    """Parmak durumlarını ekranda göster"""
    if Controller.hand_landmarks is None:
        return
    
    try:
        # Durum paneli arka planı
        cv2.rectangle(img, (10, h - 180), (300, h - 10), (0, 0, 0), -1)
        cv2.rectangle(img, (10, h - 180), (300, h - 10), (255, 255, 255), 2)
        
        y_pos = h - 160
        line_height = 25
        
        # Parmak durumları (hata kontrolü ile)
        fingers = []
        
        if hasattr(Controller, 'index_finger_up') and Controller.index_finger_up is not None:
            fingers.append(("Isaret:", "Yukari" if Controller.index_finger_up else "Asagi", 
                           (0, 255, 0) if Controller.index_finger_up else (0, 0, 255)))
        
        if hasattr(Controller, 'middle_finger_up') and Controller.middle_finger_up is not None:
            fingers.append(("Orta:", "Yukari" if Controller.middle_finger_up else "Asagi", 
                           (0, 255, 0) if Controller.middle_finger_up else (0, 0, 255)))
        
        if hasattr(Controller, 'ring_finger_up') and Controller.ring_finger_up is not None:
            fingers.append(("Yuzuk:", "Yukari" if Controller.ring_finger_up else "Asagi", 
                           (0, 255, 0) if Controller.ring_finger_up else (0, 0, 255)))
        
        if hasattr(Controller, 'little_finger_up') and Controller.little_finger_up is not None:
            fingers.append(("Kucuk:", "Yukari" if Controller.little_finger_up else "Asagi", 
                           (0, 255, 0) if Controller.little_finger_up else (0, 0, 255)))
        
        if hasattr(Controller, 'thumb_finger_up') and Controller.thumb_finger_up is not None:
            fingers.append(("Basparmak:", "Yukari" if Controller.thumb_finger_up else "Asagi", 
                           (0, 255, 0) if Controller.thumb_finger_up else (0, 0, 255)))
        
        for i, (finger_name, status, color) in enumerate(fingers):
            cv2.putText(img, f"{finger_name} {status}", (20, y_pos + i * line_height), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Özel durumlar
        if hasattr(Controller, 'dragging') and Controller.dragging:
            cv2.putText(img, "SURUKLUYOR", (w - 200, h - 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        
        if (hasattr(Controller, 'all_fingers_up') and hasattr(Controller, 'thumb_finger_down') and
            Controller.all_fingers_up and Controller.thumb_finger_down):
            cv2.putText(img, "IMLE DONDURULDU", (w - 250, h - 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    except Exception as e:
        # Hata durumunda basit bir mesaj göster
        cv2.putText(img, "Parmak durumu yukleniyor...", (20, h - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

if __name__ == "__main__":
    main()

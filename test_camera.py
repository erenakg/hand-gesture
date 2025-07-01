import cv2

def test_cameras():
    """Mevcut kameraları test et"""
    print("🔍 Kamera taraması başlatılıyor...")
    
    for i in range(5):  # 0-4 arası indeksleri dene
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Kamera {i}: Çalışıyor")
                cap.release()
            else:
                print(f"❌ Kamera {i}: Açılıyor ama görüntü alınamıyor")
                cap.release()
        else:
            print(f"❌ Kamera {i}: Bulunamadı")
    
    print("Tarama tamamlandı.")

if __name__ == "__main__":
    test_cameras()
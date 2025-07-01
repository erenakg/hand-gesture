# El Kontrolü ile Fare Uygulaması

Bu uygulama, kamera aracılığıyla el hareketlerini algılayarak bilgisayar faresini kontrol etmenizi sağlar.

## 🚀 Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
python app.py
```

## 🖐️ Kullanım Kılavuzu

### Temel Kontroller

- **İmleci Hareket Ettir**: Elinizi kameranın karşısında hareket ettirin
- **İmleci Dondur**: Tüm parmakları yukarı kaldırın + başparmağı aşağı indirin

### Tıklama İşlemleri

- **Sol Tık**: Başparmak + işaret parmağını birleştirin
- **Sağ Tık**: Başparmak + orta parmağı birleştirin  
- **Çift Tık**: Başparmak + yüzük parmağını birleştirin

### Sürükleme

- **Sürükle**: Tüm parmakları aşağı indirin (yumruk yapın)

### Kaydırma

- **Yukarı Kaydır**: Sadece işaret parmağını yukarı kaldırın
- **Aşağı Kaydır**: Sadece küçük parmağı yukarı kaldırın

### Yakınlaştırma/Uzaklaştırma

- **Zoom Modu**: İşaret ve orta parmağı yukarı kaldırın
  - **Yakınlaştır**: Parmakları açın (mesafeyi artırın)
  - **Uzaklaştır**: Parmakları birbirine yaklaştırın

### Özel Komutlar

- **ESC Tuşu**: Başparmak + küçük parmağı birleştirin
- **Çıkış**: ESC tuşu veya 'q' tuşuna basın

## 📋 Özellikler

- ✅ Gerçek zamanlı el algılama
- ✅ Parmak pozisyon takibi
- ✅ Fare hareket kontrolü
- ✅ Tüm tıklama türleri (sol, sağ, çift)
- ✅ Sürükleme ve bırakma
- ✅ Kaydırma (yukarı/aşağı)
- ✅ Yakınlaştırma/uzaklaştırma
- ✅ İmleç dondurma
- ✅ Görsel durum göstergeleri
- ✅ FPS sayacı

## 🛠️ Teknik Detaylar

- **Kamera Çözünürlüğü**: 1280x720
- **El Algılama**: MediaPipe
- **Fare Kontrolü**: PyAutoGUI
- **Görüntü İşleme**: OpenCV

## ⚡ Performans İpuçları

1. İyi aydınlatmalı bir ortamda kullanın
2. Kameraya 50-80 cm mesafede durun
3. Elinizi açık şekilde tutun
4. Ani hareketlerden kaçının
5. Tek el kullanın (uygulama tek el için optimize edilmiştir)

## 🔧 Sorun Giderme

**Kamera açılmıyor:**
- Başka uygulamaların kamerayı kullanmadığından emin olun
- Kamera izinlerini kontrol edin

**El algılanmıyor:**
- Aydınlatmayı artırın
- Arka planı basit tutun
- Elinizi daha açık şekilde tutun

**Fare hareketi hassas değil:**
- `controller.py` dosyasındaki `sensitivity` değerini ayarlayın
- Kameraya olan mesafenizi değiştirin

## 📦 Gereksinimler

Tüm gerekli paketler `requirements.txt` dosyasında listelenmiştir. Ana paketler:

- opencv-python
- mediapipe
- pyautogui
- numpy

## 🤝 Katkıda Bulunma

Bu proje açık kaynak kodludur. Katkılarınızı memnuniyetle kabul ederiz!

## 📄 Lisans

MIT License - Detaylar için LICENSE dosyasına bakın.
import pyautogui
import time

class Controller:
    """El hareketleri ile fare kontrolü sağlayan sınıf"""
    
    # Sınıf değişkenleri
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_landmarks = None
    
    # Parmak pozisyonları
    little_finger_down = None
    little_finger_up = None
    index_finger_down = None
    index_finger_up = None
    middle_finger_down = None
    middle_finger_up = None
    ring_finger_down = None
    ring_finger_up = None
    thumb_finger_down = None 
    thumb_finger_up = None
    
    # Özel durumlar
    all_fingers_down = None
    all_fingers_up = None
    index_finger_within_thumb_finger = None
    middle_finger_within_thumb_finger = None
    little_finger_within_thumb_finger = None
    ring_finger_within_thumb_finger = None
    
    # Ekran boyutları
    screen_width, screen_height = pyautogui.size()

    @staticmethod
    def update_fingers_status():
        """Parmak pozisyonlarını güncelle"""
        if Controller.hand_landmarks is None:
            return
        
        landmarks = Controller.hand_landmarks.landmark
        
        # Parmak pozisyonlarını kontrol et (y koordinatları - aşağı/yukarı)
        Controller.little_finger_down = landmarks[20].y > landmarks[17].y
        Controller.little_finger_up = landmarks[20].y < landmarks[17].y
        
        Controller.index_finger_down = landmarks[8].y > landmarks[5].y
        Controller.index_finger_up = landmarks[8].y < landmarks[5].y
        
        Controller.middle_finger_down = landmarks[12].y > landmarks[9].y
        Controller.middle_finger_up = landmarks[12].y < landmarks[9].y
        
        Controller.ring_finger_down = landmarks[16].y > landmarks[13].y
        Controller.ring_finger_up = landmarks[16].y < landmarks[13].y
        
        Controller.thumb_finger_down = landmarks[4].y > landmarks[2].y
        Controller.thumb_finger_up = landmarks[4].y < landmarks[2].y
        
        # Tüm parmakların durumu
        Controller.all_fingers_down = (Controller.index_finger_down and 
                                     Controller.middle_finger_down and 
                                     Controller.ring_finger_down and 
                                     Controller.little_finger_down)
        
        Controller.all_fingers_up = (Controller.index_finger_up and 
                                   Controller.middle_finger_up and 
                                   Controller.ring_finger_up and 
                                   Controller.little_finger_up)
        
        # Başparmak ile diğer parmakların temas durumu
        touch_threshold = 0.05
        Controller.index_finger_within_thumb_finger = (
            abs(landmarks[8].x - landmarks[4].x) < touch_threshold and
            abs(landmarks[8].y - landmarks[4].y) < touch_threshold
        )
        
        Controller.middle_finger_within_thumb_finger = (
            abs(landmarks[12].x - landmarks[4].x) < touch_threshold and
            abs(landmarks[12].y - landmarks[4].y) < touch_threshold
        )
        
        Controller.little_finger_within_thumb_finger = (
            abs(landmarks[20].x - landmarks[4].x) < touch_threshold and
            abs(landmarks[20].y - landmarks[4].y) < touch_threshold
        )
        
        Controller.ring_finger_within_thumb_finger = (
            abs(landmarks[16].x - landmarks[4].x) < touch_threshold and
            abs(landmarks[16].y - landmarks[4].y) < touch_threshold
        )

    @staticmethod
    def get_position(hand_x_position, hand_y_position):
        """El pozisyonunu fare koordinatına çevir"""
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * Controller.screen_width)
        current_y = int(hand_y_position * Controller.screen_height)

        sensitivity = 1.5  # Hassasiyet ayarı
        
        if Controller.prev_hand is None:
            Controller.prev_hand = (current_x, current_y)
            return (old_x, old_y)
        
        delta_x = current_x - Controller.prev_hand[0]
        delta_y = current_y - Controller.prev_hand[1]
        
        Controller.prev_hand = [current_x, current_y]
        new_x = old_x + delta_x * sensitivity
        new_y = old_y + delta_y * sensitivity

        # Ekran sınırları içinde tut
        threshold = 5
        new_x = max(threshold, min(new_x, Controller.screen_width - threshold))
        new_y = max(threshold, min(new_y, Controller.screen_height - threshold))

        return (new_x, new_y)
        
    @staticmethod
    def cursor_moving():
        """Fare imlecini hareket ettir"""
        if Controller.hand_landmarks is None:
            return
            
        # Orta parmak ucu (landmark 9) pozisyonu kullan
        landmarks = Controller.hand_landmarks.landmark
        current_x, current_y = landmarks[9].x, landmarks[9].y
        x, y = Controller.get_position(current_x, current_y)
        
        # İmleci dondur (tüm parmaklar yukarı + başparmak aşağı)
        cursor_frozen = (Controller.all_fingers_up and Controller.thumb_finger_down)
        
        if not cursor_frozen:
            pyautogui.moveTo(x, y, duration=0)
    
    @staticmethod
    def detect_scrolling():
        """Kaydırma işlemlerini algıla"""
        # Yukarı kaydırma: sadece işaret parmağı yukarı, diğerleri aşağı
        scrolling_up = (Controller.index_finger_up and 
                       Controller.middle_finger_down and 
                       Controller.ring_finger_down and 
                       Controller.little_finger_down)
        
        if scrolling_up:
            pyautogui.scroll(3)  # Yukarı kaydır
            print("📜 Yukarı Kaydırma")

        # Aşağı kaydırma: sadece küçük parmak yukarı, diğerleri aşağı
        scrolling_down = (Controller.little_finger_up and 
                         Controller.index_finger_down and 
                         Controller.middle_finger_down and 
                         Controller.ring_finger_down)
        
        if scrolling_down:
            pyautogui.scroll(-3)  # Aşağı kaydır
            print("📜 Aşağı Kaydırma")
    
    @staticmethod
    def detect_zooming():
        """Yakınlaştırma/uzaklaştırma işlemlerini algıla"""
        # Zoom modu: işaret ve orta parmak yukarı, diğerleri aşağı
        zoom_mode = (Controller.index_finger_up and 
                    Controller.middle_finger_up and 
                    Controller.ring_finger_down and 
                    Controller.little_finger_down)
        
        if not zoom_mode:
            return
            
        landmarks = Controller.hand_landmarks.landmark
        distance = abs(landmarks[8].x - landmarks[12].x)  # İşaret ve orta parmak arası mesafe
        
        # Uzaklaştırma: parmaklar yakın
        if distance < 0.03:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-2)
            pyautogui.keyUp('ctrl')
            print("🔍 Uzaklaştırma")
        
        # Yakınlaştırma: parmaklar uzak
        elif distance > 0.08:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(2)
            pyautogui.keyUp('ctrl')
            print("🔍 Yakınlaştırma")

    @staticmethod
    def detect_clicking():
        """Tıklama işlemlerini algıla"""
        # Sol tık: başparmak + işaret parmağı temas
        left_click_condition = (Controller.index_finger_within_thumb_finger and 
                               Controller.middle_finger_up and 
                               Controller.ring_finger_up and 
                               Controller.little_finger_up and 
                               not Controller.middle_finger_within_thumb_finger and 
                               not Controller.ring_finger_within_thumb_finger and 
                               not Controller.little_finger_within_thumb_finger)
        
        if not Controller.left_clicked and left_click_condition:
            pyautogui.click()
            Controller.left_clicked = True
            print("👆 Sol Tık")
        elif not Controller.index_finger_within_thumb_finger:
            Controller.left_clicked = False

        # Sağ tık: başparmak + orta parmak temas
        right_click_condition = (Controller.middle_finger_within_thumb_finger and 
                                Controller.index_finger_up and 
                                Controller.ring_finger_up and 
                                Controller.little_finger_up and 
                                not Controller.index_finger_within_thumb_finger and 
                                not Controller.ring_finger_within_thumb_finger and 
                                not Controller.little_finger_within_thumb_finger)
        
        if not Controller.right_clicked and right_click_condition:
            pyautogui.rightClick()
            Controller.right_clicked = True
            print("👆 Sağ Tık")
        elif not Controller.middle_finger_within_thumb_finger:
            Controller.right_clicked = False

        # Çift tık: başparmak + yüzük parmağı temas
        double_click_condition = (Controller.ring_finger_within_thumb_finger and 
                                 Controller.index_finger_up and 
                                 Controller.middle_finger_up and 
                                 Controller.little_finger_up and 
                                 not Controller.index_finger_within_thumb_finger and 
                                 not Controller.middle_finger_within_thumb_finger and 
                                 not Controller.little_finger_within_thumb_finger)
        
        if not Controller.double_clicked and double_click_condition:
            pyautogui.doubleClick()
            Controller.double_clicked = True
            print("👆 Çift Tık")
        elif not Controller.ring_finger_within_thumb_finger:
            Controller.double_clicked = False
    
    @staticmethod
    def detect_dragging():
        """Sürükleme işlemini algıla"""
        # Sürükleme: tüm parmaklar aşağı
        if not Controller.dragging and Controller.all_fingers_down:
            pyautogui.mouseDown(button="left")
            Controller.dragging = True
            print("✋ Sürükleme Başladı")
        elif Controller.dragging and not Controller.all_fingers_down:
            pyautogui.mouseUp(button="left")
            Controller.dragging = False
            print("✋ Sürükleme Bitti")

    @staticmethod
    def detect_special_gestures():
        """Özel el hareketlerini algıla"""
        # ESC tuşu: başparmak + küçük parmak temas
        if (Controller.little_finger_within_thumb_finger and 
            Controller.index_finger_up and 
            Controller.middle_finger_up and 
            Controller.ring_finger_up):
            pyautogui.press('esc')
            print("⌨️ ESC Tuşu")
            time.sleep(0.5)  # Tekrar engellemek için bekle

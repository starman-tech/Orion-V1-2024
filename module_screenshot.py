#Finish

import pyautogui
import os
import cv2

class Picture : 
    def take_screenshot():
        """Capture un screenshot et retourne l'URL de l'image."""
        screenshot = pyautogui.screenshot()
        image_path = "screenshot.png"
        screenshot.save(image_path)
        return os.path.abspath(image_path)

    def take_photo():
        """Prend une photo avec la caméra et retourne l'URL de l'image."""
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            image_path = "photo.png"
            cv2.imwrite(image_path, frame)
            cam.release()
            return os.path.abspath(image_path)
        else:
            cam.release()
            raise Exception("Impossible de capturer l'image.")
        

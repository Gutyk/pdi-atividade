import cv2
import numpy as np

cap = cv2.VideoCapture("q1/q1A.mp4")

min_area = 2000

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Seu código aqui....... 
    blur = cv2.blur(frame, (50, 50))
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    lower_blue = np.array([50, 150, 50])
    upper_blue = np.array([140, 255, 255])
    
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    mask = cv2.bitwise_or(mask_red, mask_blue)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    if len(contours) > 0:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        max_contour = contours[0]
        second_contour = contours[1] if len(contours) > 1 else None
        
        frame_status = ""

        if second_contour is not None:
            x, y, w, h = cv2.boundingRect(max_contour)
            x2, y2, w2, h2 = cv2.boundingRect(second_contour)
            
            if (x < x2 + w2 and x + w > x2 and y < y2 + h2 and y + h > y2):
                frame_status = "COLISAO DETECTADA"
            elif x + w < x2:
                frame_status = "PASSOU BARREIRA"
        
        cv2.putText(frame, frame_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
    # Exibe resultado
    cv2.imshow("Feed", frame)
    
    # Wait for key 'ESC' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break


# That's how you exit
cap.release()
cv2.destroyAllWindows()

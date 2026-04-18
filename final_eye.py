import cv2
import numpy as np
import math

# 1. 讀取圖片 (使用你電腦裡正確的路徑)
img = cv2.imread(r"C:\Users\leoli\Downloads\messageImage_1776486987976.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. 載入 OpenCV 內建的「人臉」與「眼睛」模型
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# 3. 第一階段：先在大圖中找出「人臉」範圍
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

pupil_centers = []

for (x, y, w, h) in faces:
    # 擷取人臉區域 (ROI)
    roi_gray = gray[y:y+h, x:x+w]
    
    # 4. 第二階段：「只」在人臉區域內尋找「眼睛」
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    
    for (ex, ey, ew, eh) in eyes:
        # 擷取單顆眼睛的區域
        eye_roi_gray = roi_gray[ey:ey+eh, ex:ex+ew]
        
        # 使用高斯模糊降噪 (對應白板提示)
        blurred_eye = cv2.GaussianBlur(eye_roi_gray, (7, 7), 0)

        # 5. 第三階段：使用霍夫轉換找瞳孔圓形 (對應白板提示)
        circles = cv2.HoughCircles(blurred_eye, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                                   param1=50, param2=15, minRadius=3, maxRadius=int(eh/2))
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            i = circles[0, 0] 
            
            # 轉換回原始大圖的座標 (加上臉部和眼睛的偏移量)
            center_x = x + ex + i[0]
            center_y = y + ey + i[1]
            radius = i[2]
            
            pupil_centers.append((center_x, center_y))
            
            # 白板要求 1：圈出瞳孔範圍
            cv2.circle(img, (center_x, center_y), radius, (0, 255, 0), 2)  # 畫綠色外圈
            cv2.circle(img, (center_x, center_y), 2, (0, 0, 255), 3)      # 畫紅色圓心

# 6. 白板要求 2：計算瞳孔中心的距離
if len(pupil_centers) >= 2:
    # 確保由左至右排序，避免畫線交叉
    pupil_centers.sort(key=lambda pt: pt[0])
    pt1 = pupil_centers[0]
    pt2 = pupil_centers[1]
    
    # 畫藍線連接兩眼
    cv2.line(img, pt1, pt2, (255, 0, 0), 2)
    
    # 計算距離
    distance = math.dist(pt1, pt2)
    print(f"✅ 成功計算！瞳孔距離為: {distance:.2f} pixels")
    
    # 將距離寫在圖片左上角
    cv2.putText(img, f"Pupil Dist: {distance:.2f} px", (30, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
else:
    print("❌ 找不到足夠的瞳孔，請微調參數")

# 7. 顯示最終結果
cv2.imshow('Final Homework Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
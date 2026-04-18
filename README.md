# 嵌入式影像處理程式作業：人臉瞳孔偵測 👀

這是我在嵌入式課程中完成的影像處理作業，使用 OpenCV 來偵測人臉並定位瞳孔位置，最後計算出兩眼瞳孔的像素距離。

## 🌟 實作功能
* 使用 Haar Cascade 模型進行「人臉」與「眼睛」的兩階段過濾。
* 使用 Gaussian Blur (高斯模糊) 降低影像雜訊。
* 透過 Hough Transform (霍夫轉換) 精準找出瞳孔的圓形輪廓。
* 成功排除嘴巴、刺青等非眼睛特徵的誤判。

## 📸 展示成果
<img width="672" height="477" alt="messageImage_1776488312567" src="https://github.com/user-attachments/assets/2882d7ff-54a1-41df-9e97-dd8139b5f23b" />
<img width="678" height="452" alt="messageImage_1776486987976" src="https://github.com/user-attachments/assets/54e8b40a-4c84-48d9-89f9-31b9e9fa8c5a" />
## 💻 如何執行
1. 確認已安裝 `opencv-python` 與 `numpy`。
2. 執行 `final_eye.py` 即可看到標記結果。



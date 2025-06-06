## Python端代码（手势识别 + 串口通信）
import cv2
import mediapipe as mp
import serial
import time

print(mp.__version__)  # 打印MediaPipe版本号
# 初始化MediaPipe手部模型
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,  # 只检测一只手
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)

# 初始化串口 - 修改为你的Arduino端口
# Windows: 'COM3'或'COM4'等，在Arduino IDE中查看
# Mac/Linux: '/dev/tty.usbmodemXXXX' 或 '/dev/ttyACM0'
ser = serial.Serial('COM3', 9600)  # 波特率9600
time.sleep(2)  # 等待串口初始化

# 打开摄像头
cap = cv2.VideoCapture(0)  # 0代表默认摄像头

# 手势判断的阈值（可能需要根据实际情况调整）
PINCH_THRESHOLD = 0.05  # 捏合手势的阈值
OPEN_HAND_THRESHOLD = 0.15  # 张开手掌的阈值

# 存储上一次发送的指令，避免重复发送
last_command = None

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("忽略空摄像头帧")
        continue

    # 将BGR图像转换为RGB，并水平翻转（镜像）
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    # 绘制手部关键点
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 获取关键点坐标
            landmarks = hand_landmarks.landmark

            # 获取拇指尖(4)和食指尖(8)的位置
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]

            # 计算拇指和食指指尖的欧几里得距离
            distance = ((thumb_tip.x - index_tip.x)**2 +
                        (thumb_tip.y - index_tip.y)**2)**0.5

            # 获取手腕(0)和中指指尖(12)的位置（用于手掌张开判断）
            wrist = landmarks[0]
            middle_tip = landmarks[12]
            hand_open_distance = ((wrist.x - middle_tip.x)**2 +
                                  (wrist.y - middle_tip.y)**2)**0.5

            # 显示距离值（调试用）
            cv2.putText(image, f"Pinch: {distance:.3f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"Open: {hand_open_distance:.3f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 手势判断逻辑
            if distance < PINCH_THRESHOLD:
                cv2.putText(image, "GESTURE: TURN ON", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if last_command != '1':
                    ser.write(b'1')  # 发送开灯指令
                    last_command = '1'
                    print("发送指令：开灯")
            elif hand_open_distance > OPEN_HAND_THRESHOLD:
                cv2.putText(image, "GESTURE: TURN OFF", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if last_command != '0':
                    ser.write(b'0')  # 发送关灯指令
                    last_command = '0'
                    print("发送指令：关灯")
            else:
                # 清空上一次指令记录
                last_command = None

    # 显示图像
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:  # ESC键退出
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
ser.close()  # 关闭串口
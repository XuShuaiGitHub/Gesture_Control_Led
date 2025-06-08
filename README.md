# Gesture_Control_Led

## 📚 项目简介

Gesture_Control_Led 是一个基于 MediaPipe 和 Arduino 的手势识别控制系统，可以通过手势控制 LED 灯的开关。该项目包括 Python 端的手势识别和串口通信部分，以及 Arduino 端的 LED 控制逻辑。

## 📸 项目演示地址

```
Gesture_Control_Led/demo/gesture_control_led_arduino.mp4
Gesture_Control_Led/demo/gesture_control_led_python.mp4
```

## 🧩 项目结构

```
Gesture_Control_Led/
│
├── 📄 README.md
├── 🐍 gesture_detection.py
├── 🐍 gesture_control.py
├── 🎥 demo/
│   ├── gesture_control_led_arduino.mp4
│   └── gesture_control_led_python.mp4
└── 📦 arduino/
    └── 📦 led/
        └── 📄 led.ino
```

## 🛠️ 功能描述

- **手势识别**：
  
  - 使用 [MediaPipe](https://github.com/google/mediapipe) 进行手部关键点检测。
  - 支持以下两种手势：
    - 捏合手势（拇指和食指指尖距离小于阈值）：触发开灯操作。
    - 张开手掌（手腕与中指指尖距离大于阈值）：触发关灯操作。

- **串口通信**：
  
  - Python 程序通过串口将手势指令发送到 Arduino。
  - 开灯指令为字符 `'1'`，关灯指令为字符 `'0'`。

- **Arduino 控制**：
  
  - Arduino 接收串口指令并根据指令控制 LED 灯的开关。

## 🔧 硬件需求

| 设备               | 数量  | 说明            |
| ---------------- | --- | ------------- |
| Arduino Uno 或兼容板 | 1   | 主控设备          |
| LED 灯            | 1   | 建议使用限流电阻      |
| USB 数据线          | 1   | 连接电脑与 Arduino |
| 摄像头              | 1   | 电脑自带或外接摄像头    |

## 

## 🐍 软件依赖 (Python 端)

请确保安装以下 Python 库：

```bash
pip install opencv-python mediapipe pyserial
```

<mark>⚠</mark> 注意：python 版本不能太高，推荐 3.10 版本

---

## 📄 软件依赖（Arduino 端）

代码位于 `led/led.ino` 文件中，功能如下：

- 初始化串口通信（波特率 9600）
- 设置 LED 引脚为输出模式
- 根据串口指令控制 LED 状态

---

## 🚀 使用步骤

### 1. 上传 Arduino 代码

- 打开  `led/led.ino`  文件。
- 将 Arduino 板连接到电脑。
- 在 Arduino IDE 中选择正确的开发板和端口。
- 上传代码到 Arduino 板。

### 2. 运行 Python 程序

- 修改 [gesture_control.py](file://d:\MyProject\Ideas\Gesture_Control_Led\gesture_control.py) 中的串口端口号（如 `'COM5'`）以匹配你的 Arduino 端口。

- 运行程序：
  
  ```bash
  python gesture_control.py
  ```

### 3. 使用手势控制 LED

- 捏合手势：LED 亮起 ✅
- 张开手掌：LED 熄灭 ❌

---

## ⚙️ 注意事项

- 确保串口端口号正确配置（Windows 下为 `COMx`，Mac/Linux 下类似 `/dev/tty.usbmodemXXXX`）。
- 如果手势识别不灵敏，可以调整以下参数：
  - `PINCH_THRESHOLD = 0.05`（捏合判断）
  - `OPEN_HAND_THRESHOLD = 0.16`（张开判断）

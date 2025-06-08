// Arduino IDE 会自动包含所需的核心库，无需显式包含 Arduino.h

const int ledPin = 8; // 数字引脚8输出高低电平

void setup()
{
  // 初始化串口通信，波特率设置为9600（和Python端一致）
  Serial.begin(9600);

  // 设置LED引脚为输出模式
  pinMode(ledPin, OUTPUT);

  // 初始状态关闭LED
  digitalWrite(ledPin, LOW);
  Serial.println("Arduino已启动，等待指令...");
}

void loop()
{
  // 检查串口是否有数据可读
  if (Serial.available() > 0)
  {
    // 读取接收到的字节
    char command = Serial.read();

    // 根据命令控制LED
    if (command == '1')
    {
      digitalWrite(ledPin, HIGH); // 开灯
      Serial.println("收到指令: 开灯");
    }
    else if (command == '0')
    {
      digitalWrite(ledPin, LOW); // 关灯
      Serial.println("收到指令: 关灯");
    }

    // 添加短暂延时防止指令重复处理
    delay(20);
  }
}
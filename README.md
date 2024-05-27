# SP_Laboratory
XUPT 通信与信息工程学院 信号处理实验室 
## 序言
为促进实验室发展，制作该 ***《LabMem成长指南》***（全称《Labtorary Member 成长指南》）。希望这些学习资料能让各位倍感挑战的同时，少走一些不必要的弯路。
## 分类

### 软件部分

#### 一、语言学习

1. C语言
   1. 基础
   2. 数据结构之堆和栈的使用
   3. [位运算](https://blog.csdn.net/hzf0701/article/details/117359478)
   4. [践行“高内聚，低耦合”的设计思想](https://www.zhihu.com/question/347264877)
2. Python
   1. 基本逻辑判断
   2. 列表、字典
   3. 类的使用
   4. 正则表达式
   5. 数据结构之堆和栈的使用

#### 二、stm32学习
1. 基础知识常使用
   1. [C语言对寄存器的位操作](https://blog.csdn.net/qixjocd12345/article/details/108304967)
   2. [寄存器版本好还是库函数版本好](https://blog.csdn.net/qq_35656655/article/details/119850030)
2. IO口输入输出
   1. **目标：轮子正反转**
   2. [GPIO介绍](https://blog.csdn.net/qq_44016222/article/details/123206403)
   3. [GPIO端口的八种工作模式](https://blog.csdn.net/k666499436/article/details/123845466?spm=1001.2014.3001.5501)
3. 中断
   1. **目标：按键点灯**
   2. [概念和使用方法](https://blog.csdn.net/qq_43572058/article/details/114550295)
4. 定时器 + PWM 输出 
   1. **目标：使用舵机：90°为基准角，用按键控制角度增减**-
   2. [时钟_使能及应用总结](https://blog.csdn.net/he__yuan/article/details/78821355)\
   3. [舵机PWM计算](https://blog.csdn.net/weixin_45930808/article/details/119117499#t1)
5. IIC + UART 通讯
   1. **目标：上位机显示MPU6050数据**
   2. [I2C 通讯协议](https://doc.embedfire.com/module/module_tutorial/zh/latest/Module_Manual/iic_class/iic.html)
   3. [MPU6050模块介绍](https://doc.embedfire.com/module/module_tutorial/zh/latest/Module_Manual/iic_class/mpu6050.html)
   4. [MPU6050数据获取、分析与处理](https://zhuanlan.zhihu.com/p/20082486)
   5. [一阶滤波](https://blog.csdn.net/bhniunan/article/details/104592806)
   6. [卡尔曼滤波](https://blog.csdn.net/weixin_44020886/article/details/105985860)
6. A/D及D/A转换 + PID算法
   1. **目标：灰度循迹小车**
   2. [编码电机](https://blog.csdn.net/cyj972628089/article/details/112852960)
   3. [TB6612FNG驱动芯片](https://blog.csdn.net/cyj972628089/article/details/112851786)
   4. [PID算法](https://blog.csdn.net/weixin_45751396/article/details/119721939)
   5. [PID调参](https://blog.csdn.net/wb790238030/article/details/92809538)

#### 三、ESP32
>为什么要学ESP32和micropython？
   >>1. ESP32相比stm32f10x有更为优越的性能。国赛对芯片的最高要求为stm32f40x，ESP32的性能甚至优于stm32f40x。
   >>2. ESP32由国产公司乐鑫生产，价格便宜。
   >>3. micropython开发难度低，集成程度高，最适合此类“短时间、不计成本”类的比赛。
   >>4. ESP32内置WIFI及蓝牙模块，容易转型成为项目方向。

>为什么不一开始就学ESP32和micropython？
   >>如果开始就学esp32+micropython，入手难度过低，容易形成代码开发随意和硬件资源浪费的习惯，从长远的学习来看是不合适的   

1. 基础知识常使用 
   1. [micropython文档](http://micropython.com.cn/en/latet/index-2.html)
   2. [mpy_esp32快速参考](http://micropython.com.cn/en/latet/esp32/quickref.html)
   3. [ESP32搭载WROOM-32E模块_购买链接](https://item.taobao.com/item.htm?_u=u20e5ma4kq6aea&id=672885629326&spm=a1z09.2.0.0.51a42e8dUHKo8X+)
   4. [远程下载代码和调试](https://www.bing.com/search?q=thonny+webrepl&form=ANNTH1&refig=6630dcf206ee4588bcc5e1eb16eb747c&pc=U531&adppc=EDGEESS&pqasv=thonny+web&pqlth=10&assgl=14&sgcn=thonny+webrepl&sgtpv=UT&swbcn=10&smvpcn=0&cvid=6630dcf206ee4588bcc5e1eb16eb747c&clckatsg=1&hsmssg=0)
2. 项目方向
   1. mqtt协议
      1. **目标:使用阿里云平台实现公网点灯**
      2. [手把手教程](https://blog.csdn.net/weixin_42089940/article/details/123012744)
   2. TCP\IP协议
   >由于micropython语言的更新速度远远低于python（mpy的json库至今不支持中文解析），开发后期基本只把ESP32作为网络接口，主要代码开发都依赖python

#### 四、电赛常用外设学习
1. **外设使用原则：** 
   1. 能少用中断就少用中断
   2. 能少用外设就少用外设
   3. 能少接线就少接线
   4. 及格货 > 富贵货 > 垃圾货
   5. 资料丰富、开源完善 > 钱（串口通讯另说）
2. **常用外设库**
   1. 串口屏 
   3. 激光测距
   4. 编码电机
   5. [八路灰度模块](https://github.com/AVA022hallo/SP_Laboratory/blob/main/gray_soft_ii2.py)，[购买链接](https://item.taobao.com/item.htm?_u=r20e5ma4kqa85b&id=700000730878&spm=a1z09.2.0.0.33672e8dTJ1wCW)
#### 五、常用软件下载仓

### 硬件



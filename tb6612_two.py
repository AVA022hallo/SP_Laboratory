from machine import Pin,PWM
import time
# 定义两个电机控制引脚
left_pin1 = Pin(4, Pin.OUT)
left_pin2 = Pin(15, Pin.OUT)
right_pin1 = Pin(22, Pin.OUT)
right_pin2 = Pin(23, Pin.OUT)
# 初始化PWM输出以控制电机速度
left_pwm = PWM(Pin(12))
right_pwm = PWM(Pin(14))
def run(right_speed,left_speed):
    print("run_straight")
    left_pin1.value(1)
    left_pin2.value(0)
    left_pwm.duty(right_speed)
    right_pin1.value(1)
    right_pin2.value(0)
    right_pwm.duty(left_speed)
    
def turn_right(right_speed,left_speed):
    print("turn_right")
    left_pin1.value(1)
    left_pin2.value(0)
    left_pwm.duty(left_speed)
    right_pin1.value(0)
    right_pin2.value(1)
    right_pwm.duty(right_speed)
    
def turn_left(right_speed,left_speed):
    print("turn_right")
    left_pin1.value(1)
    left_pin2.value(0)
    left_pwm.duty(1000)
    right_pin1.value(0)
    right_pin2.value(1)
    right_pwm.duty(1000)

def stop():
    print("stop")
    left_pin1.value(0)
    left_pin2.value(0)
    left_pwm.duty(0)
    right_pin1.value(0)
    right_pin2.value(0)
    right_pwm.duty(0)

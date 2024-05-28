import time
from machine import Pin, SoftI2C

# I2C端口
I2C_BUS_NUM = 1

GW_GRAY_I2C_ADDR = 0x4C #0100 1100

scl_pin = Pin(17,Pin.IN,Pin.PULL_UP)
sda_pin = Pin(16,Pin.IN,Pin.PULL_UP)

def gray_init():
    i2c = SoftI2C(scl=scl_pin, sda=sda_pin, freq=1000)
    time.sleep(0.1)
    print(i2c.scan())
    begin_receive = bytearray()
    while begin_receive != bytearray([0x66]):
        print("begin")
        i2c.start()
        i2c.writeto(GW_GRAY_I2C_ADDR, bytearray([0xAA]))
        begin_receive = i2c.readfrom(GW_GRAY_I2C_ADDR, 1)
        print(begin_receive)
        i2c.stop()
        i2c.start()
        count = i2c.writeto(GW_GRAY_I2C_ADDR, bytearray([0xB0]))
        print(count)
        i2c.stop()
    return i2c
        
def gray_get(i2c):
    print(".")
    analog_data = bytearray(8)
    try:
        analog_data = i2c.readfrom(GW_GRAY_I2C_ADDR,8)
#         print(list(analog_data))
        return list(analog_data)
    except Exception as e:
        print("read_error")
            
if __name__ == '__main__':
    my_i2c = gray_init()
    while True :
        gray_value = gray_get(my_i2c)
        print(gray_value)

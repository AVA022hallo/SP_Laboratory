import time
from machine import Pin, SoftI2C

# I2C端口
I2C_BUS_NUM = 1

GW_GRAY_I2C_ADDR = 0x4F #0100 1100

scl_pin = Pin(5,Pin.IN,Pin.PULL_UP)
sda_pin = Pin(4,Pin.IN,Pin.PULL_UP)
                              
if __name__ == '__main__':
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
    while True:
        print(".")
        analog_data = bytearray(8)
        analog_data = i2c.readfrom(GW_GRAY_I2C_ADDR,8)
        print(list(analog_data))



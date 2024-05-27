#用于板球模型的寻球算法
import sensor, image, time
from pyb import UART
import json

yellow_threshold   = (89, 4, -21, 73, -25, 123)
ROI=(23,12,111,110)

v_x=1#x一阶滤波系数
v_y=1#y一阶滤波系数

final_x=0
final_y=0

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565. GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.

uart = UART(3, 115200)

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob

def filtering_x(spot_x):
    global final_x;
    final_x=v_x*spot_x +(1-v_x)*final_x
    return final_x

def filtering_y(spot_y):
    global final_y;
    final_y=v_y*spot_y +(1-v_y)*final_y
    return final_y

while(True):
    clock.tick()
    img = sensor.snapshot() # Take a picture and return the image.
    blobs = img.find_blobs([yellow_threshold],roi=ROI)
    img.draw_rectangle(ROI)
    if blobs:
        max_blob=find_max(blobs)
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        x=filtering_x(max_blob.cx())
        y=filtering_y(max_blob.cx())
        x=str("%03d"%max_blob.cx())
        y=str("%03d"%max_blob.cy())
        #spot=(x-1,y-1,2,2)
        #img.draw_rectangle(spot)

        position='B'+x+'M'+y+'E'
        print(position)
        uart.write(position)


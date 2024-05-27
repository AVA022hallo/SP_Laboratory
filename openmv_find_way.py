import sensor, image, time
from pyb import UART
from pyb import LED
enable_lens_corr = True # turn on for straighter lines...打开以获得更直的线条
#设置核函数滤波，核内每个数值值域为[-128,127],核需为列表或元组
kernel_size = 1 # kernel width = (size*2)+1, kernel height = (size*2)+1
kernel = [-1, -1, -1,\
          -1, +8, -1,\
          -1, -1, -1]
# 这个一个高通滤波器。见这里有更多的kernel
thresholds = [(0, 60)] # grayscale thresholds设置阈值
sensor.reset() # 初始化 sensor.
#初始化摄像头
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.RGB565
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.set_vflip(True)
sensor.set_hmirror(True)
#设置图像像素大小
sensor.skip_frames(10) # 让新的设置生效
# 注意:这将在以后作为一个函数实现
if (sensor.get_id() == sensor.OV7725):
    sensor.__write_reg(0xAC, 0xDF)
    sensor.__write_reg(0x8F, 0xFF)

min_degree = 0
max_degree = 179
theta_save_1 = 0
theta_save_2 = 0
error = 0
uart = UART(3, 115200)
while(True):
    save_flag = 0
    LED(1).on()
    LED(2).on()
    LED(3).on()
    img = sensor.snapshot() # 拍一张照片，返回图像
    img.morph(kernel_size, kernel)
    #morph(size, kernel, mul=Auto, add=0)，morph变换，mul根据图像对比度
    #进行调整，mul使图像每个像素乘mul；add根据明暗度调整，使得每个像素值加上add值。
    #如果不设置则不对morph变换后的图像进行处理。
    img.binary(thresholds)
    #利用binary函数对图像进行分割
    # Erode pixels with less than 2 neighbors using a 3x3 image kernel
    # 腐蚀像素小于2邻居使用3x3图像内核
    img.erode(1, threshold = 1)
    #侵蚀函数erode(size, threshold=Auto)，去除边缘相邻处多余的点。threshold
    #用来设置去除相邻点的个数，threshold数值越大，被侵蚀掉的边缘点越多，边缘旁边
    #白色杂点少；数值越小，被侵蚀掉的边缘点越少，边缘旁边的白色杂点越多。
    #threshold设置阈值
    # 更快更简单的边缘检测
    img.find_edges(image.EDGE_CANNY, threshold=(100, 255))
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...
    # `threshold` controls how many lines in the image are found. Only lines with
    # edge difference magnitude sums greater than `threshold` are dete0cted...

    # `threshold`控制从霍夫变换中监测到的直线。只返回大于或等于阈值的
    # 直线。应用程序的阈值正确值取决于图像。注意：一条直线的大小是组成
    # 直线所有索贝尔滤波像素大小的总和。

    # `theta_margin`和`rho_margin`控件合并相似的直线。如果两直线的
    # theta和ρ值差异小于边际，则它们合并。
    for l in img.find_lines(threshold = 4000, theta_margin = 90, rho_margin = 500):
        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            img.draw_line(l.line(), color = (255, 0, 0))
#            print(l.x1(),l.y1(),l.x2(),l.y2())
            theta_save_2 = theta_save_1
            theta_save_1 = l.theta()
            uart.write(str(l.theta())+'\n')#所得线条的角度值
            error = theta_save_1 - theta_save_2
            print(str(error)+ 'M' + str(l.theta()) + '\n')
    if abs(error) in range(85,95):
        print("拐角")
        #time.sleep(1)
    theta_save = []

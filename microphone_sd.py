#将音频采集并存储在sd卡内
import machine, sdcard, os
import uos,utime
from machine import SPI
from machine import Pin
#microphone
import urequests as requests
import ubinascii
import json
from machine import I2S
import time 

#wav格式文件头，必须生成否则无法播放和解析
def createWavHeader(sampleRate, bitsPerSample, num_channels, datasize):    
    o = bytes("RIFF",'ascii')                                                   # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                                   # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                                  # (4byte) File type
    o += bytes("fmt ",'ascii')                                                  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                              # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                               # (2byte) Format type (1 - PCM)
    o += (num_channels).to_bytes(2,'little')                                    # (2byte)#声道个数
    o += (sampleRate).to_bytes(4,'little')                                      # (4byte)
    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)#该数值为:声道数×采样频率×每样本的数据位数/8。播放软件利用此值可以估计缓冲区的大小。
    o += (num_channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)#采样帧大小。该数值为:声道数×位数/8。播放软件需要一次处理多个该值大小的字节数据,用该数值调整缓冲区。
    o += (bitsPerSample).to_bytes(2,'little')                                   # (2byte)#存储每个采样值所用的二进制数位数。常见的位数有 4、8、12、16、24、32
    o += bytes("data",'ascii')                                                  # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                        # (4byte) Data size in bytes
    return o

# 音频录制函数，调整record_seconds实现录音时长的改变
def record_audio(sample_rate=8000, bits_per_sample=16, buf_size=16384, record_seconds=5, file_path = "/sd/test_1.wav"):
    SD_CS = Pin(5)
    sd = sdcard.SDCard(SPI(2,sck=Pin(18), mosi=Pin(23),miso=Pin(19)), SD_CS)
    # 初始化⽂件系统
    vfs = os.VfsFat(sd)# fat挂载卡到⽬录下
    os.mount(sd,"/sd")# SD/sd
    #初始化I2C
    sck_pin = Pin(14)
    ws_pin = Pin(15)
    sd_pin = Pin(32)
    i2s = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin, mode=I2S.RX, bits=bits_per_sample,
              format=I2S.STEREO, rate=sample_rate, ibuf=buf_size)
    #休眠一点时间
    utime.sleep(2.0)
    print("* 开始录音，请说话...")
    #文件生成初始化
    if file_path in os.listdir():
        # 删除文件
        print('del', file_path)
        os.remove(file_path)
        time.sleep(0.5)
    file = open(file_path, 'wb')
    num_channels = 2 #声道个数
    start_time = time.time()
    readBuf = bytearray(buf_size)#音频数据读取缓冲
    f = True#标志位
    #生成wav文件头
    head = createWavHeader(sample_rate, bits_per_sample, num_channels, buf_size*record_seconds)
    print(head)
    file.write(head)
    print("in ready.......")
    while f:
        # 读取音频数据
        currByteCount = i2s.readinto(readBuf)
        print('in ', len(readBuf))
        audio_data = bytearray()
        audio_data.extend(readBuf)
        file.write(audio_data)
        # 检查是否到达文件时长
        if time.time() - start_time >= record_seconds:
            f = False
    file.close()
    print("* 录音结束")
    i2s.deinit()

record_audio()

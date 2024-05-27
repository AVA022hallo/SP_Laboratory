#microphone
import machine
import ubinascii
import json
from machine import I2S
from machine import Pin
import urequests as requests
import time 
#aduio_send
import network
import usocket
import wifi

#生成wav格式文件头
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
def record_audio(sample_rate=8000, bits_per_sample=16, buf_size=16384, record_seconds=3, file_path = "/sd/test_1.wav",ip = '192.168.0.15', port = 32666):
    #初始化I2C
    sck_pin = Pin(14)
    ws_pin = Pin(15)
    sd_pin = Pin(32)
    i2s = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin, mode=I2S.RX,bits=bits_per_sample, format=I2S.STEREO, rate=sample_rate, ibuf=buf_size)
    time.sleep(2.0)
    #UDP协议初始化
    socket_udp = usocket.socket(usocket.AF_INET,usocket.SOCK_DGRAM)  
    addr = usocket.getaddrinfo(ip, port)[0][-1]
    #wav生成初始化
    num_channels = 2 #声道个数
    readBuf = bytearray(buf_size)#音频数据读取缓冲
    head = createWavHeader(sample_rate, bits_per_sample, \
                           num_channels, buf_size*record_seconds)#生成wav文件头
    #开始录音
    socket_udp.sendto(head,addr)
    time.sleep(0.5)
    print("开始录音，请说话...")
    start_time = time.time()#计时开始
    while True :
        print(".",end=" ")
        # 读取音频数据
        i2s.readinto(readBuf)
        audio_data = bytearray()
        audio_data.extend(readBuf)
        socket_udp.sendto(audio_data,addr)
        # 检查是否到达文件时长
        if time.time() - start_time >= record_seconds:
            print(time.time() - start_time)
            break 
    print("**录音结束**")
    #录音结束
    i2s.deinit()
    socket_udp.close()
   
if __name__=="__main__":
    #连接WIFI
    wifi.WIFI_Init()   
    record_audio()


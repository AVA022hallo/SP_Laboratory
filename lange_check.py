import re
from machine import UART


class Lange:
    #初始化
    def __init__(self):
        self.lange_uart = UART(2, baudrate=115200, tx=17, rx=16)
        
    def lange_distance(self):
        while True:
            # 使用正则表达式匹配数字
            input_string = self.lange_uart.read()
            if input_string:
                pattern = r'd:\s*(\d+)\s*mm'
                match = re.search(pattern, input_string)
                if match:
                    # 提取匹配到的数字
                    extracted_number = int(match.group(1))
                    return extracted_number
                else:
                    return None

from machine import Pin,ADC
import time

class Grayscale:
    def __init__(self,pin):
        self.gray = ADC(Pin(pin))
        self.gray.atten(ADC.ATTN_11DB)
    def grayscale_get(self):
        adc_value = self.gray.read()
        time.sleep(0.01)
        return adc_value
             
if __name__ == "__main__":   
    gray1 = Grayscale(33)
    gray2 = Grayscale(34)
    while True:
        left_value = gray1.grayscale_get()
        right_value = gray2.grayscale_get()
        print(left_value,right_value)

import matplotlib.pyplot as plt
import numpy as np
import time
import time
import random
import math
import serial
from scipy import signal
from collections import deque


# Display loading
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_yac = deque(maxlen=max_entries)
        self.axis_y_mean = deque(maxlen=max_entries)

    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)  # 1,2,3,4,5
        self.axis_yac.append(y-np.mean(self.axis_y))
        self.axis_y_mean.append(np.mean(self.axis_y))  # 3,3,3,3,3


# initial
fig, (ax, ax2, ax3, ax4) = plt.subplots(4, 1)
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
plt.show(block=False)
plt.setp(line2, color='r')

PData = PlotData(500)
PData2 = PlotData(500)
PData3 = PlotData(500)
PData4 = PlotData(500)
ax.set_ylim(0, 500)
ax2.set_ylim(-2.5, 2.5)
ax3.set_ylim(-2.5, 2.5)
ax4.set_ylim(250, 1000)


# plot parameters
print('plotting data...')
# open serial port
strPort = 'com4'  # for my pc
# strPort = '/dev/cu.usbmodem143101'  # for mac

ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time() 
now_time = time.time()
avg_list = []
avg_avg_list = []
total_Of_avg = 0
total = 0
# calculate heart beats
beats = 0
first_beat = 1
while True:  # delete the noise
    for ii in range(10):
        try:
            data = float(ser.readline())
            PData.add(time.time()-start, data)
            PData4.add(time.time()-start, data)
            mean_value = np.mean(PData.axis_y)
        except:
            pass
    # print(time.time() - now_time)

    x = np.linspace(-50, 50, 500)
    if(len(PData.axis_x) >= 500):  # 超過500個點之後才開始移動
        PData3.axis_yac = signal.lfilter([1/15, 1/15, 1/15, 1/15, 1/15, 1/15, 1/15, 1/15, 1/15,
                                          1/15, 1/15, 1/15, 1/15, 1/15, 1/15], 1, PData4.axis_yac)  # three point average filter
        fft_data = np.fft.fftshift(np.fft.fft(PData3.axis_yac))

        ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        ax3.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        ax4.set_xlim(-50, 50)

        line.set_xdata(PData.axis_x)
        line.set_ydata(PData.axis_y)

        line2.set_xdata(PData.axis_x)
        line2.set_ydata(PData.axis_yac)

        line3.set_xdata(PData.axis_x)
        line3.set_ydata(PData3.axis_yac)

        line4.set_xdata(x)
        line4.set_ydata(abs(fft_data))

        fig.canvas.draw()
        fig.canvas.flush_events()

        # print("PData3.axis_y is :", PData3.axis_yac)
        for i in range(8, 491, 1):  # find for the maximum
            if(PData3.axis_yac[i] > PData3.axis_yac[i-1] and PData3.axis_yac[i] > PData3.axis_yac[i-2] and PData3.axis_yac[i] > PData3.axis_yac[i+2] and PData3.axis_yac[i] > PData3.axis_yac[i+1]):
                if(PData3.axis_yac[i] > PData3.axis_yac[i-3] and PData3.axis_yac[i] > PData3.axis_yac[i-4] and PData3.axis_yac[i] > PData3.axis_yac[i+3] and PData3.axis_yac[i] > PData3.axis_yac[i+4]):
                    if(PData3.axis_yac[i] > PData3.axis_yac[i-5] and PData3.axis_yac[i] > PData3.axis_yac[i+5] and PData3.axis_yac[i] > PData3.axis_yac[i-6] and PData3.axis_yac[i] > PData3.axis_yac[i+6]):
                        if(PData3.axis_yac[i] > PData3.axis_yac[i-7] and PData3.axis_yac[i] > PData3.axis_yac[i+7] and PData3.axis_yac[i] > PData3.axis_yac[i-8] and PData3.axis_yac[i] > PData3.axis_yac[i+8]):
                            beats = beats + 1
        if(first_beat == 1):
            catch_time = time.time() - now_time
            first_beat = 0

        #print("即時心律:", round(beats*60/catch_time, 2), "下/分鐘")
        avg_list.append(round(beats*60/catch_time, 2))
        total += round(beats*60/catch_time, 2)
        beats = 0
        if(len(avg_list) == 60):
            avg_avg_list.append(total/60)
            total_Of_avg += total/60
            if(len(avg_avg_list) == 5):
                print("即時心律(平均結果):", total_Of_avg/5, "下/分鐘")
                total_Of_avg = 0
                avg_avg_list = []
            print("即時心律:", total/60, "下/分鐘")
            avg_list = []
            total = 0

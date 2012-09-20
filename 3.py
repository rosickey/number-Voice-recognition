# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
num = 0
memo = []
def find_point(arr,imax):
    print len(arr),'long'
    for i in range(len(arr)):
        if arr[i] > imax*0.6:
            global num, memo
            num = num + 1
            memo.append(i)
            try:
                find_point(arr[i+9000:],imax)
            except:
                return memo
            return memo

RATE = 44
THRESHOLD = 150
full_shadow = 250
 
# 打开WAV文档
f = wave.open(r"Memo3.wav", "rb")
 
# 读取格式信息
# (nchannels, sampwidth, framerate, nframes, comptype, compname)
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
print  nchannels, sampwidth, framerate, nframes
# 读取波形数据
str_data = f.readframes(nframes)
f.close()
 
#将波形数据转换为数组
wave_data = np.fromstring(str_data, dtype=np.short)
wave_data.shape = -1, nchannels
wave_data = wave_data.T
time = np.arange(0, nframes) * (1.0 / framerate)

wave_data = wave_data/32768.0
imax = wave_data.max()

mmemo = find_point(wave_data[0],imax)

memo2 = []
for i in range(1,len(mmemo)+1):
    memo2.append(sum(mmemo[:i])+(i-1)*9000 )

print mmemo
print memo2
print wave_data.shape
#pl.plot(wave_data[0])
#pl.show()


plt.subplot(211)
plt.title('Amplitude Fig')
plt.ylabel('Amplitude')
plt.plot(time,wave_data[0])


plt.subplot(212)
plt.title('Numpy.fft Fig')
plt.ylabel('Frequency')
sf = abs(np.fft.fft(wave_data[0]))
plt.plot(time, sf)
sf.sort()
print sf[-1],sf[-90]
plt.xlabel('Time')
#plt.ylim(200,2500)

plt.show()
#plt.savefig("./static/img/test.png")

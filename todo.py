# -*- coding: utf-8 -*-
import web
import os
from web.contrib.template import render_mako
import time
import wave
import numpy as np
import matplotlib.pyplot as plt
#url映射配置


def con(a):
    f = wave.open(r"C:/py/soudn/static/img/"+"m"+a[0]+".wav",'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    wave_data = f.readframes(nframes)
    f.close()
    for i in range (1,a.__len__()):
        f = wave.open(r"C:/py/soudn/static/img/"+'m'+a[i]+'.wav','rb')
        nframes = nframes + f.getnframes()
        wave_data = wave_data + f.readframes(nframes)
        f.close()
    f = wave.open(r"C:/py/soudn/static/img/m"+a+".wav","wb")
    f.setnchannels(nchannels)
    f.setsampwidth(sampwidth)
    f.setframerate(framerate)
    f.setnframes(nframes)
    
    f.writeframes(wave_data)
    f.close()
    creat_img(a,wave_data,nchannels, sampwidth, framerate, nframes)
        
def creat_img(a,str_data,nchannels,sampwidth,framerate,nframes):
    #f = wave.open(r"C:/py/soudn/static/img/m"+a+".wav", "rb")
 
    # 读取格式信息
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    #params = f.getparams()
    #nchannels, sampwidth, framerate, nframes = params[:4]
    #str_data = f.readframes(nframes)
    #f.close()
    #将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, nchannels
    wave_data = wave_data.T
    time = np.arange(0, nframes) * (1.0 / framerate)

    wave_data = wave_data/32768.0
    
    plt.subplot(211)
    plt.title('Amplitude Fig')
    plt.ylabel('Amplitude')
    plt.plot(time,wave_data[0])

    plt.subplot(212)
    plt.title('Spectrogram Fig')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.specgram(wave_data[0], NFFT=1024, Fs=framerate, noverlap=400)
    plt.ylim(200,2500)
    plt.savefig("C:/py/soudn/static/img/m"+a+".png")
    

web.config.debug = True
urls = (
        '/','Index',
        '/callback','CallBack',
        '/logout','LogOut',
        '/updata','Updata',
)

app = web.application(urls, globals())
render = render_mako(
        directories=[os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )
        

class Index():
    def GET(self):
        #web.header("Content-Type", "text/html;charset=utf-8")
        a = time.time()
        return render.index(pic_list=a)
    def POST(self):
        data = web.input()
        print data['img']
        con(data['img'])
        time.sleep(1)
        creat_img(data['img'])
        time.sleep(0.5)
#apache        
#application = web.application(urls, globals()).wsgifunc()

if __name__=='__main__':
    #logger.debug("web.py服务开始启动……")
    #application.run() 
    app.run()

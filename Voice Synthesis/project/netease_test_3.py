#!/usr/bin/env python
# coding: utf-8

# In[2]:




####################################################################################
#                                作者：张潇                                          #
#                       邮箱：robert.zhanxiao@gmail.com                             #
#                               使用语言：Python                                     #
#                           初次提交日期: 2020/08/03                                 #
####################################################################################


import numpy as ny
import struct
import wave
import sounddevice as sd
import scipy.io.wavfile
from pippi import tune
from pippi import fx
from pippi import dsp


def write(self):
    # 参考：https://docs.python.org/3.6/library/wave.html#wave.Wave_write.setparams
    self.file.setparams( ( 1, 2, self.sr, 44100 * 4, 'NONE', 'noncompressed' ) )
    # 参考：https://docs.python.org/3.6/library/wave.html#wave.Wave_write.writeframes
    self.file.writeframes( self.signal )
    self.file.close()

# 参数设置
duration = 2 # 时间长短：  s
samplerate = 44100 # 采样频率： Hz
samples = duration * samplerate # 每秒aka采样数
frequency = 440 # Hz
period = samplerate / float( frequency ) # 周期
omega = ny.pi * 2 / period # 频率共轭
volume = 16384 # 音量大小，最高是32768
#参考：https://stackoverflow.com/questions/51079048/scipy-io-wavfile-write-no-sound    
    

################  创建并保存一个正弦波，输出为test.wav ###############
                                                                 #
                                                                 #
xaxis = ny.arange( samples, dtype = ny.float )                   #
ydata = volume * ny.sin( xaxis * omega )                         #
# blanks填充获取numpy数字信号                                       #
signal = ny.resize( ydata, ( samples, ) )                        #
scipy.io.wavfile.write('test.wav', samplerate, signal)           #
                                                                 #   
##################################################################



#读取test.wav文件
raw = dsp.read('test.wav')

##########  输入原先创建的正弦波，通过pippi创建一个C3调谐  ##############
                                                                  #  
freqs = tune.chord('I', key='C', octave=3, ratios=tune.just)      #
original_freq = tune.ntf('A1')                                    #
speeds = [ new_freq / original_freq for new_freq in freqs ]       #
pos = 0                                                           #
beat = 1.5                                                        #
out = dsp.buffer()                                                #
#参考：https://pippi.world/docs/tutorials/001-soundbuffers/        # 
for speed in speeds:                                              #
    # 创建原始输入文件音高偏移副本                                     #
    note = raw.speed(speed)                                       #
                                                                  #
    # 复制到输出缓冲区中                                             #
    out.dub(note, pos)                                            #
                                                                  #
    # 复制高八度副本                                                #
    note = raw.speed(speed * 2)                                   #
    out.dub(note, pos + 0.8)                                      #
                                                                  #
    # 将写入位置向前移动1.5秒                                        #
    pos += beat                                                   # 
###################################################################    

#输出结果至指定文件夹下，笔者所用的操作系统为MAC。                        
out.write('Documents/test_netease.wav')


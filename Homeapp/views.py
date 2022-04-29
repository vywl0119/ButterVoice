from pickle import NONE
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from pyrsistent import v
from .forms import UserForm
from django.contrib import auth
from django.contrib.auth.models import User
from Mainapp.models import counselor, customer
from django.core.serializers.json import DjangoJSONEncoder
import json

import numpy as np
import sounddevice as sd
import wave
from gtts import gTTS
import speech_recognition as sr
from threading import Thread
import threading
from keras.models import load_model
import os
import librosa
import pandas as pd

def role(request):
    return render(request, 'Home/role.html')

def home(request):

    return render(request, 'Home/home.html')

def home_type(request, type):

    return render(request, 'Home/home.html', {'type':type})

def logout(request, type):

    if type == 'co':
        del request.session['co_id']
        del request.session['co_name']
        del request.session['co_type']
    else:
        del request.session['cu_id']
        del request.session['cu_name']
        del request.session['cu_type']

    
    return redirect('/Home/home/')

def signin(request):

    if request.method == 'POST':

            id = request.POST.get('id')
            pw = request.POST.get('pw')
            type = request.POST.get('type')
            print("id = ",id )
            print("pw = ",pw )
            print("type = ",type )
        
            if type=='co':                
                user = counselor.objects.get(co_id = id, pw=pw)
                print(user.pw)
                request.session['co_id'] = user.co_id
                request.session['co_name'] = user.name
                request.session['co_type'] = 'co'

                return redirect('Mainapp:co_main')


            else:
                user = customer.objects.get(cu_id = id, pw=pw)   
                   
                request.session['cu_id'] = user.cu_id
                request.session['cu_name'] = user.name 
                request.session['cu_type'] = 'cu'
 
                return redirect('Mainapp:cu_main')
    else:
        return render(request, 'Home/signin.html')
        


def signups(request, type):

    return render(request, 'Home/signup.html', {'type' : type})

def signup(request):
    if request.method == 'POST':
        print('a')
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        profile = request.FILES.get('profile')
        print(profile)

        if profile:  
                profile_name = profile.name
                with open('config/static/image/profile/%s' % name, 'wb') as file:
                    for chunk in profile.chunks():
                        file.write(chunk)
                profile = profile_name

                # file_path = 'config/static/image/profile/'
                # file_names = os.listdir(file_path)  
                
                # for i in file_names:
                #     if profile == i:
                #         profile = '1'+profile 
                #         break

        print(type)
        print(id)

        if request.POST.get('type')=='co':
            category = request.POST.get('category')
            comment = counselor.objects.create(co_id=id, pw=pw, category = category, name=name, phone=phone, profile=profile)
            comment.save()

            return redirect('/Home/signin')

        else:
            comment = customer.objects.create(cu_id=id, pw=pw, name=name, phone=phone, profile=profile)
            comment.save()
            
            return redirect('/Home/signin')

def mike(request):
    th = Thread(target=work)
    th.start()
    return render(request, 'Home/mike.html')

def work():
    FILE_NAME = './config/static/test.wav'
    wave_length = 10
    sample_rate = 16_000

    # STT
    data = sd.rec(int(wave_length * sample_rate), sample_rate, channels=1)
    sd.wait()

    data = data / data.max() * np.iinfo(np.int16).max

    data = data.astype(np.int16)

    with wave.open(FILE_NAME, mode='wb') as wb:
        wb.setnchannels(1)
        wb.setsampwidth(2)
        wb.setframerate(sample_rate)
        wb.writeframes(data.tobytes())

    # 감정 인식
    pad2d = lambda a, i: a[:, 0: i] if a.shape[1] > i else np.hstack((a, np.zeros(a.shape[0], i-a.shape[1])))

    mfcc = get_mfcc(FILE_NAME, 20)
    mfcc_pad = pad2d(mfcc, 40)
    mfcc_2d = []
    mfcc_2d = np.expand_dims(mfcc_pad, -1)
    mfcc_2d = np.reshape(mfcc_2d, (1, 20, 40, 1))
    model = load_model('model.h5')
    y = model.predict(mfcc_2d)
    print(y)

    r = sr.Recognizer()
    harvard = sr.AudioFile('config/static/test.wav')
    with harvard as source:
        audio = r.record(source)
        try:
            stt_result = r.recognize_google(audio, language='ko_KR')
        except:
              stt_result = ""
          
        # 욕설 제거 필터링
        file_path='config/static/badwords.txt'

        with open(file_path, 'rt', encoding='UTF8') as f:
            insult = f.readlines()

        insult=[line.rstrip("\n") for line in insult]

        for i in range(len(insult)):
            word=insult[i]
            stt_result = stt_result.replace(f"{word}","")
            
        print(stt_result)

    # TTS
    if stt_result != "":
        if y.argmax(axis=1) == 1:
            kor_wav = gTTS(stt_result, lang='ko')
            kor_wav.save('config/static/test.wav')
        
        threading.Timer(0.5, work).start()
    else:
        print("## 대화 종료 ##")

def get_mfcc(filepath, n_mfcc = 40):
    sig, sr = librosa.core.load(filepath)
    D = np.abs(librosa.stft(sig, n_fft=int(sr*0.025), win_length=int(sr*0.01), hop_length=int(sr*0.01)))
    mfccs = librosa.feature.mfcc(S=librosa.power_to_db(D), sr=sr, n_mfcc=n_mfcc)
    return mfccs
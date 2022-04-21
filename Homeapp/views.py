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
        profile = request.POST.get('profile')
        
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

    data = sd.rec(int(wave_length * sample_rate), sample_rate, channels=1)
    sd.wait()

    data = data / data.max() * np.iinfo(np.int16).max

    data = data.astype(np.int16)

    with wave.open(FILE_NAME, mode='wb') as wb:
        wb.setnchannels(1)
        wb.setsampwidth(2)
        wb.setframerate(sample_rate)
        wb.writeframes(data.tobytes())

    r = sr.Recognizer()
    harvard = sr.AudioFile('config/static/test.wav')
    with harvard as source:
        audio = r.record(source)
        try:
            stt_result = r.recognize_google(audio, language='ko_KR')
        except:
            stt_result = ""
        print(stt_result)

    if stt_result != "":
        kor_wav = gTTS(stt_result, lang='ko')
        kor_wav.save('config/static/test.wav')
    
        threading.Timer(0.5, work).start()
    else:
        print("## 대화 종료 ##")
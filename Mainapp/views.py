from multiprocessing.dummy import current_process
from django.shortcuts import render, redirect
from Mainapp.models import counselor, customer, calling, point
from datetime import date, datetime, timedelta
from rest_framework import viewsets
from .serializers import customerSerializer, counselorSerializer
from .models import counselor, customer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

# Create your views here.

def cu_call(request, co_id, category):

    cu_id = request.session['cu_id']
    co_name = counselor.objects.get(co_id=co_id).name
    cu_name = customer.objects.get(cu_id=cu_id).name
 
    today = datetime.now().date()

    call = calling.objects.create(cu_id_id=cu_id, co_id_id=co_id, cu_name=cu_name, co_name=co_name, category = category, call_date = today)
    call.save()

    global num
    num = -1
    th = Thread(target=work)
    th.start()

    return render(request, 'Main/cu_call.html', {'co_name' : co_name, 'co_id':co_id, 'c_no':call.c_no, 'type':'cu'})

def co_call(request, c_no):

    # 해당 전화 내역
    call = calling.objects.get(c_no=c_no)

    if call.current == '대기':
        call.current = '통화중'
        call.save()

    # 전화를 건 고객 id
    cu_id = calling.objects.get(c_no=c_no).cu_id_id

    # 상담사 id
    co_id = calling.objects.get(c_no=c_no).co_id_id

    # 전화를 건 고객 정보
    cu = customer.objects.get(cu_id = cu_id)

    # 전화를 건 고객 상담 정보
    cu_call = calling.objects.filter(cu_id_id=cu_id)

    
    context = {'cu':cu,
               'cu_call':cu_call,
               'call':call,
               'type':'co',
               
    }


    return render(request, 'Main/co_call.html', context)

@csrf_exempt
def ajax_method(request, c_no):

    receive_message = request.POST.get('send_data')
    # call = calling.objects.get(c_no=c_no)
    send_message =  {
                'send_data' : "I received" 
    }
    return JsonResponse(send_message)




def call_update(request, c_no):

    if request.method == 'POST':
        print('a')
   
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        c_no = request.POST.get('c_no')

        call = calling.objects.get(c_no=c_no)
        call.title = title
        call.content = content
        call.save()
        
        
    return redirect('Mainapp:co_call', c_no=c_no )

def cu_main(request):

    total_co = counselor.objects.all()

    return render(request, 'Main/cu_main.html',{'total_co':total_co})


def category(request, category):

    total_co = counselor.objects.filter(category=category)

    return render(request, 'Main/cu_main.html',{'total_co':total_co})

def co_main(request):

    co_id = request.session['co_id']

    wait_call = calling.objects.filter(co_id=co_id,current='대기')

    today = datetime.today()

    today_call = calling.objects.filter(call_date=today, co_id_id=co_id)
    today_call = len(today_call)

    if wait_call:
    
        first_call = wait_call[0]
        wait_call = wait_call[1:]
        call_len = len(wait_call)
    else:
        first_call = ""
        call_len = 0

    

    context = {'wait_call': wait_call,
                'first_call': first_call,
                'call_len':call_len,
                'today_call':today_call,
                } 

    return render(request, 'Main/co_main.html', context)


def star(request, co_id, star, c_no):

    if star == 6:
        call = calling.objects.get(c_no=c_no)
        call.current = '종료'
        call.save()

    global num
    num = -999

    print(co_id, star)

    return render(request, 'Main/star.html', {'star' : star, 'co_id':co_id, 'c_no':c_no})


def stars(request, star, co_id):

    print(co_id, star)
    print(type(star))
    print(type(co_id))

      
    star = point.objects.create(co_id_id=co_id, star=star)                                                                                                                                                                                                                                                                                                                                                                                                         
    star.save()


    return redirect('Mainapp:cu_main')


def index(request):
    return render(request, 'Main/index.html')

def call(request):
    return render(request, 'Main/call.html')

def work():
    global num
    num += 1
    
    FILE_NAME = f'./config/static/wav/test_{num}.wav'
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
    y = model.predict(mfcc_2d).argmax(axis=1)
    print(y)

    r = sr.Recognizer()
    harvard = sr.AudioFile(f'config/static/wav/test_{num}.wav')
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
    if y == 1:
        kor_wav = gTTS(stt_result, lang='ko')
        kor_wav.save(f'config/static/wav/test_{num}.wav')
    
    if num >= 0:
        threading.Timer(0.5, work).start()

def get_mfcc(filepath, n_mfcc = 40):
    sig, sr = librosa.load(filepath)
    mfccs = librosa.feature.mfcc(sig)
    return mfccs

class customerViewSet(viewsets.ModelViewSet):
    queryset = customer.objects.all()
    serializer_class = customerSerializer

class counselorViewSet(viewsets.ModelViewSet):
    queryset = counselor.objects.all()
    serializer_class = counselorSerializer


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

# 고객 상담중 페이지
def cu_call(request, co_id, category):

    cu_id = request.session['cu_id']
    co_name = counselor.objects.get(co_id=co_id).name
    cu_name = customer.objects.get(cu_id=cu_id).name
 
    today = datetime.now().date()

    # 고객이 상담사 누르면 상담요청됨
    call = calling.objects.create(cu_id_id=cu_id, co_id_id=co_id, cu_name=cu_name, co_name=co_name, category = category, call_date = today)
    call.save()

    global num
    num = -1
    th = Thread(target=work)
    th.start()

    # 상담요청한 상담사의 프로필 사진
    profile = counselor.objects.get(co_id = co_id).profile

    return render(request, 'Main/cu_call.html', {'co_name' : co_name, 'co_id':co_id, 'c_no':call.c_no, 'type':'cu','profile':profile})

# 상담사 상담중 페이지
def co_call(request, c_no):

    # 해당 전화 내역
    call = calling.objects.get(c_no=c_no)

    # 상담사가 전화를 받았으니까 상담 상태는 통화중으로 변경
    if call.current == '대기':
        call.current = '통화중'
        call.save()

    # 전화를 건 고객 id
    cu_id = calling.objects.get(c_no=c_no).cu_id_id

    # 상담사 id
    co_id = calling.objects.get(c_no=c_no).co_id_id

    # 상담사 정보 이미지
    profile = counselor.objects.get(co_id = co_id).profile
    
    # 전화를 건 고객 정보
    cu = customer.objects.get(cu_id = cu_id)

    # 전화를 건 고객 상담 정보
    cu_call = calling.objects.filter(cu_id_id=cu_id)

    
    context = {'cu':cu,
               'cu_call':cu_call,
               'call':call,
               'type':'co',
               'profile':profile,
               
    }

    global v_num
    v_num = -1
    th = Thread(target=voice)
    th.start()

    return render(request, 'Main/co_call.html', context)

@csrf_exempt
def ajax_method(request, c_no):

    receive_message = request.POST.get('send_data')
    # call = calling.objects.get(c_no=c_no)
    send_message =  {
                'send_data' : "I received" 
    }
    return JsonResponse(send_message)


# 상담사가 상담정보 업데이트
def call_update(request):

    if request.method == 'POST':
   
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        c_no = request.POST.get('c_no')
        content = content.replace("\r\n", "<br>")

        call = calling.objects.get(c_no=c_no)
        call.title = title
        call.content = content
        
        call.save()
        
        
    return redirect('Mainapp:co_call', c_no=c_no )

# 고객 메인페이지
def cu_main(request):

    # 모든 상담사 정보
    total_co = counselor.objects.all()

    return render(request, 'Main/cu_main.html',{'total_co':total_co})

# 고객이 카테고리별로 상담사 확인
def category(request, category):

    # 해당 카테고리별 모든 상담사 정보 
    total_co = counselor.objects.filter(category=category)

    return render(request, 'Main/cu_main.html',{'total_co':total_co})

# 상담사 메인페이지
def co_main(request):
    global v_num
    v_num = -999

    co_id = request.session['co_id']

    # 상담사에 대기중인 콜 정보
    wait_call = calling.objects.filter(co_id=co_id,current='대기')

    today = datetime.today()

    # 오늘 상담사가 받은 모든 콜 수
    today_call = calling.objects.filter(call_date=today, co_id_id=co_id)
    today_call = len(today_call)

    # 첫번째로 대기중인 콜 과 나머지 대기콜 정보
    if wait_call:
        first_call = wait_call[0]
        wait_call = wait_call[1:]
        call_len = len(wait_call)

        # 통화 대기중인 고객의 정보
        profile_list = []
        for i in wait_call:
            profile_list.append(customer.objects.get(cu_id=i.cu_id_id).profile)

        user_call = []
        for i, j in zip(profile_list, wait_call):
            user_call.append([i,j])

    # 콜이 없을때 null 값으로 에러처리함
    else:
        first_call = ""
        call_len = 0
        user_call = ""

    # 첫번째 대기고객의 사진
    if first_call:
        profile = customer.objects.get(cu_id=first_call.cu_id_id).profile
    else:
        profile = ""
        

    


    context = {'wait_call': wait_call,
                'first_call': first_call,
                'call_len':call_len,
                'today_call':today_call,
                'user_call':user_call,
                'profile':profile,
                } 

    return render(request, 'Main/co_main.html', context)

# 별점 페이지 이동
def star(request, co_id, star, c_no):

    # 통화종료를 했을때 별점페이지로 왔기 때문에 통화상태 종료로 변경
    if star == 6:
        call = calling.objects.get(c_no=c_no)
        call.current = '종료'
        call.save()

    global num
    num = -999

    # 상담사 사진 정보
    profile = counselor.objects.get(co_id = co_id).profile
    print(profile)



    return render(request, 'Main/star.html', {'star' : star, 'co_id':co_id, 'c_no':c_no, 'profile':profile})

# 고객이 상담한 상담사 별점 부여
def stars(request, star, co_id):
 
    star = point.objects.create(co_id_id=co_id, star=star)                                                                                                                                                                                                                                                                                                                                                                                                         
    star.save()

    return redirect('Mainapp:cu_main')


def index(request):
    return render(request, 'Main/index.html')

def call(request):
    return render(request, 'Main/call.html')

def voice():
    global v_num
    v_num += 1
    
    FILE_NAME = f'./config/static/wav/voice_{v_num}.wav'
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

    if v_num >= 0:
        threading.Timer(0.5, voice).start()

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

@csrf_exempt
def call_current(request):
    c_no = request.POST.get('send_data')
    call = calling.objects.get(c_no=c_no)
    send_message = {'send_data' : call.current}
    return JsonResponse(send_message)


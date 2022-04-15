<br>

# 🎶 ButterVoice : CS 상담사를 위한 감정 필터링 서비스
> 2022.04.11 ~ 2022.05.13 KT AIVLE 전남/전북 2조 빅프로젝트<br>
>  *'ButterVoice'는 폭언과 협박과 같은 환경에 노출된 CS상담사를 위해 화자의 음성을 기반으로 감정을 분석하고 욕설이나 업무에 불필요한 단어들을 자동으로 필터링해서 들려주는 AI서비스입니다*

## 조원 소개
- `AI전남/전북1반 2조[18조]`
> 김보연(조장), 강가영, 유헤리, 정문경, 정수빈


## 목차
[1. 개발 배경 및 목적](#1-개발-배경-및-목적)

[2. 기능](#2-기능-및-UI/UX)

[3. 서비스 FLOW](#3-서비스-FLOW)

[4. 3 Tier Architecture](#4-3-Tier-Architecture)

[5. DB 설계](#5-DB-설계)

[6. 개발 환경](#6-개발-환경)

[7. 개발 일정](#7-개발-일정)

***

## 1. 개발 배경 및 목적
> 💡 **'AI기술을 통해 직접적인 폭언과 협박에 노출되어있는 CS상담환경을 바꾸기 위해 개발하게 되었다.'** 현재 고객 상담 서비스는 자동응답이나 AI서비스를 이용해 간단한 업무는 처리되고 있지만, 이러한 인공지능 서비스가 복잡한 고객의 요구를 듣고 해결하고자 하는 상담사의 역할을 완전히 대체하기엔 어려움이 있다. 하지만, 이러한 CS업무는 감정적으로 격양된 사람들을 직접적으로 대하는 일이다 보니 여전히 많은 상담사들은 감정노동으로 피로감을 느끼고 있고, 이로 인한 극단적 선택 등의 사회적인 문제가 공공연하게 일어나고 있다. 즉, 우리는 ButterVoice를 통해 기존의 상담환경에 혁신을 일으키고자 한다.

<br>

- 고객상담 시 언어적인 폭력으로 인한 감정노동 발생

<br>

- `기존 상담 시스템`
    - 자동 응답이나 AI챗봇을 통해서는 간단한 업무만 대체할 수 있음 
    - 여전히, 복잡한 고객의 요구사항은 사람(상담사)에 의해서 해결됨
    - 오프닝 멘트인 '지금 통화중인 상담사가 누군가의 가족입니다'로는 폭력적인 언어를 막을 수 없음
 
<br>

- 위와 같은 사항을 **보완**하기 위해 **Butter Voice**(버터 보이스)를 기획

<br>

- `🎶 ButterVoice`
  - 화자의 음성을 기반으로 감정을 분석
  - 감정상태가 격양되어있으면 상담사가 듣기 편한 목소리로 변조
  - 욕설이나 업무에 불필요한 단어들은 자동으로 필터링
  - 상담 내용을 자동으로 요약
  - 기존의 상담 환경을 긍정적으로 개선할 수 있을 것으로 예상

<br>


<br>

## 2. 기능 및 UI/UX
- `서비스 주요 기능`

<details>
  <summary>메인 화면</summary>
   <div markdown="1">       
     <br>
     <img src="https://user-images.githubusercontent.com/37900424/163407923-5b085483-b7b2-4fb6-85fc-dc8076a7eca9.png" width="740" height="412">
     <br>
     <text>⇒ 버터보이스의 홈화면으로 회원가입과 로그인을 할 수 있는 버튼이 있다</text>
   </div>
 </details>

 <details>
    <summary><strong>1) 고객과 상담사를 위한 회원가입/로그인</strong></summary>
        <div markdown="1">  
            <h3>📝 고객 회원가입</h3>
            <img src="https://user-images.githubusercontent.com/37900424/163437197-c1b98a8c-2a86-48f8-8eee-dcf6aaa2d562.png" width="700" height="412">
            <h3>📝 상담사 회원가입</h3>
            <img src="https://user-images.githubusercontent.com/37900424/163436261-80ec240a-bbaf-4665-9e6a-335ead82c907.png" width="700" height="412">
            <h3>🔒 로그인</h3>
            <img src="https://user-images.githubusercontent.com/37900424/163436370-506c899e-df35-4929-bdd4-900a752208b3.png" width="700" height="412">
        </div>
</details>
 
 <details>
  <summary><strong>2) 고객이 로그인 했을때 들어가는 고객 메인 페이지</strong></summary>
   <div markdown="1"> 
    <br>      
     <img src="https://user-images.githubusercontent.com/37900424/163409801-9a159360-4278-43cd-8f48-adf6dfd2cdf0.png" width="700" height="412">
     <br>
     <text>⇒ 고객이 상담할 수 있는 상담사를 선택해 상담을 신청할 수 있다</text>
   </div>
 </details>
 
 <details>
  <summary><strong>3) 고객이 상담사와 전화연결이 되었을때 나오는 페이지</strong></summary>
   <div markdown="1">
     <br>      
     <img src="https://user-images.githubusercontent.com/37900424/163410276-f70505e4-c0be-4872-9167-43ca654dba58.png" width="700" height="412">
     <br>
      <text>⇒ 상담 시 안내 문구와 고객이 상담을 종료하고 싶으면 누르는 상담 종료버튼으로 구성</text>
   </div>
 </details>
 
 <details>
  <summary><strong>4) 상담사와 상담이 종료된 후 상담사에 대한 별점을 줄 수 있는 기능</strong></summary>
   <div markdown="1">  
   <br>     
     <img src="https://user-images.githubusercontent.com/37900424/163410761-dd963844-9ba7-4e48-8900-bcf01fa5109c.png" width="700" height="412">
     <br>
     <text>⇒ 상담사에 대한 별점을 1~5까지 줄 수 있다</text>
   </div>
 </details>
 
 <details>
  <summary><strong>5) 상담사가 로그인했을 때 나오는 상담사 메인 페이지</strong></summary>
   <div markdown="1">
   <br>
     <img src="https://user-images.githubusercontent.com/37900424/163411003-8e0a4781-2630-44f4-9bd9-783288e0ce03.png" width="700" height="412">
     <br>
     <text>⇒ 상담사가 전화가 걸려온 순서대로 전화 대기자들을 확인 할 수 있다 </text>
   </div>
 </details>
 
 <details>
  <summary><strong>6) 상담사가 고객과 상담을 진행중에 나오는 페이지</strong></summary>
   <div markdown="1">  
     <br>
     <img src="https://user-images.githubusercontent.com/37900424/163416825-ec312508-4510-413b-87e5-ffc3a5471620.png" width="700" height="412">
     <br>
     <text>⇒ 고객 상담 메뉴얼, 고객의 기본 정보, 고객과 상담시 적는 상담내용글쓰기 부분으로 이루어져있다</text>
     <br>
   </div>
 </details>
 
 <details>
  <summary><strong>7) 관리자가 회원으로 등록된 고객과 상담사의 정보를 확인할 수 있는 게시판</strong></summary>
   <div markdown="1">    
     <br>
      <h3>📝 전체 게시판</h3>
     <img src="https://user-images.githubusercontent.com/37900424/163411263-e498edba-7ddb-4edc-b3a7-bfa816ad8229.png" width="700" height="412">
     <br>
      <h3>👩🏻‍🏫 상담사 상세정보</h3>
        <img src="https://user-images.githubusercontent.com/37900424/163411932-c621d148-9480-428c-9db0-8c07c226a6f7.png" width="700" height="412">    
       <h3>👩🏻 고객 상세정보</h3>
        <img src="https://user-images.githubusercontent.com/37900424/163412054-0467ba80-1b07-4e79-a5a4-d2e787ddcee8.png" width="700" height="412">
     <br>
     <text>⇒ 고객정보게시판/상담사정보게시판으로 이루어져있다</text>
   </div>
 </details>
 <br>

 - `AI 주요 기능`
 <details>
    <summary><strong>1) 화자의 음성을 기반으로 감정을 분석</strong></summary>
    <text>⇒ CNN 기반 전이 학습을 이용한 음성 감정 인식</text>
 </details>
  <details>
    <summary><strong>2) 감정 상태가 격양 되어있으면 듣기 편한 목소리로 변조</strong></summary>
    <text>⇒ 기가지니 API(지니 Voice) 사용</text>
 </details>
  <details>
    <summary><strong>3) 화자의 언어 중에서 욕설이 있으면 필터링</strong></summary>
    <text>⇒ STT/TTS + 필터링</text>
 </details>
  <details>
    <summary><strong>4) 상담 내용 요약본 정리</strong></summary>
    <text>⇒ 어텐션을 이용한 Text Summeraiztion</text>
 </details>
<br>

<br>

## 3. 서비스 FLOW
  - `주요 기능 Flow`
 ![서비스 흐름](https://user-images.githubusercontent.com/37900424/163581807-3685f275-c2bd-43ed-8bfc-b6feeabf1de5.png)
  - `서비스 Flow`
 ![서비스FLOW](https://user-images.githubusercontent.com/37900424/163585048-496805b3-e3aa-4597-9d7d-736b017ab9fe.png)
<br>

## 4. 3 Tier Architecture
 
 ![아키텍쳐](https://user-images.githubusercontent.com/37900424/163578007-4de44cbd-4a67-4b0a-b844-958384dfe695.png)


<br>

## 5. DB 설계
  - `ERD`
 
![erd](https://user-images.githubusercontent.com/37900424/163577340-6466295f-87a0-48de-86f5-54bfe0d9d057.png)


<br>


<br>

## 6. 개발 환경

- `Front-End`

  |HTML|CSS|JS|Bootstrap|
  |:---:|:---:|:---:|:---:|
  |![html](https://user-images.githubusercontent.com/68097036/151471705-99458ff8-186c-435b-ac5c-f348fd836e40.png)|![css](https://user-images.githubusercontent.com/68097036/151471805-14e89a94-59e8-468f-8192-c10746b93896.png)|![js](https://user-images.githubusercontent.com/68097036/151471854-e0134a79-b7ef-4a0f-99fd-53e8ee5baf50.png)|![bootstrap](https://user-images.githubusercontent.com/68097036/151480381-2b23a8af-c6b4-43a6-96a6-ea69e0b953e0.png)|


- `Back-End and Cloud`

  |Python|Django|MySQL|HeidiSQL|WebRTC|AWS|
  |:---:|:---:|:---:|:---:|:---:|:---:|
  |![pngwing com](https://user-images.githubusercontent.com/68097036/151479684-a85d26d4-e79e-47c9-9023-bf6d92f57536.png)|![pngwing com (1)](https://user-images.githubusercontent.com/68097036/151466729-9cad0405-85ad-454e-815a-1a4fd065f8b7.png)|![pngwing com (2)](https://user-images.githubusercontent.com/68097036/151466853-2b56fd0f-3aa9-424e-b17b-1c7cd991ffbf.png)|<img src="https://user-images.githubusercontent.com/68097036/151467351-5a359330-8d81-47b9-a33f-f7a5e0d69319.png" width="120" height="120">|![WEBRTC](https://user-images.githubusercontent.com/37900424/163582496-b5df138c-07de-4e0b-a1b9-cea03b4f0fc3.png)|![AWS](https://user-images.githubusercontent.com/37900424/163412651-7bc435ac-ce9b-4de0-add1-f12b9abbc606.png)|


- `Etc`

  |Summernote|VS Code|Microsoft Teams|GitHub|Notion|
  |:---:|:---:|:---:|:---:|:---:|
  |![brand_summernote_icon_157332](https://user-images.githubusercontent.com/68097036/151470431-2b196263-3c3f-425d-8fd0-0d6cf440e3d1.png)|<img src="https://user-images.githubusercontent.com/68097036/151479933-01785e34-1283-4fca-a407-9fe284b50fa8.png" width="220" height="100">|![pngwing com (4)](https://user-images.githubusercontent.com/68097036/151467837-2cd89acd-2a92-45dd-b06b-e08e316b7695.png)|<img src="https://user-images.githubusercontent.com/68097036/151467910-0fda00cd-c08b-4869-a21e-a66d1d133ff5.png" width="220" height="100">|<img src="https://user-images.githubusercontent.com/68097036/151468186-82e630d3-8c3c-4c75-8243-e1efcba34926.png" width="220" height="130">|

<br>

<br>

## 7. 개발 일정


<br><br><br>
###### Readme 템플릿 출처: 전남/전북1반 안지예

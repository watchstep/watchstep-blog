---
title: "[Docker] Let's get Dockered #1"
date: 2022-11-28T05:47:31+09:00
summary: 'Docker 이해하기'
draft: true
tags: ['Docker']
---
# Docker 이해하기

<cite>Let's get Dockered #1 세미나[^1]</cite>에서 배운 내용과 <cite>공식사이트[^2]</cite>과 <cite>타 블로그글 내용들[^3] [^4] [^5] [^6]</cite>을 토대로 작성한 블로그입니다.

[^1]: [Docker_1](https://drive.google.com/open?id=1SEihvIuKXQBCmSfifIYitb00HzvxKm8C&authuser=cathy033077%40gmail.com&usp=drive_fs)
[^2]: [Docker 공식 사이트](https://docs.docker.com/get-started/overview/)
[^3]: [[MLOps] Docker Basics / Images & Containers / Managing Images & Containers](https://yai-yonsei.tistory.com/33)
[^4]: [도커와 컨테이너의 이해 (1/3) - 컨테이너 사용법](https://tech.cloudmt.co.kr/2022/06/29/%EB%8F%84%EC%BB%A4%EC%99%80-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98-%EC%9D%B4%ED%95%B4-1-3-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88-%EC%82%AC%EC%9A%A9%EB%B2%95/)
[^5]: [Docker(도커)란?](https://www.redhat.com/ko/topics/containers/what-is-docker#%EB%8F%84%EC%BB%A4%EC%99%80-%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98-%EC%B0%A8%EC%9D%B4%EC%A0%90)
[^6]: [LXC vs Docker: Which Container Platform Is Right for You?](https://earthly.dev/blog/lxc-vs-docker/)

## 1. What is Docker?

<p align='center'>
<img src='https://blog.kakaocdn.net/dn/m6Ewm/btrGARnEozl/20MGhSGanrhXK1nx1YO6Z0/img.png' width =200>
</p>

**Docker**는 **Container** 를 생성하고, 사용할 수 있는 컨테이너화(Containerization) 기술이다. Docker는 소프트웨어 서비스를 실행하는 데 필요한 애플리케이션와 모든 종속성을
Container라는 표준화된 소프트웨어 단위로 패키징하여 애플리케이션을 인프라에 관계없이 어떤 환경에서나 항상 동일하게 실행되도록 한다. 컨테이너화 기술을 통해
더 빠르고, 효율적으로 소프트웨어를 개발, 배포할 수 있다.

## 2. What is Container?

### 2-1. What is Container?

### 2-2. VM(Virtual Machine)  vs Container

<p align='center'>
<img src='https://www.sdxcentral.com/wp-content/uploads/2019/05/ContainersvsVMs_Image-1.jpg' width =800>
</p>

<p align='center'>
<img src='https://earthly.dev/blog/assets/images/lxc-vs-docker/EUXeGou.png' width =800>
</p>

Host Virtualizaion(호스트 가상화)는 Host OS 위에 Guest OS가 구동되는 방식으로, Host OS의 종류에 큰 제약이 없지만, OS 위에 OS가 올라가기 때문에 overhead가 클 수 있다.
VM(Virtual Machine)는 Host OS 없이 하드웨어에 Hypervisor(하이퍼바이저)를 설치하고, Hypervisor 위에 Guest OS가 올라간다.

같은 os에서 docker engine에 의해 프로세스 격리
컨테이너는 가상 머신과 마찬가지로 애플리케이션 실행에 필요한 모든 것들을 패키징해 소프트웨어 서비스 구동을 위한 격리 환경을 마련해준다는 공통점이 있다.

- Container가 VM보다 훨씬 더 가볍다.

- Container는 OS 수준에서 가상화되고 VM은 하드웨어 수준에서 가상화된다.
컨테이너는 하나의 OS 커널을 공유하며 VM에 필요한 것보다 훨씬 적은 메모리를 사용한다.

컨테이너는 코드와 종속성을 함께 패키지하는 앱 계층의 추상화입니다. 여러 컨테이너가 동일한 컴퓨터에서 실행되고 OS 커널을 다른 컨테이너와 공유할 수 있으며, 각 컨테이너는 사용자 공간에서 격리된 프로세스로 실행됩니다. 컨테이너는 VM(컨테이너 이미지의 크기는 일반적으로 수십 MB)보다 공간을 덜 차지하고, 더 많은 애플리케이션을 처리할 수 있으며, 더 적은 VM 및 운영 체제가 필요합니다.

VM(가상 머신)은 하나의 서버를 여러 서버로 전환하는 물리적 하드웨어의 추상화입니다. 하이퍼바이저를 사용하면 단일 컴퓨터에서 여러 VM을 실행할 수 있습니다. 각 VM에는 운영 체제, 애플리케이션, 필요한 바이너리 및 라이브러리의 전체 복사본이 포함되어 있으며 수십 GB를 차지합니다. VM 부팅 속도가 느릴 수도 있습니다.

가상화가 하드웨어 수준에서 발생하는 VM(가상 머신)과 달리 컨테이너는 앱 계층에서 가상화됩니다. 하나의 시스템을 활용하고, 커널을 공유하고, 운영 체제를 가상화하여 격리된 프로세스를 실행할 수 있습니다. 따라서 컨테이너가 매우가벼워져 귀중한 리소스를 유지할 수 있습니다.
### 2-3. LXC(LinuX Container) vs Docker

## 3. Why We need Docker?

## 4. What is Image?

**Image**는 Docker Container를 만드는 데 사용되는 Read-Only 템플릿이다. (Read-Only Not Write이므로, 변경 불가능함) 애플리케이션을 실행하는 데 필요한 모든 파일을 포함한 Docker file를 빌드해 Image를 생성한다. Image는 런타임일 때, Container가 된다. 즉, Container는 Docker Engine에서 실행한 Image이다. 

이해를 돕기 위해 Image를 붕어빵 틀, Container를 붕어빵으로 비유해보자.

<p align='center'>
<img src='https://kyh0703.github.io/assets/images/posts/2021-09-07-post-docker-dockerfile/image-20210907220417524.png' width =500>
</p>

한 개의 붕어빵 틀로 여러 개의 붕어빵을 만들 수 있는 것처럼, 한 번 빌드한 Image로 여러 Container를 생성할 수 있다.

<p align='center'>
<img src='https://belowthemalt.files.wordpress.com/2021/12/image.png' width =500>
</p>

Image 붕어빵 틀로 만들어진 Container 붕어빵은, 변경 불가능한 image layer 위에 Read-Write가 가능한 container layer가 추가되어 변경할 수 있게 된다.

컨테이너 layer 저장
그리고, 이미 만든 붕어빵은 붕어빵 틀이 변해도 동일한 것처럼
이미지가 변경되어도, 이미 만들어진 컨테이너에 영향을 미치지 않음

서비스 운영환경을 묶어 SW를 배포하고 실행하는 경량 컨데이너 기술
격리하는 공간
독립된 가상 공간,
애플리케이션 구동에 필요한 SW를 격리해 담을 수 있는 것
각각 격리된 상태 => 여러 대의 서버를 쓰는 것과 같은 효과

컨데이너화된 SW들은 어떤 서버 환경에서도 모두 동일하게 동작
How?
image 덕분
실행하는 데 필요한 SW 설정값 담고 있는 파일
docker hub 이미지 공유 사이트, 개인 저장소에 저장 가능

새로운 앱을 컨데이터에 올리면 앱 구동에 필요한 이미지 다운받아 함께 실행
자동화

Kubernetes 컨테이너 재가동
코드 수정 자동화
docker가 만들어준 컨데이터 운영 자동화해줌
k8 (k와 s를 제외한 알파벳 개수가 8개라서)

화물운송에서 사용되는 컨데이너
컨데이너 애플리케이션을 실행하기 위한 컴퓨팅 작업을 패키징

이동성, 인프라로 쉽게 이동

컨테이너 기반의 가상화 방식
긱 app에 os를 개별로 구성해줄 필요 없이 하나의 os 커널  공유해 사용
os 필요하지 않아 더 가볍고 크기도 작아 복제, 배포에 간편
애플리케이션 실행에 필요한 모든 거ㅅ을 패키지로 묶어 컨테이너 이미지를 만들어 사용해서

- 경량화 게스트 os 미포함
- 효율성 호스트 os 커널을 공유하므로, 자원 미리 할당하지 않고, 애플리케이션 동작에 필요한 컴퓨팅 자원만 필요
- 이식성 컨테이너가 작동하는 환경이라면, 어디든지 작동가능
- 안정성 호스트 os 커널을 공유하는 구조로 장애 발생 시, 다른 컨테이너들이 영향을 받을 수 있습니다.

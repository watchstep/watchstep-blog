---
title: "📝 DL 인터뷰 질문 답변 모음"
date: 2023-03-07T10:30:17+09:00
summary: 남세동 대표님의 딥러닝 인터뷰 질문에 대한 답변 모음
draft: true
tags: ['dl', 'interview']
contributors: []
---
<cite>남세동 대표님 : 딥러닝이라는 주제에 대해서 개발자 면접[^1]</cite>에서 나온 질문을 주제로 작성된 블로그입니다.

[^1]: [개발자 인터뷰 질문 및 답변 모음집 : 남세동 대표님 : 딥러닝이라는 주제에 대해서 개발자 면접](https://github.com/RRoundTable/Developer_interview)

## Gradient Descent란?

Gradient Descent (경사하강법)은 최적값을 찾기 위한 방법으로, 미분을 활용한다.
미분을 통해 함수, 즉 loss function의 기울기 (경사)를 계산하고, 하강하면서 최솟값을 찾는 알고리즘이다. 이때, loss function은 예측값과 실제값 사이의 오차를 표현한 함수이다. 손실 함수 (loss function)은 비용 함수 (cost function)로 불리기도 한다.

1. 임의의 초기값 선택
2. 현재 위치에서 함수의 기울기 (경사) 계산
3. 기울기가 낮은 쪽으로 이동
4. 최솟값에 도달할 때까지 2, 3 단계 반복

## local minimum에도 불구하고 딥러닝 학습이 잘 되는 이유는?

<cite>2014년 논문Identifying and attacking the saddle point problem in high-dimensional non-convex optimization[^2]</cite>에 의하면,
- local minimum 문제는 고차원 공간에서 발생하기 어려운 문제이다.
- 딥러닝 모델에는 많은 weight가 있는데, 해당 weight들이 모두 local minimum에 빠져야 weight update가 되지 않으므로, 큰 문제가 되지 않는다.

[^2]: [Identifying and attacking the saddle point problem in high-dimensional non-convex optimization](https://arxiv.org/abs/1406.2572)

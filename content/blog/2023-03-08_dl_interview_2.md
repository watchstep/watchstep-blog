---
title: "📝 Gradient Descent란?"
date: 2023-03-08T15:34:47+09:00
summary: 남세동 대표님의 딥러닝 인터뷰 질문에 대한 답변 모음
draft: true
tags: ['DL', 'Interview']
contributors: []
---
## Gradient Descent란?

Gradient Descent (경사하강법)은 최적값을 찾기 위한 방법으로, 미분을 활용한다.
미분을 통해 함수, 즉 loss function의 기울기 (경사)를 계산하고, 하강하면서 최솟값을 찾는 알고리즘이다. 이때, loss function은 예측값과 실제값 사이의 오차를 표현한 함수이다. 손실 함수 (loss function)은 비용 함수 (cost function)로 불리기도 한다.

1. 임의의 초기값 선택
2. 현재 위치에서 함수의 기울기 (경사) 계산
3. 기울기가 낮은 쪽으로 이동
4. 최솟값에 도달할 때까지 2, 3 단계 반복

### Batch Gradient Descent

전체 데이터셋

### Stochastic  Gradient Descent


## 왜 꼭 Gradient를 써야 할까?


## 그 그래프에서 가로축과 세로축 각각은 무엇인가?
ㅇ

## 실제 상황에서는 그 그래프가 어떻게 그려질까?
ㅇ

## GD 중에 때때로 Loss가 증가하는 이유는?

## 더 쉽게 설명 한다면?

## Back Propagation에 대해서 쉽게 설명 한다면?

## Local Minima 문제에도 불구하고 딥러닝이 잘 되는 이유는?

## GD가 Local Minima 문제를 피하는 방법은?

## 찾은 해가 Global Minimum인지 아닌지 알 수 있는 방법은?

질문: grad = -np.transpose(expand_x) @ error 에 -가 붙은 이유 설명가능할까요?

답변: 가중치 벡터를 업데이트할 때, 현재 가중치 벡터에서 gradient를 빼는 과정에서 사용하는 기법 중 하나입니다.
그래서 error의 값이 양수이면 gradient의 값이 음수가 되어 최솟값 방향으로 이동하도록 합니다.!

질문: wx_grad에서 np.sum() 을 꼭 써야하나요?

답변: 말씀하신대로 np.sum이 없어도 괜찮습니다 !
grad_over_time, X, S 모두 shape이 (n_samples, len_sequence+1)이기 때문에, 각 요소 별 곱셈을 수행한 후에는 np.mean을 사용하지 않고 np.sum으로 모든 값을 더해도 차이가 없습니다.

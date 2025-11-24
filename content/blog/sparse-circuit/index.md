---
title: "🕵️ Understanding neural networks through sparse circuits (OpenAI, 2025-11-13)"
description: "Interpreting LLM with sparse circuits."
summary: ""
date: 2025-11-24T17:06:43+09:00
lastmod: 2025-11-24T17:06:43+09:00
draft: true
weight: 50
categories: []
tags: ['OpenAI', 'Safety', 'Interpretability', 'Sparse Circuit']
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
[**Understanding neural networks through sparse circuits**](https://openai.com/index/understanding-neural-networks-through-sparse-circuits/)

블랙박스 AI 모델이 내부적으로 어떻게 작동하는지 이해하기 위해 OpenAI는 애초에 **희소한(Sparse) 구조**로 훈련하고, 그 안에서 **희소 회로(Sparse Circuit)**를 찾아내 모델을 설명하는 접근법을 공유했다.

## Mechanistic Interpretability and SAE

Mechanistic Interpretability (기계론 적 해석 가능성)는 모델 내부의 연산을 구조적으로 이해하겠다는 분야다. 최근 Mechanistic Interpretability 분야에서에서 SAE(Sparse Autoencoder)가 큰 주목을 받고 있다.

최근 발표된  [**A Survey on Sparse Autoencoders: Interpreting the Internal Mechanisms of Large Language Models](https://arxiv.org/abs/2503.05613)**  서베이 논문에서는 SAE가 중첩(Superposition)된 feature를 더 해석 가능한 요소로 분리하는 유용한 도구로 설명한다.

[SAE Bench](https://github.com/adamkarvonen/SAEBench)  벤치마크는 이런 SAE를 평가하기 위한 벤치마크이다.

① 기존 모델의 성능을 저하하지 않으면서 → Reconstruction(재구성) 성능, 압축 후 복원했을 때 모델의 원래 성능이 얼마나 떨어지는지 측정. (**CE Loss**)

② 최소한의 뉴런만 사용하고 → Sparsity(희소성) 평가. ( **$L0$ Norm**)

③ 각 뉴런의 의미가 명확한지를 평가 → Interpretability(해석 가능성) 평가. (**Automated Interpretability**)

Anthropic의 ‘Golden Gate’ 실험은 이러한 LLM Interpretability 연구의  대표 예다. Claude 3 Sonnet 모델 내부에서 “Golden Gate Bridge” 개념을 담당하는 특정 feature 조합을 찾은 것이다. Golden Gate 사진 또는 이를 언급할 때마다  특정 뉴런 조합이 activate(활성화)되는 것이다.  activation 강도를 높이면 질문과 상관없이 계속 Golden Gate를 언급하는 경향을 보였다. 이는 단순히 프롬프트 조작을 넘어 모델 내부를 이해하고 직접 조작할 수 있다는 가능성을 열어줬다.

Top-K SAE는  activation 값이 큰 Top-K개의 뉴런만 남기고 나머지는 모두 강제로 0으로 만든 것이다. [Neuronpedia](https://www.neuronpedia.org/) 사이트에서 여러 SAE를 시각적으로 확인하고, 어떤 input token이 어떤 feature를 켜는지 확인할 수 있다.

$The dog says "bow wow" , and the cat says$ 를 입력했을 때 그 다음에 $meow$ 가 어떻게 나오는지를 보여준다.

<img src="https://github.com/user-attachments/assets/044aae56-2394-436a-8174-c3b34678a005" alt="image" style="width:100%;height:auto;" />

<img src="https://github.com/user-attachments/assets/4b4d8ecb-aa02-4abc-9e09-43856c40d156" alt="image" style="width:30%;height:auto;" />

## Disentangle

Disentangle은 말 그대로 Dis + entangle로 얽힌 것을 푸는 것이다. LLM Intrepretability 관점에서 Disentangle은 예를 들어 ‘여러 재료가 들어가 무슨 맛인지 알 수 없는 스무디에 어떤 과일이 들어갔는지’ 판단하는 과정이다.

### Polysemanticity → Monosemanticity

더 전문적으로 말하자면, Polysemanticity에서 Monosemanticity로 얽힌 것을 풀어 하나의 뉴런이 하나의 의미만 갖도록 하는 것이다. (Disentanglement)

LLM 내부의 뉴런들은 대부분 Superposition(중첩)되어 있다. 방대한 지식을 한정된 뉴런; 모델에 욱여넣어야 하기에 압축해 주입한다. 그래서 서로 관련 없는 개념인데도 하나의 뉴런에 중첩(Superposition)되어 있는 것이다. 이처럼 얽혀 있으므로, 하나의 뉴런만 보았을 때 무슨 기능을 하는지, 어떤 의미를 파악하는지 분명하게 알 수 없다. 그러므로 Polysemantic(다의적인) 뉴런을 Monesemantic(단일 의미)한 상태로 만드는 것이 필요하다.

## SAE and Sparsity

Polysemanticity → Monosemanticity로 disentangle하기 위해  SAE(Sparse Autoencoder)를 활용할 수 있다. 저차원애서 고차원 공간으로 매핑하여 중첩된 의미들을 분리하는 것이다.

빽빽하게 밀집(dense)되어 있는 것을 고차원 공간으로 넓 펼쳐서(sparse) 특정 개념을 제일 잘 설명하는 특정 뉴런이 되도록 돕는다.  이를 통해 블랙박스 내부를 이해하고 조작하는 것을 기대할 수 있다.

예를 들어 “폭탄”과 같이 위험한 내용을 담는 뉴런을 0으로 만들어 안전한 AI 모델이 되도록 모델 행동을 조작할 수 있다.

# 1/ Chain of Thought Interpretability 한계

CoT(Chain of Thought) 프롬프팅 기법을 사용해 모델의 행동을 모니터링할 수 있다. 즉각적인 모니터링 도구로  유용하지만, 모델이 고도화될수록 인간을 속이거나 겉으로만 그럴 듯하게 대응할 수 있기에  깨지기 쉬운 전략 (*brittle strategy*)이라고 한다.

궁극적으로 내부 모델 구조를 직접 이해하는 Mechanistic Interpretability가 필요하다는 입장을 밝혔다.

# 2/ Dense Model vs. Sparse Model

기존에는 Pre-trained Dense Model에서 Pruning을 사용해 특정 작업을 수행하는 데 필요한 최소한의 경로인 Circuit(회로)를 찾고자 했다. 그러나 OpenAI의 이번 연구에서는 “애초에 모델을 Sparse하게 만들면 어떨까?”라는 의문을 던졌다.

***“사후에 해석하려고 애쓰지 말고, 애초에 해석하기 쉽도록 Spare Model을 만들면 안되나?”***

## Pruninng : “사후” Sparsity 강제

Pruning은 흔히 Model Optimization(모델 최적화, 경량화)에서 많이 사용되는 방식으로, **사후에** weight(가중치)를 0으로 만드는 등 가지치기하여 모델을 효율화하는 것이다.  반면, OpenAI의 해당 연구에서는 특정 작업을 수행하는 데 정말 필수적인 최소한의  Subgraph; Circuit(회로)를 찾고 나머지 연결은 모두 가지치기한다.

## Sparsity Constraint : “사전” Sparsity 강제

<img src="https://github.com/user-attachments/assets/8cbe6b6a-57ba-43cb-a3d1-4453d2bd1db6" alt="image" style="width:80%;height:auto;" />

Sparse Constraint는 Training(학습) 단계에서부터, $L1$ penalty 등을 부여해 weight(가중치)가 0이 되도록 강제하는 것이다. Pruning과 달리, Sparsity Constraint는 사후에 가지치기하는 것이 아니라 태생적으로 Sparse한 구조를 갖도록 한다. 해당 연구에서는 GPT-2와 비슷한 architecture를 사용하되, 모델을 훈련시킬 때부터 대부분의 weight를 0으로 만들어 Sparisty Constraint를 가했다.

<img src="https://github.com/user-attachments/assets/9744dbee-e7e5-4522-b896-1f2b90d94d2d" alt="image" style="width:80%;height:auto;" />

Sparsity Constraint를 가하여 처음부터 Sparse하게 학습된 모델이 사후에 Pruning된 모델보 Disentangled circuits를 발견하 것이 훨씬 쉽다고 한다.

Dense model을 사후에 pruning한 경우에는 중요한 Circuit을 찾고자 했을 때, 뉴런들이 복잡하게 얽혀 있어 깔끔하게 Circuit을 추출하기 어려웠다. 반면, Sparse Model은 ‘해당 뉴런이 여기서 신호를 입력 받아 다른 뉴런에게 보내는구나’처럼 작동 원리를 쉽게 이해할 수 있다. 또한 Sparse Model이 사후 Pruning Model보다 Interpretability와 성능 모두 더 좋다고 제시했다.

# 3/ Python 코딩 실험 :  $“$ , $‘$ 짝 맞추기

Sparse Model, 즉 애초에 Sparse한 구조를 지닌 모델이 내부 구조를 판단하기 훨씬 좋다는 것을 검증하기 위해 Python 언어로 학습된 모델이  $‘hello$는 작은 따옴표 ‘, $“hello$는 큰 따옴표 “로 닫아 짝을 완성하는 작업을 진행했다.

<img src="https://github.com/user-attachments/assets/3ab0c062-8ce7-441c-8b7e-aa27ea98c945" alt="image" style="width:90%;height:auto;" />

Sparse Transformer를 훈련한 뒤, 해당 작업을 수행하는 데 필요한 최소 Circuit를 찾은 결과 해당 Circuit은 엄청나게 단순했다. (Residual Channel 5개, 0번 MLP Layer 2개, 10번 Attention의 Query-Key Channel 1개, Value Channel 1개로 구성되어 있었다.)

1. Residual Channel에서 따옴표 인코딩
한 Residual Channel에서는 $‘$ 인코딩, 다른 Channel에서는 $“$ 인코딩
2. MLP(Multi-Layer Perceptron)  Layer에서 따옴표 인지 & 따옴표의 종류 구분
    - $‘$, $“$ 따옴표를 인지를 감지
    - 작은 따옴표인지 큰 따옴표인지 분류
3. Attention으로 이전 따옴표 조회
10번 레이어의 Attention이 중간 토큰을 무시하고, 현재 위치에서 가장 가까운 여는 따옴표 토큰을 찾아 가져오기
4. 알맞은 닫은 따옴표 출력

    마지막 토큰에서 이전 단계에서 가져온 여는 따옴표 정보를 통해 알맞은 닫은 따옴표 예측

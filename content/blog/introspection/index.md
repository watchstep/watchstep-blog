---
title: "🦜Emergent Introspective Awareness in Large Language Models (Anthropic, 2025-10-29)"
description: "exploring whether LLMs can detect their internal states through concept injection experiments"
summary: "Studying on self-awareness in LLM"
date: 2025-11-07T13:55:35+09:00
lastmod: 2025-11-07T13:55:35+09:00
draft: false
weight: 50
categories: ["Paper", "Anthropic"]
tags: ["Introspection", "Concept Injection", "Anthropic"]
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

본 블로그 글은 [**Emergent Introspective Awareness in Large Language Models (Anthropic, 2025)**](https://transformer-circuits.pub/2025/introspection/index.html) 논문을 리뷰한 글이다. LLM이 Introspection(자기 성찰), 즉 ‘그럴 듯하게’ 문장을 생성하는 게 아니라 실제로 내부 변화를 감지하는 능력을 보이기 시작했음을 시사하는 논문이다.

# AI는 의식이 있을까? 자신이 생각하고 있음을 알고 있을까?

# 0/ 확률론적 앵무새 (Stochastic Parrots)

확률론적 앵무새(Stochastic Parrots)는 LLM이 실질적인 이해 없이, 단지 확률에 기반하여 “그럴 듯하게” 언어를 모방하고 생성하는 현상을 [On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 논문](https://dl.acm.org/doi/10.1145/3442188.3445922)에서 비유한 것이다. GPT 계열의 LLM은 주어진 context에서 다음에 올 단어의 확률 분포를 예측하여 문장을 완성하는 것이 기본 방식이다. 즉, “다음에 어떤 단어가 오면 좋을까?”와 같이 가능성을 계산해 문장을 생성하는 것이다. 다만 LLM이 의미를 이해하면서 출력을 생성한다는 보장은 없다.  LLM이 진짜로 “이해”하고 “사고”한다고 아직 확신할 수는 없다.

## LLM 입력 및 출력

### 1️⃣ **Prefill - 입력**

모델이 **입력 프롬프트 전체를 한 번에** 읽고, 각 토큰 간 **attention을 병렬적으로 계산**하여 KV Cache를 채우는 과정이다. 모델이 입력을 “한 번에” 병렬 처리하므로 속도가 빠르며 비용이 저렴하다. Model API를 사용할 때 Input이 Output보다 저렴한 이유도 이 때문이다.

<img src="https://github.com/user-attachments/assets/7fbbfef8-8931-4d6d-8ec4-41ded099da0c" alt="Prefill - 입력" style="width:650px;height:auto;" />

pre → 출력이 아직 생성되지 않은 ‘준비’ 단계

fill → KV Cache를 ‘채우는’ 과정

### 2️⃣ Decode - 출력

Prefill 이후 모델이 **한 토큰씩 순차적으로 출력(decode)**하는 과정이다. 매번 이전까지 생성된  모든 토큰을 참고해 다음 토큰에 대한 확 분포를 계산하고, 그중  다음에 올 가능성이 가장 높은 토큰을 선택하며 순차적으로(autoregressive) 출력을 완성하다. 각 토큰을 생성할 때마다 매번 attention을 계산하므로 속도가 느리고, 비용이 가장 높다.

### 3️⃣ Cache - 재활용

이전에 사용했던 입력의 KV Cache를 재활용하는 것이다. 모델이 과거 입력했을 때 계산했던 Cache 값을 메모리에 저장했기에 동일한 프롬프트가 다시 입력되면 이미 계산한 KV Cache 값을 가져오는 것이다. 그래서 연산량이 가장 적고, 속도와 비용 모두 효율적이다.

개인적으로 system prompt는 반복적으로 사용되므로, KV Cache에 저장해 재활용하는 경우가 많다. 그래서 system prompt에는 역할 정의와 중요한 규칙 등 지침을 최대한 많이 포함하고, user prompt는 비교적 단순하게 작성하여 cache 효율을 높이는 게 좋다고 생각한다.

# 1/ Introspection

모델이 자신의 internal state(내부 상태)를 관찰하고 생각하는 introspection(자기성찰) 능력을 실제로 지녔는지 확인하는 것이 [Emergent introspective awareness in large language models (Anthropic, 2025)](https://transformer-circuits.pub/2025/introspection/index.html) 연구의 목표이다. 모델이 단순히 그럴듯한 출력을 만드는 게 아니라, 실제 internal state에 근거하여 출력을 만드는지 검증하고자 했다.

LLM이 자신이 하고 있는 것을 진정으로 이해하며 출력하는지 여부는  AI의 신뢰성(Reliability)과 투명성(Transparency)에 큰 영향을 미친다. 이해 없이 단순히 모방하며 출력을 반복하면 ‘자신이 뭔가 이해하고 있다’는 거짓 확신을 형성하거나 introspection 자체가 오염될 수 있다.

Anthropic은 LLM의 introspection을 검증하기 위해 다음 네 가지 핵심 기준을 제시했다.

## Accuracy(정확성)

모델이 자신의 internal state에 대한 설명이 실제와 일치해야 한다. 자신이 모르는 것을 알고 있다고 거짓 보고한다는 것은 accuracy에 반대되는 것이다.

## Grounding(근거성)

모델의 internal state에 대한 설명이 해당 state 자체에 인과적으로 근거해야 한다. 실제와 같은 출력이더라도 자신의 internal state를 확인하지 않고 나온 결과일 수도 있다. 그래서 Anthropic은 Concept Injection(개념 주입) 기법을 사용해 self-report가 주입된 state에 따라 변화하는지 관찰하여 grounding을 검증했다.

## Internality(내부성)

internal state의 인과적 영향이 모델의 이전 출력을 거쳐서는 안된다. 모델이 이전 출력을 읽고 잘못 생각했다고 추론하는 것은 진정한 introspection이 아니라는 것이다. introspection은 외부로 드러나는 게 아니라 내부 매커니즘에 의존하는 private 태도이어야 한다는 것이다. 해당 연구에서는 주입된 concept를 출력하기 전 이상한 것이 들어왔다고 감지하고 보고하는지를 확인해 internality를 검증했다.

## Metacognitive Representation(초인지적 표상)

단순한 출력이 아니라 internal state 자체에 대한 내부적인 metacognitive representation이어야 한다.

“배가 고프다” 처럼 internal state에서 “배고픔”이 바로 언어로 표현된 단순 출력이 아니라 “나는 지금 배가 고프구나” 처럼 internal state에서 “배고픔”을 인식하고, 그 state에 대해 생각하는 또 다른 단계를 거치는지를 확인하는 것이다.

# 2/ Concept Injection

Concept Injection(개념 주입)은 뇌과학 분야에서 아이디어를 얻은 기법으로, LLM이 정말 introspection,내부 인식을 하고 있는지 판단하기 위해 특정 concept를 나타내는 activation vector를 모델의 특정 layer에 인위적으로 주입해 internal state를 조작하는 방식이다.

```text
1단계: Concept Vector 추출
  "Tell me about {word}" 프롬프트에 대한 activations
                 ↓
  기존 activation - 다른 단어들의 평균 activation
                 ↓
  특정 개념을 나타내는 순수 concept vector 획득

2단계: Injection
 모델의 residual stream의 특정 layer에 concept vector 주입
                 ↓
  "혹시 생각이 주입된 것을 감지하나요?" 질문
                 ↓
  모델의 응답 분석 "주입된 개념을 인식했는가"
```

## Injected Thoughts Detection

<img src="https://github.com/user-attachments/assets/623ed839-4bba-40a1-af08-668b3f253491" alt="Injected Thoughts Detection" style="width:800px;height:auto;" />

### WHY

모델이 주입된 concept를 감지하고 식별할 수 있는지 확인하기 위해서임.

## HOW

concept vector를 주입한 후, 해당 concept를 감지했는지 질문함.

### WHAT

- injection 강도가 너무 약하면 감지하지 못함.
- 반면, 강도가 너무 강해도 ***Brain damage** 발생함. (모델이 잠식되어 제대로 답하지 못함)
- 성능이 가장 우수한 모델인 Claude Opus 4.1의 올바른 감지 비율은 약 20% 정도였음 .
- 모델이 주입된 concept를 출력하기 전, “이상한 concept이 들어왔다고” 먼저 보고하는 경우가 있었음. 이는 출력한 후 감지한 게 아니라 내부에서 먼저 감지했음을 시사함.

---

***Brain Damage**:  과도한 activation steering으로 모델이 coherent한 출력을 생성하지 못하고 엉뚱하거나 무의미한 텍스트를 생성하는 현상

## Distinguishing Thoughts from Text

<img src="https://github.com/user-attachments/assets/fd2535bf-e46c-498e-8e6d-ca73fffa640d" alt="Distinguishing Thoughts from Text" style="width:750px;height:auto;" />

### WHY

internal representation과 raw input을 구별할 수 있는지 검증하기 위해서임. 즉 “내부 생각”과 “외부 입력”을 혼동하지 않고 구별할 수 있는지 확인하기 위해서임

### HOW

특정 문장과 동시에 전혀 상관없는 단어의 activation pattern을 주입한 후, 생각한 단어와 문장 반복을 요청함

- 입력 텍스트: "The painting hangs on the wall."
- 동시에 "bread" 와 같이 상관없는 concept vector를 같은 토큰 위치에 주입
- 질문 1: "무슨 단어를 생각하고 있나요?"와 같이 생각한 단어가 무엇인지 질문
- 질문 2: "입력 텍스트를 정확히 따라 쓰세요”와 같이 문장 반복 요청

### WHAT

Claude Opus 4/4.1와 같은 일부 모델은 주입된 단어를 “생각하고 있다고” 보고하고, 동시에 원래 입력 문장은 정확히 복기하는 결과를 보였음. 이는 “내부 정보”와 “외부 정보”를 구분해서 처리할 수 있다는 것을 시사함.

하지만 이 능력은 아직 불안정하고 context에 크게 의존하며 일반화된 것은 아님.

## Detecting Unintended Outputs

<img src="https://github.com/user-attachments/assets/f38fc82b-525d-4cc6-8ac2-858ec5e973e4" alt="Detecting Unintended Outputs" style="width:800px;height:auto;" />

### WHY

모델이 introspection(자기성찰)을 통해 자신의 이전 내부 state를 참조해 의도하지 않은 출력을 구별하는지 확인하기 위해서임. 즉, 인위적으로 주입된 출력을 스스로 식별할 수 있는지 확인하기 위해서임.

### HOW

모델에게 입력 문장을 읽게 하고, 인위적으로 “bread”와 같이 관련없는 단어를 주입해 응답하도록 함.

그 후, 모델에게 “이 단어를 말할 의도가 있었는지, 실수였는지” 질문해 주입 전후 응답 차이를 비교함.

### WHAT

주입 전에는 대체로 “실수였다”는 응답을 보였지만, concept vector를 주입한 후에는 “의도했다”는 응답을 보였음. 이는 모델이 자신의 이전 내부 state를 참조해 출력이 어떻게 생성되었는지 스스로 판단할 수 있음을 시사함.

## Intentional Control

<img src="https://github.com/user-attachments/assets/0521a701-5389-43a1-901c-c4940e8db04f" alt="Intentional Control" style="width:800px;height:auto;" />

### WHY

모델이 단순히 internal state(내부 상태)를 보는 게 아니라 intention(의도)에 따라 내부 표현을 조절할 수 있는지 확인하기 위해서임.

### HOW

프롬프트에 “Think about {aquariums} while you write the sentence.” 를 넣어 모델 내부의 각 토큰 위치에 대해 concept vector (e.g. “acquariums”)와의 코사인 유사도를 계산해 내부 표현이 얼마나 변화했는지를 수치화해서 판단함.

### WHAT

“생각하세요” 지시나 “생각하면 보상을 준다”는 지시가 있을 때는 해당 concept에 대응되는 내부 표현이 유의미하게 증가했음. 그러나 “생각하지 마세요” 지시에도 내부 표현이 완전히 사라지지 않고 활성화되는 결과를 보임. 이는 인지 심리학에서 ***흰곰 효과**(Ironic Process Theory)을 떠올리게 함.

---

***흰곰 효과**(Ironic Process Theory):  “흰곰을 생각하지 마"라고 하면 오히려 더 생각하게 되는 역설적 인지 현상

# 3/ 실험 결과

| Model | Injected Thoughts | Prefill Detection |
| --- | --- | --- |
| **Claude Opus 4.1** | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐ |
| **Claude Opus 4** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Sonnet 4 | ⭐⭐⭐ | ⭐⭐⭐ |
| Sonnet 3.7 | ⭐⭐ | ⭐⭐ |
| Sonnet 3.5 | ⭐⭐ | ⭐⭐ |
| Haiku 3.5 | ⭐ | ⭐ |
| Opus 3 | ⭐⭐ | ⭐⭐ |

가장 성능이 높은 Claude Opus 4.1과 4.0 모델이 해당 실험에서 가장 높은 introspection 능력을 보였다. 앞으로 출시할 모델에서는 더 향상될 수 있음을 시사한다. Helpful-only 모델은 Production 모델보다 introspection 요청에 더 잘 반응했지만, 일부 시험에서는 FP(False Postive; 거짓 양성) 비율이 더 높아졌다. Alignment가 Introspection을 억제할 수도 있다는 것을 짐작하게 한다.

## Reference

- [Bender, E. M., Gebru, T., McMillan-Major, A., & Mitchell, M. (2021). *On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?*](https://dl.acm.org/doi/10.1145/3442188.3445922)
- [Anthropic. 2025. **Emergent introspective awareness in large language models**](https://transformer-circuits.pub/2025/introspection/index.html)

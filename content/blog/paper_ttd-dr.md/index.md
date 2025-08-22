---
title: "🔬 Deep Researcher with Test-Time Diffusion (Google Cloud;2025) 논문 리뷰"
description: "Test-Time Diffusion Deep Research"
summary: "인간의 연구 과정에서 영감을 받아 Diffusion 방식으로 발전한 AI Deep Research Agent"
date: 2025-08-22T10:49:00+09:00
lastmod: 2025-08-22T10:49:00+09:00
draft: false
weight: 50
categories: []
tags: ["paper", "LLM", "ai research agent", "test-time scaling"]
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

# [Test-Time Diffusion Deep Researcher; TTD-DR](https://arxiv.org/abs/2507.16075)

## 논문 개요

- **제목**: Deep Researcher with Test-Time Diffusion
- **저자**: Rujun Han, Yanfei Chen 외 (Google Cloud AI Research, Google Cloud)
- **발표**: 2025년 7월, arXiv:2507.16075v1
- **분야:** `AI Research Agents` `Large Language Models` `Test-Time Scaling`

## 논문 요약

Google Cloud AI Research팀이 인간의 연구 과정을 모방한 혁신적인 AI 연구 에이전트 TT**D-DR(Test-Time Diffusion Deep Researcher)**를 발표했다. 기존 Deep Research 에이전트들이 복잡한 장문 연구 보고서 생성에서 보이는 성능 한계를 극복하기 위해, 인간의 계획-초안-수정 과정을 diffusion 프로세스로 모델링한 것이 핵심이다. 초기 **"노이즈가 있는"** 초안을 점진적으로 정제하는 denoising 과정과 각 구성요소를 개별적으로 최적화하는 self-evolution 알고리즘을 결합했다. 실험 결과 OpenAI Deep Research 대비 69.1%~74.5%로 높은 성능을 보여 기존 연구 에이전트들을 크게 뛰어넘는 성과를 보였다.

## AI가 진짜 연구자처럼 생각할 수 있을까?

<img width="180" height="145" alt="Image" src="https://github.com/user-attachments/assets/0775522a-767a-4820-a51c-8d06747d81af" />

최근 ChatGPT, Claude 같은 대형 언어 모델들이 단순한 질문답변을 넘어 복잡한 연구 작업까지 수행하기 시작했다. 하지만 여전히 한계가 명확하다. 특히 **Deep Research** 작업-여러 단계의 정보 수집, 분석, 종합이 필요한 고차원적 연구-에서는 성능이 급격히 떨어진다.

문제의 핵심은 기존 AI 연구 에이전트들이 인간의 실제 연구 과정과는 다른 방식으로 작동한다는 점이다. 인간 연구자는 선형적으로 첫 문장부터 마지막 문장까지 차례대로 쓰지 않는다. 대신 전체적인 계획을 세우고, 초안을 작성한 뒤, 추가 자료를 찾아가며 반복적으로 수정해나간다.

Google의 연구팀은 바로 이 점에 주목했다. 과연 AI도 인간처럼 **"생각하고, 초안을 쓰고, 수정하는"** 방식으로 연구할 수 있을까?

## 배경 및 문제 정의

### 현재 Deep Research 에이전트의 한계

<img width="400" height="155" alt="Image" src="https://github.com/user-attachments/assets/df0a47ee-a9a6-4832-9501-c39a1b6d6a37" />

OpenAI Deep Research, Perplexity Deep Research, Grok DeepSearch 등  기존의 Deep Research Agents은 대부분 **Chain-of-Thought**, **Monte Carlo Tree Search**, **self-refinement** 같은 test-time scaling 기법들을 조합해서 만들어졌다.

이러한 접근법은 다음과 같은 문제점들을 가지고 있다:

1. **liner 또는 parallelized 방식**: 계획 → 검색 → 생성을 순차적으로 처리
2. **global context 손실**: 긴 연구 과정에서 초기 정보가 손실되거나 일관성이 떨어짐
3. **인간 인지 과정과의 괴리**: 실제 연구자의 작업 방식을 반영하지 못함, 복잡한 long-form 보고서 생성 시 성능 정체

### 인간의 연구 과정 vs Diffusion

인지과학 연구에 따르면 인간이 복잡한 주제에 대해 글을 쓸 때는 다음과 같은 패턴을 보인다:

- **High-level planning** (전체 구조 설계)
- **Draft writing** (초안 작성)
- **Multiple revision cycles** (반복적 수정)
- **Literature search during revision** (수정 과정에서의 추가 자료 수집)

이는 diffusion model이 noise가 있는 이미지를 점진적으로 정제해나가는 과정 (denoising)과 매우 유사하다.

| Diffusion | 인간의 연구 과정 |
| --- | --- |
| noise가 많은 초기 이미지 | 불완전한 초기 초안 |
| Denoising 과정 | 반복적 수정/개선 |
| 외부 조건부 정보 | 참고 자료 검색 |
| 고품질 최종 이미지 | 최종 연구 보고서 완성 |

## Diffusion으로 연구하는 AI Agent

TTD-DR의 핵심 아이디어는 **연구 보고서 생성을 diffusion 과정으로 모델링**하는 것이다.

> *"We conceptualize the generation of a complex research report as a diffusion process where an initial, noisy draft is progressively refined into a high-quality final output."*
>
>
> *"우리는 복잡한 연구 보고서 생성을 초기의 노이즈가 있는 초안이 점진적으로 정제되어 고품질의 최종 결과물이 되는 diffusion 과정으로 개념화했다."*
>

### 두 가지 핵심 메커니즘

**1. Denoising with Retrieval**

- 초기 연구 보고서(주로 LLM 내부 지식 기반)를 작성
- 각 denoising 단계에서 외부 정보 검색으로 내용을 보강
- 초안과 연구 계획이 다음 검색 방향을 동적으로 안내

**2. Self-Evolution**

- 각 구성요소(계획, 질문, 답변, 보고서 생성)를 개별적으로 최적화
- 다양한 지식 탐색을 장려하고 정보 손실을 완화
- diffusion 과정에 더 나은 context 제공

## Test-Time Diffusion Deep Researcher (TTD-DR)
: 3단계 Backbone Model + 2가지 Optimization 기법

### Backbone Deep Research Agent

<img width="320" height="62" alt="Image" src="https://github.com/user-attachments/assets/4a117607-e002-4455-91be-db46f76c323a" />

TTD-DR의 기본 구조는 3단계로 구성된다:

**Stage 1: Research Plan Generation**

- 사용자 쿼리를 받아 구조화된 연구 계획 생성
- 최종 보고서에 필요한 핵심 영역들을 나열
- 후속 정보 수집 과정의 초기 가이드라인 역할

**Stage 2: Iterative Search and Synthesis**

- **2a) Search Question Generation**: 연구 계획과 이전 컨텍스트를 바탕으로 검색 쿼리 생성
- **2b) Answer Searching**: 외부 소스 검색하여 관련 문서 찾고 요약된 답변 반환
- 연구 계획이 충분히 커버되거나 최대 반복 횟수에 도달할 때까지 순환

**Stage 3: Final Report Generation**

- 1단계의 계획과 2단계의 질문-답변 쌍들을 종합
- 포괄적이고 일관성 있는 최종 보고서 생성

### Component-wise Self-Evolution

<img width="370" height="137" alt="Image" src="https://github.com/user-attachments/assets/b8da7ef2-e2fd-40d2-b083-1b43f9f6c921" />

각 단계의 에이전트 성능을 개별적으로 향상시키는 알고리즘:

1. **Initial States**: 다양한 파라미터로 여러 답변 변형 생성 (temperature, top_k 조정)
2. **Environmental Feedback**: **LLM-as-a-judge*를 통해 Helpfulness, Comprehensiveness 평가
3. **Revision Step**: 피드백을 바탕으로 각 변형을 개선
4. **Cross-over**: 여러 개선된 변형들을 하나의 고품질 결과물로 통합

**LLM-as-a-judge: 다른 LLM이 생성한 텍스트의 품질을 평가하는 LLM*

### Report-level Denoising with Retrieval

diffusion model의 sampling 과정에서 영감을 받은 핵심 알고리즘

<img width="400" height="113" alt="Image" src="https://github.com/user-attachments/assets/e08c2553-94de-4c09-80b2-40fc3c6a391e" />

- preliminary draft를 “noisy” 시작점으로 설정
- iterative refinement를 통해 점진적으로 품질 향상
- 각 단계에서 retrieval mechanism이 외부 정보를 동적으로 통합

**계속 개선되는 초안이 검색을 안내하고, 검색이 초안을 정제하는 지속적인 피드백 루프**이다. ****이를 통해 보고서의 일관성을 유지하면서 연구가 올바른 방향으로 진행되도록 한다.

## 실험 결과

### 실험 세팅

**평가 데이터셋:**

- [**LongForm Research**](https://huggingface.co/datasets/akoksal/LongForm): 205개 실제 산업 도메인 쿼리
- **DeepConsult**: 비즈니스/컨설팅 관련 Deep Research 프롬프트
- **HLE-Search**: Humanity's Last Exam에서 검색이 필요한 쿼리 200개 선별
- **GAIA**: 실제 AI 능력 평가를 위한 multi-hop 질문 벤치마크

**평가 방법:**

- **Side-by-side comparison**: 두 보고서를 직접 비교하여 우수성 평가
- **Helpfulness & Comprehensiveness**: 장문 LLM 응답 평가
- **Human-calibrated LLM-as-a-judge**: 인간 평가자와의 alignment 비교

### 성능 비교

| 시스템 | LongForm Research | DeepConsult | HLE-Search | GAIA |
| --- | --- | --- | --- | --- |
| **TTD-DR (ours)** | **69.1%** | **74.5%** | **33.9%** | **69.1%** |
| OpenAI Deep Research | - | - | 29.1% | 67.4% |
| Perplexity Deep Research | 21.8% | 32.0% | 14.5% | 54.5% |
| Grok DeeperSearch | 16.1% | 16.0% | 19.3% | 47.9% |
| GPT-Researcher | 18.3% | 9.4% | 2.0% | 37.7% |

<img width="420" height="232" alt="Image" src="https://github.com/user-attachments/assets/c0b7f534-c8a3-443c-8791-5bb99f649ae6" />

<img width="410" height="189" alt="Image" src="https://github.com/user-attachments/assets/9635bfe0-e378-468e-855e-d3270f04dbd1" />

### 요약

1. **성능 우위**: 장문 연구 보고서 생성 작업에서 기존 시스템들 대비 2-3배 이상의 승률
2. **효율적인 test-time scaling**: 비슷한 latency time에서 더 나은 성능 달성
3. **Self-evolution 효과**: 검색 질문과 답변의 복잡도를 크게 향상시켜 정보의 풍부함 증대
4. **Denoising 효과**: 초기 9단계만으로도 최종 보고서 정보의 51.2% 통합

## 시사점

### 학문적 의의

TTD-DR은 **인간의 인지 과정을 AI 시스템 설계에 체계적으로 반영한 첫 번째 시도**로, 단순히 기존 기법들을 조합한 것이 아니라, 인지과학 연구에서 밝혀진 인간의 글쓰기 패턴을 diffusion 과정으로 추상화한 것이 기여한 부분이다.

또한 **test-time scaling의 새로운 패러다임**을 제시했다. 기존의 단순한 반복이나 샘플링 기법을 넘어, 구조화된 피드백 루프와 component-wise 최적화를 통해 효율적인 성능 향상을 달성했다.

### 산업적 영향

현재 OpenAI, Perplexity, Anthropic 등이 경쟁하고 있는 **AI Research Assistant 시장에 새로운 기준**을 제시했다. 특히 기업 환경에서 요구되는 복잡한 시장 분석, 기술 동향 조사, 전략 기획 등의 작업에서 실질적 도움을 줄 수 있는 수준에 도달했다.

Google Cloud AI Research의 이번 연구는 **검색 도구만으로도 최고 수준의 성과**를 달성했다는 점에서 주목할 만하다. 많은 경쟁사들이 다양한 proprietary tool들을 통합하는 방향으로 가는 반면, 더 효율적인 알고리즘으로 같은 결과를 얻어낸 것이다.

### 한계와 향후 연구 방향

논문에서 저자들이 명시적으로 인정한 한계점들이 있다:

1. **도구의 제약**: 현재는 검색 도구만 사용하며, 웹 브라우징이나 코딩 도구는 미포함
2. **Agent tuning 부재**: test-time scaling에만 집중하고 학습 기반 최적화는 다루지 않음
3. **계산 비용**: 여러 단계의 반복과 self-evolution으로 인한 높은 연산 비용

향후 연구에서는 multimodal 능력 통합, 더 다양한 도구 활용, 그리고 훈련 기반 접근법과의 결합이 주요 과제가 될 것으로 보인다.

## 결론

TTD-DR은 단순히 성능 수치를 개선한 것을 넘어 **AI 연구 에이전트 설계의 근본적 패러다임 전환**을 제시했다. 인간의 연구 과정을 diffusion 프로세스로 모델링하고, 초안 중심의 반복적 정제 (refining) 방식을 도입한 것은 혁신적이다.

특히 **복잡한 추가 도구 없이도 알고리즘적 개선만으로 기존 시스템들을 압도한 점**은 인상적이다. 이는 AI 연구에서 "더 많은 데이터, 더 큰 모델, 더 복잡한 도구"가 항상 정답은 아닌 것 같다. [~~(그래도 스케일링 법칙 못 참지)~~](https://arxiv.org/abs/2001.08361)

하지만 실제 상용화 관점에서는 여전히 해결해야 할 과제들이 있다. 높은 계산 비용과 제한적인 도구 활용은 현실적인 제약이다. 그럼에도 불구하고 TTD-DR이 제시한 방향성-인간의 인지 과정 모방과 체계적인 피드백 루프-은 향후 AI Research Agent 발전의 중요한 발판이 될 것이다.

Google Cloud의 해당 연구는 AI가 단순한 질문답변 도구를 넘어 진정한 **연구 파트너**로 진화할 수 있는 가능성을 보여준 의미 있는 성과다.

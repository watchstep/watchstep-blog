---
title: "🪆Matryoshka Representation Learning (Google, 2022) 논문 리뷰 (feat. EmbeddingGemma)"
description: "MRL: 고정 차원 임베딩을 넘어 유연한 차원 임베딩 (adaptive multi-embedding)"
summary: ""
date: 2025-09-04T15:10:34+09:00
lastmod: 2025-09-09T17:00:00+09:00
draft: false
weight: 50
categories: ['embedding']
tags: ['paper', 'embedding']
contributors: []
pinned: false
homepage: false
seo:
  title: ""
  description: ""
  canonical: ""
  noindex: false
---

## 0/Matryoshka Representation Learning; MRL

gemini-embedding-001 (Google, 2025), text-embedding-3-large (2024, OpenAI), voyage-context-3 (2025, Voyage AI) 등 최신 임베딩 모델에서 Matryoshka Representation Learning; MRL를 지원하다고 하는데 MRL이 뭘까?

`Matryoshka Representation Learning(MRL)`는 러시안 인형 마트료시카 처럼 하나의 임베딩  벡터 안에  여러 세분화된 정보를 담아 다운스트림 작업(downstream task)의 연산 제약 조건에 유동적으로 적응할 수 있도록 설계된 표현 학습(representation learning) 기법이다.

*"multi embedding"이라고도 부르기도 한다. 논문에서는 multi-objective MRL로 표현한다
*downstream task란 학습된 임베딩을 분류/검색/랭킹 등과 같은 후속 작업 (흔히 훈련된 모델을 다운스트림 테스크에 맞게 파인튜닝한다고 한다.)

<img src="https://github.com/user-attachments/assets/e235885c-e7be-4231-9b24-2c19cea7595c" alt="MRL 구조도" style="width:380px;height:auto;" />

&nbsp;

큰 임베딩 안에 그 자체로도 유용한 작은 임베딩들이 겹겹이 들어가 있어 상황에 맞게 꺼내 사용할 수 있다는 것이다. “책 읽기”로 비유하자면 32차원으로 책 표지와 목차를 살펴보고, 내용을 더 읽고 싶으면 128차원까지 책을 펼쳐보고, 그럼에도 부족하면 부록, 즉 최종 차원까지 보는 것이다.

일반적으로 임베딩 차원이 높을수록 성능이 올라가지만, 그럴수록 비용과 속도도 함께 증가한다. 따라서 상황에 맞게 유연하게 저차원, 고차원을 선택할 수 있도록 하는 것이다.


> 임베딩 하나 안에 간략한 정보(coarse)부터 자세한 정보(fine)까지 순서대로 담아두자! <br/>
그래서 고차원만 사용하는 게 아니라 저→중→고차원을 상황에 맞게 쓰자!
>

## 1/ rigidity ↔ flexibility?

본 논문에서는 rigidity ↔ flexibility 의 개념으로 설명하는데, 무엇을 말하는걸까?

과거 임베딩 고정 차원(fixed dimension)이라, 다른 차원이 필요한 경우 이에 맞게 모델을 다시 훈련해야했다. (오버헤드 ↑)

MRL은 계산 자원과 상황에 맞춰 바로 하나의 모델 & 하나의 임베딩 벡터로 필요한 차원의 정보를 선택하여 사용할 수 있어 유연하며 효율적이다.

임베딩 하나로 coarse → fine (전반적 → 세부적으로) 요약 정보에서 세부적인 정보를 담는 것이다. 다양한  세분성(granularity)를 고려하여 정보를 계층적으로 인코딩한다.

## 2/ 왜 필요한가?

임베딩 차원 $d$, 데이터 크기 $N$, 라벨 수 $L$에 비례하여 선형적으로 추론 비용이 증가한다.

경사 기반 학습은 의미 있는 정보가 벡터 전역으로 퍼지는 경향이 있어 낮은 차원만으로 충분한 작업임에도 큰 차원을 강제하는 비효율이 발생한다.

*여기서의 추론 비용은 계산된 deep representation(고차원 벡터; 데이터의 본질적이고 의미 있는 정보가 압축된 형태로 표현; 고 수준 표현)을 실제 다운스트림 애플리케이션(downstream application)에 활용할 때 발생하는 비용을 말한다.

MRL은 추가 추론 비용 없이 기존 파이프라인을 조금 수정해 적응형 임베딩(adaptive embeddings)을 만들 수 있다.

## 3/ 아이디어 - “앞은 요약, 뒤는 디테일”(**coarse→fine)**

<img src="https://github.com/user-attachments/assets/5b3e3205-485d-42e1-acd8-d7f2802e9f30" alt="MRL 구조도" style="width:420px;height:auto;" />

MRL은 고차원 임베딩 벡터 안에 coarse-to-fine granularity 수준의 정보를 계층적으로 인코딩한다.

$O(\\log d)$ : d-차원 벡터 안에 $M=\\{8,16,32,\\dots,d\\}$ 을 정해, 각 $m \\in \\mathcal{M}$에대해 앞 $m$개 $z_{1:m}$만 사용해도 유용하도록 학습한다. 예를 들어 1024 차원의 최종 임베딩 벡터가 있다면, 그 중 처음 512차원만 사용해도 특정 목적에 완전하고 유용한 임베딩으로 사용 가능하다.

$$
\min_{\theta_F, \{W^{(m)}\}} \frac{1}{N} \sum_{m \in \mathcal{M}} \sum_{i} c_m \mathcal{L}(W^{(m)} F(x_i; \theta_F)_{1:m}, y_i)
$$

- $F(x_i;\\theta_F)$: 입력 x로부터 d차원 임베딩 벡터 z를 생성하는 생성망
- $F(\\cdot)_{1:m}$:  생성된 d차원 중 처음 **m차원(prefix)**만 사용
- $W^{(m)}$:  m차원 임베딩을 위한 선형 분류기 가중치
- $c_m$:  각 차원별 손실에 대한 중요도 가중치(relative importance)
- $M$:  최적화할 임베딩 차원의 집합 e.g. {8, 16, 32, … , 256, 512}
- $L$:  다중 클래스 소프트맥스 크로스 엔트로피(multi-class softmax crossentropy) 손실 함수

단순히 최종 차원에 대한 손실 함수(loss function)만 최적화하는 것이 아니라 미리 정해둔 여러 중첩된(nested) 차원들 각각에 대해 동시에 손실 함수를 최적화하도록 모델 훈련한다. 모든 중간 차원을 각각의 모델에 대해 독립적으로 학습하지 않고도 동일한 성능을 유지할 수 있다. 이처럼 하나의 모델로 한 번의 forward pass만으로 모든 계층적 표현을 얻어 추론 시 상당한 계산 비용을 절감할 수 있다.

```python
# PyTorch code for Matryoshka Cross-Entropy Loss
import torch.nn as nn

class Matryoshka_CE_Loss(nn.Module):
    def __init__(self, relative_importance, **kwargs):
        super(Matryoshka_CE_Loss, self).__init__()
        self.criterion = nn.CrossEntropyLoss(**kwargs)
        self.relative_importance = relative_importance

    def forward(self, output, target):
        loss = 0
        for i in range(len(output)):
            loss += self.relative_importance[i] * self.criterion(output[i], target)
        return loss
```

## 4/ “그냥 자르기” vs. “PCA” vs. **MRL**

일반 임베딩의 앞 차원을 그냥 잘라내 사용하면, 그 앞 차원 벡터는 원본 정보를 제대로 담지 못할 가능성이 높다. 일반적으로 경사 기반 학습 모델은 임베딩 벡터의 모든 차원에 걸쳐 정보가 확산(diffuse)되어 인코딩되는 경향이 있기 때문이다. 그래서 처음 몇 차원만 떼어내 사용하면 정보의 품질을 보장할 수 없다.

PCA/SVD과 같은 사후 압축은 차원을 조금 줄이면 정확도가 올라가지만, 과하게 줄이면 정확도가 많이 감소한다. 반면, MRL은 학습 이후 단계가 아니라 end-to-end 학습 단계에서 미리 여러 차원에서 사용할 수 있도록 최적화되어 있어 정확도가 유지된다.

## 5/ EmbeddingGemma로 보는 MRL 예시

<img src="https://github.com/user-attachments/assets/a4edacb6-e98c-417c-8185-c54661e57a01" alt="EmbeddingGemma MRL 예시" style="width:750px;height:auto;" />


25년 9월에 소개된 EmbeddingGemma 모델도 MRL을 지원하는데, 공식 문서에서 MRL 설명이 간략히 잘 되어 있다.

```python {title="Python"}
# MRL test for `google/embeddinggemma-300M`
import os, numpy as np, torch
from sentence_transformers import SentenceTransformer

MODEL_ID = "google/embeddinggemma-300M"
DEVICE   = "cuda" if torch.cuda.is_available() else "cpu"
TOKEN    = os.getenv("HF_TOKEN")  # 필요 시 설정

# Load Model
model = SentenceTransformer(MODEL_ID, device=DEVICE, token=TOKEN)

data = ["아이폰", "갤럭시", "삼성", "고양이"]

def l2norm(E):  # 행별 L2 정규화
    return E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-12)

def cosine_to_anchor(E):
    a = E[0]
    sims = []
    for i in range(1, len(E)):
        s = float(np.dot(a, E[i]) / (np.linalg.norm(a)*np.linalg.norm(E[i]) + 1e-12))
        sims.append((data[i], s))
    return sims

def show(title, E):
    sims = cosine_to_anchor(E)
    print(f"\n[{title}] shape={E.shape}")
    for name, s in sims:
        print(f"  {data[0]} vs {name}: {s:.4f}")
    order = [name for name, s in sorted(sims, key=lambda x: x[1], reverse=True)]
    print("  rank:", " > ")
    return np.array([s for _, s in sims])

def spearman(u, v):  # 순위 안정성 간단 지표
    r = lambda x: np.argsort(np.argsort(-x))
    return float(np.corrcoef(r(u), r(v))[0, 1])

# ===== 1/ full embedding =====
emb_full = model.encode(data, convert_to_numpy=True)
D = emb_full.shape[1]
s_full = show("FULL", emb_full)

# ===== 2/ truncate to 512 dims +  L2 normalization =====
E512 = l2norm(emb_full[:, :min(512, D)])
s_512 = show("TRUNCATE 512 + L2", E512)

# ===== 3/ truncate to 256 dims + L2 normalization =====
E256 = l2norm(emb_full[:, :min(256, D)])
s_256 = show("TRUNCATE 256 + L2", E256)

# check MRL
print(f"\nSpearman(FULL vs 512) = {spearman(s_full, s_512):.3f}")
print(f"Spearman(FULL vs 256) = {spearman(s_full, s_256):.3f}")
print(f"Base dim = {D}")
```

```text {title="Output"}
[FULL] shape=(4, 768)
  아이폰 vs 갤럭시: 0.9355
  아이폰 vs 삼성: 0.9326
  아이폰 vs 고양이: 0.8970
  rank: 아이폰 > 갤럭시 > 삼성 > 고양이

[TRUNCATE 512 + L2] shape=(4, 512)
  아이폰 vs 갤럭시: 0.9442
  아이폰 vs 삼성: 0.9419
  아이폰 vs 고양이: 0.9133
  rank: 아이폰 > 갤럭시 > 삼성 > 고양이

[TRUNCATE 256 + L2] shape=(4, 256)
  아이폰 vs 갤럭시: 0.9568
  아이폰 vs 삼성: 0.9548
  아이폰 vs 고양이: 0.9270
  rank: 아이폰 > 갤럭시 > 삼성 > 고양이

Spearman(FULL vs 512) = 1.000
Spearman(FULL vs 256) = 1.000
Base dim = 768
```

실제로 EmbeddingGemma 모델에서 MRL이 잘 동작하는지 확인한 결과 차원을 기존 768차원에서 256차원으로 축소하였는데도 의미를 잘 나타내고 있다는 것을 확인할 수 있다.

## References

- [Matryoshka Representation Learning (2022, NeurIPS)](https://arxiv.org/abs/2205.13147)
- [GitHub 구현 코드 - RAIVNLab/MRL](https://github.com/RAIVNLab/MRL)
- [Medium - Matryoshka Embeddings: Russian Dolls for AI](https://medium.com/@pooja93palod/matryoshka-embeddings-russian-dolls-for-ai-58aa80ae7732)
- [Introducing EmbeddingGemma: The Best-in-Class Open Model for On-Device Embeddings](https://developers.googleblog.com/en/introducing-embeddinggemma/)
- [Generate Embeddings with Sentence Transformers](https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers)

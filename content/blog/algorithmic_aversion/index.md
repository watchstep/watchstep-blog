---
title: "😵 What is Algorithmic Aversion? How can we handle this when using AI?"
description: "Algorithmic Aversion"
summary: ""
date: 2025-11-05T09:26:45+09:00
lastmod: 2025-11-05T09:26:45+09:00
draft: false
weight: 50
categories: ['psychology']
tags: ['algorithmic aversion', 'blackbox']
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

# 0/ Algorithmic Aversion

**Algorithmic Aversion** (**알고리즘 혐오**)은 알고리즘이 인간보다 더 정확하게 예측함에도 불구하고 알고리즘 기반 결정을 기피하는 심리적 현상을 말한다.

[Dietvorst et al. (2015)](https://marketing.wharton.upenn.edu/wp-content/uploads/2016/10/Dietvorst-Simmons-Massey-2014.pdf)은 실험을 통해 사람들이 **알고리즘의 단 한 번의 실수를 목격하는 것만으로, 알고리즘에 대한 신뢰를 급격히 상실하고, 인간의 판단을 더 선호**하는 경향을 입증했다.

- 알고리즘이 인간보다 더 나은 성과를 보여도 알고리즘을 선택하지 않았다
- MBA 학생 성과 예측 실험에서 알고리즘은 인간보다 15-29% 더 적은 오류를 보였다
- 항공 승객 수 예측 실험에서 알고리즘은 90-97% 더 적은 오류를 보였다
- 알고리즘이 더 좋은 성능을 보임에도 불구하고, 알고리즘의 실수를 본 실험 참가자들은 알고리즘을 사용하기를 거부했다.

# 1/ 왜 이런 현상이 발생하는가?

algorithmic aversion은 단순히 성능 문제보다는 인간의 심리적 기대와 불안감에서 비롯된다.

## 인간은 되고, 기계는 안돼, 기계는 완벽해야 한다는 기대

인간의 실수에 대해서는 더 빨리 용서하고, 관대하게 대하는 반면, 알고리즘은 완벽해야 한다고 기대하므로, 알고리즘의 실수는 용납하지 못하는 이중적인 경향을 보인다고 한다. ~~(기계한테 내로남불)~~

같은 실수를 해도 알고리즘은 인간보다 신뢰를 빨리 잃을 수 있다는 것이다. 기대가 클수록 실망도 커지는 것처럼 기계에게 요구하는 완벽함이 너무 높아 실수에서 오는 실망감이 더 보이는 경향이 있다는 것이다.

## 블랙박스 (Blackbox) 문제에서 오는 불안감

알고리즘이 어떤 과정을 거쳐 그런 결정을 내렸는지 알 수 없을 때, 통제력을 잃었다고 느끼며 불안해 하는 것도 algorithmic aversion의 주요 원인 중 하나이다. 내가 이해할 수 없는 무언가에 중요한 결정을 맡기고 싶어 하지 않는 것은 당연한 심리인 것 같다.

# 2/ 실제 사례

## 의료 도메인

[2025년 JAMA Network Open 연구](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2830240)에 따르면, 환자의 65.8%가 AI를 책임감 있게 사용할 것이라고 신뢰하지 않으며, 57.7%는 AI 도구가 자신에게 해를 끼치지 않을 것이라는 확신이 없다고 답했다. 이는 환자들이 AI가 “비인격적”으로 인식하고, 자신의 복잡하고 미묘한 건강 상태를 AI가 잘 판단하지 못할 것이라고 두려워하기 때문이다.

## HR 도메인

2018년 [아마존의 AI 채용 도구가 여성에게 편향](https://www.reuters.com/article/world/insight-amazon-scraps-secret-ai-recruiting-tool-that-showed-bias-against-women-idUSKCN1MK0AG/?utm_source=chatgpt.com)된 결과를 보여 논란이 된 것처럼 인간 데이터를 바탕으로 훈련된 AI에는 편향이 내재될 수 있다. 반면, Pymetrics나 Unilever와 같은 HR 기업은 채용 의사결정에 대한 편향은 줄이며 AI의 능력을 잘 활용하여 객관적인 채용 평가 도구를 개발하였다. 게임형 평가와 구조화된 인간 평가를 결합하여 효율성은 높이면서 공정성을 지키기 위해 노력하고 있다.

# 3/ 어떻게 극복할 수 있을까?

## 투명성 (Transparency) / 설명 가능성 (Explainability)

알고리즘이 어떻게 의사결정을 하는지 명확히 설명하는 것은 기본적인 해결책이다. 블랙박스 모델의 속을 들여다 볼 수 있도록 XAI (Explainable AI)를 통해 해석할 수 있어야 한다.

## Human in the loop;  HITL

[Management Science (2018)](https://dl.acm.org/doi/abs/10.1287/mnsc.2016.2643)에 실린 후속 연구에 의하면 2-5% 정도의 조정 권한만 주어져도 알고리즘 사용 의향이 크게 증가한다고 한다. 이는 인간에게 약간의 통제권을 부여하면 알고리즘의 성능을 크게 저하시키지 않으면서도 사용자의 판단이 알고리즘과 거의 일치하도록 유도할 수 있다는 것을 보여준다.

# 4/ AI와의 상호작용

AI 기반 의사결정(AI-based decision making)을 두려워하기보다, 오류를 발견했을 때 어떻게 대처할지 고민하고 AI를 효율적으로 활용하여 시간과 비용을 절약하는 방법을 찾아야 한다고 생각한다. 이는 개인과 비즈니스 모두에 적용되는 필수적인 태도라고 느낀다.

미래에는 AI가 우리 일상에 더 많이 차지하게 될 것이므로, AI와 상호작용하는 능력과 인간만이 할 수 있는 고유의 능력을 발전시켜야 한다고 본다.

과거 GPT -3.0일 때 많이 발생하던 할루시네이션(Hallucination) 현상이 현재 GPT- 5.0에서는 크게 개선된 것과 같이, AI는 끊임없이 발전될 것이다.  지금 범하는 오류가 미래에도 발생할 것이라 단정할 수 없다는 것이다. 이러한 발전을 염두에 두고 대비하는 것이 AI 시대에 매우 필요하다고 느낀다.

아직 AI의 내부 작동 방식에 관하여 정확히 밝혀진 것은 없지만, 이러한 블랙박스(Blackbox) 문제가 해결되면, algorithmic aversion도 더욱더 완화될 것이라 기대해 본다.

## Reference

- [Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). **Algorithm Aversion: People Erroneously Avoid Algorithms After Seeing Them Err**. *Journal of Experimental Psychology: General*.](https://marketing.wharton.upenn.edu/wp-content/uploads/2016/10/Dietvorst-Simmons-Massey-2014.pdf)
- [Dietvorst, B. J., Simmons, J. P., & Massey, C. (2018). **Overcoming Algorithm Aversion: People Will Use Imperfect Algorithms If They Can (Even Slightly) Modify Them**. *Management Science*.](https://dl.acm.org/doi/abs/10.1287/mnsc.2016.2643)
- [Algorithm Aversion - The Decision Lab](https://thedecisionlab.com/reference-guide/psychology/algorithm-aversion)

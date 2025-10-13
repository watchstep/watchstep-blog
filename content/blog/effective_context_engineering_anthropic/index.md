---
title: "🎱 Effective context engineering for AI agents (Anthropic, 2025-09-29)"
description: ""
summary: ""
date: 2025-10-13T12:06:53+09:00
lastmod: 2025-10-13T12:06:53+09:00
draft: false
weight: 50
categories: ['context engineering', 'agent', 'anthropic', 'claude']
tags: ['tech blog', 'context engineering', 'agent', 'anthropic', 'claude']
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

# AI 에이전트의 성능을 극대화하기 위한 효과적인 컨텍스트 엔지니어링 전략

**[Effective context engineering for AI agents (Anthropic, 2025-09-29)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**

# 0/ Context란?

Context는 LLM에서 샘플링(sampling)할 때 포함되는 토큰(token) 집합 전체를 의미한다. 여기에는 system prompt, message history, examples, tool outputs, 외부 데이터까지 포함된다. Context engineering(컨텍스트 엔지니어링)은 원하는 결과를 일관되게 얻기 위해 이러한 전체 토큰의 유용성을 최적화하는 것이다.

LLM을 잘 다루기 위해서는 thinking in context가 필요하다. 이는 전체 상태를 살펴보고 각 상태가 어떤 잠재적인 행동을 도출할 수 있을지 고려하는 방식을 말한다. 매 턴마다 어떤 토큰을 추가하고, 제외할 것인지 결정하는 것이 중요하다.

# 1/ Context engineering vs. Prompt engineering

<img width="650" height="auto" alt="Context Engineering과 Prompt Engineering 비교 다이어그램" src="https://github.com/user-attachments/assets/e038345c-4e89-468c-87a2-50787ca14fb6" />

Anthropic에서는 context engineering을 prompt engineering의 자연스러운 진보로 본다.

Prompt engineering이 최적의 결과를 위해 system prompt를 작성하고 체계화하는 것이라면,

Context engineering은 LLM inference동안 prompt 외부의 정보까지 포함하여 최적의 정보 토큰들을 전략에 맞춰 조작하는 것이다.

prompting은  system prompt를 잘 작성하는 것에 초점을 둔다. 반면 Context engineering은 단순히 좋은 프롬프트를 작성하는 것을 넘어, 여러 번의 추론, 긴 추론 시간을 요구하는 agent의 전체적인 context state (system instructions, tools, MCP 등)을 지속적으로 관리해야한다.

에이전트 루프가 길수록 다음 턴에 어떤 토큰을 포함할지가 에이전트의 성능을 좌우한다. Context engineering은 지속적으로 발전하는 정보들로부터 제한된 context window를 어떻게 전략적으로 조작할지 고려한다.

# 2/ Agent 설계할 때 Context engineering이 중요한 이유

## Context Rot

[Context Rot : How increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot)

해당 연구에 의하면, 토큰 수가 증가할수록 모델이 해당 컨텍스트에서 정보를 정확히 파악하는 능력이 떨어지는 현상이 발생한다고 한다.

<img width="500" height="auto" alt="Context Rot - 토큰 수 증가에 따른 모델 성능 저하 그래프" src="https://github.com/user-attachments/assets/bfbc01c8-ebb2-4f8f-8a9b-c25ca3155f29" />

이는 Transformer의 구조적 한계때문이다. Transformer는 모든 토큰은 다른 모든 토큰과의 관계를 계산해야한다. 전체 context에서 $N^2$쌍의 관계가 발생하게 되는데, attention budget은 유한하다. context 크기가 커질수록 context rot(컨텍스트 부식)으로 recall 정확도가 떨어진다. 그래서 간결하지만 정보 밀도는 높은 context와 무엇을 앞에 두고 무엇을 제외할 것인지 (배치/선별)이 중요하다.

# 2/ Effective Context engineering 전략

<img width="650" height="auto" alt="효과적인 Context Engineering 전략 개념도" src="https://github.com/user-attachments/assets/ff043338-1e6f-4925-8e2c-2368ce078986" />

좋은 context engineering이란 원하는 결과의 가능성을 극대화하는 high-signal 토큰들의 가능한 집합들 중 가장 작은 집합을 찾는 것이다. 즉, 가장 적은 토큰으로 원하는 결과를 최대한 얻는 것이다.

## 1️⃣ System prompt

system prompt는 반드시 minimal해야 한다. 여기서의 minimal은 짧게 작성하라는 의미가 아니라, 불필요한 정보를 제거하고 필요한 정보만 간결하게 포함하라는 뜻이다.

정보가 너무 과도하면 너무 복잡하고, 너무 모호하면 정보가 부족하다. specific 과 vague 사이의 적절한 균형을 찾아야 한다.

### 구조화

다음과 같이 명확한 섹션 구분을 추천한다:

- `<background_information>`
- `<instructions>`
- `## Tool guidance`
- `## Output description`

 XML 태깅이나 Markdown 헤더를 활용해 프롬프트를 구조화하는 것을 권한다.

## 최소로 시작

최소한의 프롬프트로 시작하여 직접 실험해보면서 점진적으로 보강하는 것이 효과적이다.

## 2️⃣ Tools

도구는 Token efficient , agent behavior efficient해야한다.

- 기능 중복을 최소화해야 한다.
- 명확하고 간결한 tool description
- 오류에 강건한 tool 설계
- 툴셋이 크면 툴 선택하는 것이 모호해짐

## 3️⃣ Few-shot prompting

천 마디 말보다는 한 장의 그림이 나은 것처럼 few-shot examples은 그림의 역할을 할 수 있다. 구체적인 예시를 통해 모델이 원하는 동작을 이해할 수 있도록 돕는다.

# 3/ Context Retrieval & Agent Search

## “just in time”

Claude Code는 이 접근법(`CLAUDE.md`)을 사용해 복잡한 데이터 분석을 수행한다. 전통적인 embedding 기반 접근 대신 가벼운 참조 (파일 경로, 데이터베이스 쿼리 등)을 유지하고 런타임에 동적으로 정보를 가져오는 것이다.

Just In Time은 인간의 인지 방식을 반영한 접근법으로,  우리가 모든 정보를 머릿속에 저장하지 않고, 필요할 때마다 외부 자료를 찾는 것과 같이 에이전트를 설계하는 것이다.

- 모든 정보를 기억하지 않고, 외부 파일 시스템을 색인화하여 필요에 따라 연관 정보를 검색하여 가져온다. 필요한 정보만 선택적으로 가져옴으로써 context rot를 방지한다.
- 즉, 파일 시스템을 단순히 저장소가 아니라 구조화된 외부 메모리로 사용한다.
- 에이전트가 정보를 쉽게 탐색하고 회수할 수 있도록 convention을 지정해 파일 이름을 작성, timestamp를 추가, 명확한 디렉토리 구조를 설계하면 좋다.

# 3/ L**ong-Horizon Tasks**

Agent 간단한 정의 : **An LLM agent runs tools in a loop to achieve a goal.**

Long-Horizon을 요구하는 복잡한 장기 테스트를 수행하는 에이전트를 위한 전략

## 1️⃣ Compaction

제한된 context window의 한계때문에 compaction(압축)은 중요하다. 성능 저하를 최소화하면서 content를 증류하는 것이 목적이다.

Claude Code에서는 메시지 히스토리를 모델에게 전달하여 가장 중요한 세부사항을 요약하고 압축하도록 구현한다. 모델은 아키텍처 결정사항, 미해결된 버그, 구현 세부사항은 보존하면서 중복된 tool 출력이나 메시지는 폐기한다.

(Claude Code 사용할 때 일정 대화를 진행한 후에는 `/clear` 명령으로 context 초기화해주는 것이 좋다.)

### Recall → Precision

초기에는 recall를 최대화하여 정보를 놓치지 않는 것이 중요하고 (즉, 추후에 사용될 정보가 제거되지 않도록), 그 이후에는 현재 작업과 관련 없는 불필요한 정보를 제거하여 precision을 개선하는 방식으로 반복하는 것이 좋다. (recall를 확보한 후에 precision을 확보하는 것을 권장한다.)

## 2️⃣ Structured note-taking (agentic memory)

context 밖의 파일 기반 메모리로 진행 상황을 추적하고, 지식을 누적한다. 필요 시에만 다시 로딩하고, 장기적인 작업에서 일관성을 유지하고, context가 초기화되어도 작업을 이어갈 수 있도록 한다.

- to-do list 작성 및 주기적 업데이트 (목표를 잊지 않고 계속 목표를 향할 수 있도록 암송)
- [NOTES.md](http://NOTES.md) 파일로 중요한 context 유지
- 복잡한 과제 해결 과정 추적

Claude Sonnet 4.5는 built-in memory tool을 제공하여 컨텍스트가 초기화되어도 이전 상태를 복원하고 작업을 이어갈 수 있다.

*Agent의 4가지 핵심 구성요소(Perception, Planning, Action, Memory) 중 Memory는 필수로, 메모리 관리는 중요하다.

<img width="450" height="auto" alt="LLM 기반 자율 에이전트의 4가지 핵심 구성요소 다이어그램 (Perception, Planning, Action, Memory)" src="https://github.com/user-attachments/assets/10dd5ad9-8a7f-41d8-ba8b-86371efc8348" />

A Survey on Large Language Model based Autonomous Agents (2023)

## 3️⃣  Sub-agent architectures

복잡한  테스크에는 multi-agent 아키텍처가 적합하다. Main agent는 planning & synthesis에 집중하고, Sub-agents는 특정 영역을 깊이 탐색한 후 요약을 산출한다. 이러한 계층적 구조는 각 에이전트가 자신의 context 내에 효율적으로 행동하면서도 복잡한 최종 목표를 달성할 수 있도록 한다.

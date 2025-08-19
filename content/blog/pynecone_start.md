---
title: "🌳 Pynecone 시작하기 (Python으로 웹앱 만들기)"
date: 2023-04-10T01:57:05+09:00
draft: false
tags: ['Pynecone']
contributors: []
summary : "Pynecone 시작하기"
---

## **Pynecone이란? (그래도 React 종말은...)**

{{< youtube 47BL6WLZJ1g >}}

**특징 (공식 사이트** [https://pynecone.io/](https://pynecone.io/) **에서 말하는…)**

- **Pure Python**
새로운 언어 배울 필요 없어요 파이썬이랑 해당 프레임워크를 사용할 줄만 알면 돼요
- **Easy to Learn**
- **Full Flexibility**
확장성 좋아요
- **Batteries Included**
Pynecone 하나로  프론트엔드, 백엔드, 배포 다 할 수 있어요

---

- Pynecone : Pure Python으로 interactive web app을 만들 수 있음 (JavaScript, React, NextJS 몰라도 됨)
- Styling을 위해 Chakra UI를 사용함
- NextJS app과 FastAPI 서버 간의 모든 통신 처리 가능
- AI와 같이 파이썬 패키지를 많이 사용하는 경우, FastAPI 백엔드 사용하니 좋을 듯
- 노마드 코더왈, ReactJS가 아닌 Flutter처럼 느껴져서 좋아
- 그래도 그냥 JS, React, NextJS 배우자

## Let’s Started with Pynecone!

### 1. Pynecone Installiation

- Python 3.7버전 이상
- NodeJS 12.22.0 버전 이상

![Untitled](https://user-images.githubusercontent.com/88659167/230783615-aad3184a-0dc8-41c0-880d-715183c70d9d.png)

************pip************를 통해 설치

```bash
pip install pynecone-io
```

### 2. Create a Project

**모든 Pynecone function, class는 `pc.` 접두사로 시작!**

**<kbd>pc init</kbd> : Initialize a template app in new directory**

![Untitled 1](https://user-images.githubusercontent.com/88659167/230783609-de0fc64b-e1ee-46a6-b57d-ae71fc353634.png)

![Untitled 2](https://user-images.githubusercontent.com/88659167/230783610-6c902c8b-d71b-46e4-9257-61c6587e29b3.png)

위와 같이 기본 템플릿을 생성해줌

**directory structure**

```python
MY_FIRST_PYNECONE_APP
├── .web
├── assets
├── my_first_pynecone_app
│   ├── __init__.py
│   └── my_first_pynecone_app.py
└── pcconfig.py
```

1. **`.web`**
NextJS 앱으로 컴파일 다운되어서 `.web` 디렉토리에 저장됨
해당 디렉토리 손 댈 필요 없지만, 디버깅에 유용함
각각의 Pynecone 페이지는 .js 파일로 컴파일되어서 `.web/pages` 디렉터로리에 저장됨

1. **`assets`**
favicon , 폰트, 이미지 등과 같은 asset들은 저장하는 디렉토리
`assets/image.png` 로 image를 해당 디렉토리에 저장하면, 아래와 같이 해당 이미지를 디스프레이할 수 있음.

    ```python
    pc.image(src="image.png")
    ```

2. **Main Project : `{my_first_pynecone_app}/{my_first_pynecone_app.py}`**
<kbd>pc init</kbd> 하면, 해당 디렉토리 이름과 같은 이름의 app (디렉토리이름.py) 를 생성해줌.

3. **Configuration :** `**pcconfig.py`**
app에 관한 configuration 관한 파일임.
아래와 같이 default로 생성됨

    ```python
    import pynecone as pc

    config = pc.Config(
        app_name="my_first_pynecone_app",
        db_url="sqlite:///pynecone.db",
        env=pc.Env.DEV,
    )
    ```


### 3. Run the app

```bash
pc run
```

![Untitled 3](https://user-images.githubusercontent.com/88659167/230783611-b3926416-ebc1-4ce1-bb2a-c4b07b3afd62.png)

[http://localhost:3000/](http://localhost:3000/)

![Untitled 4](https://user-images.githubusercontent.com/88659167/230783613-b97edc49-042e-4bd8-b65b-a03d546cdc80.png)

### 4. The Structure of a Pynecone App

**my_first__pynecone_app.py**

```python
"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

# State는 모든 variable들 (**vars**)을 정의
class State(pc.State):
    """The app state."""

    pass

# Frontend
def index():
    return pc.center(
        pc.vstack(
            **pc.heading**("Welcome to Pynecone!", font_size="2em"),
            **pc.box**("Get started by editing ", pc.code(filename, font_size="1em")),
            **pc.link**(
                "Check out our docs!",
                href=docs_url,
                border="0.1em solid",
                padding="0.5em",
                border_radius="0.5em",
                _hover={
                    "color": "rgb(107,99,246)",
                },
            ),
            spacing="1.5em",
            font_size="2em",
        ),
        padding_top="10%",
    )

# Routing
# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
# Compiling
app.compile()
```

<kbd>pc.heading()</kbd>, <kbd>pc.box()</kbd> <kbd>pc.link()</kbd> 과 같은 **[50개 이상의 built-in components](https://pynecone.io/docs/library)**  있음

프론트엔드, 백엔드 모두 해결함.

## My first pynecone app

![Untitled 5](https://user-images.githubusercontent.com/88659167/230783614-90f21437-8b72-47e2-b185-8b612e0fcaa3.png)

### **Reference**

- **Pynecone** : [https://pynecone.io/](https://pynecone.io/)
- **Pynecone Example APP** : https://github.com/pynecone-io/pynecone-examples
- **reddit에 pynecone 개발진이 직접 작성한 글 :**
[https://martinii.fun/397](https://martinii.fun/397)
- [https://www.reddit.com/r/Python/comments/10h6l7e/pynecone_new_features_and_performance_improvements/](https://www.reddit.com/r/Python/comments/10h6l7e/pynecone_new_features_and_performance_improvements/)
- [https://dalle.pynecone.app/](https://dalle.pynecone.app/)
- [https://www.reddit.com/r/Python/comments/zh0pmy/pynecone_web_apps_in_pure_python/](https://www.reddit.com/r/Python/comments/zh0pmy/pynecone_web_apps_in_pure_python/)

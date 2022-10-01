<p align="center"><img src="assets/img/logo.png" height="200px" width="200px"></p>

# <p style="text-align: center;">[watchstep's blog](https://blog.watchstep.me/)</p>

### This blog is built using [HUGO](https://gohugo.io/) & [Netlify](https://www.netlify.com/)
 ### My previous blog is [Take heed : 개발 블로그](https://takeheed.tistory.com/)
### Based on [Blowfish](https://jamstackthemes.dev/theme/blowfish/) theme
---
- [**Add Page**](#add-page)
- [**Add External Page**](#add-external-page)
- [**Thumbnails**](#thumbnails)
- [**Simple Page**](#simple-page)
- [**Start the HUGO Server Before Publish**](#start-the-hugo-server-before-publish)

### Add Page
```
hugo new posts/<page-name>.md
```
**Page Example :**
```
---
title: "Title"
date: 2022-01-25
description: "It's blog post"
summary: "How to write blog post"
tags: ["how", "write", "blog"]
---
_This_ is the content of my blog post.
```

### Add External Page
```
hugo new -k external posts/<file-name>.md
```
**External Page Example :**
```
---
title: "External Link"
date: 2022-01-25
externalUrl: "https://takeheed.tistory.com/"
summary: "I wrote a post on Tistory."
showReadingTime: false
_build:
  render: "false"
  list: "local"
---
```

### Thumbnails
```
content
└── thumnail-example
    ├── index.md
    └── featured.png
```
The image file should starts with `feature*` like `featured.png`.

### Simple Page
```
---
title: "Simple Page"
date: 2022-03-08
description: 'A full-width template that just places Markdown content into the page without any special theme features.'
layout: "simple"
---
_This_ page content is now full-width without any special theme features.
```

### Start the HUGO server Before Publish
```
hugo server
```
Start the HUGO server with `draft` (`draft` : true => Hugo will not publish  ) enabled
```
hugo server -D
```
HUGO new site at http://localhost:1313/


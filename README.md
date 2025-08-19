# Watchstep Blog

[![Hugo](https://img.shields.io/badge/Hugo-Doks-blue?style=for-the-badge&logo=hugo)](https://gohugo.io/)
[![Node.js](https://img.shields.io/badge/Node.js-20.10.0-green?style=for-the-badge&logo=node.js)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Netlify](https://img.shields.io/badge/Netlify-Deployed-00C7B7?style=for-the-badge&logo=netlify)](https://blog.watchstep.me)

A static site powered by **Hugo v0.145.0‑extended** and **Node v20.10.0 / npm v10.2.4**.
Built with the **Doks** template.

**[🌐 Live Demo ↗](https://blog.watchstep.me)**

## 🚀 Quick Start

```bash
git clone https://github.com/watchstep/watchstep-blog.git
cd watchstep-blog

npm ci            # Install locked dependencies
npm run dev       # Start local server → http://localhost:1313
```

## 🔨 Build & Deploy

```bash
npm run build     # ⇒ hugo --minify --gc → public/
```

## 📄 Writing Content

```bash
# Create new post
npm run create blog/my-post/index.md

# Preview locally (`draft:true`)
npm run dev
```

**Quick tips:**
- Markdown files are located under the `content/` folder
- Posts with `draft: true` are only visible in local preview
- Set `draft: false` in frontmatter to publish
- Add images to `content/posts/my-post/images/`
- Use `npm run dev` for live reload during writing

## 🛠️ Updating Doks Template

```bash
# Check & update to latest version
npm outdated @thulite/doks-core
npm install @thulite/doks-core@latest @thulite/images@latest @thulite/seo@latest

# Or install specific versions
npm install @thulite/doks-core@1.6.0 @thulite/images@3.1.0
```

> Check release notes and changelog for potential conflicts with custom `config/` or `layouts/` files

## 📂 Project Structure

```
content/         # Markdown posts & pages
assets/          # Sass/JS processed by Hugo Pipes
static/          # Static files (favicons, images, etc.)
config/          # hugo.toml + environment configs
```

**Key files excluded from Git:**
```
public/          # Build output
resources/       # Hugo cache
node_modules/    # Dependencies
```

## 📝 License & Credits

- **Template** © Henk Verlinde (MIT License)
- **Content** © Juii Kim, 2025

---

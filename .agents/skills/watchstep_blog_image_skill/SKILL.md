---
name: watchstep_blog_image_skill
description: Normalize local images in Watchstep Hugo blog posts. Use when a post `index.md` contains pasted Markdown image links, URL-encoded folder names, or inconsistent local filenames and the user wants them converted into stable local HTML image tags such as `image_1.png`, `image_2.png`, and so on.
---

# Watchstep Blog Image Skill

Use this skill when working on `watchstep-blog` posts that contain local Markdown image links in `content/posts/<slug>/index.md`.

This skill is specifically useful for posts like `content/posts/emr_rag_kakaotalk_chatbot_2/index.md`, where image links were pasted with long URL-encoded folder names such as:

```md
![image.png](RAG%20with%20Gemini%20File%20Search.../image%203.png)
```

The bundled script rewrites those references into stable local HTML tags and renames the image files in post order.

## Workflow

1. Run a dry run first.
2. Review the planned renames and warnings.
3. Run the real command.
4. Re-open `index.md` and confirm the images now use local `src="image_N.ext"` paths.

## Commands

Run from the repository root:

```bash
python3 .agents/skills/watchstep_blog_image_skill/scripts/normalize_post_images.py content/posts/YOUR_POST/index.md --dry-run
python3 .agents/skills/watchstep_blog_image_skill/scripts/normalize_post_images.py content/posts/YOUR_POST/index.md
```

For the current post:

```bash
python3 .agents/skills/watchstep_blog_image_skill/scripts/normalize_post_images.py content/posts/emr_rag_kakaotalk_chatbot_2/index.md --dry-run
python3 .agents/skills/watchstep_blog_image_skill/scripts/normalize_post_images.py content/posts/emr_rag_kakaotalk_chatbot_2/index.md
```

## Behavior

- Finds local Markdown image references in source order.
- Resolves URL-encoded paths and also falls back to same-folder basenames.
- Renames matched files to `image_1.png`, `image_2.png`, and so on, preserving the original extension except normalizing `.jpeg` to `.jpg`.
- Replaces each matched Markdown image with:

```html
<img width="500" height="auto" alt="" src="image_1.png" />
```

- Leaves remote URLs such as `https://...` unchanged.
- Leaves unresolved local references unchanged and prints a warning.
- Keeps already-converted HTML images untouched because it only rewrites Markdown image syntax.

## Rules

- Do not overwrite unrelated existing files.
- Preserve the visual order from `index.md`.
- Default to `width="500"` and `alt=""`.
- Use `--preserve-alt` only when the user explicitly wants Markdown alt text retained.
- Report warnings when an image cannot be resolved instead of guessing.

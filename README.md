# Watchstep Blog

A modern blog built with Hugo and Doks theme.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Hugo (Extended version)
- Git

### Installation
```bash
git clone <your-repo-url>
cd watchstep-blog
npm install
make serve
```

## 📝 Creating Blog Posts

Cross-platform blog post creation:

```bash
make new-post
```

**Features:**
- **OS Detection**: Automatically uses the right script for your OS
- **Smart Naming**: Converts title to clean folder name (lowercase, underscores)
- **Original Title**: Keeps original title in file content
- **Date Structure**: Organizes posts by year/month

**Example:**
- Input: `Hi  안녕  ApPle`
- Folder: `hi_안녕_apple`
- Title in file: `Hi  안녕  ApPle`

## 🛠️ Available Commands

```bash
make help      # Show all commands
make serve     # Start development server
make build     # Build the site
make deploy    # Deploy to GitHub
make new-post  # Create a new blog post
make clean     # Clean build files
```

## 📁 Project Structure

```
content/
├── blog/
│   ├── 2024/
│   │   ├── 01/
│   │   │   └── my-post/
│   │   │       └── index.md
│   │   └── 02/
│   └── 2023/
├── docs/
└── _index.md

scripts/
├── new-post.bat      # Windows
├── new-post-mac.sh   # macOS
└── new-post.sh       # Linux
```

## 🎨 Customization

- Edit `config/_default/params.toml` for site configuration
- Modify `assets/scss/` for styling
- Update `layouts/` for custom templates

## 📦 Deployment

The site is configured for automatic deployment via Netlify. Simply push to the main branch to deploy.

## 📄 License

This project is licensed under the MIT License.

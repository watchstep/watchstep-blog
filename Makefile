.PHONY: help serve build deploy new-post clean

# Detect OS
ifeq ($(OS),Windows_NT)
    NEW_POST_SCRIPT = scripts/new-post.bat
    OS_NAME = Windows
    RM_CMD = rmdir /s /q
    DATE_CMD = powershell -Command "Get-Date -Format 'yyyy-MM-dd HH:mm'"
else
    NEW_POST_SCRIPT = scripts/new-post.sh
    OS_NAME = Unix (macOS/Linux)
    RM_CMD = rm -rf
    DATE_CMD = date +'%Y-%m-%d %H:%M'
endif

# Main commands
help:
	@echo "Available commands:"
	@echo "  make dev    - Run local server"
	@echo "  make build      - Build the site"
	@echo "  make deploy     - Push to GitHub (auto deploy)"
	@echo "  make new-post   - Create a new blog post"
	@echo "  make clean      - Clean build files"
	@echo ""
	@echo "Detected OS: $(OS_NAME)"
	@echo "Using script: $(NEW_POST_SCRIPT)"

# Run local server
dev:
	npm run dev

# Build the site
build:
	npm run build

# Push to GitHub (Netlify auto deploy)
deploy:
	git add .
	git commit -m "chore: update blog $(shell $(DATE_CMD))"
	git push origin main

# Create a new blog post (OS-aware)
new-post:
	$(NEW_POST_SCRIPT)

# Clean build files
clean:
	$(RM_CMD) public resources

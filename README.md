# 🌟 Best of Open Source

**Community-driven collection** of high-quality open source projects, with weekly investigations published to our blog.

> 📝 **Note:** This repository contains the public blog and investigation data. Video generation and content processing is handled in a private pipeline.

## 🎯 What's Here

- **Investigations Database** - Markdown files with detailed analysis of open source projects
- **Blog Frontend** - Astro-based static site with search and tags
- **Scanner Module** - Public tools for discovering repositories
- **Community Contributions** - Open to pull requests for new investigations!

## 🌐 Live Site

Visit our blog at: **[https://iberi22.github.io/bestof-opensorce](https://iberi22.github.io/bestof-opensorce)**

## 🏗️ Project Structure

\\\
investigations/      # Markdown database (⭐ main content)
website/             # Astro blog frontend
web/                 # React dashboard (legacy)
src/
├── scanner/         # GitHub repository scanner
└── persistence/     # Data storage layer
scripts/
└── run_scanner.py   # Public scanner script
\\\

## 🚀 Contributing

We welcome contributions! To add a new investigation:

1. Fork this repository
2. Create a new markdown file in \investigations/\
3. Follow the frontmatter format:

\\\yaml
---
url: https://github.com/owner/repo
name: Project Name
category: web-framework
language: JavaScript
stars: 10000
status: active
reviewed: false
---
\\\

4. Submit a pull request

## 🔧 Local Development

### Blog Website (Astro)

\\\ash
cd website
npm install
npm run dev
\\\

### Scanner Script

\\\ash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_scanner.py
\\\

## 📊 Stats

- **Investigations:** Microsoft.PowerShell.Commands.GenericMeasureInfo.Count+ projects analyzed
- **Categories:** AI, Web Frameworks, Developer Tools, DevOps, etc.
- **Languages:** Python, JavaScript, TypeScript, Go, Rust, and more

## 🤝 Community

- **Discussions:** [GitHub Discussions](https://github.com/iberi22/bestof-opensorce/discussions)
- **Issues:** [Report bugs or request features](https://github.com/iberi22/bestof-opensorce/issues)

## 📝 License

**MIT License** - This repository is open source and free to use.

---

**Note:** Video generation, TTS, and advanced content processing are handled in a private repository to protect API keys and proprietary assets.

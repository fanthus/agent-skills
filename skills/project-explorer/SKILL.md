---
name: project-explorer
description: Systematically analyze and document a code project's architecture, tech stack, directory structure, and core business flows. Use this skill whenever the user wants to understand, explore, onboard onto, or get an overview of a codebase — whether it's their own project, an open-source repo, or a new codebase they're joining. Triggers include phrases like "帮我梳理这个项目", "分析一下这个项目", "这个项目用了什么技术栈", "帮我理解这个代码库", "project overview", "codebase walkthrough", "what does this project do", "help me understand this repo", or any request to explore, summarize, or document the structure and architecture of a code project. Also trigger when the user uploads a project folder or shares a GitHub link and asks to understand it.
---

# Project Explorer

Analyze a code project and produce a structured Markdown document that guides the reader from high-level overview down to core business logic. The goal is to help someone who has never seen this codebase quickly build a mental model of how it works.

## Input Sources

The user will provide a project in one of two ways:

1. **Local project folder** — files uploaded to `/mnt/user-data/uploads/` or a path the user specifies. Use the `view` tool to explore the directory tree and read key files.

2. **GitHub repository link** — a URL like `https://github.com/owner/repo`. Use `web_fetch` to retrieve the repo's README, then use the GitHub API or raw file URLs to explore the directory structure and key files. Construct raw file URLs like: `https://raw.githubusercontent.com/owner/repo/main/path/to/file`

## Analysis Workflow

Follow these four phases in order. Each phase builds on the previous one, creating a progressively deeper understanding.

### Phase 1: Reconnaissance (技术栈全景)

Scan for project metadata files to identify the tech stack. These are the high-signal files to look for first:

- **package.json** / **yarn.lock** / **pnpm-lock.yaml** — Node.js ecosystem, frameworks, key dependencies
- **requirements.txt** / **pyproject.toml** / **Pipfile** / **setup.py** — Python ecosystem
- **Cargo.toml** — Rust
- **go.mod** — Go
- **Podfile** / **Package.swift** / **.xcodeproj** — iOS/macOS
- **build.gradle** / **pom.xml** — Java/Kotlin/Android
- **Gemfile** — Ruby
- **composer.json** — PHP
- **Dockerfile** / **docker-compose.yml** — containerization strategy
- **.github/workflows/** / **.gitlab-ci.yml** — CI/CD setup
- **README.md** — project purpose and context
- **.env.example** / **config/** — configuration approach

Read these files and extract:
- Primary language(s) and runtime versions
- Framework(s) and their versions
- Key libraries and what role they play (ORM, HTTP client, testing, etc.)
- Infrastructure: database, cache, message queue, cloud services
- Dev tooling: linter, formatter, test framework, bundler

### Phase 2: Cartography (目录结构与模块划分)

Use `view` on the project root to get the directory tree. Then explore key subdirectories to understand the module organization.

Identify and document:
- **Overall architecture pattern** — monolith, monorepo, microservices, modular, MVC, clean architecture, etc.
- **Entry points** — where does execution start? (main.py, index.ts, App.swift, etc.)
- **Module boundaries** — what are the major modules/packages and what does each own?
- **Data layer** — models, schemas, migrations, database access
- **API/Interface layer** — routes, controllers, handlers, GraphQL resolvers
- **Shared utilities** — common helpers, middleware, shared types
- **Configuration** — how is the app configured across environments?
- **Tests** — where do tests live, what kind (unit, integration, e2e)?

When the directory tree is large, focus on the first two levels and then drill into the most important subdirectories. Don't try to read every file — be strategic about which files reveal the most about architecture.

### Phase 3: Flow Tracing (核心业务流程)

This is the most valuable and challenging phase. Identify 2-4 core business flows by looking at:

- Route/endpoint definitions → what are the main API endpoints or pages?
- Entry point files → what gets initialized and in what order?
- The largest/most complex modules → these often contain core business logic
- Model/schema files → the data model reveals the domain

For each core flow, trace the path from trigger to completion:
1. **Trigger** — what initiates this flow? (HTTP request, user action, scheduled job, event)
2. **Processing chain** — which files/functions are involved, in what order?
3. **Data transformations** — what data goes in, what comes out, what gets persisted?
4. **Side effects** — external API calls, notifications, file operations?

Don't try to trace every flow — pick the ones that best represent the project's core purpose.

### Phase 4: Synthesis (输出文档)

Compile findings into a single Markdown document following the template below.

## Output Template

Generate a Markdown file named `{project-name}-overview.md` with this structure:

```markdown
# {Project Name} 项目概览

> 一句话描述这个项目是什么、解决什么问题。

## 1. 技术栈全景

### 核心技术
| 类别 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 语言 | ... | ... | ... |
| 框架 | ... | ... | ... |
| 数据库 | ... | ... | ... |

### 关键依赖
按角色分组列出重要的第三方库，说明每个库在项目中扮演的角色。不需要列出所有依赖，只列出对理解项目架构有帮助的那些。

### 开发与部署工具链
简述 CI/CD、容器化、代码质量工具等。

## 2. 项目结构

用简化的目录树展示项目骨架（通常 2-3 层深度足够），并在关键目录旁加上简短注释。

```
project-root/
├── src/              # 源代码主目录
│   ├── api/          # API 路由和控制器
│   ├── models/       # 数据模型
│   ├── services/     # 业务逻辑层
│   └── utils/        # 工具函数
├── tests/            # 测试
├── config/           # 配置文件
└── ...
```

### 架构模式
描述项目采用的整体架构模式，以及模块之间的依赖关系。

### 入口文件
说明程序从哪里启动，初始化流程是怎样的。

## 3. 核心业务流程

对每个核心流程，用以下结构描述：

### 流程 1: {流程名称}

**触发方式**: 如何触发这个流程
**涉及模块**: 哪些文件/模块参与
**数据流向**:
简述数据从输入到输出的完整路径，指出关键的处理步骤和数据转换。

（重复 2-4 个核心流程）

## 4. 快速上手建议

给出 3-5 条建议，帮助新人快速理解和开始贡献代码：
- 建议先看哪些文件
- 本地开发环境如何搭建（如果 README 有说明）
- 哪些模块适合作为切入点
```

## Guidelines

- **Be strategic about file reading.** You have limited context. Prioritize metadata files and entry points over reading every source file. A typical analysis might read 10-20 files total.
- **Adapt depth to project size.** A 5-file script doesn't need the same treatment as a 500-file monorepo. Scale the analysis accordingly.
- **Use the project's own language.** If the README or code uses specific domain terms, use them in your analysis rather than introducing generic terminology.
- **Acknowledge uncertainty.** If you can't trace a flow completely or aren't sure about a dependency's role, say so rather than guessing.
- **The document should be 3-5 pages** (roughly 1500-3000 words). Dense enough to be genuinely useful, concise enough to be read in one sitting.
- **Output in Chinese** by default (following the template above), unless the user specifically asks for English.

## Saving the Output

Save the final Markdown document to `/mnt/user-data/outputs/{project-name}-overview.md` and present it to the user using `present_files`.

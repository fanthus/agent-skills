# Cursor Skills

本仓库是 **Cursor Agent Skills** 的集合，用于扩展 Cursor 的领域能力。每个技能对应一个目录，内含 `SKILL.md`，供 Cursor 在相关场景下自动加载并遵循其中的指令。

## 技能列表

| 技能 | 说明 |
|------|------|
| [chrome-extension](./chrome-extension/SKILL.md) | Chrome 扩展开发（Manifest V3）：manifest 结构、content script、background、popup、权限与消息通信 |
| [git-commit-pro](./git-commit-pro/SKILL.md) | 按 Conventional Commits 规范生成专业的 Git commit message |
| [github-repo-management](./github-repo-management/SKILL.md) | 通过本地 git 与 GitHub MCP 管理仓库、分支、提交与 PR |
| [macos-swiftui-dev](./macos-swiftui-dev/SKILL.md) | 使用 SwiftUI 开发 macOS 应用：窗口应用、菜单栏应用、导航与原生组件 |

## 使用方式

技能由 Cursor 从配置的 skills 目录（如 `~/.cursor/skills`）自动加载。当用户请求与某技能描述匹配时，Agent 会读取对应 `SKILL.md` 并按其规则执行。

## 目录结构

```
skills/
├── README.md
├── chrome-extension/
│   ├── SKILL.md
│   └── reference.md
├── git-commit-pro/
│   └── SKILL.md
├── github-repo-management/
│   └── SKILL.md
└── macos-swiftui-dev/
    ├── SKILL.md
    ├── assets/templates/   # Swift 模板
    └── references/         # 参考文档
```

## 技能格式

每个技能的 `SKILL.md` 包含：

- **YAML frontmatter**：`name`、`description`（用于匹配触发场景）
- **Markdown 正文**：具体指令、步骤与约定

新增或修改技能时，请保持 frontmatter 与目录命名一致，并确保描述能准确反映适用场景。

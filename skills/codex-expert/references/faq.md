# Codex 常见问题与解决方案（FAQ）

来源：GitHub Issues、Discussions、官方文档、社区反馈。

---

## 🔧 安装与启动

**Q: 怎么安装 Codex CLI？**
```bash
npm install -g @openai/codex        # npm
yarn global add @openai/codex       # yarn
pnpm add -g @openai/codex           # pnpm
```
或直接从 GitHub Releases 下载平台对应二进制：
https://github.com/openai/codex/releases

**Q: 安装后运行 `codex` 报 "command not found"？**
```bash
npm bin -g        # 检查全局 bin 路径
export PATH="$(npm bin -g):$PATH"   # 临时修复
# 永久修复：把上面这行加入 ~/.zshrc 或 ~/.bashrc
```
或者直接用 npx：`npx @openai/codex`

**Q: 如何升级到最新版本？**
```bash
npm update -g @openai/codex
codex --version   # 确认版本
```

---

## 🔑 认证问题

**Q: 如何登录？**
```bash
codex login
# 推荐选 "Sign in with ChatGPT"（支持最新功能）
# 或选 "Enter API Key" 直接用 OPENAI_API_KEY
```

**Q: 登录后仍然提示未认证 / token 过期？**
```bash
codex logout
codex login     # 重新登录
```

**Q: 企业账号验证失败，一直转圈或报错？**
- 已知：第三方 org 验证系统有 bug，可能导致账号无法完成认证
- 解决：联系 OpenAI Support（https://help.openai.com），说明 org 验证问题
- 临时绕过：使用个人账号 + API Key 模式

**Q: API Key 和 ChatGPT 账号登录有什么区别？**
| 特性 | ChatGPT 账号 | API Key |
|------|-------------|---------|
| Cloud threads | ✅ | ❌ |
| Codex Web 功能 | ✅ | 部分 |
| 速率限制 | 按计划 | 按 token |
| 推荐场景 | 日常使用 | CI/自动化 |

---

## 📦 沙箱与权限错误

**Q: Windows 上出现 "sandbox mandate errors" 或沙箱报错？**
```powershell
# PowerShell
$env:CODEX_UNSAFE_ALLOW_NO_SANDBOX=1
npx @openai/codex "你的任务"

# CMD
set CODEX_UNSAFE_ALLOW_NO_SANDBOX=1
npx @openai/codex "你的任务"
```
永久设置：在系统环境变量中添加 `CODEX_UNSAFE_ALLOW_NO_SANDBOX=1`。

**Q: Codex 无法写入某个目录，报权限错误？**
```toml
# ~/.codex/config.toml
[sandbox]
policy = "workspace-write"
allow_paths = ["/path/to/allowed/dir"]
```
或临时：
```bash
codex exec -c 'sandbox.allow_paths=["/tmp/mydir"]' "任务"
```

**Q: 如何完全不限制沙箱（完全自动化）？**
```bash
codex exec --sandbox danger-full-access --approval never "任务"
# ⚠️ 仅在完全受信任的环境（如专用 VM）中使用
```

---

## 🧠 记忆功能

**Q: 如何清除所有记忆？**
```bash
codex debug clear-memories
```

**Q: 记忆文件存在哪里？**
默认路径：`~/.codex/memories/`
自定义路径：在 config.toml 中设置 `codex_home = "/my/path"` 后，记忆在 `/my/path/memories/`。

**Q: 如何关闭记忆功能？**
```toml
[memory]
enabled = false
```

**Q: 记忆太多会影响性能吗？**
新版本支持 diff-based 遗忘（自动清理不常用记忆）和 usage-aware 选择。
可手动限制：
```toml
[memory]
max_items = 50
```

---

## ⚡ 非交互模式（exec）

**Q: 如何在 CI/CD 中完全自动化运行 Codex？**
```bash
export OPENAI_API_KEY="sk-..."
codex exec --approval never "运行所有测试，修复失败的用例"
```

**Q: 如何获取结构化 JSON 输出？**
```bash
codex exec --json "任务" | jq .
```

**Q: 如何恢复上次未完成的 session？**
```bash
codex exec --last "继续之前的任务"
codex exec --last --all  # 包含其他目录的 session
```

**Q: exec 模式下如何指定工作目录？**
```bash
codex exec --cd /path/to/project "修复 bug"
```

**Q: 如何验证 Codex 输出符合特定格式？**
```bash
codex exec --output-schema ./schema.json "生成数据"
```

---

## 🐙 GitHub 集成

**Q: 如何设置 PR 自动 review？**
1. 访问 chatgpt.com/codex → Settings
2. 连接 GitHub 仓库
3. 开启 "Automatic reviews"

**Q: 如何手动触发某个 PR 的 review？**
在 PR 的任意评论中输入：
```
@codex review
```

**Q: 如何自定义 Review 规则？**
在仓库根目录创建 `AGENTS.md`：
```markdown
## Review guidelines
- 不在日志中记录用户 PII（姓名、邮件、IP）
- 所有 API 路由必须有认证检查
- SQL 查询必须使用参数化，禁止字符串拼接
- 新增功能必须有对应测试
```

**Q: 如何在 GitHub Actions 中使用 Codex？**
```yaml
name: Codex Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: openai/codex-action@v1
        with:
          prompt: "审查这个 PR，重点关注安全性和代码质量"
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
```

---

## 🔌 MCP 集成

**Q: 如何添加 MCP server？**
方法一：命令行
```bash
codex mcp add
```
方法二：直接编辑 config.toml：
```toml
[[mcp_servers]]
name = "my-server"
command = ["npx", "-y", "@my/mcp-server"]
env = { TOKEN = "$MY_TOKEN" }
```

**Q: 如何查看已配置的 MCP servers？**
```bash
codex mcp list
```

**Q: MCP server 启动失败怎么排查？**
```bash
# 手动运行 server 命令看报错
npx -y @modelcontextprotocol/server-github
# 检查环境变量是否正确设置
echo $GITHUB_TOKEN
```

---

## 📊 速率限制与配额

**Q: 遇到速率限制（rate limit）怎么办？**
- 等待几分钟后重试
- 升级到 Plus/Pro 获得 2x 速率限制
- API Key 用户可在 platform.openai.com 申请提高限制

**Q: 不同计划的 Codex 配额？**
| 计划 | 说明 |
|------|------|
| Free / Go | 有限免费体验（限时活动）|
| Plus / Pro | 2x 标准速率限制 |
| Team / Business | 2x，团队共享配额 |
| Enterprise | 定制配额，联系销售 |
| API Key | 按实际 token 用量计费 |

---

## 🐛 获取帮助的资源

- **GitHub Issues**（报 bug / 搜索已知问题）：https://github.com/openai/codex/issues
- **GitHub Discussions**（功能建议 / 使用问题）：https://github.com/openai/codex/discussions
- **官方文档**：https://developers.openai.com/codex
- **Changelog**（最新版本更新）：https://developers.openai.com/codex/changelog
- **App 故障排查**：https://developers.openai.com/codex/app/troubleshooting
- **OpenAI Help**：https://help.openai.com

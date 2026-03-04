# Codex config.toml 完整参考

配置文件位置：`~/.codex/config.toml`（可通过环境变量 `CODEX_HOME` 或 `--codex-home` 覆盖）

---

## 顶层字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | 自动选择 | 模型名称，如 `codex-mini-latest`、`gpt-4o`、`o4-mini` |
| `approval` | string | `on-request` | 审批策略：`on-request` / `never` |
| `reasoning_effort` | string | 自动 | 推理强度：`low` / `medium` / `high` |
| `codex_home` | string | `~/.codex` | Codex 数据目录，包含记忆、配置等 |

---

## [sandbox] 沙箱配置

```toml
[sandbox]
# 策略：workspace-write（默认）| read-only | danger-full-access
policy = "workspace-write"

# 额外允许写入的路径（列表，可添加多个）
allow_paths = ["/tmp/scratch", "/var/log/myapp"]
```

**三种策略说明：**
- `workspace-write`：只能读写当前 git workspace，不能访问外部网络
- `read-only`：只读，无法修改任何文件（适合审查类任务）
- `danger-full-access`：完全访问权限，⚠️ 危险，仅用于完全受信任的环境

---

## [memory] 记忆配置

```toml
[memory]
enabled = true        # 是否启用记忆功能
max_items = 100       # 记忆条目上限
```

记忆文件存储在 `~/.codex/memories/`（或 `codex_home/memories/`）。

---

## [[mcp_servers]] MCP 服务器配置

可定义多个（使用 `[[]]` 数组语法）：

```toml
[[mcp_servers]]
name = "github"
command = ["npx", "-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "$GITHUB_TOKEN" }

[[mcp_servers]]
name = "filesystem"
command = ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]

[[mcp_servers]]
name = "custom-server"
command = ["python", "/path/to/my_mcp_server.py"]
env = { API_KEY = "$MY_API_KEY", DEBUG = "true" }
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 服务器标识名（唯一） |
| `command` | string[] | 启动命令及参数数组 |
| `env` | map | 注入的环境变量，支持 `$VAR` 引用宿主变量 |

---

## [profiles.*] 多配置方案

可定义多个 profile，用 `--profile <name>` 选择：

```toml
[profiles.strict]
model = "codex-mini-latest"
approval = "on-request"
sandbox.policy = "read-only"

[profiles.auto]
approval = "never"
sandbox.policy = "danger-full-access"

[profiles.ci]
model = "codex-mini-latest"
approval = "never"
sandbox.policy = "workspace-write"
reasoning_effort = "low"
```

**用法：**
```bash
codex exec --profile ci "运行所有测试"
codex exec --profile strict "审查这段代码"
```

---

## [otel] 可观测性/审计日志

```toml
[otel]
enabled = true
endpoint = "http://localhost:4317"   # OTLP gRPC endpoint
```

---

## 完整示例配置

```toml
model = "codex-mini-latest"
approval = "on-request"
reasoning_effort = "medium"

[sandbox]
policy = "workspace-write"
allow_paths = ["/tmp"]

[memory]
enabled = true
max_items = 150

[[mcp_servers]]
name = "github"
command = ["npx", "-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "$GITHUB_TOKEN" }

[[mcp_servers]]
name = "brave-search"
command = ["npx", "-y", "@modelcontextprotocol/server-brave-search"]
env = { BRAVE_API_KEY = "$BRAVE_API_KEY" }

[profiles.fast]
model = "codex-mini-latest"
approval = "never"
reasoning_effort = "low"

[profiles.safe]
approval = "on-request"
sandbox.policy = "read-only"

[otel]
enabled = false
```

---

## CLI 行内覆盖（优先级高于 config.toml）

```bash
# 单个字段
codex exec -c approval=never "任务"
codex exec -c sandbox.policy=danger-full-access "任务"

# 字符串值需引号
codex exec -c 'model="gpt-4o"' "任务"

# 多个 -c 可叠加
codex exec -c approval=never -c 'model="codex-mini-latest"' -c reasoning_effort=low "任务"

# 数组值
codex exec -c 'sandbox.allow_paths=["/tmp","/var"]' "任务"
```

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | API Key 认证（替代 codex login）|
| `CODEX_HOME` | 覆盖默认的 `~/.codex` 路径 |
| `CODEX_UNSAFE_ALLOW_NO_SANDBOX` | `=1` 在 Windows 上跳过沙箱（sandbox mandate 报错时使用）|
| `CODEX_QUIET_MODE` | `=1` 减少 CLI 输出（适合 CI 日志）|

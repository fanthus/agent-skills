---
name: proto2api-spec
description: 将 protobuf/proto 接口定义按 DATA_SPEC.md 规范转换为 API 字段路径文档，并同时产出 Markdown 与对应 HTML。自动调用当用户请求将 proto/protobuf 接口数据平铺、展开嵌套字段、生成字段路径表或生成 API 文档时。
---

# Proto2API Spec

将 `.proto` 或 protobuf 接口定义转换为标准 API 字段路径文档，并先生成 Markdown，再转换出对应 HTML。

## 何时读取引用

- 需要字段路径、数组标注、枚举、通用数据结构展开规则时，读取 [DATA_SPEC.md](references/DATA_SPEC.md)。
- 需要生成完整 `API_DOC.md`、目录锚点、接口模板或保存路径时，读取 [API_DOC_SPEC.md](references/API_DOC_SPEC.md)。

## 输入

- 原始 `.proto` 文件
- protobuf message 片段
- 能还原 Req/Resp message 的 protobuf 接口定义

## 核心流程

1. 读取 proto/protobuf 定义。
2. 识别接口消息，尤其是 `XXXReq` 和 `XXXResp`。
3. 将请求字段按 proto 字段结构展开。
4. 将响应字段按 `code`、`message`、`data` 三层结构展开。
5. 对所有嵌套对象、数组和枚举应用 [DATA_SPEC.md](references/DATA_SPEC.md)。
6. 按 [API_DOC_SPEC.md](references/API_DOC_SPEC.md) 输出 Markdown 表格或完整 API 文档。
7. 以 Markdown 为源文档生成对应 HTML，HTML 结构和内容应跟随 Markdown 文档。

## HTML 生成规则

- 始终先生成 Markdown，再由 Markdown 转换 HTML。
- 优先使用 `markdown-it` 将 Markdown 转换为 HTML；如果当前项目已有 `markdown-it` 依赖或相关脚本，直接复用。
- 找不到 `markdown-it` 时，再使用当前项目或系统已有的其他 Markdown 转 HTML 工具，例如 `pandoc`、`cmark`、`markdown`、`marked`、Python `markdown` 包等；发现可用工具时直接调用转换。
- 若项目已提供文档构建脚本、静态站点工具或 npm/pnpm/yarn 脚本，优先复用现有脚本。
- 没有现成转换工具时，可使用标准库或轻量脚本实现基础转换，但不得跳过 Markdown 源文档。
- HTML 只需要参考 Markdown 格式生成：保留标题层级、目录链接、表格、锚点、枚举说明和接口字段表，不额外引入复杂样式。
- HTML 文件名默认与 Markdown 同名，仅扩展名改为 `.html`，例如 `docs/API_DOC_20260429.md` 对应 `docs/API_DOC_20260429.html`。

## 字段转换规则

- 普通字段使用驼峰字段路径：`roomId`、`data.room.roomName`。
- 嵌套对象使用点路径：`data.rtcConfig.appId`。
- repeated message 使用元素类型标注：`data.rtcTokens[RTCTokenInfo].channelType`。
- repeated scalar 使用基础类型标注：`data.options[string]`。
- 数组字段不得输出空括号：避免 `data.items[]`，必须写成 `data.items[ElementType]`。
- 枚举字段类型保留枚举类型名，枚举值说明参考 [DATA_SPEC.md](references/DATA_SPEC.md)。

## 输出要求

- 请求字段和响应字段分表输出。
- 响应字段必须包含 `code` 和 `message`。
- 有 `data` 对象时，所有业务字段必须以 `data.` 开头。
- 生成完整接口文档时，必须包含目录、枚举类型说明、接口锚点和字段表。
- 生成完整接口文档时，必须同时交付 `.md` 和 `.html` 两份文件；HTML 必须由最终 Markdown 转换得到。
- 输出前检查字段路径是否都能回到 proto 定义中的字段或类型。

## 快速示例

```proto
message StudentJoinResp {
  ErrorCode code = 1;
  string message = 2;
  Data data = 3;
}
```

输出字段：

```text
code
message
data.room.roomId
data.rtcTokens[RTCTokenInfo].channelType
```

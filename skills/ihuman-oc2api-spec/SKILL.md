---
name: ihuman-oc2api-spec
description: 将 protobuf 生成的 Objective-C 类按 DATA_SPEC.md 规范转换为 API 字段路径文档，并同时产出 Markdown 与对应 HTML。自动调用当用户请求将 OC 接口数据平铺、展开嵌套字段、从 .pbobjc.h 生成字段路径表或生成 OC API 文档时。
---

# iHuman OC2API Spec

将 protobuf 生成的 Objective-C 类，尤其是 `.pbobjc.h`，转换为标准 API 字段路径文档，并交付 Markdown 与对应 HTML。

## 何时读取引用

- 需要字段路径、数组标注、枚举、通用数据结构展开规则时，读取 [DATA_SPEC.md](references/DATA_SPEC.md)。
- 需要 OC 属性到文档字段的映射细节时，读取 [OC_MAPPING.md](references/OC_MAPPING.md)。
- 需要生成完整 `API_DOC.md`、目录锚点、OC 访问路径或保存路径时，读取 [API_DOC_SPEC.md](references/API_DOC_SPEC.md)。
- 需要生成或优化 HTML 展示样式时，读取 [HTML_STYLE_SPEC.md](references/HTML_STYLE_SPEC.md)。

## 输入

- protobuf 生成的 Objective-C header：`.pbobjc.h`
- Objective-C protobuf 类片段
- 包含 `XXXReq`、`XXXResp`、`XXXResp_Data` 的 OC 代码

## 核心流程

1. 读取 OC header 或类定义。
2. 识别 `XXXReq`、`XXXResp` 和 `XXXResp_Data`。
3. 将 OC 属性名映射为标准 API 字段路径。
4. 识别以 `Array` 结尾的数组属性，并补充 `[ElementType]`。
5. 对所有嵌套对象、数组和枚举应用 [DATA_SPEC.md](references/DATA_SPEC.md)。
6. 先生成 Markdown 字段表或完整 Markdown 文档；生成完整文档时按 [API_DOC_SPEC.md](references/API_DOC_SPEC.md) 输出目录、枚举说明、HTTP 网关表、OC 访问路径、请求字段和响应字段。
7. 再将 Markdown 转换为同名 HTML 片段。优先使用 `markdown-it`；可调用项目已有依赖、全局 `markdown-it` CLI，或通过 `npx markdown-it` 执行转换。若不可用，再使用 `pandoc`、`markdown`、`marked`、项目已有脚本或可用语言库生成结构与 Markdown 对应的 HTML。
8. 按 [HTML_STYLE_SPEC.md](references/HTML_STYLE_SPEC.md) 将 HTML 片段包装为完整可阅读页面：补齐 `doctype/head/body`、内联样式、左侧目录、表格滚动容器、代码块样式、移动端与打印样式。包装层只改变展示，不改变 Markdown 派生内容。

## 关键映射

- `resp.code` -> `code`
- `resp.message` -> `message`
- `resp.data_p.xxx` -> `data.xxx`
- `resp.data_p.rtcTokensArray` -> `data.rtcTokens[RTCTokenInfo]`
- `resp.data_p.xxxArray[i].yyy` -> `data.xxx[ElementType].yyy`

更完整的 OC 命名和数组规则见 [OC_MAPPING.md](references/OC_MAPPING.md)。

## 输出要求

- 请求字段和响应字段分表输出。
- 生成完整接口文档时，单个接口必须使用 [API_DOC_SPEC.md](references/API_DOC_SPEC.md) 中的当前接口块格式：接口标题、`HTTP 网关` 表、`OC 访问路径`、请求字段表、响应字段表。
- `HTTP 网关` 表必须包含 `Method`、`Path`、`Path 常量`、`SDK 方法`、`请求类`、`响应类`；Method 固定为 `POST`，Path 必须使用网络路径常量对应的真实 HTTP path。
- 响应字段必须包含 `code` 和 `message`。
- 文档字段必须使用标准 API 路径，而不是 OC 访问表达式。
- 生成完整接口文档时，每个接口必须包含对应的 OC 访问路径示例，示例内同时声明请求类实例和响应解析实例。
- 空请求字段表必须输出一行 `| - | - | 无 |`。
- 数组字段不得输出空括号：避免 `data.items[]`，必须写成 `data.items[ElementType]`。
- 基本类型数组的字段路径和类型必须同时体现数组：例如 `tags[string]` 的类型写 `string[]`，`selectedOptions[int32]` 的类型写 `int32[]`。
- 最终产物必须同时包含 Markdown 和完整 HTML 页面。HTML 以 Markdown 为唯一来源生成，正文结构、标题、表格、代码块和目录应与 Markdown 保持一致；可在外层增加页面壳、样式和非侵入式增强脚本。
- 保存到文件时，先写入 `.md`，再生成同名 `.html`；例如 `docs/API_DOC_OC_YYYYMMDD.md` 对应 `docs/API_DOC_OC_YYYYMMDD.html`。

## 快速示例

OC 访问路径：

```objc
ILILStudentJoinReq *req = [[ILILStudentJoinReq alloc] init];
ILILStudentJoinResp *resp = [ILILStudentJoinResp parseFromData:data];
resp.data_p.rtcTokensArray[0].channelType;
```

文档字段：

```text
data.rtcTokens[RTCTokenInfo].channelType
```

完整接口文档的单接口块必须包含 `HTTP 网关` 表，不得回退到旧版只写网络路径常量的格式。

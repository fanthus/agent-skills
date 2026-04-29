# OC API_DOC.md 文档生成规范

## 文档结构

```markdown
# Student Live OC API 接口文档

---

## 目录
（接口列表，点击跳转）

---

## 枚举类型说明
（所有枚举类型的详细说明表格）

---

## 进入/退出课堂

### <span id="studentjoin">StudentJoin</span> - 学生加入房间

**OC 访问路径：**
```objc
StudentJoinResp *resp = [StudentJoinResp parseFromData:data];
resp.data_p.rtcTokensArray[0].channelType;
```

**请求字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| roomId | string | 房间 ID |

**响应字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | ErrorCode | 错误码 |
| message | string | 错误信息 |
| data.rtcTokens[RTCTokenInfo].channelType | ChannelType | RTC 频道类型 |
```

## 目录锚点

文档开头必须包含目录，并按接口分组：

```markdown
## 目录

### 进入/退出课堂
- [StudentJoin](#studentjoin---学生加入房间)

### 互动接口
- [SubmitQuizAnswer](#submitquizanswer---学生提交答题)
```

## 接口锚点

每个接口标题使用 `<span id="xxx">` 标记：

```markdown
### <span id="studentjoin">StudentJoin</span> - 学生加入房间
```

锚点 ID 使用接口名小写。

## OC 访问路径

每个接口必须包含 `OC 访问路径` 小节。路径示例使用真实的 OC 类名和属性访问表达式，但字段表仍输出标准 API 字段路径。

## 枚举类型说明

枚举类型说明必须放在目录之后、接口之前。枚举值参考 `DATA_SPEC.md`。

## 保存路径

完整 OC API 文档默认保存到 `docs/API_DOC_OC_YYYYMMDD.md`。

同时生成对应 HTML，默认保存到同名 `docs/API_DOC_OC_YYYYMMDD.html`。HTML 必须由 Markdown 转换得到，优先使用 `markdown-it`；可调用项目已有依赖、全局 `markdown-it` CLI，或通过 `npx markdown-it` 执行转换。

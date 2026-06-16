# API_DOC.md 文档生成规范

## 文档结构

```markdown
# Student Live API 接口文档

---

## 目录
（接口列表，点击跳转）

---

## 枚举类型说明
（所有枚举类型的详细说明表格）

---

## Activity 接口

### <span id="submitquizanswer">SubmitQuizAnswer</span> - 学生提交答题

**请求字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| roomId | string | 房间 ID |

**响应字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | ErrorCode | 错误码 |
| message | string | 错误信息 |
| data.quiz.quizId | string | 答题 ID |
```

## 目录锚点

文档开头必须包含目录，并按接口分组：

```markdown
## 目录

### Activity 接口
- [SubmitQuizAnswer](#submitquizanswer---学生提交答题)
- [SubmitVote](#submitvote---学生提交投票)

### Live 接口
- [StudentJoin](#studentjoin---学生加入房间)
```

## 接口锚点

每个接口标题使用 `<span id="xxx">` 标记：

```markdown
### <span id="studentjoin">StudentJoin</span> - 学生加入房间
```

锚点 ID 使用接口名小写：

| 接口 | 锚点 ID |
|------|---------|
| SubmitQuizAnswer | submitquizanswer |
| SubmitVote | submitvote |
| GrabRedPacket | grabredpacket |

## 枚举类型说明

枚举类型说明必须放在目录之后、接口之前。枚举值参考 `DATA_SPEC.md`。

## 字段表模板

```markdown
**请求字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| fieldName | type | 描述 |
| nested.object | type | 描述 |
| array[ElementType].field | type | 描述 |

**响应字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | ErrorCode | 错误码 |
| message | string | 错误信息 |
| data.field | type | 描述 |
| data.object.nested | type | 描述 |
| data.array[ElementType].elementField | type | 描述 |
```

## 保存路径

完整 API 文档默认保存到 `docs/API_DOC_YYYYMMDD.md`。

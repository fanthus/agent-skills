# OC API_DOC.md 文档生成规范

## 文档结构

完整 OC API 文档必须使用当前接口块格式，不再使用旧版“只输出网络路径常量 + OC 访问路径 + 字段表”的格式。

```markdown
# SuperClass SDK OC 网络接口文档

> 生成来源：`SuperClassSDK/Classes/Core/ILLiveNetworkManager.h/.m`、`SuperClassSDK/Classes/Core/ILNetworkDefine.m` 与 `ILProtocolBuffer` 当前 `.pbobjc.h`。

---

## 目录
（接口列表，点击跳转）

---

## 枚举类型说明
（所有枚举类型的详细说明表格）

---

## 用户

### <span id="getuseraddress---获取用户地址信息">GetUserAddress</span> - 获取用户地址信息

获取用户地址信息

**HTTP 网关：**

| 项 | 值 |
|----|----|
| Method | `POST` |
| Path | `/user/api/base/get_user_address` |
| Path 常量 | `ILNetworkPathUserGetAddress` |
| SDK 方法 | `fetchUserAddressWithSuccess` |
| 请求类 | `ILIUGetUserAddressReq` |
| 响应类 | `ILIUGetUserAddressResp` |

**OC 访问路径：**

```objc
ILIUGetUserAddressReq *req = [[ILIUGetUserAddressReq alloc] init];
ILIUGetUserAddressResp *resp = [ILIUGetUserAddressResp parseFromData:data];
resp.data_p.userAddressArray[0].userAddressId;
```

**请求字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| - | - | 无 |

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | ErrorCode | 错误码 |
| `message` | string | 错误信息 |
| `data.userAddress[UserAddress].userAddressId` | int64 | - |
| `data.userAddress[UserAddress].userId` | int64 | - |
| `data.userAddress[UserAddress].receiverName` | string | 收件人 |
| `data.userAddress[UserAddress].receiverPhone` | string | 联系方式，手机号 |
| `data.userAddress[UserAddress].receiverPhonePrefix` | string | 手机国际区号 |
| `data.userAddress[UserAddress].area` | string | 行政区域 |
| `data.userAddress[UserAddress].detailAddress` | string | 具体地址 |
| `data.userAddress[UserAddress].isDefault` | bool | 是否默认地址 |
| `data.userAddress[UserAddress].tags[string]` | string[] | 用户自定义标签 |
```

## 目录锚点

文档开头必须包含目录，并按接口分组。目录链接必须指向接口标题中的 `<span id="...">`。

```markdown
## 目录

### 用户
- [GetUserAddress - 获取用户地址信息](#getuseraddress---获取用户地址信息)

### 直播互动
- [SubmitQuizAnswer - 提交答题选项（每人只能提交一次）](#submitquizanswer---提交答题选项-每人只能提交一次)
```

## 接口锚点

每个接口标题必须使用 `<span id="...">` 标记：

```markdown
### <span id="getuseraddress---获取用户地址信息">GetUserAddress</span> - 获取用户地址信息
```

锚点 ID 规则：

- 基础格式：`接口名小写---接口中文标题`
- 中文标题来自 SDK 方法注释的首句或接口说明。
- 标题中的空白和标点归一为 `-`，去掉首尾多余 `-`。
- 没有接口标题时，锚点 ID 可退化为接口名小写。

## HTTP 网关

每个接口必须包含 `HTTP 网关` 小节，且必须使用下列表格结构：

```markdown
**HTTP 网关：**

| 项 | 值 |
|----|----|
| Method | `POST` |
| Path | `/真实/http/path` |
| Path 常量 | `ILNetworkPath...` |
| SDK 方法 | `xxxWith...` |
| 请求类 | `XXXReq` |
| 响应类 | `XXXResp` |
```

字段来源：

- `Method` 固定为 `POST`。
- `Path 常量` 来自 `ILLiveNetworkManager.m` 中 `initWithPath:` 使用的常量。
- `Path` 来自路径常量实现文件，例如 `ILNetworkDefine.m` 中 `NSString * const ILNetworkPath... = @"/..."`。
- `SDK 方法` 使用 `ILLiveNetworkManager` 暴露的方法名，不带参数标签。
- `请求类` 使用真实 OC request 类。
- `响应类` 使用真实 OC response 类。

## OC 访问路径

每个接口必须包含 `OC 访问路径` 小节。示例必须同时声明请求类实例和响应解析实例，并给出一个真实响应字段访问表达式。

```objc
XXXReq *req = [[XXXReq alloc] init];
XXXResp *resp = [XXXResp parseFromData:data];
resp.data_p.itemsArray[0].id;
```

OC 访问路径只用于示例；字段表仍必须输出标准 API 字段路径，例如 `data.items[Item].id`。

## 请求字段

请求字段必须输出三列表格：

```markdown
**请求字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `roomId` | int64 | 房间ID |
```

当请求类没有字段时，必须输出：

```markdown
| 字段 | 类型 | 说明 |
|------|------|------|
| - | - | 无 |
```

## 响应字段

响应字段必须输出三列表格，且每个响应都必须包含 `code` 和 `message`。

```markdown
**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | ErrorCode | 错误码 |
| `message` | string | 错误信息 |
| `data.rtcTokens[RTCTokenInfo].channelType` | ChannelType | RTC 频道类型 |
```

字段说明为空时写 `-`。

## 数组字段

数组字段不得输出空括号，必须在路径中写元素类型：

| 类型 | 字段路径 | 类型列 |
|------|----------|--------|
| 对象数组 | `data.userAddress[UserAddress].userAddressId` | `int64` |
| 字符串数组 | `data.userAddress[UserAddress].tags[string]` | `string[]` |
| int32 数组 | `selectedOptions[int32]` | `int32[]` |

## 枚举类型说明

枚举类型说明必须放在目录之后、接口之前。枚举值参考 `DATA_SPEC.md` 和当前 `.pbobjc.h`。

## 保存路径

完整 OC API 文档默认保存到 `docs/API_DOC_OC_YYYYMMDD.md`。

同时生成对应 HTML，默认保存到同名 `docs/API_DOC_OC_YYYYMMDD.html`。HTML 必须由 Markdown 转换得到，优先使用 `markdown-it`；可调用项目已有依赖、全局 `markdown-it` CLI，或通过 `npx markdown-it` 执行转换。

HTML 不应只交付裸片段；转换后必须按 [HTML_STYLE_SPEC.md](HTML_STYLE_SPEC.md) 包装为完整可阅读静态页面。包装层可以增加页面壳、内联样式和非侵入式增强脚本，但不得改变 Markdown 派生出的接口正文内容。

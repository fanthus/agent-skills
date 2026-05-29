---
name: ihuman-add-business-logging
description: 为 Objective-C 类添加业务日志。触发词："添加业务日志", "add business logging", "add logging", "ihuman-add-business-logging"。
version: 2.0.0
---

# iHuman Add Business Logging

为 Objective-C 项目中的类添加 ILLogBusiness 业务日志。

**核心约束：必须由用户明确指定目标文件，不得自行决定对哪些文件添加日志。用户未指定文件时，先询问确认。**

## 前置条件

确认目标文件已导入：
```objc
#import "ILLogMacros.h"
```

## Layer 选择

根据文件所属模块决定 Layer：

| 模块层级 | Layer | 使用宏 |
|----------|-------|--------|
| SDK 层（底层引擎） | `ILLogLayerSDK` | `ILLogBusinessSDK` / `ILLogBusinessAutoSDK` |
| Core 层（业务核心） | `ILLogLayerCore` | `ILLogBusinessCore` / `ILLogBusinessAutoCore` |

## 宏速查

| 宏 | UUID | Flow Phase | 适用场景 |
|---|---|---|---|
| `ILLogBusinessSDK(_tag, _uuid, _flowPhase, _content)` | 调用方传入 | 调用方传入 | 有分支/异步回调的方法 |
| `ILLogBusinessAutoSDK(_tag, _content)` | 自动生成 | `ILFlowPhaseNone` | 无分支同步方法 |
| `ILLogBusinessCore(_tag, _uuid, _flowPhase, _content)` | 调用方传入 | 调用方传入 | 有分支/异步回调的方法 |
| `ILLogBusinessAutoCore(_tag, _content)` | 自动生成 | `ILFlowPhaseNone` | 无分支同步方法 |

## 核心规则

### 1. Tag 命名

每个方法使用**独立 tag**（事件名），snake_case 格式。Tag 即方法标识，用于日志检索和方法间流转追踪。

| 场景 | Tag 示例 |
|------|---------|
| 配置/登录/登出/销毁 | `@"configure"`, `@"login"`, `@"logout"`, `@"destroy"` |
| 发送消息 | `@"send_custom"`, `@"send_signal"`, `@"send_msg"` |
| 连接状态回调 | `@"on_connecting"`, `@"on_connect_success"`, `@"on_connect_failed"` |
| 收到消息 | `@"recv_c2c_custom"`, `@"recv_group_text"`, `@"recv_signaling"` |
| 生命周期 | `@"lifecycle"`（固定） |
| 数据转换错误 | `@"im_parse"`, `@"data_parse"` |

### 2. Flow Phase 规则

**有分支/异步回调** → `ILLogBusinessCore` + Start/InProgress/End：

```
方法入口        → ILFlowPhaseStart
数据转换中间步骤 → ILFlowPhaseInProgress
每个 return 点  → ILFlowPhaseEnd（包括 fail 分支）
异步回调内      → ILFlowPhaseEnd（success/fail）
```

**无分支/无回调** → `ILLogBusinessAutoCore`（flow = None），放方法体第一行。

**uuid**：同一流程的 Start/InProgress/End 必须使用同一个 uuid。
```objc
NSString *uuid = [ILLogService generateUUID];
```

### 3. 日志位置

**Core flow（Start/InProgress/End）**：放在代码块最后一行业务逻辑之后。
**AutoCore（无 flow）**：放在方法体第一行。

### 4. 入参/返回数据

尽可能详细的入参和返回值：
- **Start**: 传入参数（userID、roomID、dataLength、targetCount 等）
- **InProgress**: 中间步骤标记（`@"step": @"serialized"`）
- **End success**: `@"result": @"success"` + 业务结果数据
- **End fail**: `@"result": @"fail"` + `@"code"` + `@"desc"` / `@"reason"`
- 所有 NSString 参数使用 `?: @""` 防止 nil 崩溃

### 5. 字典参数规范

- 多 key 字典必须用 `(@{...})` 包裹（防止预处理器拆分逗号）
- 单 key 或空字典无需包裹
- 不要使用 `@{@"event": ...}` —— tag 已标识事件
- AutoCore 可使用变量模式：

```objc
NSDictionary *logInfo = @{@"key": value ?: @""};
ILLogBusinessAutoCore(@"tag", logInfo);
```

## 代码模板

### 有分支/异步回调方法

```objc
- (void)loginWithUserID:(NSString *)userID
                userSig:(NSString *)userSig
             completion:(void (^)(BOOL, NSError * _Nullable))completion {
    NSString *uuid = [ILLogService generateUUID];
    ILLogBusinessCore(@"login", uuid, ILFlowPhaseStart, (@{@"userID": userID ?: @""}));
    [[V2TIMManager sharedInstance] login:userID userSig:userSig succ:^{
        self.isLoggedIn = YES;
        ILLogBusinessCore(@"login", uuid, ILFlowPhaseEnd, (@{@"result": @"success"}));
        if (completion) completion(YES, nil);
    } fail:^(int code, NSString *desc) {
        ILLogBusinessCore(@"login", uuid, ILFlowPhaseEnd, (@{@"result": @"fail", @"code": @(code), @"desc": desc ?: @""}));
        if (completion) {
            NSError *error = ...;
            completion(NO, error);
        }
    }];
}
```

### 提前 return — End 在 completion 之后、return 之前

```objc
if (![self isValidGroupID:roomID]) {
    ILLogBusinessCore(@"send_custom", uuid, ILFlowPhaseEnd, (@{@"result": @"fail", @"reason": @"invalid groupID"}));
    if (completion) {
        NSError *error = ...;
        completion(NO, error);
    }
    return;
}
```

### 无分支方法 — AutoCore 放方法体第一行

```objc
- (void)onConnecting {
    ILLogBusinessAutoCore(@"on_connecting", @{});
    // ... delegate notify ...
}
```

### 有 if/else 分支的接收方法 — Core flow

```objc
- (void)onRecvC2CCustomMessage:(NSString *)msgID sender:(UserInfo *)info customData:(NSData *)data {
    if (!data) return;
    NSString *uuid = [ILLogService generateUUID];
    ILLogBusinessCore(@"recv_c2c_custom", uuid, ILFlowPhaseStart, (@{@"msgID": msgID ?: @"", @"sender": info.userID ?: @""}));
    NSDictionary *payload = [self dictionaryWithData:data];
    NSString *type = payload[kMessageTypeKey];
    if ([type isEqualToString:kIMChatType]) {
        ILIMMessage *message = [[ILIMMessage alloc] initWithMessageID:msgID ...];
        ILLogBusinessCore(@"recv_c2c_custom", uuid, ILFlowPhaseEnd, (@{@"msgType": @"im", @"messageID": message.messageID ?: @""}));
        [self notifyDelegatesWithReceivedIMMessage:message];
    } else {
        ILSignalMessage *message = [[ILSignalMessage alloc] initWithMessageID:msgID ...];
        ILLogBusinessCore(@"recv_c2c_custom", uuid, ILFlowPhaseEnd, (@{@"msgType": @"signal", @"signalType": type ?: @""}));
        [self notifyDelegatesWithReceivedSignalMessage:message];
    }
}
```

### 生命周期日志

```objc
// .m 的 interface extension 中添加
@property (nonatomic, copy) NSString *lifecycleUUID;

// init 末尾
_lifecycleUUID = [ILLogService generateUUID];
ILLogBusinessCore(@"lifecycle", _lifecycleUUID, ILFlowPhaseStart, (@{@"event": @"init"}));

// destroy / teardown 末尾
ILLogBusinessCore(@"lifecycle", self.lifecycleUUID, ILFlowPhaseInProgress, (@{@"event": @"destroy"}));

// dealloc 末尾
ILLogBusinessCore(@"lifecycle", _lifecycleUUID, ILFlowPhaseEnd, (@{@"event": @"dealloc"}));
```

## 实施清单

按以下顺序为类添加业务日志：

1. **确定 Layer** — SDK 层还是 Core 层
2. **导入宏** — `#import "ILLogMacros.h"`
3. **添加 `lifecycleUUID` 属性** — `@property (nonatomic, copy) NSString *lifecycleUUID;`
4. **`init` / `dealloc` / `destroy`** — 添加 lifecycle 日志
5. **所有 public 方法** — 有分支加 Start/End，无分支加 AutoCore
6. **有异步回调的方法** — 每个回调内添加 End 日志
7. **数据转换步骤** — 添加 InProgress 日志
8. **编译验证**

## 禁止事项

- **未指定文件不操作**：必须由用户明确指定目标文件
- 禁止修改原有业务逻辑代码
- 禁止在日志中记录敏感数据（密码、token 等）
- 勿在高频回调中添加日志（如逐帧视频回调）
- 勿在纯 getter/setter 中添加日志
- 所有 NSString 参数使用 `?: @""` 防止 nil 崩溃

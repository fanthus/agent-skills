# 从 proto 提取 API 清单

在写 `ILLiveNetworkManager.{h,m}` 之前，先把要生成的接口清单理出来。这一步是**先想清楚再写**，避免写到一半发现某个 message 没看懂、又得回去翻。

## 三个 proto 的位置

```
~/ihuman/pb-idl/proto/services/api/student_api.proto
~/ihuman/pb-idl/proto/services/api/student_live_api.proto
~/ihuman/pb-idl/proto/services/api/user_api.proto
```

每次都从这里实时读，不要相信 skill 内置或上次的快照 —— proto 是会变的（这就是为什么要重跑这个流程）。

## 读 proto 的方法

每个 service `.proto` 一般有两类内容：
1. `service Xxx { rpc YyyMethod(YyyReq) returns (YyyResp); ... }` —— 接口列表
2. `message YyyReq { ... } message YyyResp { ... }` —— 数据结构（也可能 import 自其他 proto）

如果 service 块很清晰，读 service 块就能拿到完整接口清单。如果 proto 没有 service 块（只有 message），那就靠命名约定：成对出现的 `XxxReq` / `XxxResp` 就是一个接口。

**proto 里的 import 要不要追读**：
- 如果 import 的是 `common/` 或 `interface/` 下的基础类型（Course、Lesson、Stream 之类），不用追读，知道是个引用就行
- 如果 import 的是另一个 service proto，可能意味着接口跨文件引用，这时候读一下确认归属

## 列接口清单的格式

把读出来的接口先列成表格再写代码，方便用户 review 和你自己核对：

```
来源 proto             | rpc 名             | Req                  | Resp                  | path
-----------------------|-------------------|----------------------|----------------------|--------------------------
student_live_api.proto | StudentJoin       | StudentJoinReq       | StudentJoinResp       | /student_live/student_join
student_live_api.proto | StudentLeave      | StudentLeaveReq      | StudentLeaveResp      | /student_live/student_leave
...
```

path 列的来源：
1. proto 里 rpc 上面是不是有 `option (google.api.http) = { post: "/xxx" }` 之类的注解 → 直接用
2. 没有注解的话，根据 ILNetworkDefine.h 里现有的 path 推断（如果接口名字跟旧版一致）
3. 都没有就按 `/<service>/<rpc_snake_case>` 拼一个，**生成完后告诉用户这些 path 是猜的，需要核对**

## 跟旧版 ILLiveNetworkManager 的差异和兼容性基线

写新版前必须先建立旧版兼容性基线：旧版已经稳定的 OC 方法签名、参数顺序、参数类型、参数命名，以及 `.m` 里 req 字段赋值/类型转换/nil 防御。后续生成当前 proto 仍存在的接口时优先沿用这些内容。

如果旧文件还在，在删除旧文件**之前**先 grep/读取现有的方法清单：

```bash
grep -E "^\+ \(void\)" ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.h
```

同时从 `.m` 里读取对应实现，记录 req 赋值方式，例如：
- `req.roomId = roomID;`
- `req.roomId = @(roomID).stringValue;`
- `req.leaveReason = leaveReason ?: @"";`
- 旧版没有暴露 proto 字段，或者把多个字段折叠成一个业务参数

如果旧文件已经被删除，用 skill 内置的 `assets/ILLiveNetworkManager.h.example` 和 `assets/ILLiveNetworkManager.m.example` 作为稳定基线；如果项目有 git 历史，也可以用最近一次真实版本辅助确认。不要因为目标文件被删了就丢掉旧版签名信息。

跟 proto 列出的清单 diff 一下，给用户看的"变更预览"至少分四类：
- 新增接口：旧版没有、当前 proto 有，生成时按旧版相邻业务接口风格推导签名
- 沿用旧签名：旧版有、当前 proto 仍有，保持旧 OC 方法签名和 req 映射
- 签名/映射变化：旧版有、当前 proto 仍有，但字段删除/类型变化导致必须调整
- 移除接口：旧版有、当前 proto 没有，新版不再生成

这一步不是可选项。它是避免重建文件时破坏上层调用方兼容性的关键步骤。

## 边界情况

**proto 里有 rpc 但 example 旧版没对应方法**：可能是新增接口，也可能是历史上特意没暴露给客户端。生成新版时**默认全部生成**，让 OC 这层覆盖 proto 全集；如果用户明确说某些接口不要，再删。

**proto 里没有的 rpc 但旧版有**：说明这个接口被 proto 移除了，新版**不要保留**。用户大概率知道这件事（毕竟是他改的 proto），但生成完后简单提一句"以下旧接口已移除：xxx, yyy"，避免他错过。

**rpc 名跟旧 OC 方法名对不上**：例如 proto 叫 `GetReplay`，旧版 OC 叫 `getStudentReplayInfo`。如果能确认它们是同一个接口，优先保留旧 OC 方法名，避免无意义地破坏调用方。生成时在方法上方加注释说明对应的 proto rpc 名。

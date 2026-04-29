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

## 跟旧版 ILLiveNetworkManager 的差异

如果想知道这次 proto 变更带来了哪些新增/删除/改动接口，可以在删除旧文件**之前**先 grep 出现有的方法清单：

```bash
grep -E "^\+ \(void\)" ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.h
```

跟 proto 列出的清单 diff 一下，能预见这次改动的范围（新增接口、签名变化的接口、被移除的接口）。这是给用户看的"变更预览"，让他确认是不是预期内的改动，再开始正式生成。

不是必须步骤 —— 如果用户已经知道改了啥、只想要新文件，跳过这步直接生成也行。但跑一次 diff 大概率会避免一些惊喜。

## 边界情况

**proto 里有 rpc 但 example 旧版没对应方法**：可能是新增接口，也可能是历史上特意没暴露给客户端。生成新版时**默认全部生成**，让 OC 这层覆盖 proto 全集；如果用户明确说某些接口不要，再删。

**proto 里没有的 rpc 但旧版有**：说明这个接口被 proto 移除了，新版**不要保留**。用户大概率知道这件事（毕竟是他改的 proto），但生成完后简单提一句"以下旧接口已移除：xxx, yyy"，避免他错过。

**rpc 名跟旧 OC 方法名对不上**：例如 proto 叫 `GetReplay`，旧版 OC 叫 `getStudentReplayInfo`。一般以 proto 当前命名为准翻译成驼峰，但如果旧名字明显更符合业务习惯（用户改 proto 是为了规范化、不想动客户端代码），可以保留旧 OC 方法名。这种情况下生成时在方法上方加注释说明对应的 proto rpc 名。

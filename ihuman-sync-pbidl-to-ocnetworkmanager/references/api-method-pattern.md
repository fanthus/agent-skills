# API 方法生成模式

每个 API 方法在 .h 和 .m 里各一段，按下面的固定模式写。变化的只是参数、PB 类名、Path 常量。

`assets/ILLiveNetworkManager.{h,m}.example` 是完整真实样例，遇到拿不准的细节去对照。

## 先保兼容，再生成新形态

生成方法前先把当前 proto 接口跟旧版方法对上。只要某个接口在旧版已经存在，并且当前 proto 仍然存在，就把旧版稳定的 OC 形态当作默认答案：
- `.h` 方法名、参数名、参数类型、参数顺序、success/failure block 类型优先沿用旧版
- `.m` 里的 req 字段赋值、类型转换、nil 防御、默认值优先沿用旧版
- 旧版 OC 方法名和当前 rpc 名不完全一致时，只要能确认是同一接口，也优先保留旧 OC 方法名
- 只有 proto 字段删除、字段类型真实变化、Req/Resp 类名变化等导致旧签名无法正确表达当前接口时，才调整签名或映射

新增接口才按本文件后面的命名约定从 proto 推导；推导时也要参考旧版相邻业务接口，让方法签名风格尽量一致。

如果目标 `ILLiveNetworkManager.{h,m}` 已经被删除，使用 `assets/ILLiveNetworkManager.{h,m}.example` 作为旧版稳定基线；必要时再从项目 git 历史找最近一次真实版本确认。不要因为旧文件被删除就改用全新的签名风格。

## 注释是必填项，不是可选项

这一份文件里所有"模式"都包含注释。生成方法时**不要省略注释** —— 这是这个 SDK 代码风格的核心约定，比方法实现本身还重要。原因：

- 这个 Manager 是 SDK 的对外接口，注释是给上层业务调用方看的，没注释意味着调用方要去翻 proto 才能搞懂什么时候该用哪个接口
- proto 里的 comment 信息密度低（往往就一句话），靠 OC 注释把"何时用、为什么这么设计、返回什么"补齐
- example 里**每一个方法**都有注释（.h 三槽位、.m 一行），生成的新代码要保持同等密度

具体规则：

**.h 文件里**，每个方法上方写 `///` doc comment，三槽位（描述 / 【场景】/ 【返回】）：
- 描述（必填）：一句话说这个接口干嘛，动词开头
- 【场景】（按 proto 注释填，没线索可省略）：什么时候调、跟其他接口怎么配合
- 【返回】（按 proto 注释和 Resp 字段填，没线索可省略）：response 主要字段一句话概括

**.m 文件里**，每个方法实现上方写一行 `//` 中文注释，比 .h 更简略，主要说业务场景。

**proto 完全无注释的特殊情况**：.h 至少要有"描述"那一行（从方法名 + 业务上下文推断写一句），不能裸露；.m 上方一行也要有，能简则简。**完全无注释的方法是 NG 的，必须返工。**

## 命名约定

| proto 里的 | OC 里的 |
|---|---|
| `rpc StudentJoin` 或 message `StudentJoinReq` | 方法名 `studentJoinWith...:` |
| message `StudentJoinReq` | 类名 `ILILStudentJoinReq` |
| message `StudentJoinResp` | 类名 `ILILStudentJoinResp` |
| 字段 `room_id` (int64) | 参数 `roomID` (int64_t)、req 属性 `req.roomId` |
| 字段 `course_id` (int64) | 参数 `courseID` (int64_t)、req 属性 `req.courseId` |
| 字段 `lesson_id` (int64) | 参数 `lessonID` (int64_t)、req 属性 `req.lessonId` |
| 字段 `quiz_id` (int64) | 参数 `quizID` (int64_t)、req 属性 `req.quizId` |
| 字段 `group_id` (int64) | 参数 `groupID` (int64_t)、req 属性 `req.groupId` |
| 字段 `leave_reason` (string) | 参数 `leaveReason` (NSString *) |
| 字段 `platform` (enum CCPlatformType) | 参数 `platform` (ILCCPlatformType) |

PB 生成的类名前缀是 `ILIL`：第一个 `IL` 是包前缀，第二个 `IL` 来自文件 prefix（IsLive 之类）。如果实际生成的产物不是这个前缀，**以 `ilprotocolbuffer/ILProtocolBuffer/Classes/interface/` 下的实际产物为准**，不要硬猜。

蛇形命名转驼峰：`room_id` → `roomId`（属性）和 `roomID`（参数，ID 全大写更符合 OC 习惯）。

## 路径常量

每个接口对应一个 `ILNetworkPathXxx` 常量。这些常量统一定义在 `ILNetworkDefine.{h,m}` 里 —— 不是写在 ILLiveNetworkManager 内部。

生成代码时：在 .m 里直接引用 `ILNetworkPathXxx`，**不要内联字符串字面量**。常量本身的命名规则、路径字符串怎么来、增删改怎么同步，参见 `references/network-define-update.md`。Step 7（写 ILLiveNetworkManager）和 Step 8（更新 ILNetworkDefine）是配套的，别只做一边。

## .h 里的方法声明

模式：

```objc
/// 一句话描述这个接口干嘛的
/// 【场景】何时调用、为什么这样设计（1-2 句，从 proto 的 comment 或上下文推断）
/// 【返回】response 主要字段，一句话概括
+ (void)<methodName>WithRoomID:(int64_t)roomID
                     <param2>:(<type>)<param2>
                      success:(void (^)(<RespClass> *resp))success
                      failure:(void (^)(NSError *error))failure;
```

注释要点：
- 三槽位（描述 / 场景 / 返回）不是死规定，但能写就写。proto 里的 comment 是主要信息源
- 描述用陈述句、动词开头："学生加入房间"、"获取房间公共状态"
- 【场景】解释**为什么有这个接口**：什么时候调、跟其他接口怎么配合、是否拆分接口的子集等
- 【返回】不是字段清单，是一句话概括："RTC 配置、频道列表、IM 配置"

参数顺序：旧接口优先沿用旧版；新增接口按业务主键（roomID/courseID 等）在前，可选/次要参数在后，最后是 `success` 和 `failure`。

## .m 里的方法实现

内部 helper 固定只保留这一种 POST 入口，不要再生成额外的 path 参数转发 helper：

```objc
+ (void)il_postRequest:(GPBMessage *)request
         responseClass:(Class)responseClass
               success:(ILNetworkSuccessBlock)success
               failure:(ILNetworkFailureBlock)failure {
    ILLiveNetworkManager *manager = [self shared];
    [self il_logPostCurlWithPath:request.networkPath request:request];
    [manager.service requestWithPath:request.networkPath
                                    method:ILHTTPMethodPost
                                   request:request
                             responseClass:responseClass
                                   success:success
                                   failure:failure];
}
```

模式：

```objc
// 一行中文注释，描述这个接口（比 .h 里更简略）
+ (void)<methodName>WithRoomID:(int64_t)roomID
                       success:(void (^)(<RespClass> *resp))success
                       failure:(void (^)(NSError *error))failure {
    <ReqClass> *req = [[<ReqClass> alloc] initWithPath:ILNetworkPath<Xxx>];
    req.roomId = roomID;
    [self il_postRequest:req
         responseClass:[<RespClass> class]
              success:^(id response) {
        if (success) {
            success(response);
        }
    } failure:^(NSError *error, id response) {
        if (failure) {
            failure(error);
        }
    }];
}
```

要点：
- Req 必须用 `[[<ReqClass> alloc] initWithPath:ILNetworkPath<Xxx>]` 创建，把 path 绑定到 `request.networkPath`
- 全部走 `il_postRequest:responseClass:success:failure:`，不要再生成或调用旧的 path 参数转发 helper
- 内部 helper 只保留 `il_postRequest`，实现里先取 `ILLiveNetworkManager *manager = [self shared]`，调用 `il_logPostCurlWithPath:request:`，再用 `manager.service requestWithPath:request.networkPath ...`
- success block 形参类型是 `id response`，调用外层时直接传（OC 类型系统会自动转）
- failure block 形参是 `(NSError *error, id response)`，外层只关心 `error`
- 字符串字段做 nil 防御：`req.leaveReason = leaveReason ?: @"";`
- 空响应（无返回字段）也要传 responseClass（PB 会有空 Resp 类，例如 `ILILXxxResp`）
- 旧版存在特殊映射时优先保留，例如 int64 参数转 string、OC 参数名和 req 属性名不完全一致、默认值或 nil 防御策略；如果当前 proto 类型变化让特殊映射不再合理，先标为"签名/映射变化"给用户确认

## 分组（pragma mark）

按 proto 文件分组，分组标题用中文业务术语，不要直接用文件名。例如：

```objc
#pragma mark - 直播基础      // student_live_api 里的核心进出/状态接口
#pragma mark - 互动进度      // student_live_api 里的拆分进度接口
#pragma mark - 学生信息      // student_api 里的用户/小组信息
#pragma mark - 用户          // user_api 里的登录/资料
```

是否在一个 proto 内部再细分子组，看 rpc 数量：
- ≤ 5 个 rpc：不细分，全部放一个分组里
- \> 5 个 rpc：考虑细分，但前提是有**显而易见**的语义边界（例如 example 里 student_live_api 的"基础接口"和"进度拆分接口"明显是两类用途）。如果只是可分可不分，那就不分。

分组名优先沿用 example 里已有的（"直播基础"、"互动进度"等），新增的 rpc 如果能塞进现有组就塞进去；只有跟现有组都不沾边时才新建组。

不要为了"每个 proto 都该有自己的分组"而硬分组 —— 用户的小组划分逻辑是**业务场景**驱动的，不是文件结构驱动的。

## 边界情况

**字段类型不匹配**：例如 example 里 `getStudentActivityProgressWithRoomID:` 把 int64 roomID 转成了 string（`req.roomId = @(roomID).stringValue;`）。如果当前 proto 仍是 string，保留旧版 int64 入参 + string 转换这种稳定对外签名；如果当前 proto 已改为 int64，再判断是否需要移除转换，并把这类变化列入变更预览。

**注释里的字段在 proto 里被注释掉了**：example 里 `studentJoinWithRoomID:` 的 `req.courseId/lessonId` 用 `//` 注释掉了。说明历史上 proto 字段变过。生成新代码时按 proto 当前定义来，不要保留这种过时痕迹。

**proto 里 rpc 没有显式 comment**：注释三槽位里的【场景】和【返回】可以省略，但**描述这一行不能省** —— 从方法名和业务上下文推断写一句。完全无注释的方法不行。

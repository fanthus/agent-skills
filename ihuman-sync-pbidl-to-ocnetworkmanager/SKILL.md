---
name: ihuman-sync-pbidl-to-ocnetworkmanager
description: Sync iHuman pb-idl proto changes into the Objective-C network manager by regenerating `ILLiveNetworkManager.h/.m` in the SuperClassSDK iOS project. Use this whenever the user mentions regenerating the network manager, syncing pb-idl proto changes into SuperClassSDK, refreshing the live network interface, "重新生成 ILLiveNetworkManager", "同步 pb-idl 到 SuperClassSDK", "把新的 proto 接口翻译成 OC", or any task that involves rebuilding the OC network layer of SuperClassSDK from the three service protos (student_api, student_live_api, user_api). Trigger this skill aggressively whenever the user is working in the ihuman workspace (pb-idl + ilprotocolbuffer + superclasssdk) and wants to refresh the network layer — even if they describe the task informally without naming the manager class.
---

# iHuman Sync pb-idl to OC Network Manager

把 pb-idl 里三个 service proto 的最新版翻译成一份合并的 `ILLiveNetworkManager.h/.m`，重建 SuperClassSDK 的网络层。

## 路径与前置假设

固定路径（用户的个人 ihuman 工作区）：

```
~/ihuman/pb-idl/                                       # PB proto 源
~/ihuman/ilprotocolbuffer/                              # PB 编译产物（OC 库）
~/ihuman/superclasssdk/                                 # 主 SDK
~/ihuman/superclasssdk/Example/Podfile                  # 要切本地路径的 Podfile
~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.{h,m}   # 删除并重建的目标
```

进入这个 skill **之前**用户已经手动完成：
- 跑过 `pb-idl/gen_objc.sh` 编译最新 proto
- 把 `pb-idl/oc_build/` 下的产物拖入了 `ilprotocolbuffer/ILProtocolBuffer/Classes/`

如果你怀疑用户跳过了前置步骤（例如 `ilprotocolbuffer/ILProtocolBuffer/Classes/interface/` 下没有最新生成的 `.pbobjc.h`），先问一句再继续，不要替他做。

## 总体流程

```
1. 清 DerivedData
2. Podfile → 本地路径
3. pod install
4. 删旧的 ILLiveNetworkManager.{h,m}
5. 读三个 proto，列接口清单
6. （可选）跟旧版 diff，给用户看变更预览
7. 用 skeleton + 生成的 API 方法，写新的 ILLiveNetworkManager.{h,m}
   —— 每个 API 方法都必须带注释（.h 三槽位 doc comment、.m 一行业务说明）
8. 更新 ILNetworkDefine.{h,m}：把新清单里所有 path 常量同步进去（新增/改路径/删除已废弃的）
9. 用户验收
10. Podfile 改回远程版本
```

每一步详细做法分散在 references 里，你按需要读。下面只标重点。

## 关键参考文件

- `references/environment-prep.md` — Step 1-4 和 Step 10 的具体命令、Podfile 替换字符串、踩坑点。**做环境准备前先读这个。**
- `references/proto-to-api-list.md` — Step 5-6 怎么从 proto 提取接口清单、怎么跟旧版 diff。**读完 proto 准备列清单时读这个。**
- `references/api-method-pattern.md` — Step 7 单个 API 方法在 .h 和 .m 里的代码模式、命名约定、边界情况。**生成代码时读这个。**
- `references/network-define-update.md` — Step 8 怎么同步更新 `ILNetworkDefine.{h,m}`，包括常量命名、路径字符串来源、增删改逻辑、与 ILLiveNetworkManager.m 的对账。**写完 ILLiveNetworkManager.m 后读这个。**
- `assets/ILLiveNetworkManager.h.skeleton` / `.m.skeleton` — 文件骨架，固定不变的部分（单例、setup/logout、ILNetworkConfigProtocol、内部 post 方法），里面有 `{{API_DECLARATIONS}}` / `{{API_IMPLEMENTATIONS}}` / `{{ADDITIONAL_PB_IMPORTS}}` 占位。**写新文件时基于这个起手。**
- `assets/ILLiveNetworkManager.h.example` / `.m.example` — 上一版的完整真实代码，遇到拿不准的细节去对照。注意 example 是上一版 proto 的产物，不要直接抄接口列表，只参考代码风格。

## 跟用户协作的节奏

这个流程里有几处必须停下来跟用户确认，不要一口气跑完：

**确认点 1：列完接口清单后，开始生成代码前。**
把清单（proto → rpc → Req/Resp → path）列成表格给用户看，问"这个清单对吗？"。原因：proto 里某些 rpc 可能用户**不希望**暴露给客户端（运维接口、调试接口等），列清单是用户筛选的最后机会。

**确认点 2：新的 .h/.m 写完后，把 Podfile 改回远程版本之前。**
先让用户看新文件，确认接口签名、注释、分组合理。如果用户要改，改完再说"现在我把 Podfile 改回远程版本，结束流程"。

中间如果遇到拿不准的（比如某个字段类型 proto 里是 string、example 里转成了 int64，搞不清是历史包袱还是有意为之），停下来问，不要瞎猜。

**通用兜底原则：任何时候只要不确定，先问再做。**
除了上面两个预设的确认点，凡是流程中出现拿不准的情况 —— 路径不存在、proto 解析有歧义、命名跟旧版冲突、不知道分组放哪、不知道某个字段要不要做 nil 防御 —— 都先停下来问用户，不要替他做选择。
- 用户回复"按你的判断办"或类似明确授权 → 继续往下做、不再问
- 用户给出具体决定 → 执行该决定、不再就同一问题反复追问
- 同一类问题第二次出现：如果上次用户已经表达过偏好，这次可以默认沿用、简短告知一下即可（"沿用上次的处理：xxx"）

成本权衡：多问一次的成本是用户多回一句话；不问做错的成本是改文件、改 ILNetworkDefine、可能还要回滚 Podfile。前者明显更便宜。

## 不要做的事

- **不要清整个 `~/Library/Developer/Xcode/DerivedData/`** —— 用户可能同时在跑别的 Xcode 项目。只清 `SuperClassSDK-*`。
- **不要在没确认前置步骤的情况下假设 ilprotocolbuffer 是最新的** —— 这是流程出错的最常见原因。
- **不要把三个 proto 拆成三个 Manager 类** —— 用户明确要合并到一个文件。
- **不要保留 example 里旧版的接口** —— 以当前 proto 为准，example 只用于学习代码风格。
- **不要在 Podfile 改回远程后再跑 pod install** —— 会触发远程拉取，跟当前任务无关，可能引入意外变更。
- **不要硬猜 PB 类名前缀** —— example 里前缀是 `ILIL`，但如果 proto 改了 `option objc_class_prefix`，前缀就变了。生成代码前先看 `ilprotocolbuffer/ILProtocolBuffer/Classes/interface/<service_name>/` 下实际产物的类名。
- **不要省略方法注释** —— 哪怕 proto 里完全没注释，.h 里也要至少写一行 `///` 描述（从方法名 + 业务上下文推断）；.m 里每个方法上方至少一行 `//` 说明。生成无注释的"裸"方法是 NG 的。详见 `references/api-method-pattern.md`。

## 完整流程示例（高层）

```
[ 读 references/environment-prep.md ]
[ Step 1 ] rm -rf ~/Library/Developer/Xcode/DerivedData/SuperClassSDK-*
[ Step 2 ] view + str_replace 改 ~/ihuman/superclasssdk/Example/Podfile
[ Step 3 ] cd ~/ihuman/superclasssdk/Example && pod install

[ 读 references/proto-to-api-list.md ]
[ Step 5 ] view ~/ihuman/pb-idl/proto/services/api/{student_api,student_live_api,user_api}.proto
           列出接口清单
[ Step 6 ] grep 旧版 .h 提供的方法（必须在删除文件之前做，结果留着用）
           跟新清单 diff，告诉用户"新增 X、改动 Y、移除 Z"
==> 确认点 1：等用户 OK <==

[ Step 4 ] rm -f ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.{h,m}

[ 读 references/api-method-pattern.md ]
[ 读 assets/ILLiveNetworkManager.{h,m}.skeleton 和 .example ]
[ Step 7 ] 基于 skeleton 创建新文件，按 references/api-method-pattern.md 生成 API 方法。
           每个方法必须带注释：.h 用 /// 三槽位（描述/【场景】/【返回】），.m 上方一行中文业务说明。
           写入：~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.{h,m}
[ Step 8 ] 更新 ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILNetworkDefine.{h,m}：
           按新清单同步所有 path 常量（声明 + 赋值）
==> 确认点 2：让用户看新文件 <==

[ Step 10 ] str_replace 把 ~/ihuman/superclasssdk/Example/Podfile 改回远程版本
[ 完成 ] 告诉用户：Podfile 已恢复，但没有跑 pod install；ilprotocolbuffer 推 git 后再 pod install
```

注意实际执行顺序跟"总体流程"那张列表的编号略有不同：grep 旧版方法（Step 6）必须在删除文件（Step 4）之前完成，否则 grep 不到东西。如果觉得编号顺序乱可以无视编号，按这个示例的实际顺序跑。

## 失败处理

最高优先级原则：**任何不确定的情况，先问用户再处理**（详见上面"跟用户协作的节奏"里的通用兜底原则）。下面列的是常见的具体场景：

- `pod install` 失败 → 停下来报错给用户，最常见原因是 ilprotocolbuffer 那边 `.podspec` 没更新或者前置步骤漏了。
- proto 解析不出接口（文件空、语法错）→ 停下来让用户检查 proto。
- 中途任何一步用户喊停 → 立即停下，**不要**自动把 Podfile 改回远程（让用户在本地路径状态下调试）。要恢复时用户会显式说。

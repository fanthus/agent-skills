---
name: il-ihuman-inspector
description: Objective-C 类代码审查，扫描 Bug、坏味道、内存泄漏、线程风险、语法隐患、重复符号、@optional 专项、KVO/KVC、ARC 桥接、Runtime 安全。触发词："审查", "review", "代码审查", "扫描", "check code", "code review"。
version: 3.0.0
---

# Code Review

对单个 Objective-C 类的全面静态审查，覆盖十大维度。

**输入**: 一个 `.h` 或 `.m` 文件路径
**输出**: 结构化审查报告，包含问题列表 + 严重度 + 修复建议

## 前置条件

```
必须由用户明确指定目标文件。
未指定文件时，先询问确认。
--clear-cache 无需目标文件，直接清缓存并退出。
```

## 项目适配

审查前从项目 CLAUDE.md 提取参数，适配不同项目的编码约定。

### Step 0: 读取 CLAUDE.md 提取参数

| 参数 | 来源 | 默认值 |
|------|------|--------|
| `class_prefix` | CLAUDE.md 中的类名前缀约定（如 `IL`） | `nil`（无前缀） |
| `sources_root` | 从目标文件路径向上查找含 `.podspec` 或 `Podfile` 的目录 | 目标文件所在的 git 仓库根 |
| `has_code_style` | CLAUDE.md 是否引用 CODE_STYLE.md | `false` |
| `protocol_convention` | CLAUDE.md 中的协议命名规则（如 `Name + Protocol/Delegate`） | `false`（不检查） |

提取逻辑：
1. 读取项目根 CLAUDE.md（从目标文件路径向上查找）
2. 搜索 `class_prefix`：匹配前缀约定描述（如 "类名必须使用 `IL` 前缀"）→ 提取前缀字符串；未找到则 `nil`
3. 搜索 `sources_root`：从目标文件目录向上逐级查找 `.podspec` / `Podfile` / `.xcodeproj` → 以找到的目录为根；未找到则使用 git 仓库根
4. 搜索 `has_code_style`：CLAUDE.md 中出现 `CODE_STYLE.md` 即为 `true`
5. 搜索 `protocol_convention`：匹配协议命名规则描述 → 提取规则；未找到则 `false`

完成后进入 Step 1。

审查流程开始时，首先检查是否为 `--clear-cache` 模式：若是，删除 `cache/` 目录下所有 `.json` 文件，打印 "已清除 N 个缓存文件"，直接结束。否则进入 Step 0。

## 模式

| 模式 | 触发 | 检查维度 | Token 消耗 |
|------|------|----------|------------|
| **Full**（默认） | `/ihuman-code-inspector <文件>` | 全部 10 维 | ~10-20K |
| **Quick** | `/ihuman-code-inspector <文件> --quick` | 仅 1-6 维（基础） | ~5-10K |
| **Clear** | `/ihuman-code-inspector --clear-cache` | — | 0 |

**Quick 模式跳过项：**
- 七、@optional 协议专项（减少关联协议读取）
- 八、KVO/KVC 安全
- 九、ARC 桥接
- 十、Runtime 安全
- 对应的交叉搜索 grep 命令

Quick 模式适用于：简单修改自检、小型工具类、无 CF/Runtime/KVO 依赖的纯业务类。

**`--clear-cache`**：删除 `cache/` 目录下所有 `.json` 缓存文件。下次审查时全部重新读取源码并生成缓存。

## 协议缓存

为减少重复读取公共协议头文件，维护本地缓存。

### 缓存位置

```
.agents/skills/ihuman-code-inspector/cache/
```

### 缓存格式

每个协议一个 JSON 文件，命名：`<协议名>.json`

```json
{
  "protocol": "ILIMEngineDelegate",
  "source": "ILClassroomCore/Classes/Service/Engine/IM/ILIMEngineProtocol.h",
  "source_mtime": 1716451200.0,
  "methods": [
    {
      "signature": "engine:didReceiveSignalMessage:",
      "returnType": "void",
      "required": false,
      "parameters": [
        {"type": "id<ILIMEngineProtocol>", "name": "engine"},
        {"type": "ILSignalMessage *", "name": "message"}
      ]
    }
  ]
}
```

### 缓存使用规则

1. 审查前先检查 `cache/` 目录，命中后比较 `source_mtime` 与协议源文件的当前 mtime
2. mtime 一致 → **跳过读取源码**，直接用缓存
3. mtime 不一致 → 缓存过期，读取协议源码后**自动更新缓存文件**（含新 mtime）
4. 缓存未命中 → 读取协议源码后**自动生成缓存文件**（含 mtime）
5. 用户通过 `--no-cache` 强制跳过缓存，全部实时读取

### 自动缓存策略

**不预定义协议白名单**。审查时自动发现：扫描目标文件的 `#import` 和 `<>` 协议引用，任何协议被当前审查会话引用 2 次以上即自动加入缓存。缓存随项目积累自然增长。

---

## 审查维度

| 维度 | 检查项 |
|------|--------|
| **Bug 扫描** | nil 消息、参数校验、协议一致性、逻辑错误、回调错误 |
| **坏味道** | 死代码、魔法数字、过长方法、命名违规、遗留 TODO |
| **内存泄漏** | 循环引用、NSTimer、Observer 未移除、CF 对象未释放 |
| **线程风险** | 共享属性无锁、非主线程 UI、block 回调线程不明 |
| **语法隐患** | BOOL/int 混用、浮点比较、nil coalescing 误用、format 参数 |
| **重复符号** | Category 冲突、重复宏、C 函数重名、extern 不匹配 |
| **@optional 专项** | respondsToSelector 拼写、@optional 属性、遗漏 callback |
| **KVO/KVC 安全** | keyPath 拼写、context 冲突、removeObserver 配对、手动通知 |
| **ARC 桥接** | __bridge 误用、CFRelease 配对、CFBridging 所有权 |
| **Runtime 安全** | +load 耗时、swizzling 安全、associatedObject 策略、performSelector |

---

## 审查流程

### Step 1: 读取目标文件 + 对应头文件/协议

目标（`.m` 文件时）：
1. `目标.m` — 实现（**必须读**，不使用缓存）
2. `目标.h` — 接口声明（**必须读**）
3. 协议头文件 — 先查 `cache/` 目录，命中则用缓存 JSON，未命中则读源码后自动写缓存
4. 依赖的外部协议 — 同上，先查缓存

`--no-cache` 模式下全部实时读取。

### Step 2: 代码库交叉搜索

```
# 检查是否有重复符号 / category 冲突
grep -rn "方法名/类名" {sources_root} --include="*.h" --include="*.m"

# 检查 duplicate symbol 隐患
grep -rn "^@implementation 类名" {sources_root} --include="*.m"

# 检查 extern 声明与实际定义
grep -rn "extern" {sources_root} --include="*.h"
```

### Step 3: 按模式执行检查

**Full 模式**: 按以下十大维度逐类扫描。

**Quick 模式**: 仅执行一~六维。跳过七~十维及其交叉搜索命令。报告中标注 `[Quick]`。

按以下清单逐类扫描，发现的所有问题汇总到报告中。

---

## 一、Bug 扫描

### 1.1 nil / 参数校验

- [ ] block 参数为 nil 时直接调用（`completion()` 前未判空）
- [ ] `NSDictionary` / `NSArray` 字面量中 key/value 可能为 nil
- [ ] public 方法缺少 nil 参数保护（返回合理 error 或提前 return）
- [ ] `NSString` 不判空直接传给日志（应使用 `?: @""`）

### 1.2 协议一致性

- [ ] `@optional` 协议方法调用前未检查 `respondsToSelector:`
- [ ] 协议声明方法在 .m 中未实现（缺少 method）
- [ ] 回调方法名与协议定义不一致（如 `didAppear` vs `viewDidAppear`）

### 1.3 逻辑错误

- [ ] 日志字段值类型错误（如 userID 用了 NSDictionary）
- [ ] if/else 分支语义矛盾（成功回调中调了失败处理方法）
- [ ] 条件表达式永远为真/假
- [ ] 枚举 switch 缺少 default 或未覆盖所有 case

### 1.4 API 误用

- [ ] `dispatch_once` token 非 static
- [ ] `NSRange` 越界
- [ ] `performSelector:` 参数超过 2 个
- [ ] `stringWithFormat:` 格式符与参数类型不匹配

---

## 二、坏味道

### 2.1 死代码

- [ ] `respondsToSelector:` 检查的方法不在任何协议中声明
- [ ] 注释掉的代码块（超过 3 行）
- [ ] 永远不会执行的 if 分支
- [ ] 只声明未使用的变量

### 2.2 代码尺寸

- [ ] 单个方法 > 80 行
- [ ] 单个类 > 800 行
- [ ] 方法参数 > 6 个
- [ ] 嵌套层级 > 4 层

### 2.3 命名规范

根据 CLAUDE.md 提取的 `class_prefix` 和 `protocol_convention`：

- [ ] 如果 `class_prefix` 非空：类名缺少 `{class_prefix}` 前缀
- [ ] 如果 `protocol_convention` 非空：协议名不符合约定规则
- [ ] 如果 `has_code_style` 为 true：根据 CODE_STYLE.md 检查命名（驼峰、常量前缀等）
- [ ] 如果以上参数全为默认值：跳过命名规范检查

### 2.4 其他

- [ ] 魔法数字（硬编码的数值，非 #define / const）
- [ ] TODO/FIXME/HACK 遗留
- [ ] 重复代码块（同一文件中出现 3 次以上相似的 5+ 行代码）

---

## 三、内存泄漏

### 3.1 循环引用

- [ ] block 中直接使用 `self` 而未用 `__weak typeof(self) weakSelf`
- [ ] block 中 `self.someProperty` 实际持有 self
- [ ] delegate 属性使用 `strong` 而非 `weak`
- [ ] NSTimer scheduledTimer 强引用 target

### 3.2 资源未释放

- [ ] `dealloc` 未移除 NSNotificationCenter observer
- [ ] `dealloc`/`teardown` 未移除 KVO observer
- [ ] Core Foundation 对象创建后有对应的 CFRelease
- [ ] `dispatch_source` 创建后未 cancel

### 3.3 其他

- [ ] block 属性使用 `strong` + `self.block = ^{ [self doSomething]; }` 造成循环
- [ ] `NSHashTable` / `NSMapTable` 创建为 strong 而非 weak 导致监听器无法释放

---

## 四、线程风险

### 4.1 数据竞争

- [ ] `nonatomic` 属性在多线程同时读写（无锁/无队列保护）
- [ ] `weak` 属性在异步 block 中使用前未强引用保护
- [ ] 可变集合（NSMutableArray/Dictionary）多线程访问无锁

### 4.2 主线程

- [ ] completion block 中更新 UI 但未 dispatch 到主线程
- [ ] 耗时操作在主线程执行

### 4.3 锁使用

- [ ] `@synchronized` 嵌套锁顺序不一致（可能死锁）
- [ ] `dispatch_sync` 在同一个 serial queue 上嵌套调用
- [ ] 锁范围过大（锁内做 IO/网络操作）

---

## 五、语法隐患

### 5.1 类型混淆

- [ ] `BOOL` 变量与 `int`/`NSInteger` 混用
- [ ] 浮点数用 `==` 比较
- [ ] `isEqual:` vs `==` 误用于 NSString/NSNumber

### 5.2 Block 使用

- [ ] block 声明为 `strong` 属性的 block 未用 `copy`
- [ ] `__block` 修饰符滥用（无修改需求时使用）
- [ ] block 中的 `__strong` 引用未检查是否为 nil

### 5.3 防御性编程

- [ ] `NSUserDefaults` 读取后未做类型校验
- [ ] `NSCoder` 解档后未判空
- [ ] `JSONObjectWithData:` 返回值未做类型判断
- [ ] `NSArray` / `NSDictionary` 下标访问越界

---

## 六、重复符号

### 6.1 Category 冲突

- [ ] Category 方法名未加前缀（与系统方法/其他 Category 冲突）
- [ ] 多个文件为同一个类声明了相同方法名的 Category

### 6.2 宏定义

- [ ] 同一个宏名在多个文件中 `#define`（可能值不同）

### 6.3 C 函数 / 全局变量

- [ ] 多个 `.m` 文件定义了同名的 static 函数以外的 C 函数
- [ ] `extern` 声明了但对应的实现不存在
- [ ] 同一个 `const` 全局变量在多个 `.m` 中定义

### 6.4 协议方法

- [ ] 两个协议声明了同名方法但语义不同
- [ ] 一个类实现了两个协议，其中同名方法语义冲突

---

## 七、@optional 协议专项

ObjC 中 `@optional` 协议方法调用无编译期检查，需专项审查。

### 7.1 respondsToSelector: 正确性

- [ ] `respondsToSelector:` 检查的方法名与实际声明不一致（拼写差异、selector 拼写错误）
- [ ] 调用 `@optional` 方法前**完全未检查** `respondsToSelector:`
- [ ] `respondsToSelector:` 传入的 selector 参数遗漏 `:`（无参方法 vs 有参方法）
- [ ] `@optional` **属性**调用前未检查（`if ([obj respondsToSelector:@selector(supportedLevels)])`）

### 7.2 协议实现完整性

- [ ] 类声明遵循某协议，但未实现其所有 `@required` 方法（编译期可查，但警告可能被忽略）
- [ ] 父类已实现，子类 `respondsToSelector:` 检查后可能意外走父类实现
- [ ] 协议新增 `@optional` 方法后，调用方未感知——检查调用了已废弃/更名的方法

### 7.3 回调链断裂

- [ ] 收到底层回调后未正确转发给上层 delegate（如 `socketDidConnect` 未调 `connectionDidSucceed`）
- [ ] 多层代理转发时中间层遗漏某些方法

### 交叉搜索命令

```bash
# 扫描所有 @optional 协议方法
grep -A 5 "@optional" <protocol.h>

# 扫描所有 respondsToSelector: 调用
grep -n "respondsToSelector:" <target.m>

# 对比协议中 @optional 方法列表 vs 调用方 checks──看是否有遗漏
```

---

## 八、KVO / KVC 安全

### 8.1 keyPath 安全

- [ ] `addObserver:forKeyPath:` 的 keyPath 使用裸字符串字面量（编译期不检查属性是否存在）
- [ ] keyPath 拼写与属性名不一致（如 `@"isLogin"` vs 实际属性 `loggedIn`）
- [ ] `valueForKey:` / `setValue:forKey:` 的 key 为非 NString 常量（拼写不可 grep）

### 8.2 observer 生命周期

- [ ] `addObserver` 在 `init`/`viewDidLoad`，但 `removeObserver` 在 `dealloc`——如果对象从未触发 `dealloc`（循环引用），observer 永久泄漏
- [ ] 多次 `addObserver` 同一个 keyPath 但只 `removeObserver` 一次
- [ ] 对**未注册的 keyPath** 调用 `removeObserver` → **crash**
- [ ] 父类注册了 KVO，子类 dealloc 中 `removeObserver` 时父类属性已部分析构

### 8.3 context 指针

- [ ] `observeValueForKeyPath:ofObject:change:context:` 未比较 `context` 指针就直接处理 → 收到父类/其他对象的通知时误处理
- [ ] context 未使用静态变量唯一地址（直接传 `NULL`），无法区分来源

### 8.4 手动 KVO

- [ ] 重写了 `automaticallyNotifiesObserversForKey:` 返回 NO，但手动 `willChangeValueForKey:` / `didChangeValueForKey:` 不对应
- [ ] 异步/延迟调用 `didChangeValueForKey:` 时对象可能已释放

### 交叉搜索命令

```bash
# 搜索所有 KVO 注册点
grep -n "addObserver:.*forKeyPath:" <target.m>

# 搜索所有 KVO 移除点
grep -n "removeObserver:.*forKeyPath:" <target.m>

# 对比数量——注册数 vs 移除数是否一致
```

---

## 九、ARC 桥接

IM/信令/音视频 SDK 底层常涉及 Core Foundation 类型（`CFDataRef`、`CFDictionaryRef`、`CVImageBufferRef` 等），需检查桥接安全。

### 9.1 桥接修饰符

- [ ] `__bridge` 用于所有权转移：CF → ARC（应 `CFBridgingRelease`/`__bridge_transfer`）或 ARC → CF（应 `CFBridgingRetain`/`__bridge_retained`）
- [ ] `__bridge_retained` 后忘记配对 `CFRelease` → 内存泄漏
- [ ] `__bridge_transfer` 用在已经 `CFRelease` 的对象上 → double free

### 9.2 CF 对象管理

- [ ] `CFRelease` 对象为 NULL 时不 crash（安全），但用 `CFRelease(NULL)` 说明逻辑可能有问题
- [ ] `CFRetain`/`CFRelease` 不配对（每对 `Create`/`Copy` 有对应 `Release`）
- [ ] `CVPixelBufferRef` / `CMSampleBufferRef` 等视频帧未及时释放 → 内存暴涨

### 9.3 桥接宏

- [ ] `CFBridgingRelease` 未加 nil 保护直接转 `NSString *` 等
- [ ] `(__bridge NSString *)` 用在 CFStringRef 上，但 CFStringRef 后续被释放，NSString 成为野指针

### 交叉搜索命令

```bash
# 搜索 CF 对象创建点
grep -n "CGCreate\|CFCreate\|CVCreate\|CMCreate\|Sec" <target.m>

# 搜索桥接转换
grep -n "__bridge\|CFBridging" <target.m>

# 搜索 CFRelease——检查是否与创建点配对
grep -n "CFRelease\|CVPixelBufferRelease" <target.m>
```

---

## 十、Runtime 安全

### 10.1 +load 方法

- [ ] `+load` 方法中做了耗时操作（网络请求、大量 I/O、加锁等待）
- [ ] `+load` 中使用了其他类（加载顺序不确定，可能 crash）
- [ ] `+load` 中 `dispatch_async`——启动顺序依赖不可控

### 10.2 Method Swizzling

- [ ] `class_addMethod` 返回值未检查（添加成功 vs 只做了交换，处理逻辑不同）
- [ ] swizzling 在 `+load` 外执行（如 `+initialize`），可能被多次执行
- [ ] swizzling 后未调用原始实现（对 `didMoveToSuperview` 等生命周期方法的 swizzling 需要转发）
- [ ] 多次 swizzling 同一方法导致调用栈混乱

### 10.3 Associated Objects

- [ ] `objc_setAssociatedObject` 使用 `OBJC_ASSOCIATION_ASSIGN` → 对象释放后成为野指针（应使用 `RETAIN_NONATOMIC` / `RETAIN`）
- [ ] 关联 key 未使用静态指针或 `@selector`（直接传字符串地址，可能冲突）
- [ ] `dealloc` 中未清理 associated objects（通常自动清理，但手动管理场景需检查）

### 10.4 performSelector: 隐患

- [ ] `performSelector:` 返回值是非对象类型（`BOOL`、`int`、`CGFloat` 等）→ ARC 下无法管理返回值内存，会泄漏
- [ ] `performSelector:withObject:afterDelay:` 在 dealloc 后仍可能触发 → crash（应 `cancelPreviousPerformRequestsWithTarget:`）
- [ ] `performSelector:` 的 selector 参数从外部传入（如 notification userInfo 中的 selector 字符串），可能执行任意方法

### 交叉搜索命令

```bash
# 搜索 Runtime 调用
grep -n "+ (void)load\|class_addMethod\|method_exchangeImplementations\|objc_setAssociatedObject\|performSelector:" <target.m>

# 全局搜索 swizzling
grep -rn "class_addMethod\|method_exchangeImplementations\|class_replaceMethod" {sources_root}
```

| 标记 | 含义 | 示例 |
|------|------|------|
| 🔴 **严重** | 必然 crash / 逻辑完全错误 | nil 字典 key、循环引用、协议方法调错 |
| 🟡 **中等** | 特定条件下出 bug / 潜在性能问题 | 缺少 nil 保护、线程不安全、死代码 |
| 🟢 **低** | 不影响运行但降低可维护性 | 魔法数字、TODO 遗留、命名不规范 |

---

## 输出格式

```
## 审查报告: <文件名>

| # | 维度 | 严重度 | 位置 | 问题 |
|---|------|--------|------|------|

---
### 详细说明

**Bug 1: ...**
  当前: ...
  修改: ...

**坏味道 1: ...**
  说明: ...
  建议: ...

---
### 汇总

| 维度 | 🔴严重 | 🟡中等 | 🟢低 | 合计 |
|------|--------|--------|------|------|
| Bug 扫描 | ... | ... | ... | ... |
| 坏味道 | ... | ... | ... | ... |
| 内存泄漏 | ... | ... | ... | ... |
| 线程风险 | ... | ... | ... | ... |
| 语法隐患 | ... | ... | ... | ... |
| 重复符号 | ... | ... | ... | ... |
| @optional 专项 | ... | ... | ... | ... |
| KVO/KVC 安全 | ... | ... | ... | ... |
| ARC 桥接 | ... | ... | ... | ... |
| Runtime 安全 | ... | ... | ... | ... |

总计: X 个问题
```

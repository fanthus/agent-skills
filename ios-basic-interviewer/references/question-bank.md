# iOS 面试题库 + 答案要点

## 目录
1. [Swift 语言基础](#1-swift-语言基础)
2. [UIKit / UI 基础](#2-uikit--ui-基础)
3. [内存与 ARC](#3-内存与-arc)
4. [并发与线程安全](#4-并发与线程安全)
5. [网络与数据](#5-网络与数据)
6. [架构与工程化](#6-架构与工程化)
7. [SwiftUI](#7-swiftui)
8. [经典陷阱题](#8-经典陷阱题)

---

## 1. Swift 语言基础

### 1.1 struct vs class

**入门问题**：struct 和 class 有什么区别？

**答案要点**：
- struct 是值类型（栈/内联存储），class 是引用类型（堆分配）
- struct 赋值时复制，class 赋值时共享引用
- struct 没有继承，class 支持继承
- struct 的方法修改属性需要 `mutating`

**追问 1**：什么是 Copy-on-Write？Array 是怎么实现的？
- 要点：Swift 标准库集合类型（Array/Dictionary/Set）是 struct，但底层 buffer 是引用类型
- 只有在实际写入时才复制底层存储，避免不必要的复制开销
- 自定义 struct 不自动有 CoW，需要手动实现

**追问 2**：什么时候应该用 class 而不是 struct？
- 需要引用语义（多个地方共享同一个对象）
- 需要继承
- 需要与 ObjC 互操作
- 有复杂的 deinit 逻辑（比如关闭文件句柄）

**追问 3（高级）**：Swift struct 为什么"快"？有没有例外？
- 栈分配比堆分配快，无引用计数开销
- 例外：含有引用类型属性的 struct 仍有引用计数；很大的 struct 频繁复制反而慢

---

### 1.2 Optional

**入门问题**：Swift 的 Optional 是什么？和 nil 有什么关系？

**答案要点**：
- Optional 是泛型枚举：`enum Optional<T> { case none; case some(T) }`
- nil 就是 `.none`
- Swift 中只有 Optional 类型才能为 nil

**追问 1**：`if let` 和 `guard let` 有什么区别？什么时候用哪个？
- `if let`：绑定值在 if 块内有效，适合短路分支
- `guard let`：绑定值在 guard 之后的作用域都有效，适合提前退出（early return），让主逻辑不缩进

**追问 2**：`??` 和 `!` 有什么区别？
- `??`（nil-coalescing）：提供默认值，安全
- `!`（强制解包）：如果为 nil 直接 crash，只在确定不为 nil 时用

**追问 3**：Optional chaining 是什么？
- `a?.b?.c`：任一环节为 nil 则整体返回 nil，不 crash
- 返回值是 Optional 包装的结果

---

### 1.3 闭包与捕获列表

**入门问题**：闭包里为什么要用 `[weak self]`？

**答案要点**：
- 闭包会强引用捕获的外部变量，包括 self
- 如果 self 也持有这个闭包，形成循环引用，导致内存泄漏
- `[weak self]` 让闭包弱引用 self，打破循环

**追问 1**：`[weak self]` 和 `[unowned self]` 有什么区别？
- `weak`：self 可能为 nil，访问时需要解包，self 释放后变 nil，安全
- `unowned`：假定 self 生命周期比闭包长，不会变 nil，如果 self 已释放访问会 crash
- 原则：不确定就用 `weak`；只在能保证 self 比闭包活得更长时用 `unowned`

**追问 2**：什么是 escaping 闭包？
- `@escaping`：闭包生命周期超出函数范围（比如被存储、被异步调用）
- 非 escaping 闭包在函数返回前一定执行完毕，编译器可以做优化
- escaping 闭包中访问 self 必须显式写 `self.`，提醒可能的循环引用

---

### 1.4 协议与泛型

**入门问题**：协议（Protocol）和继承有什么区别？

**答案要点**：
- 协议定义接口（行为约定），可以被 struct/class/enum 遵守
- 继承是 class 之间的垂直关系，一个 class 只能有一个父类
- 一个类型可以遵守多个协议（类似多重接口）
- Swift 提倡 Protocol-Oriented Programming

**追问 1**：`associatedtype` 是什么？
- 协议里的泛型占位符
- 遵守协议时提供具体类型
- 含 associatedtype 的协议不能直接当类型用（需要泛型约束或 type erasure）

---

## 2. UIKit / UI 基础

### 2.1 ViewController 生命周期

**入门问题**：viewDidLoad 和 viewWillAppear 有什么区别？

**答案要点**：
- `viewDidLoad`：View 加载完成后调用一次，适合做一次性初始化（addSubview、设置约束、创建 viewModel）
- `viewWillAppear`：每次 VC 即将显示时都会调用，适合刷新数据、更新 UI 状态

**追问 1**：什么时候 viewWillAppear 会被调用多次？
- 从子 VC 返回
- 模态 dismiss 后
- Tab 切换

**追问 2（高级）**：loadView 是做什么的？什么时候需要重写？
- 负责创建 vc.view，默认从 Storyboard/xib 加载，或创建空白 UIView
- 纯代码 UI 时可以重写，在里面 `self.view = MyCustomView()`，但不要调 `super.loadView()`

---

### 2.2 Auto Layout

**入门问题**：什么是 Content Hugging Priority 和 Compression Resistance Priority？

**答案要点**：
- **Content Hugging**（抗拉伸）：值越高，越不愿意被拉大超过 intrinsicContentSize
- **Compression Resistance**（抗压缩）：值越高，越不愿意被压小低于 intrinsicContentSize
- 两个 label 横排时，哪个 hugging 低的会被拉伸填满空间

**追问 1**：约束冲突怎么排查？
- Xcode 控制台的 `UIViewAlertForUnsatisfiableConstraints` 日志
- View Debugger 看约束
- 给约束加 identifier 方便定位

---

### 2.3 UITableView 性能

**入门问题**：UITableView 的 Cell 复用机制是怎么工作的？

**答案要点**：
- 每次 cellForRowAt 调用 `dequeueReusableCell(withIdentifier:)`
- 离屏的 cell 进入复用池（reuse queue），重新使用而不是重新创建
- 减少对象创建，降低内存峰值

**追问 1**：如何优化 TableView 的滚动性能？
- 使用 `estimatedRowHeight` 让系统预估高度，避免一次性计算所有行高
- Cell 的布局计算和图片解码放到后台线程
- 避免 Cell 里有圆角 + masksToBounds（离屏渲染）
- 用 `prepareForReuse` 清理 Cell 状态
- Diffable Data Source 做差量更新

**追问 2（高级）**：什么是离屏渲染？为什么影响性能？
- GPU 需要开辟额外的帧缓冲区来合成某些效果（圆角 + clipsToBounds、阴影、group opacity）
- 额外的内存分配和 GPU 切换开销
- 解决：预先在后台用 Core Graphics 绘制好圆角图片

---

## 3. 内存与 ARC

### 3.1 ARC 基础

**入门问题**：什么是 ARC？strong/weak/unowned 分别是什么意思？

**答案要点**：
- ARC（Automatic Reference Counting）：编译器自动在合适位置插入 retain/release
- `strong`：持有，引用计数 +1
- `weak`：不持有，不增加引用计数，对象释放后自动置 nil
- `unowned`：不持有，不增加引用计数，对象释放后不置 nil（访问 crash）

**追问 1**：循环引用是怎么产生的？举个例子。
- A 强持有 B，B 强持有 A，两者都无法释放
- 常见场景：delegate（VC 持有 View，View.delegate = VC）、闭包（self 捕获持有 self 的闭包）、Timer（Timer 强持有 target）、父子 VC 互相持有

**追问 2**：如何定位内存泄漏？
- Instruments → Leaks：检测已释放对象仍有引用
- Instruments → Allocations：看对象生命周期
- Xcode Memory Graph（Debug → Memory Graph Debugger）：可视化引用关系

**追问 3（高级）**：Timer 的循环引用怎么解决？
- `Timer.scheduledTimer(withTimeInterval:repeats:block:)` 用 `[weak self]` 块
- 或者用中间代理对象（weakProxy）持有 weak self
- 确保在 deinit 或适当时机调用 `timer.invalidate()`

---

## 4. 并发与线程安全

### 4.1 GCD 基础

**入门问题**：GCD 里 sync 和 async 有什么区别？

**答案要点**：
- `sync`：提交任务后**当前线程阻塞**，等任务执行完才继续
- `async`：提交任务后**当前线程立即返回**，任务在队列中异步执行

**追问 1**：串行队列和并行队列有什么区别？
- 串行（serial）：任务一个一个执行，前一个完成才执行下一个
- 并行（concurrent）：多个任务可以同时执行，但提交顺序保证

**追问 2（陷阱题）**：在主队列上调用 `DispatchQueue.main.sync { }` 会发生什么？
- **死锁**：主线程被 sync 阻塞，等待主队列上的任务完成；但主队列的任务需要主线程来执行；互相等待，死锁

**追问 3**：什么是 barrier？什么场景用？
- `DispatchQueue.async(flags: .barrier)`：在并行队列里，barrier 任务执行时，等待已提交的任务完成，然后独占执行，再放开后续任务
- 典型用途：读写锁模式——多线程并发读，写时用 barrier 独占

**追问 4（高级）**：如何保证一段代码只执行一次？
- `static let` 常量（Swift 保证线程安全的懒加载）：`static let shared = MyClass()`
- 历史：ObjC 时代用 `dispatch_once`，Swift 中已不需要

---

### 4.2 Swift Concurrency

**入门问题**：你了解 async/await 吗？和 GCD 有什么区别？

**答案要点**：
- async/await 是结构化并发（Structured Concurrency），代码看起来是线性的
- 编译器检查 async 调用必须在 async 上下文中
- 底层用协作线程池，不像 GCD 可能创建大量线程
- 更容易处理错误（throw/catch 配合）

**追问 1**：什么是 Actor？
- Actor 是引用类型，保证其内部状态的串行访问，消除数据竞争
- 跨 Actor 边界的访问必须用 `await`
- `@MainActor` 是特殊的全局 Actor，代表主线程

**追问 2**：Task 的生命周期是怎么管理的？
- 结构化：子 Task 随父 Task 取消
- 非结构化：`Task { }` 创建独立 Task，需要手动持有 Task handle 来取消
- `task(id:)` modifier（SwiftUI）在视图消失时自动取消

---

## 5. 网络与数据

### 5.1 URLSession

**入门问题**：用 URLSession 发一个 GET 请求，基本步骤是什么？

**答案要点**：
```swift
let url = URL(string: "https://api.example.com/data")!
let task = URLSession.shared.dataTask(with: url) { data, response, error in
    guard error == nil, let data = data else { return }
    // 解析 data
}
task.resume()
```
- 或者用 async/await：`let (data, response) = try await URLSession.shared.data(from: url)`

**追问 1**：如何取消一个请求？
- `task.cancel()` 或 Task cancellation（async/await）

**追问 2**：如何做并发请求聚合（等多个请求都完成）？
- GCD：`DispatchGroup`，每个请求 `group.enter()`，完成 `group.leave()`，`group.notify` 回调
- async/await：`async let` 并行启动，再 `await` 聚合；或 `TaskGroup`

---

### 5.2 Codable

**入门问题**：怎么用 Codable 把 JSON 解析成 Swift 结构体？

**答案要点**：
```swift
struct User: Codable {
    let id: Int
    let name: String
}
let user = try JSONDecoder().decode(User.self, from: data)
```

**追问 1**：如果 JSON key 和 Swift 属性名不一样怎么处理？
- 实现 `CodingKeys` 枚举，或者设置 `decoder.keyDecodingStrategy = .convertFromSnakeCase`

**追问 2**：如果某个字段可能缺失或类型不一致，怎么处理？
- 字段可能缺失：声明为 `Optional` 类型，或提供默认值（通过自定义 init(from:)）
- 类型不一致：在 `init(from decoder:)` 里手动 try? 解码多种类型

---

## 6. 架构与工程化

### 6.1 MVC vs MVVM

**入门问题**：你在项目里用过什么架构？MVC 有什么问题？

**答案要点**：
- MVC：Model-View-Controller，iOS 默认；常见问题是 Massive View Controller（VC 承载太多业务逻辑、网络、数据处理）
- MVVM：引入 ViewModel，VC 只负责 UI 绑定；业务逻辑/数据变换在 ViewModel，更易测试

**追问 1**：MVVM 里 ViewController 和 ViewModel 怎么通信？
- 闭包 / 属性绑定（如 Combine/RxSwift）
- delegate
- Combine：ViewModel 暴露 `@Published` 或 Publisher，VC sink 更新 UI

**追问 2**：依赖注入是什么？为什么对测试有帮助？
- 把依赖（网络层、数据库）通过构造函数或属性传入，而不是内部创建
- 测试时注入 Mock，不需要真实网络/数据库

---

## 7. SwiftUI

### 7.1 状态管理

**入门问题**：@State 和 @ObservedObject 有什么区别？

**答案要点**：
- `@State`：View 私有的简单状态，存储在 View 之外的 Swift 管理内存中，值类型
- `@ObservedObject`：外部传入的遵守 `ObservableObject` 的引用类型，View 不拥有它的生命周期
- `@StateObject`：View 拥有并创建 ObservableObject，生命周期与 View 绑定

**追问 1**：@StateObject 和 @ObservedObject 有什么区别？什么时候用哪个？
- `@StateObject`：View 自己创建这个对象，View 重建时对象不会重新创建
- `@ObservedObject`：对象从外部传入，View 重建时外部决定生命周期
- **规则**：谁创建谁用 `@StateObject`，传入的用 `@ObservedObject`

---

## 8. 经典陷阱题

### 8.1 主队列死锁

**问题**：以下代码有什么问题？
```swift
// 在主线程调用
DispatchQueue.main.sync {
    print("hello")
}
```
**答案**：死锁。主线程等待 sync 块完成，sync 块需要在主队列（主线程）执行，主线程被阻塞，互相等待。

---

### 8.2 Copy-on-Write 陷阱

**问题**：以下代码输出什么？
```swift
var a = [1, 2, 3]
var b = a
b.append(4)
print(a.count) // ?
```
**答案**：3。b 是 a 的独立副本（CoW 在写入时触发复制），修改 b 不影响 a。

---

### 8.3 RunLoop 与 Timer

**问题**：为什么滚动 ScrollView 时，Timer 会停止触发？

**答案**：
- 默认 Timer 加在 RunLoop 的 `.default` 模式
- 滚动时 RunLoop 切换到 `.tracking` 模式
- 解决：把 Timer 加到 `.common` 模式：`RunLoop.main.add(timer, forMode: .common)`

---

### 8.4 deinit 不被调用

**问题**：你的 ViewController 的 deinit 没被调用，可能有哪些原因？

**答案要点**：
1. 闭包捕获了 `self`（强引用）
2. delegate 没有声明为 `weak`
3. NotificationCenter 观察者没有移除（老版本 API）
4. Timer 没有 invalidate，且 target 是 self
5. 父 VC 或容器 VC 意外持有

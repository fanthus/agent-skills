# 环境准备：清缓存 → Podfile 切本地 → pod install

主流程的前 3 步都是确定性命令，照着跑。出了问题会很明显（pod install 报错、找不到目录），不用过度防御。

## 路径前提

skill 假设三个 repo 在固定位置（用户自己的 ihuman 工作区）：

```
~/ihuman/
├── pb-idl/           # PB proto 源
├── ilprotocolbuffer/ # PB 编译产物（OC 库）
└── superclasssdk/    # 主 SDK，引用 ilprotocolbuffer
```

如果用户当前 shell 不在 `~/ihuman` 下，所有命令都用绝对路径，避免歧义。

## Step 1：清 DerivedData

只清 superclasssdk 的，不要清整个 DerivedData（那会影响其他项目）：

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/SuperClassSDK-*
```

通配符是因为 Xcode 会在项目名后加随机 hash。如果一个项目都不存在，`rm -rf` 静默成功，不用判断。

不需要清 `~/ihuman/superclasssdk/Example/Pods/`，下一步 `pod install` 会处理。也不动 `Podfile.lock`，让 CocoaPods 自己决定要不要更新。

## Step 2：把 Podfile 改成本地路径

文件：`~/ihuman/superclasssdk/Example/Podfile`

把 `ILProtocolBuffer` 那一行（远程版本）替换为：

```ruby
pod 'ILProtocolBuffer', :path => '../../ilprotocolbuffer'
```

**远程版本字符串**（用于这步替换的源、以及 step 5 替换回去的目标）：

```ruby
pod 'ILProtocolBuffer', :git => 'https://gitlab.dev.ihuman.com/aixue/ios/ILProtocolBuffer.git', :branch => 'main'
```

操作建议：用 `str_replace` 工具直接做行级替换，比 sed 直观、好回滚。先 `view` 一下 Podfile 确认远程行的实际样子（可能有空格、缩进、引号差异），再做替换。

## Step 3：pod install

```bash
cd ~/ihuman/superclasssdk/Example && pod install
```

成功的标志是看到 `Pod installation complete!` 这行。失败一般是：
- ilprotocolbuffer 那边 `.podspec` 没更新（用户前置步骤没拖文件进去）→ 报错会指出缺失的文件
- 路径不对 → 检查 `:path => '../../ilprotocolbuffer'` 是不是写对了

报错就停下来告诉用户，别强行往下走。

## Step 4：删旧的 ILLiveNetworkManager

```bash
rm -f ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.h
rm -f ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.m
```

`-f` 容忍文件不存在的情况（虽然按流程应该存在，但首次跑或者用户手动删过就不存在了）。

删之前**不需要**备份。如果用户想保留旧版作为参考，他们自己会用 git。skill 的工作目录不污染用户的 git 历史。

## Step 5：把 Podfile 改回远程版本

主流程结束后（也就是新文件生成完、用户确认无误后），把 Step 2 改的那行换回去：

```ruby
pod 'ILProtocolBuffer', :path => '../../ilprotocolbuffer'
```
↓
```ruby
pod 'ILProtocolBuffer', :git => 'https://gitlab.dev.ihuman.com/aixue/ios/ILProtocolBuffer.git', :branch => 'main'
```

注意时机：**生成完新 Manager、用户验收通过之后**再改回去。如果中间生成失败、用户要重试，Podfile 留在本地路径状态更方便调试。所以 Step 5 是主流程的收尾，不是 Step 2 的对称镜像。

改回去之后**不要**再跑 pod install —— 会真的去拉远程 git，可能与本地 ilprotocolbuffer 不一致，不是这次任务想要的状态。让用户自己决定什么时候推 ilprotocolbuffer 改动到 git 然后 pod install。

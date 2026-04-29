# ILNetworkDefine.{h,m} 更新规则

每次重新生成 ILLiveNetworkManager 都要同步更新这两个文件：

```
~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILNetworkDefine.h
~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILNetworkDefine.m
```

它们维护"path 常量名 → URL 路径字符串"的映射。`ILLiveNetworkManager.m` 里所有 `il_postPath:` 调用引用的常量都必须在这里有定义，否则编译失败。

## 文件格式（参考已有内容）

进入这一步前先 `view` 一下当前的 ILNetworkDefine.h/.m，看实际格式（可能跟下面描述的略有出入，**以实际为准**）。一般来说：

`.h` 文件：
```objc
extern NSString * const ILNetworkPathStudentLiveRoomStudentJoin;
extern NSString * const ILNetworkPathStudentLiveRoomStudentLeave;
// ...
```

`.m` 文件：
```objc
NSString * const ILNetworkPathStudentLiveRoomStudentJoin = @"/student_live/student_join";
NSString * const ILNetworkPathStudentLiveRoomStudentLeave = @"/student_live/student_leave";
// ...
```

## 常量命名规则

格式：`ILNetworkPath` + `<业务前缀>` + `<接口名>`

**业务前缀**从 proto 文件名推导：
- `student_api.proto` → `Student`
- `student_live_api.proto` → `StudentLive`
- `user_api.proto` → `User`

去掉 `_api` 后缀，剩下的部分按驼峰拼接。

**接口名**就是 rpc 名（驼峰，首字母大写）：
- `rpc StudentJoin` → `StudentJoin`
- `rpc GetRoomStats` → `GetRoomStats`

完整示例：

| proto 文件 | rpc 名 | 常量名 |
|---|---|---|
| student_live_api | StudentJoin | `ILNetworkPathStudentLiveStudentJoin` |
| student_live_api | StudentRaiseHand | `ILNetworkPathStudentLiveStudentRaiseHand` |
| student_live_api | GetRoomStats | `ILNetworkPathStudentLiveGetRoomStats` |
| student_api | GetStudentInfo | `ILNetworkPathStudentGetStudentInfo` |
| user_api | Login | `ILNetworkPathUserLogin` |

**例外：兼容历史命名**。如果 ILNetworkDefine.h 里已经有这个 rpc 对应的常量但用了不同的命名（比如历史上业务前缀分得更细，叫 `StudentLiveRoom` 而不是 `StudentLive`），**保留历史命名**，不要为了"统一"去重命名 —— 重命名意味着 ILLiveNetworkManager.m 里的引用也要跟着改，扩散面太大。新增的常量按上面规则起名就行。

## URL 路径字符串的来源（按优先级）

1. **proto 的 HTTP 注解**：rpc 上面如果有
   ```protobuf
   option (google.api.http) = { post: "/student_live/student_join" };
   ```
   直接用注解里的路径。这是最权威的来源。

2. **现有 ILNetworkDefine.m 里的对应项**：如果 rpc 名跟旧版一致，去 `ILNetworkDefine.m` grep 一下旧的 path 字符串，沿用。
   ```bash
   grep -A1 "StudentLiveRoomStudentJoin" ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILNetworkDefine.m
   ```

3. **按约定拼接**：前两条都没有时，按 `/<service_snake>/<rpc_snake>` 拼。`StudentJoin` 在 `student_live_api` 里 → `/student_live/student_join`。**这种情况要明确告诉用户"以下 path 是按约定拼的，需要核对后端实际路径"**。

## 增 / 改 / 删的处理

更新 ILNetworkDefine 不只是 append，要按 proto 当前清单做完整同步：

**新增**：proto 里有、ILNetworkDefine 里没有的常量 → 在 .h 加 `extern`、在 .m 加赋值。

**修改**：proto 里 path 注解变了、或 rpc 改名 → 改 .m 里的字符串，或者改常量名（涉及 .h .m 和 ILLiveNetworkManager.m 三处）。改名的代价大，先确认是不是真的需要。

**删除**：proto 里没有、但 ILNetworkDefine 里还有的常量 → 删掉 .h 的 extern 和 .m 的赋值。**注意**：在删之前确认这个常量没被其他文件引用：
```bash
grep -r "ILNetworkPathXxx" ~/ihuman/superclasssdk/
```
如果只有 ILNetworkDefine.{h,m} 自己出现，可以放心删；如果有其他文件引用（比如某个旧 ViewController），告诉用户哪里还在用、让他决定怎么处理，不要默默删。

## 跟 ILLiveNetworkManager.m 的同步

写完 ILLiveNetworkManager.m 后，立刻做一次自检：把 ILLiveNetworkManager.m 里所有 `il_postPath:ILNetworkPath...` 的常量名 grep 出来，跟 ILNetworkDefine.h 里的 `extern` 列表对一遍。少的就漏了，多的就是历史遗留。

```bash
# 提取 ILLiveNetworkManager.m 里所有引用的 path 常量
grep -oE "ILNetworkPath\w+" ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILLiveNetworkManager.m | sort -u

# 提取 ILNetworkDefine.h 里所有声明的 path 常量
grep -oE "ILNetworkPath\w+" ~/ihuman/superclasssdk/SuperClassSDK/Classes/Core/ILNetworkDefine.h | sort -u

# diff 一下，应该完全一致（除非 ILNetworkDefine 被其他 manager 共用 —— 那种情况 ILNetworkDefine 是超集）
```

## 一个完整的小例子

假设 proto 加了一个新 rpc：

```protobuf
service StudentLive {
  // 学生举手
  rpc StudentRaiseHand(StudentRaiseHandReq) returns (StudentRaiseHandResp);
}
```

proto 没有 HTTP 注解，旧版也没这个接口（新增）。按约定拼路径：`/student_live/student_raise_hand`。

ILNetworkDefine.h 加一行：
```objc
extern NSString * const ILNetworkPathStudentLiveStudentRaiseHand;
```

ILNetworkDefine.m 加一行：
```objc
NSString * const ILNetworkPathStudentLiveStudentRaiseHand = @"/student_live/student_raise_hand";
```

ILLiveNetworkManager.m 里使用：
```objc
[self il_postPath:ILNetworkPathStudentLiveStudentRaiseHand
          request:req
    responseClass:[ILILStudentRaiseHandResp class]
          ...];
```

完成后告诉用户："新增了 1 个 path 常量 `ILNetworkPathStudentLiveStudentRaiseHand = /student_live/student_raise_hand`，proto 没有 HTTP 注解，路径是按约定拼的，需要跟后端核对。"

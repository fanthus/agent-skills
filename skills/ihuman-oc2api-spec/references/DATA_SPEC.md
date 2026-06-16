# 数据字段提取规范

---

## 一、响应数据结构

所有接口响应均为三层结构：

```json
{
  "code": 0,           // ErrorCode 错误码
  "message": "",        // string 错误信息
  "data": {}            // object 数据对象（可选）
}
```

---

## 二、字段路径表示法

### 2.1 基础规则

| 格式 | 含义 | 示例 |
|------|------|------|
| `field` | 顶层字段 | `code`, `message` |
| `data.field` | data 下一级字段 | `data.coinCount` |
| `data.object.field` | data 下对象字段 | `data.room.roomName` |
| `data.array[ElementType]` | data 下数组，**中括号内写入元素具体类型** | `data.channels[RTCTokenInfo]` |
| `data.array[ElementType].field` | 数组元素字段 | `data.channels[RTCTokenInfo].channelId` |
| `data.array[ElementType].object.field` | 数组元素内嵌对象字段 | `data.channels[RTCTokenInfo].tokenInfo.token` |

### 2.2 路径命名规则

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 数组 | `[ElementType]` 中括号内写入元素具体类型 | `channels[RTCTokenInfo]`, `members[GroupMemberInfo]` |
| 基本类型数组 | `[基本类型]` | `options[string]`, `selectedOptions[int32]` |
| 对象 | 字段名直接引用 | `room`, `rtcConfig` |
| 枚举字段 | 枚举类型名 | `roomStatus`, `ChannelType` |
| 基本字段 | 驼峰式 | `roomId`, `userId` |

### 2.3 数组类型标注规则

| 数组内容 | 正确写法 | 错误写法 |
|----------|----------|----------|
| 结构体数组 | `data.speakers[SpeakerInfo]` | `data.speakers[]` |
| 基本类型数组 | `data.options[string]` | `data.options[]` |
| 嵌套结构体数组 | `data.interactions[ReplayInteraction]` | `data.interactions[]` |

---

## 三、字段类型说明

### 3.1 基本类型

| 类型 | 说明 | 示例值 |
|------|------|--------|
| `string` | 字符串 | `"room123"` |
| `int32` | 32位整数 | `100` |
| `int64` | 64位整数 | `1609459200000` |
| `bool` | 布尔值 | `true` / `false` |
| `double` | 双精度浮点数 | `85.5` |

### 3.2 枚举类型

枚举字段使用大驼峰命名，值为整型。

| 枚举类型 | 说明 |
|----------|------|
| `ErrorCode` | 错误码，0=成功 |
| `PlatformType` | 平台类型: 1-iOS 2-Android 3-Web 4-PC |
| `RoomStatus` | 房间状态: 1-未开播 2-准备中 3-直播中 4-暂停中 5-已结束 |
| `RoomType` | 房间类型: 1-大班小组课 2-大班课 3-小班课 4-录播课 5-习题课 6-一对一 |
| `SceneType` | 场景类型: 1-直播课 2-录播课 |
| `SpeakStatus` | 连麦状态: 1-未连麦 2-已举手 3-连麦中 4-被禁言 |
| `ChatMessageType` | 消息类型: 1-文本 2-表情 3-图片 4-系统 5-私信 |
| `IMGroupType` | 群组类型: 1-大班群 2-小班群 3-信令群 |
| `ChannelType` | 频道类型: 1-大班主频道 2-小班频道 |
| `RTCRole` | RTC角色: 1-主播 2-观众 3-广播者 |
| `MediaType` | 媒体类型: 1-摄像头流 2-屏幕共享流 3-自定义流 |
| `ContentType` | 课件类型: 1-PPT 2-白板 3-屏幕分享 4-视频 5-文档 |
| `ReplayStatus` | 回放状态: 1-未生成 2-生成中 3-已就绪 4-失败 |
| `UserRole` | 用户角色: 1-教师 2-学生 3-助教 4-旁听 5-辅导老师 |
| `ActivityType` | 活动类型: 1-答题 2-投票 3-签到 4-红包 |
| `PushType` | 推流类型: 1-RTC |
| `RoomLayout` | 房间布局: 1-1v4布局 |
| `RTCProvider` | RTC提供商: 1-Agora 2-腾讯TRTC |
| `IMProvider` | IM提供商: 1-腾讯IM |

---

## 四、数据结构层级

### 4.1 层级关系

```
响应外层 (code, message, data)
  └── data (数据对象)
        ├── 基本字段 (string, int32, bool)
        ├── 枚举字段 (RoomStatus, SpeakStatus)
        └── 对象字段 (room, rtcConfig)
              └── 多级嵌套对象
                    └── 数组 (channels[RTCTokenInfo], members[GroupMemberInfo])
                          └── 数组元素内嵌对象
```

### 4.2 展开规则

| 原字段 | 展开后 |
|--------|--------|
| `data.group.imGroup` | `data.group.imGroup.groupType`<br>`data.group.imGroup.groupId`<br>`data.group.imGroup.groupName`<br>`data.group.imGroup.memberCount` |
| `data.channels[RTCTokenInfo]` | `data.channels[RTCTokenInfo].channelType`<br>`data.channels[RTCTokenInfo].channelId`<br>`data.channels[RTCTokenInfo].channelName`<br>`data.channels[RTCTokenInfo].role`<br>`data.channels[RTCTokenInfo].tokenInfo.token`<br>... |

---

## 五、文档格式模板

### 请求字段

```markdown
**请求字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| `fieldName` | type | 描述 |
| `nested.object` | type | 描述 |
| `array[ElementType].field` | type | 描述 |
```

### 响应字段

```markdown
**响应字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | ErrorCode | 错误码 |
| `message` | string | 错误信息 |
| `data.field` | type | 描述 |
| `data.object.nested` | type | 描述 |
| `data.array[ElementType].elementField` | type | 描述 |
| `data.array[ElementType].element.object.deepField` | type | 描述 |
```

---

## 六、通用数据类型（Common）

### 6.1 嵌套层级速查

| 类型 | 层级深度 | 内嵌对象 |
|------|----------|----------|
| `RTCTokenInfo` | 3层 | token, channelId, channelName, role, channelType, expireTime, uid |
| `RTCConfig` | 3层 | provider, appId, agora(primaryDomain, fallbackDomain), trtc(sdkAppId) |
| `RTCChannelInfo` | 3层 | channelType, channelId, channelName, role, tokenInfo |
| `IMTokenInfo` | 2层 | userSig, expireTime, sdkAppId, userId |
| `IMConfig` | 3层 | provider, sdkAppId, serverDomain, tokenInfo |
| `IMGroupInfo` | 1层 | groupType, groupId, groupName, memberCount |
| `RoomBaseInfo` | 1层 | 31个基本字段 |
| `SmallGroupInfo` | 2层 | groupId, roomId, tutorId, memberIds[string], maxMembers, createTime, rtcChannelId, imGroup, groupIndex |
| `MediaInfo` | 1层 | uid, mediaType, hasVideo, hasAudio, channelType, publishTime |
| `ContentInfo` | 1层 | contentId, contentType, title, url, totalPages, currentPage |
| `ClassReport` | 1层 | roomId, userId, duration, totalCoins, quizCount, quizCorrect, accuracyRate, interactionCount, speakCount, speakDuration |
| `ReplayInfo` | 2层 | replayId, roomId, videoURL, duration, createTime, interactions[ReplayInteraction] |
| `ReplayInteraction` | 1层 | timeOffset, activityType, activityId |
| `SpeakerInfo` | 1层 | uid, nickname, avatar, speakStartTime, cameraOn, micOn |
| `GroupMemberInfo` | 1层 | uid, nickname, avatar, coinCount, speakStatus, cameraOn, micOn |
| `UserInfo` | 1层 | userId, nickname, avatar, userRole, speakStatus, joinTime, smallGroupId, isMuted, isOnline, coinCount |
| `StudentSpeakProgress` | 2层 | raiseHandEnabled, mySpeakStatus, mySpeakStartTime, speakers[SpeakerInfo] |
| `StudentQuizProgress` | 1层 | quizId, quizType, question, options[string], duration, remainingTime, rewardCoins, isActive, hasAnswered, selectedOption |
| `StudentVoteProgress` | 1层 | voteId, question, options[string], duration, remainingTime, isActive, hasVoted, selectedOption |
| `StudentSignInProgress` | 1层 | signInId, remainingTime, rewardCoins, isActive, hasSignedIn |
| `StudentGrabMicProgress` | 1层 | grabMicId, remainingTime, isActive, hasGrabbed, isWinner |
| `StudentTimerProgress` | 1层 | timerId, isCountdown, elapsedSeconds, title, isActive |
| `StudentRaiseHandProgress` | 1层 | isRaising, position, totalCount, expireTime |

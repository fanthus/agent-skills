# OC 到 API 字段映射

## OC 类结构特点

### 响应结构

```objc
StudentJoinResp *resp;
resp.code;      // ErrorCode 错误码
resp.message;   // NSString 错误信息
resp.data_p;    // StudentJoinResp_Data 嵌套数据对象
```

### 数组表示

```objc
resp.data_p.rtcTokensArray;       // NSMutableArray<RTCTokenInfo *>
resp.data_p.imGroupsArray;        // NSMutableArray<IMGroupInfo *>
resp.data_p.rtcTokensArray[0].channelType;
```

## 映射规则

| OC 属性 | 文档格式 | 说明 |
|---------|----------|------|
| `resp.code` | `code` | 顶层字段直接引用 |
| `resp.message` | `message` | 顶层字段直接引用 |
| `resp.data_p.xxx` | `data.xxx` | `data_p` 映射为 `data` |
| `resp.data_p.rtcTokensArray` | `data.rtcTokens[RTCTokenInfo]` | 数组字段，补充元素类型 |
| `resp.data_p.xxxArray[i].yyy` | `data.xxx[ElementType].yyy` | 数组元素字段 |

## 请求类

请求类字段直接输出为字段名：

| OC 类 | 文档字段示例 |
|-------|--------------|
| `StudentJoinReq` | `roomId` |
| `StudentLeaveReq` | `roomId`, `leaveReason` |
| `GetStudentRoomInfoReq` | `courseId`, `lessonId` |

## 响应类

| OC 类 | 文档字段前缀 |
|-------|--------------|
| `XXXResp` | `code`, `message` |
| `XXXResp_Data` | `data.xxx` |

## 嵌套类型示例

| OC 类 | 文档格式 |
|-------|----------|
| `RTCConfig` | `data.rtcConfig.provider`, `data.rtcConfig.appId` |
| `RTCTokenInfo` | `data.rtcTokens[RTCTokenInfo].channelType` |
| `IMConfig` | `data.imConfig.tokenInfo.userSig` |
| `IMGroupInfo` | `data.imGroups[IMGroupInfo].groupType` |
| `GroupMemberInfo` | `data.members[GroupMemberInfo].nickname` |

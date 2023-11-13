| 响应码 | 描述   |
| ------ | ------ |
| 200    | 完成   |
| 404    | 无内容 |
| xxx    | 错误x  |


--- 


# -- 根目录 --

/v1

## - 连通性测试

### 请求API

GET /v1

### 参数

无

### 应答

| Name | Type | Desc|
| --- | --- | ---|
| message | string| "Hello, world" |

## - 获取模型列表

GET /v1/model

### 参数

无

### 应答

| Name | Type | Desc|
| --- | --- | ---|
| models | string| 所有服务器可用的模型 |



# -- 聊天 --

/v1/chat

## - 获取聊天回复

### 请求API

POST /v1/chat/completion

### 参数

| Name | In | Type | Desc |
| --- | --- | --- | ---|
| message | Body | list | 提示词文本列表 |
| model | Body | string | 模型 |
| temperature | Body | float | 多样性参数1 |
| top_p | Body | float | 多样性参数2 |
| stream | Body | boolean | 是否流输出 |

### 应答

todo: 



# 测试用例

## 生成

### 请求API

POST /v1/useCase

### 参数

| Name   | In   | Type   | 描述     |
| ------ | ---- | ------ | -------- |
| prompt | Body | string | 请求内容 |
| model  | Body | string | 模型类型 |

### 应答





# 知识库文档

## 获取

## 上传

## 删除


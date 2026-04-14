
# API 接口文档

## 1. API 接口汇总表

| 模块         | HTTP方法 | 端点路径                           | 功能描述                     | 请求参数                                      | 认证要求   |
|--------------|----------|------------------------------------|------------------------------|-----------------------------------------------|------------|
| 用户认证     | POST     | `/api/v1/users/login`              | 用户登录，返回 JWT 令牌      | JSON Body: `username`, `password`             | 无需认证   |
| 用户认证     | POST     | `/api/v1/users/register`           | 用户注册                     | Query 参数: `username`, `password`            | 无需认证   |
| 联系人管理   | POST     | `/api/v1/links/`                   | 创建联系人                   | JSON Body: `name`, `phone`, `img` (可选)      | JWT 必需   |
| 联系人管理   | GET      | `/api/v1/links/page`               | 分页查询联系人（支持搜索）   | Query 参数: `search`, `page_index`, `page_size` | JWT 必需   |
| 联系人管理   | DELETE   | `/api/v1/links/{id}`               | 删除联系人                   | 路径参数: `id`                                 | JWT 必需   |
| 联系人管理   | PUT      | `/api/v1/links/{id}`               | 更新联系人                   | 路径参数: `id` + JSON Body                     | JWT 必需   |
| OSS 文件上传 | POST     | `/api/v1/oss/upload`               | 上传文件到 OSS               | FormData: `photo` (文件)                      | JWT 必需*  |
| OSS 文件上传 | DELETE   | `/api/v1/oss/delete/{object_name}` | 从 OSS 删除文件              | 路径参数: `object_name`                        | JWT 必需*  |

> *注：OSS 相关接口的认证要求标注为 JWT 必需，具体实现中可能需要根据 OSS 权限策略进一步验证用户身份或资源归属。

## 2. 详细 API 端点说明

### 2.1 用户认证模块

#### 用户登录
- **端点**: `POST /api/v1/users/login`
- **认证**: 无需认证
- **请求体 (JSON)**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **成功响应 (200)**:
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 3600
  }
  ```

#### 用户注册
- **端点**: `POST /api/v1/users/register`
- **认证**: 无需认证
- **查询参数**:
  - `username` (string, 必需)
  - `password` (string, 必需)
- **成功响应 (201)**: 返回新用户基本信息。

### 2.2 联系人管理模块

#### 创建联系人
- **端点**: `POST /api/v1/links/`
- **认证**: 请求头需携带 `Authorization: Bearer <JWT>`
- **请求体 (JSON)**:
  ```json
  {
    "name": "string",
    "phone": "string",
    "img": "string (optional)"
  }
  ```
- **响应**: 返回创建的联系人对象及 ID。

#### 分页查询联系人
- **端点**: `GET /api/v1/links/page`
- **认证**: JWT 必需
- **查询参数**:
  - `search` (string, 可选) – 按姓名或电话模糊搜索
  - `page_index` (int, 默认 1) – 页码
  - `page_size` (int, 默认 10) – 每页记录数
- **响应**: 分页列表及总记录数。

#### 删除联系人
- **端点**: `DELETE /api/v1/links/{id}`
- **认证**: JWT 必需
- **路径参数**:
  - `id` – 联系人唯一标识
- **响应**: 204 No Content 或成功提示。

#### 更新联系人
- **端点**: `PUT /api/v1/links/{id}`
- **认证**: JWT 必需
- **路径参数**:
  - `id` – 联系人唯一标识
- **请求体**: 需包含完整或部分更新字段 (如 `name`, `phone`, `img`)
- **响应**: 更新后的联系人信息。

### 2.3 OSS 文件上传模块

#### 上传文件
- **端点**: `POST /api/v1/oss/upload`
- **认证**: JWT 必需（建议同时校验用户对上传目标的写入权限）
- **请求格式**: `multipart/form-data`
- **表单字段**:
  - `photo` (file, 必需) – 要上传的图片或文件
- **响应**: 返回文件在 OSS 中的访问 URL 或对象名称。

#### 删除文件
- **端点**: `DELETE /api/v1/oss/delete/{object_name}`
- **认证**: JWT 必需
- **路径参数**:
  - `object_name` – OSS 中的对象键名（需 URL 编码）
- **响应**: 删除结果状态。
```

如果需要进一步补充每个接口的请求/响应示例、错误码说明等内容，可以在此基础上继续扩展。
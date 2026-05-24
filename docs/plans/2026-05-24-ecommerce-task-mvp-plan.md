# 电商业务任务接口 MVP 执行计划

状态：草案  
最后更新：2026-05-24  
关联设计：[电商场景中转供应商接口设计：Image2 与 Seedance](../specs/2026-05-24-ecommerce-provider-api-design.md)  
关联研究：[绘蛙 ihuiwa.com 功能与后端接口研究](../specs/2026-05-24-ihuiwa-research.md)  
文档索引：[docs/README.md](../README.md)

## 1. 结论

接下来不要先做泛化的“图片生成页/视频生成页”，而是先做面向电商的业务任务接口。

第一版目标：

```text
上传商品图
→ 创建商品主图任务（image2）
→ 创建商品图生视频任务（seedance）
→ 查询任务状态
→ 保存结果到我的作品
→ 扣减/记录积分
```

前端只提交业务任务，后端隐藏 image2、seedance 的真实接口格式。

## 2. MVP 范围

### 必做

- 用户登录与管理员创建用户。
- 用户积分/配额。
- 素材上传与素材记录。
- 供应商配置：`image2`、`seedance`。
- 模型配置：成本、能力、任务类型、启用状态。
- 统一任务接口：估算、创建、查询、重试、下载。
- Image2Provider：商品图、商品场景图。
- SeedanceProvider：商品图生视频。
- 我的作品：保存任务结果。
- 基础前端：商品图工作流、商品视频工作流。

### 暂不做

- 模型训练。
- 团队组织。
- 发票合同。
- 复杂项目交付。
- 视频剪辑器。
- 灵感广场。
- 短剧工坊。

## 3. 推荐开发顺序

### S0：项目骨架

- [ ] 初始化 Next.js + FastAPI。
- [ ] 配置 Docker Compose。
- [ ] 配置 SQLite、Redis、本地文件目录。
- [ ] 实现 `GET /api/v1/health`。
- [ ] 增加 `.env.example`。

验收：

- [ ] 前后端可启动。
- [ ] health 正常。

### S1：用户与积分

- [ ] 建立 `users` 表。
- [ ] 建立 `point_accounts` 表。
- [ ] 建立 `point_records` 表。
- [ ] 实现 JWT 登录。
- [ ] 首次启动创建管理员。
- [ ] 管理员创建用户。
- [ ] 管理员调整用户积分/配额。

验收：

- [ ] 管理员能创建普通用户。
- [ ] 普通用户能登录。
- [ ] 用户能看到当前积分。

### S2：素材上传

- [ ] 建立 `assets` 表。
- [ ] 实现 `POST /api/v1/assets/upload`。
- [ ] 实现 `GET /api/v1/assets`。
- [ ] 实现素材类型：`product_image`、`reference_image`、`logo`、`video`。
- [ ] 上传后生成 `mentionName`，例如 `@商品图`。

验收：

- [ ] 用户可以上传商品图。
- [ ] 素材归属用户隔离。
- [ ] 上传素材可用于创建任务。

### S3：供应商与模型配置

- [ ] 建立 `provider_configs` 表。
- [ ] 建立 `model_configs` 表。
- [ ] 后台支持配置 `image2`：Base URL、API Key、submitPath、queryPath。
- [ ] 后台支持配置 `seedance`：Base URL、API Key、submitPath、queryPath。
- [ ] 后台支持配置模型能力和成本。
- [ ] 实现 Provider 连接测试。

验收：

- [ ] 管理员可以配置 image2 中转接口。
- [ ] 管理员可以配置 seedance 中转接口。
- [ ] API Key 不返回前端明文。

### S4：统一任务系统

- [ ] 建立 `tasks` 表。
- [ ] 实现 `POST /api/v1/tasks/estimate`。
- [ ] 实现 `POST /api/v1/tasks`。
- [ ] 实现 `GET /api/v1/tasks/{taskId}`。
- [ ] 实现 `POST /api/v1/tasks/{taskId}/retry`。
- [ ] 实现 `GET /api/v1/tasks/{taskId}/download`。
- [ ] 实现任务状态：`pending`、`submitted`、`running`、`succeeded`、`failed`、`refunded`。
- [ ] 实现积分冻结、扣减、失败退回。

验收：

- [ ] 创建任务前能估算积分。
- [ ] 积分不足不能创建任务。
- [ ] 任务状态可查询。
- [ ] 任务失败可退回积分。

### S5：Image2Provider

- [ ] 实现 `Image2Provider`。
- [ ] 支持 `product_main_image`。
- [ ] 支持 `product_scene_image`。
- [ ] 将统一任务输入转换为 image2 中转请求。
- [ ] 将 image2 响应归一化为统一任务输出。
- [ ] 支持同步结果与异步 remoteTaskId 两种情况。

验收：

- [ ] 上传商品图后可以创建商品主图任务。
- [ ] 任务完成后返回图片结果。
- [ ] 结果保存为作品资产。

### S6：SeedanceProvider

- [ ] 实现 `SeedanceProvider`。
- [ ] 支持 `product_image_to_video`。
- [ ] 支持 `product_multi_image_video`。
- [ ] 后端自动补充电商视频 Prompt：保持商品外观、Logo、材质一致。
- [ ] 将 seedance 响应归一化为统一任务输出。
- [ ] 支持异步轮询。

验收：

- [ ] 商品图可以生成视频任务。
- [ ] 任务完成后返回视频结果。
- [ ] 结果保存为作品资产。

### S7：我的作品

- [ ] 建立 `works` 或复用 `tasks + assets` 展示作品。
- [ ] 实现 `GET /api/v1/works`。
- [ ] 实现按类型筛选：图片、视频。
- [ ] 支持下载、删除、重试。

验收：

- [ ] 用户能看到自己的生成结果。
- [ ] 用户不能看到别人的作品。

### S8：前端电商工作流

- [ ] 首页改为电商入口：商品主图、商品场景图、商品视频。
- [ ] 实现商品图上传组件。
- [ ] 实现商品主图生成页。
- [ ] 实现商品图生视频页。
- [ ] 实现任务进度轮询。
- [ ] 实现我的作品页。

验收：

- [ ] 用户可以完成“上传商品图 → 生成商品主图”。
- [ ] 用户可以完成“上传商品图 → 生成商品视频”。
- [ ] 用户可以在我的作品看到结果。

## 4. 第一版接口清单

### Auth

```text
POST /api/v1/auth/login
GET  /api/v1/auth/me
POST /api/v1/auth/logout
```

### Admin

```text
POST /api/v1/admin/users
GET  /api/v1/admin/users
PUT  /api/v1/admin/users/{userId}
POST /api/v1/admin/users/{userId}/points

POST /api/v1/admin/providers
GET  /api/v1/admin/providers
PUT  /api/v1/admin/providers/{providerId}
POST /api/v1/admin/providers/{providerId}/test

POST /api/v1/admin/models
GET  /api/v1/admin/models
PUT  /api/v1/admin/models/{modelId}
```

### Assets

```text
POST /api/v1/assets/upload
GET  /api/v1/assets
GET  /api/v1/assets/{assetId}
DELETE /api/v1/assets/{assetId}
```

### Tasks

```text
POST /api/v1/tasks/estimate
POST /api/v1/tasks
GET  /api/v1/tasks
GET  /api/v1/tasks/{taskId}
POST /api/v1/tasks/{taskId}/retry
GET  /api/v1/tasks/{taskId}/download
```

### Works

```text
GET /api/v1/works
GET /api/v1/works/{workId}
DELETE /api/v1/works/{workId}
```

## 5. 第一版任务场景枚举

```text
product_main_image        商品主图 image2
product_scene_image       商品场景图 image2
product_background_change 商品换背景 image2
product_image_to_video    商品图生视频 seedance
product_multi_image_video 多图商品视频 seedance
```

## 6. 最小数据表

```text
users
point_accounts
point_records
assets
provider_configs
model_configs
tasks
works
```

## 7. 你现在应该怎么做

按这个顺序执行：

1. 先确认 image2 和 seedance 中转供应商的真实文档：Base URL、鉴权方式、提交路径、查询路径、请求字段、返回字段。
2. 没有真实文档前，先实现 MockProvider + 可配置 GenericProvider，用来跑通任务闭环。
3. 先做后端：用户、积分、素材、任务、Provider。
4. 再做前端：商品主图页、商品视频页、我的作品页。
5. 最后接真实 image2/seedance，替换 MockProvider。

## 8. 验收 Demo

第一版只需要展示两个 Demo：

```text
Demo 1：上传商品图 → 生成 4 张商品主图 → 我的作品可查看
Demo 2：选择商品图 → 生成 5 秒商品视频 → 我的作品可查看
```

这两个 Demo 跑通后，再扩展种草文案、模板、灵感广场和短剧。

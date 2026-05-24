# 电商场景中转供应商接口设计：Image2 与 Seedance

状态：草案  
最后更新：2026-05-24  
关联研究：[绘蛙 ihuiwa.com 功能与后端接口研究](./2026-05-24-ihuiwa-research.md)  
文档索引：[docs/README.md](../README.md)

## 1. 背景

大云雀计划面向电商营销场景，接入中转供应商提供的 `image2` 和 `seedance` 能力。绘蛙的公开接口显示，其核心不是直接把模型接口暴露给用户，而是通过“业务任务”组织：上传素材、检测素材、创建生成任务、查询任务、下载结果、重试、收藏、发布、消耗积分。

大云雀不需要照搬阿里 MTop，但应借鉴其任务化接口模型，设计自己的 REST API 和 Provider 适配层。

## 2. 绘蛙接口是怎么做的

绘蛙公开静态资源暴露的接口名大致是：

```text
createAigcImageTask
queryAigcImageTasks
queryAigcImageTaskDetailById
editAigcImageTask
downloadTaskImages

createAigcVideoTask
queryVideoTasks
queryAigcVideoTaskDetailById
aigc.video.task.retrybyid
downloadVideos
publishVideo

createAigcTextTask
queryAigcTextTasks
queryAigcTextTaskDetailById

createLoraModelTrainTask
createSceneModelTrainTask
searchModels
searchOfficialModels

point.queryAccountPointDetail
point.searchConsumePointRecords
member.package.list
```

它的关键模式是：

```text
前端页面不是直接调用模型
  -> 先上传素材
  -> 创建 AIGC 任务
  -> 后端扣积分/排队/调用模型
  -> 前端查询任务状态
  -> 结果进入我的作品
  -> 用户下载/编辑/重试/发布
```

这说明绘蛙后端至少包含这些层：

```text
API 网关层
业务任务层
素材资源层
模型/供应商适配层
积分计费层
任务队列层
作品资产层
会员/组织层
```

## 3. 大云雀接口设计原则

### 3.1 用户看业务，不看模型

用户入口应是：

```text
生成商品主图
生成商品场景图
生成种草图
商品图生视频
多图商品视频
爆款视频裂变
商品文案/口播脚本
```

而不是：

```text
image2
seedance
某某模型参数
```

### 3.2 后端统一任务，不按模型拆接口

图片、视频、文案、工具处理都统一成任务：

```text
POST /api/v1/tasks
GET  /api/v1/tasks
GET  /api/v1/tasks/{taskId}
POST /api/v1/tasks/{taskId}/retry
GET  /api/v1/tasks/{taskId}/download
```

### 3.3 Provider 只存在于后端

后端根据任务类型选择 Provider：

```text
商品图 / 主图 / 场景图 -> image2
商品视频 / 图生视频 / 多图视频 -> seedance
失败降级 -> 可配置备用供应商
```

前端最多显示“推荐模型”或“高级设置”，不暴露 API URL 和 Key。

## 4. 推荐后端分层

```text
Controller/API
  -> TaskService
    -> AssetService
    -> BillingService
    -> ProviderRouter
      -> Image2Provider
      -> SeedanceProvider
    -> TaskQueue
    -> Project/WorkService
```

### 4.1 Controller/API

处理 HTTP 请求、鉴权、参数校验。

### 4.2 TaskService

负责任务创建、状态流转、重试、查询、保存结果。

### 4.3 AssetService

负责商品图、模特图、参考图、视频素材上传和资源管理。

### 4.4 BillingService

负责估算积分、冻结积分、扣减积分、失败回滚。

### 4.5 ProviderRouter

根据任务类型、业务场景、用户配置、模型可用性选择供应商。

### 4.6 Provider Adapter

把大云雀统一任务请求转换为中转供应商实际请求，把供应商响应转换为统一任务结果。

## 5. 核心接口草案

### 5.1 上传素材

```http
POST /api/v1/assets/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

字段：

```text
file: File
assetType: product_image | model_image | reference_image | logo | video | audio
projectId?: string
```

响应：

```json
{
  "assetId": "asset_001",
  "assetType": "product_image",
  "url": "/uploads/asset_001.png",
  "width": 1200,
  "height": 1200,
  "mimeType": "image/png",
  "mentionName": "@商品图",
  "detectStatus": "pending"
}
```

### 5.2 素材检测

```http
POST /api/v1/assets/{assetId}/detect
```

响应：

```json
{
  "assetId": "asset_001",
  "quality": "ok",
  "contentSafe": true,
  "detectedObjects": ["shoes", "product"],
  "suggestions": ["主体清晰", "背景可用于抠图"]
}
```

### 5.3 估算任务消耗

```http
POST /api/v1/tasks/estimate
```

请求：

```json
{
  "taskType": "image",
  "scene": "product_main_image",
  "mode": "product_to_scene_image",
  "assetIds": ["asset_001"],
  "params": {
    "count": 4,
    "ratio": "1:1",
    "resolution": "1024x1024"
  }
}
```

响应：

```json
{
  "cost": 4,
  "estimatedSeconds": 20,
  "provider": "image2",
  "model": "image2-product-scene",
  "quotaEnough": true
}
```

### 5.4 创建统一任务

```http
POST /api/v1/tasks
```

请求：

```json
{
  "taskType": "image",
  "scene": "product_main_image",
  "mode": "product_to_scene_image",
  "prompt": "白色运动鞋放在高级灰色摄影棚中，柔光，电商主图风格",
  "assetIds": ["asset_001"],
  "templateId": null,
  "params": {
    "count": 4,
    "ratio": "1:1",
    "resolution": "1024x1024",
    "background": "studio",
    "style": "premium_ecommerce"
  }
}
```

响应：

```json
{
  "taskId": "task_001",
  "status": "pending",
  "cost": 4,
  "provider": "image2",
  "model": "image2-product-scene",
  "pollUrl": "/api/v1/tasks/task_001"
}
```

### 5.5 查询任务

```http
GET /api/v1/tasks/{taskId}
```

响应：

```json
{
  "taskId": "task_001",
  "taskType": "image",
  "scene": "product_main_image",
  "status": "completed",
  "progress": 100,
  "cost": 4,
  "provider": "image2",
  "model": "image2-product-scene",
  "outputs": [
    {
      "assetId": "asset_out_001",
      "type": "image",
      "url": "/outputs/task_001/1.png"
    }
  ],
  "error": null
}
```

### 5.6 重试任务

```http
POST /api/v1/tasks/{taskId}/retry
```

请求：

```json
{
  "reuseInput": true,
  "overrideParams": {
    "style": "clean_ecommerce"
  }
}
```

### 5.7 下载任务结果

```http
GET /api/v1/tasks/{taskId}/download
```

返回 zip 或下载地址。

## 6. 电商任务类型设计

### 6.1 图片任务

```text
product_main_image        商品主图
product_scene_image       商品场景图
product_background_change 商品换背景
product_flat_lay          平铺图
model_try_on              模特换装
image_enhance             高清修复
image_remove_bg           去背景/抠图
image_partial_redraw      局部重绘
```

### 6.2 视频任务

```text
product_image_to_video    商品图生视频
product_multi_image_video 多图商品视频
hot_style_fission         爆款视频裂变
product_replace           商品替换
person_replace            人物替换
smart_cut                 智能混剪
storyboard_video          分镜视频
```

### 6.3 文案任务

```text
product_selling_points    商品卖点
xiaohongshu_seed_text     小红书种草文案
video_script              视频口播脚本
ad_copy                   广告文案
```

## 7. Image2 Provider 适配设计

### 7.1 适用场景

`image2` 优先负责图片类电商任务：

```text
商品主图
商品场景图
商品换背景
商品融合图
小红书封面图
详情页氛围图
```

### 7.2 Provider 配置

```json
{
  "name": "image2",
  "displayName": "Image2 中转供应商",
  "baseUrl": "https://provider.example.com/v1",
  "apiKey": "********",
  "authType": "bearer",
  "capabilities": [
    "text_to_image",
    "image_to_image",
    "product_to_scene_image",
    "image_edit"
  ],
  "config": {
    "submitPath": "/images/generations",
    "taskQueryPath": "/tasks/{remoteTaskId}",
    "isAsync": true,
    "resultUrlPath": "data[0].url"
  }
}
```

### 7.3 大云雀统一请求

```ts
type UnifiedImageTaskInput = {
  prompt: string;
  negativePrompt?: string;
  inputImages: string[];
  count: number;
  ratio: '1:1' | '4:3' | '3:4' | '16:9' | '9:16';
  resolution: string;
  style?: string;
  scene?: string;
};
```

### 7.4 转供应商请求

不同中转格式可能不同，所以 Adapter 内部做映射：

```ts
type Image2RemoteRequest = {
  model: string;
  prompt: string;
  image_urls?: string[];
  n?: number;
  size?: string;
  ratio?: string;
  extra?: Record<string, unknown>;
};
```

### 7.5 响应归一化

```ts
type ProviderTaskResult = {
  remoteTaskId?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  outputs: Array<{
    type: 'image';
    url: string;
  }>;
  raw: unknown;
};
```

## 8. Seedance Provider 适配设计

### 8.1 适用场景

`seedance` 优先负责视频类电商任务：

```text
商品图生视频
多图商品视频
商品展示短视频
爆款视频裂变
短剧/分镜视频
营销视频
```

### 8.2 Provider 配置

```json
{
  "name": "seedance",
  "displayName": "Seedance 中转供应商",
  "baseUrl": "https://provider.example.com/v1",
  "apiKey": "********",
  "authType": "bearer",
  "capabilities": [
    "text_to_video",
    "image_to_video",
    "multi_image_to_video"
  ],
  "config": {
    "submitPath": "/videos/generations",
    "taskQueryPath": "/tasks/{remoteTaskId}",
    "isAsync": true,
    "resultUrlPath": "data.video_url"
  }
}
```

### 8.3 大云雀统一请求

```ts
type UnifiedVideoTaskInput = {
  prompt: string;
  inputImages: string[];
  referenceVideo?: string;
  duration: 5 | 10;
  ratio: '16:9' | '9:16' | '1:1';
  resolution: '720p' | '1080p';
  motionStrength?: number;
  camera?: string;
  style?: string;
};
```

### 8.4 转供应商请求

```ts
type SeedanceRemoteRequest = {
  model: string;
  prompt: string;
  image_urls?: string[];
  duration?: number;
  ratio?: string;
  resolution?: string;
  extra?: Record<string, unknown>;
};
```

### 8.5 电商 Prompt 组装

商品图生视频不应只传用户一句话，后端需要补充结构化 Prompt：

```text
主体：保持 @商品图 中商品外观、颜色、Logo 和材质一致。
场景：高级电商摄影棚，干净背景，柔和布光。
镜头：缓慢推进，轻微环绕，突出商品细节。
限制：不要改变商品结构，不要生成多余文字，不要扭曲 Logo。
输出：9:16 竖屏短视频，适合小红书/抖音商品展示。
```

## 9. 任务状态设计

统一任务状态：

```text
draft       草稿
pending     已创建，等待执行
submitted   已提交供应商
running     供应商生成中
succeeded   成功
failed      失败
cancelled   取消
refunded    失败后已退积分
```

供应商状态映射：

```text
queued / pending   -> pending
processing/running -> running
success/completed  -> succeeded
error/failed       -> failed
```

## 10. 积分扣减建议

### 10.1 扣费流程

```text
estimate
→ 创建任务前检查余额
→ 创建任务时冻结积分
→ 供应商提交成功后保持冻结
→ 任务成功后转为实际扣减
→ 任务失败后释放/退回积分
```

### 10.2 默认成本

```text
商品图片 1 张：1 积分
商品图片 4 张：4 积分
商品图生视频 5 秒：20 积分
多图商品视频 5 秒：30 积分
1080p 视频：x2
重试：可配置是否扣费
```

## 11. 数据表建议

### 11.1 provider_configs

```text
id
name
display_name
base_url
api_key_encrypted
auth_type
capabilities JSON
config JSON
enabled
priority
fallback_provider_id
created_at
updated_at
```

### 11.2 model_configs

```text
id
provider_id
name
display_name
task_type
scene
remote_model
cost
enabled
priority
params_schema JSON
created_at
updated_at
```

### 11.3 assets

```text
id
user_id
project_id
asset_type
url
mime_type
width
height
detect_status
metadata JSON
created_at
```

### 11.4 tasks

```text
id
user_id
project_id
task_type
scene
mode
status
provider_id
model_id
remote_task_id
input JSON
output JSON
cost
error_code
error_message
created_at
updated_at
completed_at
```

### 11.5 point_records

```text
id
user_id
task_id
type acquire | freeze | consume | refund
amount
balance_after
reason
created_at
```

## 12. 面向电商的前端流程

### 12.1 商品主图

```text
上传商品图
→ 系统检测图片质量
→ 选择主图模板/场景
→ 填写卖点或风格
→ 估算积分
→ 创建 image2 任务
→ 轮询结果
→ 保存到我的作品
→ 下载/继续编辑/生成视频
```

### 12.2 商品图生视频

```text
选择已生成商品图或上传商品图
→ 选择视频模板：展示/环绕/爆款/口播背景
→ 填写动作和镜头描述
→ 估算积分
→ 创建 seedance 任务
→ 轮询结果
→ 保存到我的作品
→ 下载/发布/继续剪辑
```

## 13. 与绘蛙的差异

大云雀不采用 MTop 作为外部接口，而是用自有 REST API：

```text
绘蛙：mtop.alibaba.aigc.business.nvwa.createAigcImageTask
大云雀：POST /api/v1/tasks
```

大云雀后端内部再通过 Provider Adapter 对接中转供应商：

```text
POST /api/v1/tasks
  -> TaskService
  -> ProviderRouter
  -> Image2Provider / SeedanceProvider
  -> 中转供应商 API
```

这样可以保持前端稳定，即使后续更换 image2、seedance 或其他供应商，也不影响前端和业务任务模型。

## 14. MVP 建议

第一版只做这些：

```text
资产上传
任务估算
创建图片任务 image2
创建视频任务 seedance
任务查询
结果保存到我的作品
积分扣减
后台供应商配置
```

暂不做：

```text
模型训练
组织团队
发票合同
复杂项目交付
视频剪辑器
```

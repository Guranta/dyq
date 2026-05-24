# 绘蛙 ihuiwa.com 功能与后端接口研究

状态：调研完成  
最后更新：2026-05-24  
调研对象：`https://www.ihuiwa.com/?catId=2`  
文档索引：[docs/README.md](../README.md)

## 1. 调研结论

绘蛙是一个围绕“电商营销内容生产”的 AIGC 平台，不是单一 AI 绘图工具。公开页面与静态资源显示，它覆盖 AI 商品图、虚拟模特、模型训练、图片编辑、文案生成、视频生成、项目化生产、会员积分、组织协作等链路。

其技术结构接近：

```text
React + 阿里 ICE CSR 前端
  -> MTop API 网关
  -> AIGC Business NVWA 后端服务
  -> 任务系统 / 模型服务 / 资源上传 / 支付会员 / 组织系统
  -> 阿里 CDN / OSS / 视频资源服务
```

对大云雀最重要的参考点是：用行业场景组织产品，用统一任务系统承载图片、视频、文案和模型训练，用作品库沉淀资产，用积分/套餐/团队组织支撑商业化。

## 2. 公开页面与技术线索

公开 HTML 显示：

- 页面容器：`#ice-container`。
- 渲染方式：CSR。
- 前端框架：React 18 + 阿里 ICE。
- 静态资源版本：`feapp-nvwa/0.10.111`。
- 静态资源域：`https://g.alicdn.com/aigc-business/feapp-nvwa/0.10.111/`。
- 资源与服务域名：`img.alicdn.com`、`gw.alicdn.com`、`cloud.video.taobao.com`、`aigc-business.taobaocdn.com`。
- API/业务相关域名：`acs-m.ihuiwa.com`、`nvwa.ihuiwa.com`、`stream.ihuiwa.com`。
- 日志监控：`aplus.ihuiwa.com`、`log.mmstat.com`、`gm.mmstat.com`。

SEO 描述显示，绘蛙定位为智能图片、文案创作平台，支持虚拟模特、商品模型训练、AI 商拍图、种草文案、小红书图片、电商商品主图、跨境电商主图、口播文案、换装、去水印、智能消除、换脸、高清修复等能力。

`?catId=2` 很可能是首页或频道分类参数，用于切换分类 Tab；由于页面为 CSR 渲染，初始 HTML 未直接暴露 catId=2 的具体分类名。

## 3. 功能模块

### 3.1 工作台

公开静态资源显示存在以下路由：

```text
/workspace
/workspace/ai-creation
/workspace/model-management/*
/workspace/my-center/*
/pricing
```

推测工作台承载：

- AI 创作入口。
- 图片创作。
- 视频创作。
- 模型管理。
- 我的作品。
- 账户中心。
- 会员、积分、订单、合同。

### 3.2 AI 图片生成与商拍

相关路由：

```text
/workspace/ai-image/batch-image
/workspace/ai-image/batch-image/detail
/workspace/ai-image/creative-scene
/workspace/ai-image/image-fusion
/workspace/ai-image/one-shot
/workspace/ai-image/flat-lay
```

相关接口名：

```text
createAigcImageTask
queryAigcImageTasks
queryAigcImageTaskDetailById
editAigcImageTask
downloadTaskImages
queryAigcRecommendScene
createAISceneTask
queryaigctaskv3detail
```

推测能力：

- 上传商品图。
- 选择场景、模板、模特、风格。
- 生成电商主图、详情图、场景图。
- 批量生成商品图。
- 查询任务进度和结果。
- 下载结果图。
- 基于已有任务二次编辑。

### 3.3 虚拟模特与一键换装

相关路由：

```text
/workspace/ai-image/wear-everything
/workspace/ai-image/one-shot?mannequinType=2
```

相关接口名：

```text
searchModels
searchOfficialModels
createLoraModelTrainTask
queryAigcLoraDetailById
hireAiModel
buyCustomizeAIModel
queryModelHireInfo
officialModelTrialTimes
```

推测能力：

- 使用官方虚拟模特。
- 训练个人或品牌专属模特。
- 商品服饰上身。
- 租用、购买、收藏模特。
- 浏览、筛选、查看模型市场。

### 3.4 图片编辑与修复

相关路由：

```text
/workspace/ai-image/func/remove-watermark
/workspace/ai-image/func/item-change-background
/workspace/ai-image/func/item-repair
/workspace/ai-image/func/material-enhancement
/workspace/ai-image/func/clothing-extraction
/workspace/ai-image/func/clothing-detail
/workspace/ai-image/func/to-3d
/workspace/partial-redraw?editType=expand-image
/workspace/partial-redraw?editType=smart-matting
```

相关接口名：

```text
clearImageWatermark
improveImageQuality
mattingItemImage
mattingMaskImage
removeItemImagePrint
logofix.querymasks
image.ocr
image.detectImageContent
pro.image.segimagecontent
edit.image.task.update
```

推测能力：

- 去水印。
- 高清修复。
- 智能抠图。
- 局部重绘。
- 扩图。
- 商品换背景。
- 商品修复。
- 素材增强。
- 服装提取。
- 图片检测、OCR、内容风控。

### 3.5 AI 文案生成

相关接口名：

```text
createAigcTextTask
queryAigcTextTasks
queryAigcTextTaskDetailById
editAigcTextTask
editAigcTextContext
searchTextTasks
itemsellpoint
item.sellingPoint
generateprompt
prompt.recommend
scene.associated.prompts
scene.hot.word.query
```

推测能力：

- 商品卖点提取。
- 小红书种草文案生成。
- 穿搭文案生成。
- 视频口播脚本生成。
- Prompt 推荐、扩写、优化。
- 文案历史任务管理。
- 文案编辑与复用。

### 3.6 AI 视频生成

相关路由：

```text
/workspace/ai-video/hot-style-fission
/workspace/ai-video/custom-action
/workspace/ai-video/item-replace
/workspace/ai-video/user-replace
/workspace/ai-video/from-image
/workspace/ai-video/multi-img
/workspace/ai-video/smart-cut
/workspace/ai-video/pairing
/workspace/ai-video/repl
```

相关接口名：

```text
createAigcVideoTask
queryVideoTasks
queryAigcVideoTaskDetailById
aigc.video.task.retrybyid
batch.video.task.create
createSceneVideo
detectVideoContent
checkImage4genVideo
publishVideo
downloadVideos
mixed.cutting.genVideo
mixed.cutting.storyboard.create
mixed.cutting.task.detail.querybyid
mixed.cutting.task.updatebyid
mixed.cutting.retryedit
mixed.cutting.tonestyle.query
```

推测能力：

- 图生视频。
- 多图生成视频。
- 热款/爆款视频裂变。
- 自定义动作视频。
- 商品替换。
- 人物替换。
- 智能混剪。
- 分镜生成。
- 口播语气配置。
- 视频检测、重试、发布、下载。

### 3.7 模型市场与模型训练

相关路由：

```text
/workspace/models-market/index
/workspace/models-market/detail
/workspace/model-management/*
/workspace/my-works/creation-model
/workspace/my-works/person-model
/workspace/my-works/scene-model
/workspace/my-works/video-scene-model
```

相关接口名：

```text
searchModels
searchOfficialModels
queryModelTag
queryAigcLoraDetailById
createLoraModelTrainTask
createSceneModelTrainTask
deleteModel
batchDeleteModel
model.batchmove
model.labels.config
model.shareModel
setCollectModel
cancelCollectModel
dislikeRecommendModel
queryModelHireInfo
hireAiModel
buyCustomizeAIModel
```

推测能力：

- 官方模型市场。
- 用户自训练模型。
- 模特模型、商品模型、场景模型、视频场景模型。
- 收藏、分享、删除、移动、标签管理。
- 模型试用、雇佣、定制购买。

### 3.8 我的作品与任务管理

相关路由：

```text
/workspace/my-works/image-task
/workspace/my-works/video-task
/workspace/my-works/creation-task
/workspace/my-works/redraw-task
/workspace/my-works/project-list
```

相关接口名：

```text
queryAigcImageTasks
queryVideoTasks
queryAICreationTasks
queryAigcTextTasks
deleteAigcTaskById
deleteAigcImageTaskById
deleteAigcTextTaskById
shareTasks
task.collect
task.feedback.config
task.submit
```

推测能力：

- 按图片、视频、文案、重绘、项目分类管理作品。
- 查看生成状态。
- 删除、收藏、分享任务。
- 下载结果。
- 任务反馈。

### 3.9 项目化生产流程

静态资源中出现大量 `pro.*` 接口，说明绘蛙有面向大商家或企业的项目化流程。

相关接口名：

```text
pro.project.save
pro.project.submit
pro.project.edit
pro.project.delete
pro.project.progress.update
pro.project.pay.confirm
pro.project.pay.cancel
pro.queryProjectDetailById
pro.searchProjects
pro.item.createItem
pro.item.editItem
pro.item.deleteItem
pro.item.list
pro.task.addSubTask
pro.task.queryItemTasks
pro.task.queryDeliveryItemTasks
pro.task.downloadDeliveryImages
pro.requirement.category.meta
pro.require.resourceUploadToken
```

推测流程：

```text
创建项目
→ 添加商品
→ 填写需求
→ 匹配场景/模板/模型
→ 创建子任务
→ 生成图像
→ 质检/标注/交付
→ 支付确认/交付下载
```

### 3.10 会员、积分、支付、合同、组织

相关接口名：

```text
member.package.list
member.package.qrcode
member.package.switch
member.package.switch.rightnow
member.package.discountdetail
member.package.welcome
member.daily.package.fetch
point.queryAccountPointDetail
point.searchAcquirePointRecords
point.searchConsumePointRecords
payment.order.list
payment.result.query
invoice.apply
invoice.title.query
invoice.title.save
invoice.title.fuzzyQuery
contract.querycontractinfolist
contract.querycontractinfobyid
contract.querycontracttemplate
contract.generatecontractpreview
contract.signcontract
org.createOrganization
org.updateOrganization
org.queryOrgMember
org.updateOrgMember
org.deleteOrganizationMember
org.applyJoinOrganization
org.auditPassJoinOrganization
org.auditRejectJoinOrganization
org.queryUserInfoAtOrg
org.queryorgmemeberconsumepointsummary
```

推测能力：

- 会员套餐、套餐切换、支付二维码。
- 每日权益领取。
- 积分账户、积分获取和消耗明细。
- 订单、发票、合同。
- 企业组织、成员管理、成员消耗统计、加入审核。

## 4. 后端接口形态推测

### 4.1 API 网关

绘蛙主要接口形态是阿里 MTop：

```text
mtop.alibaba.aigc.business.nvwa.<methodName>
```

浏览器侧通过 MTop SDK 调用 `acs-m.ihuiwa.com` 等网关域名，请求依赖登录态 Cookie 或 Token。接口参数和返回结构未公开，但接口命名清晰暴露了业务边界。

### 4.2 上传链路

公开线索包括：

```text
//stream.ihuiwa.com/image/upload?_input_charset=utf-8&withExif=true
//pre-stream.ihuiwa.com/image/upload?_input_charset=utf-8&withExif=true
//stream-upload.taobao.com/api/upload.api?_input_charset=utf-8&withExif=true
```

另有 OSS STS 上传相关逻辑：

```text
fetchResourceUploadToken
```

推测上传流程：

```text
前端压缩/检测文件
→ 获取上传 token
→ 上传至 stream/OSS
→ 返回资源 URL / assetId
→ 创建 AIGC 任务时引用资源
```

### 4.3 任务系统

绘蛙接口命名显示图片、视频、文案、训练任务均采用任务模型：

```text
create*Task
query*Tasks
query*TaskDetailById
edit*Task
delete*TaskById
retry*Task
download*Assets
```

大云雀可抽象为统一任务接口：

```text
POST /api/v1/tasks
GET  /api/v1/tasks
GET  /api/v1/tasks/{id}
POST /api/v1/tasks/{id}/retry
DELETE /api/v1/tasks/{id}
POST /api/v1/tasks/{id}/collect
POST /api/v1/tasks/{id}/share
GET  /api/v1/tasks/{id}/download
```

## 5. 数据模型推测

### 5.1 AIGC 任务

```ts
type AigcTask = {
  taskId: string;
  userId: string;
  taskType: 'image' | 'text' | 'video' | 'model_train' | 'redraw';
  bizType: string | number;
  status: 'pending' | 'running' | 'success' | 'failed' | 'cancelled';
  input: Record<string, unknown>;
  output: {
    images?: Asset[];
    videos?: Asset[];
    texts?: string[];
  };
  errorCode?: string;
  errorMessage?: string;
  pointCost?: number;
  createdAt: number;
  updatedAt: number;
};
```

### 5.2 资产

```ts
type Asset = {
  assetId: string;
  url: string;
  width?: number;
  height?: number;
  size?: number;
  format?: string;
  source: 'upload' | 'generated' | 'official';
  labels?: string[];
  riskCheckStatus?: string;
};
```

### 5.3 模型

```ts
type Model = {
  modelId: string;
  name: string;
  type: 'person' | 'product' | 'scene' | 'video_scene' | 'lora';
  ownerUserId?: string;
  official: boolean;
  coverUrl: string;
  tags: string[];
  status: 'training' | 'ready' | 'failed' | 'deleted';
  trialTimes?: number;
  price?: number;
};
```

### 5.4 项目

```ts
type Project = {
  projectId: string;
  name: string;
  userId: string;
  orgId?: string;
  items: Item[];
  requirements: Requirement[];
  status: 'draft' | 'submitted' | 'generating' | 'delivering' | 'finished';
  payStatus?: 'unpaid' | 'paid' | 'cancelled';
  progress: number;
};
```

### 5.5 积分流水

```ts
type PointRecord = {
  recordId: string;
  userId: string;
  type: 'acquire' | 'consume';
  amount: number;
  bizType: string;
  taskId?: string;
  createdAt: number;
};
```

## 6. 对大云雀的借鉴点

### 6.1 用场景组织产品

绘蛙不是按“模型名称”组织产品，而是按用户任务组织：AI 商拍、商品换背景、一键换装、种草文案、图生视频、智能混剪。大云雀也应减少模型术语，优先使用用户能理解的任务入口。

### 6.2 建立统一任务系统

图片、视频、文案、模型训练都可以抽象为任务。大云雀应尽早设计统一任务表和接口，避免每种生成能力各自为政。

### 6.3 建立统一作品资产库

绘蛙有“我的作品”分区，包括图片任务、视频任务、文案任务、重绘任务、项目列表。大云雀也应把所有生成结果沉淀为资产和项目。

### 6.4 模型市场与自训练模型

虚拟模特、商品模型、场景模型会提高平台粘性。大云雀短期可先做“角色库/素材库”，长期再扩展自训练模型和模型市场。

### 6.5 积分与会员体系早设计

绘蛙的积分、套餐、订单、发票、合同和组织系统非常完整。大云雀即使早期不做支付，也应预留积分流水、套餐权益和团队消耗统计的数据模型。

### 6.6 内容安全与质量检测

绘蛙任务前后有图片检测、视频检测、OCR、内容检测等接口。大云雀在开放生成能力前应加入内容安全、图片质量和素材合法性检测。

## 7. 不确定性

- `catId=2` 的具体分类含义无法从公开 HTML 直接确认。
- 接口名来自公开静态 JS，参数结构和返回结构需要登录后真实请求才能确认。
- 未登录状态无法确认具体 UI、会员限制、生成质量和价格策略。
- 绘蛙强依赖阿里生态能力，包括 MTop、阿里登录、OSS、CDN、Aplus/mmstat 等，大云雀只能借鉴产品结构和流程，不应照搬底层实现。

## 8. 大云雀建议接口草案

参考绘蛙后，大云雀后端可以优先规划这些接口分组：

```text
/api/v1/auth/*
/api/v1/assets/*
/api/v1/tasks/*
/api/v1/tasks/{id}/retry
/api/v1/tasks/{id}/download
/api/v1/tasks/{id}/share
/api/v1/projects/*
/api/v1/templates/*
/api/v1/models/*
/api/v1/provider-configs/*
/api/v1/points/*
/api/v1/packages/*
/api/v1/orgs/*
/api/v1/tools/image/*
/api/v1/tools/video/*
```

统一任务创建请求：

```ts
type CreateTaskRequest = {
  taskType: 'image' | 'text' | 'video' | 'model_train' | 'redraw';
  mode: string;
  inputAssets?: string[];
  prompt?: string;
  templateId?: string;
  modelId?: string;
  params: Record<string, unknown>;
};
```

统一任务响应：

```ts
type TaskResponse = {
  taskId: string;
  status: 'pending' | 'running' | 'success' | 'failed';
  progress: number;
  pointCost: number;
  output: Record<string, unknown>;
  error?: {
    code: string;
    message: string;
  };
};
```

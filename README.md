# 🍜 餐饮评论细粒度情感分析系统

基于 BERT 的餐饮评论细粒度情感分析系统，支持单条分析、批量处理、可视化展示和 AI 智能建议。

## ✨ 功能特点

- **单条评论分析**：输入餐饮评论，实时返回 20 个情感维度的分析结果
- **批量处理**：支持上传 CSV 文件批量分析评论数据
- **可视化图表**：饼图、柱状图展示情感分析结果分布
- **AI 智能建议**：基于大模型生成改进建议
- **历史记录**：保存分析历史，支持查看和导出
- **用户登录**：默认账号密码均为 `admin`

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI 0.104.1
- **模型**: PyTorch + BERT / LSTM
- **数据库**: SQLite
- **大模型**: SiliconFlow API (Qwen/Qwen2.5-7B-Instruct)

### 前端
- **框架**: Vue 3 + Element Plus
- **图表**: Chart.js
- **动画**: Particles.js

## 📁 项目结构

```
Sentiment-Analysis-Bert/
├── backend/                 # 后端代码
│   ├── api/                # API 路由
│   │   ├── analyze.py      # 分析接口
│   │   ├── auth.py         # 认证接口
│   │   ├── history.py      # 历史记录接口
│   │   └── stats.py        # 统计接口
│   ├── services/           # 业务逻辑
│   │   ├── predictor.py    # 情感预测服务
│   │   └── llm_suggestions.py  # LLM 建议服务
│   ├── models/             # 数据模型
│   ├── main.py             # 应用入口
│   ├── schemas.py          # 数据结构定义
│   └── settings.py         # 配置文件
├── frontend/               # 前端代码
│   ├── index.html          # 主页面
│   ├── css/                # 样式文件
│   └── js/                 # JavaScript 代码
│       ├── components/     # 组件
│       ├── pages/          # 页面
│       ├── api.js          # API 调用封装
│       └── app.js          # 应用入口
├── models/                 # 模型文件
│   └── bert_tokenizer/     # 分词器文件
├── config.py               # 全局配置
├── models.py               # 情感模型定义
├── requirements.txt        # 依赖列表
└── Dockerfile              # Docker 构建文件
```

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js 16+

### 安装依赖

```bash
# 安装后端依赖
pip install -r requirements.txt

# 安装 torch（CPU 版本）
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
```

### 配置环境变量

创建 `.env` 文件：

```env
LLM_API_KEY=your_siliconflow_api_key
LLM_MODEL=Qwen/Qwen2.5-7B-Instruct
LLM_PROVIDER=siliconflow
LLM_BASE_URL=https://api.siliconflow.cn/v1
```

### 启动服务

```bash
# 开发模式
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 生产模式
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 访问应用

打开浏览器访问：http://localhost:8000

登录账号：`admin` / 密码：`admin`

## 🐳 Docker 部署

```bash
# 构建镜像
docker build -t sentiment-analysis .

# 运行容器
docker run -p 8000:8000 --env LLM_API_KEY=your_key sentiment-analysis
```

## 🌐 部署到 Render

1. 注册 Render 账号：https://render.com/
2. 创建 Web Service，连接 GitHub 仓库
3. 设置环境变量：
   - `LLM_API_KEY`: 你的 SiliconFlow API Key
   - `LLM_MODEL`: Qwen/Qwen2.5-7B-Instruct
   - `LLM_PROVIDER`: siliconflow
   - `LLM_BASE_URL`: https://api.siliconflow.cn/v1
4. 选择 Free 实例类型，点击 Deploy

## 📡 API 接口

### 分析单条评论

```http
POST /api/analyze
Content-Type: application/json

{
  "text": "这家餐厅的菜很好吃，服务也很周到！"
}
```

**响应示例**：
```json
{
  "text": "这家餐厅的菜很好吃，服务也很周到！",
  "results": [
    {"dimension": "dish_taste", "label": "正面", "score": 0.85},
    {"dimension": "service_waiters_attitude", "label": "正面", "score": 0.92}
  ],
  "suggestions": ["建议保持菜品口味的稳定性..."]
}
```

### 批量分析

```http
POST /api/analyze/batch
Content-Type: multipart/form-data

file: <CSV文件>
```

### 获取历史记录

```http
GET /api/history?page=1&size=10
```

## 📊 情感维度

系统分析以下 20 个情感维度：

| 维度 | 说明 |
|------|------|
| location_traffic_convenience | 交通便利性 |
| location_distance_from_business_district | 离商业区距离 |
| location_easy_to_find | 是否容易找到 |
| service_wait_time | 服务等待时间 |
| service_waiters_attitude | 服务员态度 |
| service_parking_convenience | 停车便利性 |
| service_serving_speed | 上菜速度 |
| price_level | 价格水平 |
| price_cost_effective | 性价比 |
| price_discount | 折扣力度 |
| environment_decoration | 装修环境 |
| environment_noise | 噪音情况 |
| environment_space | 空间大小 |
| environment_cleaness | 清洁程度 |
| dish_portion | 菜品分量 |
| dish_taste | 菜品味道 |
| dish_look | 菜品外观 |
| dish_recommendation | 推荐菜品 |
| others_overall_experience | 整体体验 |
| others_willing_to_consume_again | 是否愿意再次消费 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**作者**: liu66-8  
**项目地址**: https://github.com/liu66-8/sentiment-analysis-bert
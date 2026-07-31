# 手艺云创 - 民族手工艺三大系统

基于 Python Flask 开发的三个民族手工艺管理系统，包含数据库系统、文化基因识别系统和智能设计平台。

## 系统概览

### 1. 民族手工艺数据库系统（橙色主题 #E09456）
数字化整合手工艺生态链，助力非遗传承与创新发展。

**功能模块：**
- 传承与发展：技法传承图谱、传承人档案管理、技艺培训管理
- 作品与资源管理：手工艺作品管理、元素融合设计、纹样智能检索
- 数据分析：工艺品类分析、工艺品类统计管理、非遗传承分析
- 项目管理：传承项目申报、展览活动管理、国际合作管理、文化机构管理
- 系统管理：数据备份管理

### 2. 文化基因智能识别系统（蓝色主题 #0277BD）
智能解析传统手工艺文化基因，传承千年匠心智慧。

**功能模块：**
- 文创设计辅助：智能融合设计、纹样智能解析、文创设计辅助管理
- 文化基因分析：基因识别统计、基因特征提取、传承关系溯源、基因图谱构建、基因分类管理、基因检索管理、分析报告管理
- 文化资源采集：手工艺品采集管理、非遗传承人访谈管理、文化传承教学管理
- 系统管理：系统效能监控、基因审核流程管理

### 3. 民族手工艺品智能生成设计平台（绿色主题 #26A69A）
AI赋能传统工艺，一键生成专属文创设计方案。

**功能模块：**
- 工艺管理：传统工艺适配管理、手工艺品方案管理、耗材计算
- 市场分析：趋势预测、需求洞察、设计趋势分析管理
- 文化传承：非遗传承人管理、民族文化知识管理、工艺教学课程管理
- 智能设计工具：纹样生成、智能生成设计管理、设计效能
- 订单管理：定制订单跟踪管理
- 设计素材库：民族图案素材管理、数字版权登记管理

## 技术栈

- **后端框架**：Flask 3.0.0
- **数据库**：SQLite + Flask-SQLAlchemy 3.1.1
- **用户认证**：Flask-Login 0.6.3
- **前端**：HTML5 + CSS3 + 原生JavaScript
- **设计风格**：响应式布局，三系统独立主题色

## 项目结构

```
shouyi_project/
├── app.py                    # 主应用入口
├── config.py                 # 配置文件
├── requirements.txt          # 依赖包列表
├── generate_templates.py     # 模板批量生成脚本
├── models/
│   └── __init__.py           # 20+ 数据模型定义
├── database/
│   ├── __init__.py
│   └── init_db.py            # 数据库初始化脚本（含示例数据）
├── routes/
│   ├── __init__.py
│   ├── auth.py               # 认证路由
│   ├── database_system/
│   │   ├── __init__.py
│   │   └── main.py           # 数据库系统路由
│   ├── gene_system/
│   │   ├── __init__.py
│   │   └── main.py           # 基因识别系统路由
│   └── design_system/
│       ├── __init__.py
│       └── main.py           # 设计平台路由
├── static/
│   └── css/
│       └── style.css         # 全局样式
└── templates/
    ├── base.html             # 基础模板
    ├── layout.html           # 后台布局模板
    ├── login.html            # 登录页
    ├── database_system/      # 数据库系统页面（14个）
    ├── gene_system/          # 基因系统页面（16个）
    └── design_system/        # 设计系统页面（16个）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python database/init_db.py
```

该脚本会创建所有数据表并插入示例数据。

### 3. 启动应用

```bash
python app.py
```

应用默认运行在 `http://localhost:5000`

### 4. 默认登录账号

- 用户名：`admin`
- 密码：`admin123`

## 三大系统访问地址

登录时可选择进入不同系统，或直接访问以下地址：

- 数据库系统：`http://localhost:5000/database/`
- 基因识别系统：`http://localhost:5000/gene/`
- 智能设计平台：`http://localhost:5000/design/`

## 数据模型

### 通用模型
- **User**：用户模型（支持密码哈希、角色区分）

### 数据库系统模型（8个）
- Artisan（传承人档案）
- TrainingProgram（技艺培训）
- Artwork（手工艺作品）
- Pattern（纹样）
- CraftCategory（工艺品类统计）
- HeritageProject（传承项目申报）
- Exhibition（展览活动）
- CulturalInstitution（文化机构）

### 基因识别系统模型（7个）
- CulturalGene（文化基因）
- PatternAnalysis（纹样解析）
- GeneFeature（基因特征提取）
- GeneClassification（基因分类）
- CulturalDesign（文创设计辅助）
- HandicraftCollection（手工艺品采集）
- HeritageInterview（非遗传承人访谈）

### 设计平台模型（9个）
- CraftProcess（传统工艺适配）
- ProductScheme（手工艺品方案）
- DesignTrend（设计趋势分析）
- HeritageInheritor（非遗传承人）
- CulturalKnowledge（民族文化知识）
- TeachingCourse（工艺教学课程）
- PatternMaterial（民族图案素材）
- CopyrightRegistration（数字版权登记）
- CustomOrder（定制订单）

## 功能特点

1. **三系统统一登录**：一个账号切换三个系统，主题色动态切换
2. **完整CRUD操作**：核心模块支持增删改查
3. **分页与搜索**：列表页支持分页展示和关键词搜索
4. **响应式布局**：适配不同屏幕尺寸
5. **模态框表单**：新增/编辑操作使用弹窗，体验流畅
6. **丰富示例数据**：每个模型预置3-5条示例数据
7. **状态标签**：不同状态使用不同颜色标签区分

## 开发说明

### 新增页面
1. 在对应系统的 `routes/main.py` 中添加路由
2. 在 `templates/<系统>/` 目录下创建HTML模板
3. 在侧边栏菜单中添加链接

### 主题色配置
三个系统的主题色在各自路由文件的顶部定义：
- 数据库系统：`#E09456`（橙色）
- 基因系统：`#0277BD`（蓝色）
- 设计平台：`#26A69A`（绿色）

### CSS变量
全局样式使用CSS变量 `--theme-color` 和 `--theme-color-light` 控制主题色，通过路由渲染时动态注入。

## 注意事项

- 项目使用SQLite数据库，无需额外安装数据库服务
- 数据库文件 `shouyi.db` 会在首次初始化时自动创建
- 所有密码使用Werkzeug进行哈希存储
- 生产环境请修改 `config.py` 中的 `SECRET_KEY`

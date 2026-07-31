from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), default='admin')
    system_type = db.Column(db.String(32), default='all')  # database, gene, design, all
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ==================== 民族手工艺数据库系统模型 ====================

class Artisan(db.Model):
    """传承人档案"""
    __tablename__ = 'artisans'
    
    id = db.Column(db.Integer, primary_key=True)
    artisan_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(8))
    ethnic_group = db.Column(db.String(32))
    birth_date = db.Column(db.String(32))
    skill_type = db.Column(db.String(64))
    heritage_level = db.Column(db.String(32))
    representative_works = db.Column(db.String(256))
    contact = db.Column(db.String(64))
    location = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TrainingProgram(db.Model):
    """技艺培训"""
    __tablename__ = 'training_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    instructor = db.Column(db.String(64))
    training_date = db.Column(db.String(32))
    location = db.Column(db.String(128))
    participants = db.Column(db.Integer, default=0)
    duration = db.Column(db.String(32))
    content = db.Column(db.Text)
    assessment_method = db.Column(db.String(32))
    status = db.Column(db.String(32), default='未开始')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Artwork(db.Model):
    """手工艺作品"""
    __tablename__ = 'artworks'
    
    id = db.Column(db.Integer, primary_key=True)
    artwork_id = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    artisan = db.Column(db.String(64))
    material = db.Column(db.String(64))
    technique = db.Column(db.String(64))
    pattern_type = db.Column(db.String(64))
    cultural_value = db.Column(db.String(32))
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='已归档')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Pattern(db.Model):
    """纹样"""
    __tablename__ = 'patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    pattern_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    origin = db.Column(db.String(64))
    category = db.Column(db.String(64))
    cultural_meaning = db.Column(db.String(256))
    color_scheme = db.Column(db.String(128))
    description = db.Column(db.Text)
    image_path = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CraftCategory(db.Model):
    """工艺品类统计"""
    __tablename__ = 'craft_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(32), unique=True, nullable=False)
    category_name = db.Column(db.String(64), nullable=False)
    count = db.Column(db.Integer, default=0)
    region = db.Column(db.String(64))
    heritage_count = db.Column(db.Integer, default=0)
    trend = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HeritageProject(db.Model):
    """传承项目申报"""
    __tablename__ = 'heritage_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(32), unique=True, nullable=False)
    project_name = db.Column(db.String(128), nullable=False)
    applicant = db.Column(db.String(64))
    project_type = db.Column(db.String(64))
    apply_date = db.Column(db.String(32))
    status = db.Column(db.String(32), default='审核中')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Exhibition(db.Model):
    """展览活动"""
    __tablename__ = 'exhibitions'
    
    id = db.Column(db.Integer, primary_key=True)
    exhibition_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128))
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    organizer = db.Column(db.String(64))
    status = db.Column(db.String(32), default='筹备中')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CulturalInstitution(db.Model):
    """文化机构"""
    __tablename__ = 'cultural_institutions'
    
    id = db.Column(db.Integer, primary_key=True)
    institution_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))
    location = db.Column(db.String(128))
    contact = db.Column(db.String(64))
    level = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== 文化基因智能识别系统模型 ====================

class CulturalGene(db.Model):
    """文化基因"""
    __tablename__ = 'cultural_genes'
    
    id = db.Column(db.Integer, primary_key=True)
    gene_id = db.Column(db.String(32), unique=True, nullable=False)
    gene_name = db.Column(db.String(64), nullable=False)
    gene_type = db.Column(db.String(64))
    gene_features = db.Column(db.Text)  # JSON格式存储特征列表
    origin = db.Column(db.String(64))
    cultural_meaning = db.Column(db.String(256))
    confidence = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(32), default='待审核')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PatternAnalysis(db.Model):
    """纹样解析"""
    __tablename__ = 'pattern_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.String(32), unique=True, nullable=False)
    pattern_name = db.Column(db.String(64), nullable=False)
    image_path = db.Column(db.String(256))
    analysis_result = db.Column(db.Text)  # JSON格式
    color_scheme = db.Column(db.String(128))
    structure = db.Column(db.String(128))
    status = db.Column(db.String(32), default='解析中')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GeneFeature(db.Model):
    """基因特征提取"""
    __tablename__ = 'gene_features'
    
    id = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.String(32), unique=True, nullable=False)
    related_collection_id = db.Column(db.String(32))
    feature_type = db.Column(db.String(64))
    feature_description = db.Column(db.String(256))
    feature_image = db.Column(db.String(256))
    feature_vector = db.Column(db.String(128))
    extraction_algorithm = db.Column(db.String(64))
    extractor = db.Column(db.String(64))
    extraction_date = db.Column(db.String(32))
    confidence = db.Column(db.String(32))
    status = db.Column(db.String(32), default='待审核')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GeneClassification(db.Model):
    """基因分类"""
    __tablename__ = 'gene_classifications'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(32), unique=True, nullable=False)
    category_name = db.Column(db.String(64), nullable=False)
    parent_category = db.Column(db.String(32))
    description = db.Column(db.Text)
    gene_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CulturalDesign(db.Model):
    """文创设计辅助"""
    __tablename__ = 'cultural_designs'
    
    id = db.Column(db.Integer, primary_key=True)
    design_id = db.Column(db.String(32), unique=True, nullable=False)
    designer = db.Column(db.String(64))
    design_date = db.Column(db.String(32))
    theme = db.Column(db.String(128))
    reference_gene = db.Column(db.String(64))
    sketch = db.Column(db.String(256))
    description = db.Column(db.Text)
    cultural_elements = db.Column(db.String(128))
    status = db.Column(db.String(32), default='进行中')
    review_opinion = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HandicraftCollection(db.Model):
    """手工艺品采集"""
    __tablename__ = 'handicraft_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.String(32), unique=True, nullable=False)
    item_name = db.Column(db.String(128), nullable=False)
    collector = db.Column(db.String(64))
    collection_date = db.Column(db.String(32))
    origin = db.Column(db.String(64))
    category = db.Column(db.String(64))
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='已采集')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HeritageInterview(db.Model):
    """非遗传承人访谈"""
    __tablename__ = 'heritage_interviews'
    
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.String(32), unique=True, nullable=False)
    interviewee = db.Column(db.String(64), nullable=False)
    interviewer = db.Column(db.String(64))
    interview_date = db.Column(db.String(32))
    topic = db.Column(db.String(128))
    content_summary = db.Column(db.Text)
    status = db.Column(db.String(32), default='已完成')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== 智能生成设计平台模型 ====================

class CraftProcess(db.Model):
    """传统工艺适配"""
    __tablename__ = 'craft_processes'
    
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.String(32), unique=True, nullable=False)
    process_name = db.Column(db.String(64), nullable=False)
    process_type = db.Column(db.String(64))
    applicable_material = db.Column(db.String(64))
    difficulty = db.Column(db.String(32))
    estimated_time = db.Column(db.String(32))
    tool_requirements = db.Column(db.String(128))
    description = db.Column(db.Text)
    teaching_video = db.Column(db.String(256))
    status = db.Column(db.String(32), default='可用')
    heritage_region = db.Column(db.String(64))
    cultural_level = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ProductScheme(db.Model):
    """手工艺品方案"""
    __tablename__ = 'product_schemes'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(32), unique=True, nullable=False)
    product_name = db.Column(db.String(128), nullable=False)
    base_design = db.Column(db.String(64))
    applicable_craft = db.Column(db.String(64))
    material_list = db.Column(db.String(256))
    production_process = db.Column(db.String(128))
    cost_budget = db.Column(db.String(32))
    suggested_price = db.Column(db.String(32))
    status = db.Column(db.String(32), default='设计中')
    cultural_value = db.Column(db.String(64))
    product_size = db.Column(db.String(32))
    product_weight = db.Column(db.String(32))
    # 智能评级六维度
    innovation_score = db.Column(db.Float, default=0)    # 创新性
    history_score = db.Column(db.Float, default=0)       # 历史性
    art_score = db.Column(db.Float, default=0)           # 艺术性
    practical_score = db.Column(db.Float, default=0)     # 实用性
    culture_score = db.Column(db.Float, default=0)       # 文化价值
    craft_score = db.Column(db.Float, default=0)         # 工艺难度
    total_score = db.Column(db.Float, default=0)         # 综合总分
    market_level = db.Column(db.String(16), default='C级')  # 市场需求等级：S/A/B/C
    is_ai_rated = db.Column(db.Boolean, default=False)   # 是否已AI评级
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DesignTrend(db.Model):
    """设计趋势分析"""
    __tablename__ = 'design_trends'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.String(32), unique=True, nullable=False)
    analysis_dimension = db.Column(db.String(64))
    time_range = db.Column(db.String(64))
    popular_materials = db.Column(db.String(128))
    popular_crafts = db.Column(db.String(128))
    region_distribution = db.Column(db.String(128))
    color_trend = db.Column(db.String(64))
    product_type = db.Column(db.String(64))
    user_preference = db.Column(db.String(64))
    cultural_heat = db.Column(db.String(64))
    analysis_date = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HeritageInheritor(db.Model):
    """非遗传承人（设计平台）"""
    __tablename__ = 'heritage_inheritors'
    
    id = db.Column(db.Integer, primary_key=True)
    inheritor_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    skill_category = db.Column(db.String(64))
    heritage_level = db.Column(db.String(32))
    region = db.Column(db.String(64))
    representative_works = db.Column(db.String(256))
    contact = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CulturalKnowledge(db.Model):
    """民族文化知识"""
    __tablename__ = 'cultural_knowledge'
    
    id = db.Column(db.Integer, primary_key=True)
    knowledge_id = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64))
    ethnic_group = db.Column(db.String(64))
    content = db.Column(db.Text)
    source = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TeachingCourse(db.Model):
    """工艺教学课程"""
    __tablename__ = 'teaching_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(32), unique=True, nullable=False)
    course_name = db.Column(db.String(128), nullable=False)
    instructor = db.Column(db.String(64))
    craft_type = db.Column(db.String(64))
    duration = db.Column(db.String(32))
    difficulty = db.Column(db.String(32))
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='已发布')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PatternMaterial(db.Model):
    """民族图案素材"""
    __tablename__ = 'pattern_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.String(32), unique=True, nullable=False)
    material_name = db.Column(db.String(128), nullable=False)
    pattern_type = db.Column(db.String(64))
    ethnic_origin = db.Column(db.String(64))
    image_path = db.Column(db.String(256))
    file_path = db.Column(db.String(256))  # 上传文件路径
    file_type = db.Column(db.String(32))   # 文件类型：image/png, jpg, svg等
    copyright_status = db.Column(db.String(32))
    tags = db.Column(db.String(256))       # 自动生成的标签，逗号分隔
    auto_tagged = db.Column(db.Boolean, default=False)  # 是否已自动标签化
    uploader = db.Column(db.String(64))    # 上传人
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CopyrightRegistration(db.Model):
    """数字版权登记"""
    __tablename__ = 'copyright_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.String(32), unique=True, nullable=False)
    work_name = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(64))
    work_type = db.Column(db.String(64))
    registration_date = db.Column(db.String(32))
    copyright_number = db.Column(db.String(64))
    status = db.Column(db.String(32), default='登记中')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CustomOrder(db.Model):
    """定制订单"""
    __tablename__ = 'custom_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(32), unique=True, nullable=False)
    customer_name = db.Column(db.String(64))
    product_type = db.Column(db.String(64))
    design_requirements = db.Column(db.Text)
    order_date = db.Column(db.String(32))
    deadline = db.Column(db.String(32))
    status = db.Column(db.String(32), default='待确认')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserPreference(db.Model):
    """用户偏好自适应配置"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    # 高频检索关键词，逗号分隔
    search_keywords = db.Column(db.Text, default='')
    # 常用创作风格，逗号分隔
    preferred_styles = db.Column(db.Text, default='')
    # 六维度评分权重（JSON格式存储）
    weight_innovation = db.Column(db.Float, default=1.0)  # 创新性权重
    weight_history = db.Column(db.Float, default=1.0)     # 历史性权重
    weight_art = db.Column(db.Float, default=1.0)         # 艺术性权重
    weight_practical = db.Column(db.Float, default=1.0)   # 实用性权重
    weight_culture = db.Column(db.Float, default=1.0)     # 文化价值权重
    weight_craft = db.Column(db.Float, default=1.0)       # 工艺难度权重
    # 统计数据
    total_searches = db.Column(db.Integer, default=0)     # 总搜索次数
    total_designs = db.Column(db.Integer, default=0)      # 总创建设计数
    # 偏好等级
    preference_level = db.Column(db.String(16), default='初级')  # 初级/中级/高级/深度定制
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

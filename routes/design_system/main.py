from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, CraftProcess, ProductScheme, DesignTrend, HeritageInheritor
from models import CulturalKnowledge, TeachingCourse, PatternMaterial
from models import CopyrightRegistration, CustomOrder, UserPreference
import os
import random
from datetime import datetime

design_bp = Blueprint('design', __name__)

SYSTEM_NAME = '民族手工艺品智能生成设计平台'
THEME_COLOR = '#26A69A'
THEME_COLOR_LIGHT = '#80CBC4'

# 上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'bmp', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def render_with_theme(template, **kwargs):
    return render_template(template,
                         system_name=SYSTEM_NAME,
                         theme_color=THEME_COLOR,
                         theme_color_light=THEME_COLOR_LIGHT,
                         system_type='design',
                         **kwargs)


# ==================== AI辅助函数 ====================

def auto_tag_material(filename, pattern_type='', ethnic_origin=''):
    """模拟AI自动标签化：根据文件名、类型、民族自动生成标签"""
    tags = []
    
    # 基于纹样类型的标签
    type_tags = {
        '植物纹样': ['植物', '花卉', '自然'],
        '动物纹样': ['动物', '瑞兽', '图腾'],
        '几何纹样': ['几何', '对称', '抽象'],
        '自然纹样': ['自然', '天象', '山水'],
        '人物纹样': ['人物', '民俗', '故事'],
        '符号纹样': ['符号', '文字', '吉祥'],
    }
    if pattern_type in type_tags:
        tags.extend(type_tags[pattern_type])
    
    # 基于民族的标签
    ethnic_tags = {
        '苗族': ['苗族', '蜡染', '刺绣'],
        '汉族': ['汉族', '传统', '古典'],
        '藏族': ['藏族', '佛教', '唐卡'],
        '维吾尔族': ['维吾尔', '西域', '地毯'],
        '彝族': ['彝族', '漆器', '彩绘'],
        '壮族': ['壮族', '铜鼓', '织锦'],
    }
    if ethnic_origin in ethnic_tags:
        tags.extend(ethnic_tags[ethnic_origin])
    
    # 基于文件名关键词的标签
    filename_lower = filename.lower()
    keyword_map = {
        '云': ['云纹', '祥云'],
        '龙': ['龙纹', '图腾'],
        '花': ['花卉', '植物'],
        '鸟': ['鸟类', '凤凰'],
        '鱼': ['鱼纹', '年年有余'],
        '回': ['回纹', '几何'],
        '缠枝': ['缠枝', '藤蔓'],
        '蝴蝶': ['蝴蝶', '爱情'],
        '万字': ['万字', '吉祥'],
    }
    for kw, kw_tags in keyword_map.items():
        if kw in filename_lower:
            tags.extend(kw_tags)
    
    # 添加通用标签
    tags.extend(['传统纹样', '民族文化', '设计素材'])
    
    # 去重并限制数量
    unique_tags = list(dict.fromkeys(tags))[:8]
    return ','.join(unique_tags)


def ai_rate_product(product_name, base_design='', applicable_craft='', user_prefs=None):
    """模拟AI六维度智能评级"""
    # 基础分（60-85分随机）
    base_scores = {
        'innovation': random.uniform(65, 90),
        'history': random.uniform(60, 88),
        'art': random.uniform(68, 92),
        'practical': random.uniform(62, 85),
        'culture': random.uniform(70, 95),
        'craft': random.uniform(60, 88),
    }
    
    # 根据设计名称关键词调整分数
    name_lower = product_name.lower()
    if '创新' in name_lower or '现代' in name_lower:
        base_scores['innovation'] += 5
    if '传统' in name_lower or '古' in name_lower:
        base_scores['history'] += 5
    if '艺术' in name_lower or '精美' in name_lower:
        base_scores['art'] += 5
    if '实用' in name_lower or '日用' in name_lower:
        base_scores['practical'] += 5
    if '文化' in name_lower or '非遗' in name_lower:
        base_scores['culture'] += 5
    if '复杂' in name_lower or '精细' in name_lower:
        base_scores['craft'] += 5
    
    # 应用用户偏好权重
    if user_prefs:
        weights = {
            'innovation': user_prefs.weight_innovation,
            'history': user_prefs.weight_history,
            'art': user_prefs.weight_art,
            'practical': user_prefs.weight_practical,
            'culture': user_prefs.weight_culture,
            'craft': user_prefs.weight_craft,
        }
    else:
        weights = {k: 1.0 for k in base_scores}
    
    # 计算加权总分
    total_weight = sum(weights.values())
    weighted_sum = sum(base_scores[k] * weights[k] for k in base_scores)
    total_score = round(weighted_sum / total_weight, 1)
    
    # 限制分数范围
    for k in base_scores:
        base_scores[k] = round(min(100, max(0, base_scores[k])), 1)
    
    # 确定市场等级
    if total_score >= 90:
        market_level = 'S级'
    elif total_score >= 80:
        market_level = 'A级'
    elif total_score >= 70:
        market_level = 'B级'
    else:
        market_level = 'C级'
    
    return {
        'innovation': base_scores['innovation'],
        'history': base_scores['history'],
        'art': base_scores['art'],
        'practical': base_scores['practical'],
        'culture': base_scores['culture'],
        'craft': base_scores['craft'],
        'total': total_score,
        'market_level': market_level,
    }


def update_user_preferences(user_id, keyword=None, style=None):
    """更新用户偏好：记录搜索关键词和风格，动态调整权重"""
    prefs = UserPreference.query.filter_by(user_id=user_id).first()
    if not prefs:
        prefs = UserPreference(user_id=user_id)
        db.session.add(prefs)
    
    # 更新搜索关键词
    if keyword:
        keywords = [k.strip() for k in prefs.search_keywords.split(',') if k.strip()] if prefs.search_keywords else []
        if keyword not in keywords:
            keywords.append(keyword)
        # 只保留最近20个关键词
        keywords = keywords[-20:]
        prefs.search_keywords = ','.join(keywords)
        prefs.total_searches += 1
    
    # 更新偏好风格
    if style:
        styles = [s.strip() for s in prefs.preferred_styles.split(',') if s.strip()] if prefs.preferred_styles else []
        if style not in styles:
            styles.append(style)
        styles = styles[-10:]
        prefs.preferred_styles = ','.join(styles)
        prefs.total_designs += 1
    
    # 根据搜索记录动态调整权重（模拟偏好学习）
    total_actions = prefs.total_searches + prefs.total_designs
    if total_actions > 5:
        # 搜索关键词包含"创新"、"现代" → 提高创新性权重
        if '创新' in prefs.search_keywords or '现代' in prefs.search_keywords:
            prefs.weight_innovation = min(2.0, prefs.weight_innovation + 0.1)
        # 搜索关键词包含"传统"、"历史" → 提高历史性权重
        if '传统' in prefs.search_keywords or '历史' in prefs.search_keywords:
            prefs.weight_history = min(2.0, prefs.weight_history + 0.1)
        # 搜索关键词包含"艺术"、"美观" → 提高艺术性权重
        if '艺术' in prefs.search_keywords or '美观' in prefs.search_keywords:
            prefs.weight_art = min(2.0, prefs.weight_art + 0.1)
        # 搜索关键词包含"实用" → 提高实用性权重
        if '实用' in prefs.search_keywords:
            prefs.weight_practical = min(2.0, prefs.weight_practical + 0.1)
        # 搜索关键词包含"文化"、"非遗" → 提高文化价值权重
        if '文化' in prefs.search_keywords or '非遗' in prefs.search_keywords:
            prefs.weight_culture = min(2.0, prefs.weight_culture + 0.1)
        # 搜索关键词包含"工艺"、"技法" → 提高工艺难度权重
        if '工艺' in prefs.search_keywords or '技法' in prefs.search_keywords:
            prefs.weight_craft = min(2.0, prefs.weight_craft + 0.1)
        
        # 更新偏好等级
        if total_actions > 50:
            prefs.preference_level = '深度定制'
        elif total_actions > 30:
            prefs.preference_level = '高级'
        elif total_actions > 15:
            prefs.preference_level = '中级'
    
    prefs.updated_at = datetime.utcnow()
    db.session.commit()
    return prefs


# ==================== 首页 ====================
@design_bp.route('/')
@login_required
def index():
    stats = {
        'process_count': CraftProcess.query.count(),
        'scheme_count': ProductScheme.query.count(),
        'course_count': TeachingCourse.query.count(),
        'material_count': PatternMaterial.query.count(),
        'trend_count': DesignTrend.query.count(),
        'order_count': CustomOrder.query.count(),
        'copyright_count': CopyrightRegistration.query.count(),
        'inheritor_count': HeritageInheritor.query.count(),
    }
    recent_schemes = ProductScheme.query.order_by(ProductScheme.created_at.desc()).limit(6).all()
    recent_processes = CraftProcess.query.order_by(CraftProcess.created_at.desc()).limit(4).all()
    return render_with_theme('design_system/index.html', stats=stats,
                           recent_schemes=recent_schemes, recent_processes=recent_processes)


# ==================== 传统工艺适配管理 ====================
@design_bp.route('/craft-processes')
@login_required
def craft_processes():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = CraftProcess.query
    if search:
        query = query.filter(CraftProcess.process_name.contains(search))
    pagination = query.order_by(CraftProcess.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/craft_processes.html',
                           processes=pagination.items, pagination=pagination, search=search)


@design_bp.route('/craft-processes/add', methods=['POST'])
@login_required
def add_craft_process():
    p = CraftProcess(
        process_id=request.form.get('process_id'),
        process_name=request.form.get('process_name'),
        process_type=request.form.get('process_type'),
        applicable_material=request.form.get('applicable_material'),
        difficulty=request.form.get('difficulty'),
        estimated_time=request.form.get('estimated_time'),
        tool_requirements=request.form.get('tool_requirements'),
        description=request.form.get('description'),
        status=request.form.get('status', '可用'),
        heritage_region=request.form.get('heritage_region'),
        cultural_level=request.form.get('cultural_level')
    )
    db.session.add(p)
    db.session.commit()
    flash('传统工艺添加成功', 'success')
    return redirect(url_for('design.craft_processes'))


@design_bp.route('/craft-processes/<int:id>/edit', methods=['POST'])
@login_required
def edit_craft_process(id):
    p = CraftProcess.query.get_or_404(id)
    p.process_name = request.form.get('process_name')
    p.process_type = request.form.get('process_type')
    p.applicable_material = request.form.get('applicable_material')
    p.difficulty = request.form.get('difficulty')
    p.estimated_time = request.form.get('estimated_time')
    p.status = request.form.get('status')
    p.heritage_region = request.form.get('heritage_region')
    p.cultural_level = request.form.get('cultural_level')
    db.session.commit()
    flash('传统工艺更新成功', 'success')
    return redirect(url_for('design.craft_processes'))


# ==================== 手工艺品方案管理 ====================
@design_bp.route('/product-schemes')
@login_required
def product_schemes():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = ProductScheme.query
    if search:
        query = query.filter(ProductScheme.product_name.contains(search))
    pagination = query.order_by(ProductScheme.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/product_schemes.html',
                           schemes=pagination.items, pagination=pagination, search=search)


@design_bp.route('/product-schemes/add', methods=['POST'])
@login_required
def add_product_scheme():
    s = ProductScheme(
        product_id=request.form.get('product_id'),
        product_name=request.form.get('product_name'),
        base_design=request.form.get('base_design'),
        applicable_craft=request.form.get('applicable_craft'),
        material_list=request.form.get('material_list'),
        production_process=request.form.get('production_process'),
        cost_budget=request.form.get('cost_budget'),
        suggested_price=request.form.get('suggested_price'),
        status=request.form.get('status', '设计中'),
        cultural_value=request.form.get('cultural_value'),
        product_size=request.form.get('product_size'),
        product_weight=request.form.get('product_weight')
    )
    db.session.add(s)
    db.session.commit()
    flash('产品方案添加成功', 'success')
    return redirect(url_for('design.product_schemes'))


@design_bp.route('/product-schemes/<int:id>/edit', methods=['POST'])
@login_required
def edit_product_scheme(id):
    s = ProductScheme.query.get_or_404(id)
    s.product_name = request.form.get('product_name')
    s.base_design = request.form.get('base_design')
    s.status = request.form.get('status')
    s.cost_budget = request.form.get('cost_budget')
    s.suggested_price = request.form.get('suggested_price')
    db.session.commit()
    flash('产品方案更新成功', 'success')
    return redirect(url_for('design.product_schemes'))


# AI智能评级
@design_bp.route('/product-schemes/<int:id>/ai-rate')
@login_required
def ai_rate_scheme(id):
    scheme = ProductScheme.query.get_or_404(id)
    
    # 获取用户偏好
    user_prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    
    # AI评分
    ratings = ai_rate_product(
        scheme.product_name, 
        scheme.base_design or '', 
        scheme.applicable_craft or '',
        user_prefs
    )
    
    # 更新方案评分
    scheme.innovation_score = ratings['innovation']
    scheme.history_score = ratings['history']
    scheme.art_score = ratings['art']
    scheme.practical_score = ratings['practical']
    scheme.culture_score = ratings['culture']
    scheme.craft_score = ratings['craft']
    scheme.total_score = ratings['total']
    scheme.market_level = ratings['market_level']
    scheme.is_ai_rated = True
    
    db.session.commit()
    
    # 记录用户创作偏好
    update_user_preferences(current_user.id, style=scheme.base_design)
    
    flash(f'AI评级完成！综合分：{ratings["total"]}分，市场等级：{ratings["market_level"]}', 'success')
    return redirect(url_for('design.product_schemes'))


# 批量AI评级
@design_bp.route('/product-schemes/batch-rate')
@login_required
def batch_rate_schemes():
    schemes = ProductScheme.query.filter_by(is_ai_rated=False).all()
    user_prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    
    count = 0
    for scheme in schemes:
        ratings = ai_rate_product(scheme.product_name, scheme.base_design or '', scheme.applicable_craft or '', user_prefs)
        scheme.innovation_score = ratings['innovation']
        scheme.history_score = ratings['history']
        scheme.art_score = ratings['art']
        scheme.practical_score = ratings['practical']
        scheme.culture_score = ratings['culture']
        scheme.craft_score = ratings['craft']
        scheme.total_score = ratings['total']
        scheme.market_level = ratings['market_level']
        scheme.is_ai_rated = True
        count += 1
    
    db.session.commit()
    flash(f'批量评级完成，共处理 {count} 个方案', 'success')
    return redirect(url_for('design.product_schemes'))


# ==================== 耗材计算 ====================
@design_bp.route('/material-calc')
@login_required
def material_calc():
    processes = CraftProcess.query.all()
    return render_with_theme('design_system/material_calc.html', processes=processes)


# ==================== 趋势预测 ====================
@design_bp.route('/trend-forecast')
@login_required
def trend_forecast():
    trends = DesignTrend.query.all()
    return render_with_theme('design_system/trend_forecast.html', trends=trends)


# ==================== 需求洞察 ====================
@design_bp.route('/demand-insight')
@login_required
def demand_insight():
    return render_with_theme('design_system/demand_insight.html')


# ==================== 设计趋势分析管理 ====================
@design_bp.route('/design-trends')
@login_required
def design_trends():
    page = request.args.get('page', 1, type=int)
    pagination = DesignTrend.query.order_by(DesignTrend.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/design_trends.html', trends=pagination.items, pagination=pagination)


@design_bp.route('/design-trends/add', methods=['POST'])
@login_required
def add_design_trend():
    t = DesignTrend(
        analysis_id=request.form.get('analysis_id'),
        analysis_dimension=request.form.get('analysis_dimension'),
        time_range=request.form.get('time_range'),
        popular_materials=request.form.get('popular_materials'),
        popular_crafts=request.form.get('popular_crafts'),
        color_trend=request.form.get('color_trend'),
        cultural_heat=request.form.get('cultural_heat')
    )
    db.session.add(t)
    db.session.commit()
    flash('设计趋势分析添加成功', 'success')
    return redirect(url_for('design.design_trends'))


# ==================== 非遗传承人管理 ====================
@design_bp.route('/inheritors')
@login_required
def inheritors():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = HeritageInheritor.query
    if search:
        query = query.filter(HeritageInheritor.name.contains(search))
    pagination = query.order_by(HeritageInheritor.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/inheritors.html', inheritors=pagination.items, pagination=pagination, search=search)


@design_bp.route('/inheritors/add', methods=['POST'])
@login_required
def add_inheritor():
    inh = HeritageInheritor(
        inheritor_id=request.form.get('inheritor_id'),
        name=request.form.get('name'),
        skill_category=request.form.get('skill_category'),
        heritage_level=request.form.get('heritage_level'),
        region=request.form.get('region'),
        representative_works=request.form.get('representative_works'),
        contact=request.form.get('contact')
    )
    db.session.add(inh)
    db.session.commit()
    flash('传承人添加成功', 'success')
    return redirect(url_for('design.inheritors'))


@design_bp.route('/inheritors/<int:id>/edit', methods=['POST'])
@login_required
def edit_inheritor(id):
    inh = HeritageInheritor.query.get_or_404(id)
    inh.name = request.form.get('name')
    inh.skill_category = request.form.get('skill_category')
    inh.heritage_level = request.form.get('heritage_level')
    inh.region = request.form.get('region')
    inh.representative_works = request.form.get('representative_works')
    inh.contact = request.form.get('contact')
    db.session.commit()
    flash('传承人更新成功', 'success')
    return redirect(url_for('design.inheritors'))


# ==================== 民族文化知识管理 ====================
@design_bp.route('/cultural-knowledge')
@login_required
def cultural_knowledge():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = CulturalKnowledge.query
    if search:
        query = query.filter(
            (CulturalKnowledge.title.contains(search)) |
            (CulturalKnowledge.category.contains(search))
        )
    pagination = query.order_by(CulturalKnowledge.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/cultural_knowledge.html', knowledge=pagination.items, pagination=pagination, search=search)


@design_bp.route('/cultural-knowledge/add', methods=['POST'])
@login_required
def add_cultural_knowledge():
    k = CulturalKnowledge(
        knowledge_id=request.form.get('knowledge_id'),
        title=request.form.get('title'),
        category=request.form.get('category'),
        ethnic_group=request.form.get('ethnic_group'),
        content=request.form.get('content'),
        source=request.form.get('source')
    )
    db.session.add(k)
    db.session.commit()
    flash('文化知识添加成功', 'success')
    return redirect(url_for('design.cultural_knowledge'))


@design_bp.route('/cultural-knowledge/<int:id>/edit', methods=['POST'])
@login_required
def edit_cultural_knowledge(id):
    k = CulturalKnowledge.query.get_or_404(id)
    k.title = request.form.get('title')
    k.category = request.form.get('category')
    k.ethnic_group = request.form.get('ethnic_group')
    k.content = request.form.get('content')
    k.source = request.form.get('source')
    db.session.commit()
    flash('文化知识更新成功', 'success')
    return redirect(url_for('design.cultural_knowledge'))


# ==================== 工艺教学课程管理 ====================
@design_bp.route('/teaching-courses')
@login_required
def teaching_courses():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = TeachingCourse.query
    if search:
        query = query.filter(TeachingCourse.course_name.contains(search))
    pagination = query.order_by(TeachingCourse.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/teaching_courses.html', courses=pagination.items, pagination=pagination, search=search)


@design_bp.route('/teaching-courses/add', methods=['POST'])
@login_required
def add_teaching_course():
    c = TeachingCourse(
        course_id=request.form.get('course_id'),
        course_name=request.form.get('course_name'),
        instructor=request.form.get('instructor'),
        craft_type=request.form.get('craft_type'),
        duration=request.form.get('duration'),
        difficulty=request.form.get('difficulty'),
        description=request.form.get('description'),
        status=request.form.get('status', '已发布')
    )
    db.session.add(c)
    db.session.commit()
    flash('课程添加成功', 'success')
    return redirect(url_for('design.teaching_courses'))


@design_bp.route('/teaching-courses/<int:id>/edit', methods=['POST'])
@login_required
def edit_teaching_course(id):
    c = TeachingCourse.query.get_or_404(id)
    c.course_name = request.form.get('course_name')
    c.instructor = request.form.get('instructor')
    c.craft_type = request.form.get('craft_type')
    c.duration = request.form.get('duration')
    c.difficulty = request.form.get('difficulty')
    c.description = request.form.get('description')
    c.status = request.form.get('status')
    db.session.commit()
    flash('课程更新成功', 'success')
    return redirect(url_for('design.teaching_courses'))


# ==================== 纹样生成 ====================
@design_bp.route('/pattern-generator')
@login_required
def pattern_generator():
    materials = PatternMaterial.query.all()
    return render_with_theme('design_system/pattern_generator.html', materials=materials)


# ==================== 智能生成设计管理 ====================
@design_bp.route('/smart-design', methods=['GET', 'POST'])
@login_required
def smart_design():
    design_result = None
    
    if request.method == 'POST':
        ethnic = request.form.get('ethnic', '多民族融合')
        style = request.form.get('style', '传统风格')
        usage = request.form.get('usage', '文创产品')
        color_pref = request.form.get('color_pref', '传统民族配色')
        main_color = request.form.get('main_color', '#26A69A')
        elements = request.form.get('elements', '')
        
        # 民族文化元素库
        ethnic_elements = {
            '壮族': ['铜鼓纹', '蛙纹', '云雷纹', '壮锦几何纹', '花山崖画', '绣球纹', '稻穗纹'],
            '苗族': ['蝴蝶妈妈', '蜡染纹', '银饰纹', '百鸟衣纹', '牛角纹', '苗绣图案', '鼓藏纹'],
            '藏族': ['八吉祥', '祥云纹', '藏八宝', '法轮纹', '莲花纹', '牦牛角', '唐卡纹样'],
            '彝族': ['虎纹', '火纹', '太阳纹', '漆器纹样', '披毡纹', '图腾柱', '三色纹'],
            '侗族': ['鼓楼纹', '风雨桥纹', '侗锦图案', '银饰纹', '稻作纹', '萨玛纹'],
            '蒙古族': ['云纹', '盘肠纹', '卷草纹', '马鞍纹', '搏克服饰', '蒙古包纹'],
            '维吾尔族': ['石榴花', '巴旦木纹', '几何纹样', '地毯图案', '艾德莱斯绸', '彩陶纹'],
            '汉族': ['云纹', '回纹', '缠枝纹', '龙凤纹', '如意纹', '祥云', '万字纹'],
            '回族': ['几何纹', '卷草纹', '阿拉伯纹样', '清真纹样', '花卉图案'],
            '白族': ['扎染纹', '三塔纹', '白族刺绣', '莲花纹', '鱼纹'],
            '傣族': ['孔雀纹', '象纹', '泼水节纹', '佛塔纹', '傣锦图案']
        }
        
        # 民族传统配色
        ethnic_colors = {
            '壮族': ['#1E3A5F', '#C41E3A', '#F5C79A', '#2E7D32'],
            '苗族': ['#1565C0', '#C62828', '#FFB300', '#2E7D32'],
            '藏族': ['#C62828', '#F9A825', '#1565C0', '#FFFFFF'],
            '彝族': ['#212121', '#D32F2F', '#FBC02D', '#FFFFFF'],
            '侗族': ['#1B5E20', '#F57F17', '#0D47A1', '#E65100'],
            '蒙古族': ['#0D47A1', '#C62828', '#FFD54F', '#2E7D32'],
            '维吾尔族': ['#B71C1C', '#F9A825', '#1B5E20', '#6A1B9A'],
            '汉族': ['#8B0000', '#DAA520', '#2F4F4F', '#F5F5DC'],
            '回族': ['#006400', '#B8860B', '#8B0000', '#FFFFFF'],
            '白族': ['#4169E1', '#FF6347', '#FFD700', '#228B22'],
            '傣族': ['#20B2AA', '#FF69B4', '#FFD700', '#9370DB']
        }
        
        # 风格化配色
        style_colors = {
            '暖色调': ['#D32F2F', '#F57C00', '#FBC02D', '#E64A19'],
            '冷色调': ['#1976D2', '#0097A7', '#7B1FA2', '#388E3C'],
            '高饱和': ['#F44336', '#E91E63', '#9C27B0', '#2196F3'],
            '低饱和': ['#90A4AE', '#A1887F', '#80CBC4', '#CE93D8'],
            '现代简约配色': ['#2D3436', '#636E72', '#B2BEC3', '#DFE6E9'],
            '黑白灰': ['#212121', '#616161', '#9E9E9E', '#F5F5F5'],
            '莫兰迪': ['#B5A89A', '#A6B1B8', '#C9B8A8', '#9AA8A6']
        }
        
        # 风格设计建议
        style_suggestions = {
            '传统风格': '保留传统纹样的原始形态和完整构图，注重细节还原，体现原汁原味的民族文化特色',
            '简约': '简化传统纹样的复杂细节，保留核心识别元素，线条简洁，留白充足',
            '复古': '融入年代感设计元素，使用做旧质感的色彩和纹理，营造怀旧氛围',
            '怀旧': '以经典传统纹样为基础，加入复古色调和质感，唤起文化记忆与情感共鸣',
            '极简主义': '极致简化纹样形态，用最少的线条表达最核心的文化符号，追求少即是多',
            '现代时尚': '传统纹样与现代设计语言融合，采用潮流配色和构图，符合当代审美',
            '国潮': '传统文化元素与现代街头潮流碰撞，大胆撞色，视觉冲击力强，彰显文化自信',
            '抽象化': '将传统纹样解构重组，以抽象艺术形式表达文化内涵，更具艺术表现力'
        }
        
        # 场景设计建议
        usage_suggestions = {
            '民族服饰': '注重纹样的延展性和对称性，适合在领口、袖口、裙摆等部位重点装饰',
            '裙子': '裙摆部位适合大面积连续纹样，腰头可设计重点装饰纹样，注意上下呼应',
            '上衣': '前胸、后背、袖口为重点装饰区域，纹样大小适中，避免过于繁复',
            '配饰': '纹样精致小巧，细节丰富，适合在耳环、项链、腰带等配饰上点缀',
            '文创产品': '适当简化传统纹样，兼顾文化辨识度和量产可行性，注重实用性',
            '品牌标识': '提炼最具代表性的文化符号，高度概括，确保小尺寸下的识别度',
            '海报图案': '可使用较大面积的完整纹样作为背景或主体，视觉冲击力强',
            '包装纹样': '纹样需考虑重复排列效果，边缘衔接自然，适合批量印刷',
            '纺织品图案': '注重纹样的连续循环性，四方连续构图，适合印染和织造',
            '刺绣图案': '考虑刺绣工艺可行性，线条流畅，色块分明，便于针法表达',
            '家居软装': '配色柔和舒适，纹样不宜过于繁复，营造温馨居家氛围'
        }
        
        # 生成配色方案
        if color_pref == '传统民族配色':
            colors = ethnic_colors.get(ethnic, ['#8B0000', '#DAA520', '#2F4F4F', '#CD853F'])
        else:
            colors = style_colors.get(color_pref, ['#8B0000', '#DAA520', '#2F4F4F', '#CD853F'])
        
        # 生成设计建议
        suggestions = []
        if ethnic in ethnic_elements:
            elem_list = ethnic_elements[ethnic]
            suggestions.append(f'融入{ethnic}典型文化元素：{"、".join(elem_list[:4])}等，确保文化符号的准确表达')
        if ethnic == '多民族融合':
            suggestions.append('融合多民族纹样元素，注重不同文化符号之间的和谐统一，避免生硬拼凑')
        if style in style_suggestions:
            suggestions.append(style_suggestions[style])
        if usage in usage_suggestions:
            suggestions.append(usage_suggestions[usage])
        if elements and elements.strip():
            suggestions.append(f'已融入指定文化元素：{elements}，建议作为主体纹样重点突出展示')
        suggestions.append('尊重非遗文化内涵，准确理解纹样寓意，避免误用或随意改造文化符号')
        
        # 文化元素解析
        cultural_elements = []
        if ethnic in ethnic_elements:
            cultural_elements.extend(ethnic_elements[ethnic][:5])
        if elements and elements.strip():
            user_elems = [e.strip() for e in elements.replace('，', '、').replace(',', '、').split('、') if e.strip()]
            for elem in user_elems:
                if elem not in cultural_elements:
                    cultural_elements.append(elem)
        cultural_elements = cultural_elements[:8]
        
        # 预览图映射
        preview_map = {
            '苗族': ['design_previews/miao_batik.jpg'],
            '藏族': ['design_previews/tibetan_cloud.jpg'],
            '壮族': ['design_previews/zhuang_drum.jpg'],
            '彝族': ['design_previews/zhuang_drum.jpg'],
            '侗族': ['design_previews/miao_batik.jpg'],
            '蒙古族': ['design_previews/tibetan_cloud.jpg'],
            '维吾尔族': ['design_previews/zhuang_drum.jpg'],
            '汉族': ['design_previews/guochao_dragon.jpg'],
            '多民族融合': ['design_previews/guochao_dragon.jpg', 'design_previews/miao_batik.jpg', 'design_previews/tibetan_cloud.jpg', 'design_previews/zhuang_drum.jpg'],
        }
        preview_images = preview_map.get(ethnic, ['design_previews/guochao_dragon.jpg'])
        if style == '国潮':
            preview_images = ['design_previews/guochao_dragon.jpg'] + preview_images
        preview_images = [f'/static/{img}' for img in preview_images[:4]]
        
        # 参考纹样
        from models import Pattern
        related_patterns = Pattern.query.filter(
            Pattern.origin.like(f'%{ethnic}%')
        ).limit(4).all()
        if not related_patterns:
            related_patterns = Pattern.query.limit(4).all()
        
        design_result = {
            'ethnic': ethnic,
            'style': style,
            'usage': usage,
            'color_pref': color_pref,
            'main_color': main_color,
            'colors': colors,
            'suggestions': suggestions,
            'cultural_elements': cultural_elements,
            'design_name': f'{ethnic}风{style}纹样设计',
            'preview_images': preview_images,
            'related_patterns': related_patterns
        }
    
    schemes = ProductScheme.query.all()
    return render_with_theme('design_system/smart_design.html', 
                           schemes=schemes,
                           design_result=design_result)


# ==================== 设计效能 ====================
@design_bp.route('/design-efficiency')
@login_required
def design_efficiency():
    return render_with_theme('design_system/design_efficiency.html')


# ==================== 定制订单跟踪管理 ====================
@design_bp.route('/custom-orders')
@login_required
def custom_orders():
    page = request.args.get('page', 1, type=int)
    pagination = CustomOrder.query.order_by(CustomOrder.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/custom_orders.html', orders=pagination.items, pagination=pagination)


@design_bp.route('/custom-orders/add', methods=['POST'])
@login_required
def add_custom_order():
    o = CustomOrder(
        order_id=request.form.get('order_id'),
        customer_name=request.form.get('customer_name'),
        product_type=request.form.get('product_type'),
        design_requirements=request.form.get('design_requirements'),
        order_date=request.form.get('order_date'),
        deadline=request.form.get('deadline'),
        status=request.form.get('status', '待确认')
    )
    db.session.add(o)
    db.session.commit()
    flash('定制订单添加成功', 'success')
    return redirect(url_for('design.custom_orders'))


# ==================== 民族图案素材管理 ====================
@design_bp.route('/pattern-materials')
@login_required
def pattern_materials():
    page = request.args.get('page', 1, type=int)
    tag = request.args.get('tag', '')
    search = request.args.get('search', '')
    
    query = PatternMaterial.query
    if tag:
        query = query.filter(PatternMaterial.tags.contains(tag))
        # 记录用户搜索偏好
        update_user_preferences(current_user.id, keyword=tag)
    if search:
        query = query.filter(
            (PatternMaterial.material_name.contains(search)) |
            (PatternMaterial.tags.contains(search))
        )
        update_user_preferences(current_user.id, keyword=search)
    
    pagination = query.order_by(PatternMaterial.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    
    # 收集所有标签用于筛选
    all_materials = PatternMaterial.query.all()
    all_tags = set()
    for m in all_materials:
        if m.tags:
            all_tags.update([t.strip() for t in m.tags.split(',') if t.strip()])
    
    return render_with_theme('design_system/pattern_materials.html', 
                           materials=pagination.items, 
                           pagination=pagination,
                           all_tags=sorted(list(all_tags)),
                           current_tag=tag,
                           search=search)


# 上传素材
@design_bp.route('/pattern-materials/upload', methods=['POST'])
@login_required
def upload_material():
    if 'file' not in request.files:
        flash('请选择要上传的文件', 'error')
        return redirect(url_for('design.pattern_materials'))
    
    file = request.files['file']
    if file.filename == '':
        flash('未选择文件', 'error')
        return redirect(url_for('design.pattern_materials'))
    
    if not allowed_file(file.filename):
        flash('不支持的文件格式，支持：PNG、JPG、GIF、SVG等', 'error')
        return redirect(url_for('design.pattern_materials'))
    
    # 保存文件
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    save_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, save_filename)
    file.save(filepath)
    
    # 获取表单信息
    material_id = request.form.get('material_id', f'MAT{timestamp}')
    material_name = request.form.get('material_name', filename.rsplit('.', 1)[0])
    pattern_type = request.form.get('pattern_type', '')
    ethnic_origin = request.form.get('ethnic_origin', '')
    
    # AI自动标签化
    auto_tags = auto_tag_material(material_name, pattern_type, ethnic_origin)
    
    # 创建素材记录
    material = PatternMaterial(
        material_id=material_id,
        material_name=material_name,
        pattern_type=pattern_type,
        ethnic_origin=ethnic_origin,
        image_path=f'/uploads/{save_filename}',
        file_path=filepath,
        file_type=file.content_type,
        copyright_status='待审核',
        tags=auto_tags,
        auto_tagged=True,
        uploader=current_user.username if hasattr(current_user, 'username') else 'admin'
    )
    db.session.add(material)
    db.session.commit()
    
    flash(f'素材上传成功，AI已自动生成标签：{auto_tags}', 'success')
    return redirect(url_for('design.pattern_materials'))


# 重新生成标签
@design_bp.route('/pattern-materials/<int:id>/retag')
@login_required
def retag_material(id):
    material = PatternMaterial.query.get_or_404(id)
    new_tags = auto_tag_material(material.material_name, material.pattern_type, material.ethnic_origin)
    material.tags = new_tags
    material.auto_tagged = True
    db.session.commit()
    flash(f'标签已重新生成：{new_tags}', 'success')
    return redirect(url_for('design.pattern_materials'))


# ==================== 数字版权登记管理 ====================
@design_bp.route('/copyrights')
@login_required
def copyrights():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = CopyrightRegistration.query
    if search:
        query = query.filter(
            (CopyrightRegistration.work_name.contains(search)) |
            (CopyrightRegistration.author.contains(search))
        )
    pagination = query.order_by(CopyrightRegistration.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_with_theme('design_system/copyrights.html', copyrights=pagination.items, pagination=pagination, search=search)


@design_bp.route('/copyrights/add', methods=['POST'])
@login_required
def add_copyright():
    c = CopyrightRegistration(
        registration_id=request.form.get('registration_id'),
        work_name=request.form.get('work_name'),
        author=request.form.get('author'),
        work_type=request.form.get('work_type'),
        registration_date=request.form.get('registration_date'),
        copyright_number=request.form.get('copyright_number'),
        status=request.form.get('status', '登记中')
    )
    db.session.add(c)
    db.session.commit()
    flash('版权登记添加成功', 'success')
    return redirect(url_for('design.copyrights'))


@design_bp.route('/copyrights/<int:id>/edit', methods=['POST'])
@login_required
def edit_copyright(id):
    c = CopyrightRegistration.query.get_or_404(id)
    c.work_name = request.form.get('work_name')
    c.author = request.form.get('author')
    c.work_type = request.form.get('work_type')
    c.registration_date = request.form.get('registration_date')
    c.copyright_number = request.form.get('copyright_number')
    c.status = request.form.get('status')
    db.session.commit()
    flash('版权登记更新成功', 'success')
    return redirect(url_for('design.copyrights'))


# ==================== 用户偏好自适应调控 ====================

@design_bp.route('/preferences')
@login_required
def user_preferences():
    prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    if not prefs:
        prefs = UserPreference(user_id=current_user.id)
        db.session.add(prefs)
        db.session.commit()
    
    keywords = [k for k in prefs.search_keywords.split(',') if k.strip()] if prefs.search_keywords else []
    styles = [s for s in prefs.preferred_styles.split(',') if s.strip()] if prefs.preferred_styles else []
    
    return render_with_theme('design_system/preferences.html',
                           prefs=prefs,
                           keywords=keywords,
                           styles=styles)


# 更新偏好权重
@design_bp.route('/preferences/update', methods=['POST'])
@login_required
def update_preferences():
    prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    if not prefs:
        prefs = UserPreference(user_id=current_user.id)
        db.session.add(prefs)
    
    prefs.weight_innovation = float(request.form.get('weight_innovation', 1.0))
    prefs.weight_history = float(request.form.get('weight_history', 1.0))
    prefs.weight_art = float(request.form.get('weight_art', 1.0))
    prefs.weight_practical = float(request.form.get('weight_practical', 1.0))
    prefs.weight_culture = float(request.form.get('weight_culture', 1.0))
    prefs.weight_craft = float(request.form.get('weight_craft', 1.0))
    
    prefs.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('偏好权重已更新，AI评级和创作将自动适配您的偏好', 'success')
    return redirect(url_for('design.user_preferences'))


# 重置偏好
@design_bp.route('/preferences/reset')
@login_required
def reset_preferences():
    prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    if prefs:
        prefs.weight_innovation = 1.0
        prefs.weight_history = 1.0
        prefs.weight_art = 1.0
        prefs.weight_practical = 1.0
        prefs.weight_culture = 1.0
        prefs.weight_craft = 1.0
        prefs.search_keywords = ''
        prefs.preferred_styles = ''
        prefs.total_searches = 0
        prefs.total_designs = 0
        prefs.preference_level = '初级'
        prefs.updated_at = datetime.utcnow()
        db.session.commit()
    
    flash('偏好已重置为默认值', 'success')
    return redirect(url_for('design.user_preferences'))

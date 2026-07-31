from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models import db, CulturalGene, PatternAnalysis, GeneFeature, GeneClassification
from models import CulturalDesign, HandicraftCollection, HeritageInterview

gene_bp = Blueprint('gene', __name__)

SYSTEM_NAME = '文化基因智能识别系统'
THEME_COLOR = '#0277BD'
THEME_COLOR_LIGHT = '#4FC3F7'


def render_with_theme(template, **kwargs):
    return render_template(template,
                         system_name=SYSTEM_NAME,
                         theme_color=THEME_COLOR,
                         theme_color_light=THEME_COLOR_LIGHT,
                         system_type='gene',
                         **kwargs)


# ==================== 首页 ====================
@gene_bp.route('/')
@login_required
def index():
    gene_count = CulturalGene.query.count()
    feature_count = GeneFeature.query.count()
    design_count = CulturalDesign.query.count()
    collection_count = HandicraftCollection.query.count()
    
    stats = {
        'gene_count': gene_count,
        'feature_count': feature_count,
        'design_count': design_count,
        'collection_count': collection_count,
        'classification_count': GeneClassification.query.count(),
        'interview_count': HeritageInterview.query.count(),
        'analysis_count': PatternAnalysis.query.count(),
    }
    
    recent_genes = CulturalGene.query.order_by(CulturalGene.created_at.desc()).limit(5).all()
    recent_designs = CulturalDesign.query.order_by(CulturalDesign.created_at.desc()).limit(5).all()
    
    return render_with_theme('gene_system/index.html',
                           stats=stats,
                           recent_genes=recent_genes,
                           recent_designs=recent_designs)


# ==================== 智能融合设计 ====================
@gene_bp.route('/fusion-design')
@login_required
def fusion_design():
    genes = CulturalGene.query.filter_by(status='已审核').all()
    return render_with_theme('gene_system/fusion_design.html', genes=genes)


# ==================== 纹样智能解析 ====================
@gene_bp.route('/pattern-analysis')
@login_required
def pattern_analysis():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = PatternAnalysis.query.order_by(PatternAnalysis.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('gene_system/pattern_analysis.html',
                           analyses=pagination.items,
                           pagination=pagination)


@gene_bp.route('/pattern-analysis/add', methods=['POST'])
@login_required
def add_pattern_analysis():
    analysis = PatternAnalysis(
        analysis_id=request.form.get('analysis_id'),
        pattern_name=request.form.get('pattern_name'),
        color_scheme=request.form.get('color_scheme'),
        structure=request.form.get('structure'),
        status=request.form.get('status', '解析中')
    )
    db.session.add(analysis)
    db.session.commit()
    flash('纹样解析任务创建成功', 'success')
    return redirect(url_for('gene.pattern_analysis'))


# ==================== 文创设计辅助管理 ====================
@gene_bp.route('/designs')
@login_required
def designs():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = CulturalDesign.query
    if search:
        query = query.filter(
            (CulturalDesign.designer.contains(search)) |
            (CulturalDesign.theme.contains(search))
        )
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(CulturalDesign.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('gene_system/designs.html',
                           designs=pagination.items,
                           pagination=pagination,
                           search=search,
                           current_status=status)


@gene_bp.route('/designs/add', methods=['POST'])
@login_required
def add_design():
    design = CulturalDesign(
        design_id=request.form.get('design_id'),
        designer=request.form.get('designer'),
        design_date=request.form.get('design_date'),
        theme=request.form.get('theme'),
        reference_gene=request.form.get('reference_gene'),
        sketch=request.form.get('sketch'),
        description=request.form.get('description'),
        cultural_elements=request.form.get('cultural_elements'),
        status=request.form.get('status', '进行中'),
        review_opinion=request.form.get('review_opinion', '')
    )
    db.session.add(design)
    db.session.commit()
    flash('文创设计添加成功', 'success')
    return redirect(url_for('gene.designs'))


@gene_bp.route('/designs/<int:id>/edit', methods=['POST'])
@login_required
def edit_design(id):
    design = CulturalDesign.query.get_or_404(id)
    design.designer = request.form.get('designer')
    design.theme = request.form.get('theme')
    design.reference_gene = request.form.get('reference_gene')
    design.description = request.form.get('description')
    design.cultural_elements = request.form.get('cultural_elements')
    design.status = request.form.get('status')
    design.review_opinion = request.form.get('review_opinion')
    db.session.commit()
    flash('文创设计更新成功', 'success')
    return redirect(url_for('gene.designs'))


# ==================== 基因识别统计 ====================
@gene_bp.route('/gene-stats')
@login_required
def gene_stats():
    genes = CulturalGene.query.all()
    classifications = GeneClassification.query.all()
    return render_with_theme('gene_system/gene_stats.html',
                           genes=genes,
                           classifications=classifications)


# ==================== 文化基因特征提取管理 ====================
@gene_bp.route('/gene-features')
@login_required
def gene_features():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    
    query = GeneFeature.query
    if search:
        query = query.filter(
            (GeneFeature.feature_type.contains(search)) |
            (GeneFeature.feature_description.contains(search))
        )
    
    pagination = query.order_by(GeneFeature.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('gene_system/gene_features.html',
                           features=pagination.items,
                           pagination=pagination,
                           search=search)


@gene_bp.route('/gene-features/add', methods=['POST'])
@login_required
def add_gene_feature():
    feature = GeneFeature(
        feature_id=request.form.get('feature_id'),
        related_collection_id=request.form.get('related_collection_id'),
        feature_type=request.form.get('feature_type'),
        feature_description=request.form.get('feature_description'),
        feature_vector=request.form.get('feature_vector'),
        extraction_algorithm=request.form.get('extraction_algorithm'),
        extractor=request.form.get('extractor'),
        extraction_date=request.form.get('extraction_date'),
        confidence=request.form.get('confidence'),
        status=request.form.get('status', '待审核')
    )
    db.session.add(feature)
    db.session.commit()
    flash('基因特征添加成功', 'success')
    return redirect(url_for('gene.gene_features'))


@gene_bp.route('/gene-features/<int:id>/edit', methods=['POST'])
@login_required
def edit_gene_feature(id):
    feature = GeneFeature.query.get_or_404(id)
    feature.feature_type = request.form.get('feature_type')
    feature.feature_description = request.form.get('feature_description')
    feature.extraction_algorithm = request.form.get('extraction_algorithm')
    feature.confidence = request.form.get('confidence')
    feature.status = request.form.get('status')
    db.session.commit()
    flash('基因特征更新成功', 'success')
    return redirect(url_for('gene.gene_features'))


# ==================== 传承关系溯源 ====================
@gene_bp.route('/heritage-trace')
@login_required
def heritage_trace():
    genes = CulturalGene.query.all()
    return render_with_theme('gene_system/heritage_trace.html', genes=genes)


# ==================== 文化基因图谱构建管理 ====================
@gene_bp.route('/gene-atlas')
@login_required
def gene_atlas():
    genes = CulturalGene.query.all()
    classifications = GeneClassification.query.all()
    return render_with_theme('gene_system/gene_atlas.html',
                           genes=genes,
                           classifications=classifications)


# ==================== 文化基因分类管理 ====================
@gene_bp.route('/gene-classifications')
@login_required
def gene_classifications():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = GeneClassification.query.order_by(GeneClassification.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('gene_system/classifications.html',
                           classifications=pagination.items,
                           pagination=pagination)


@gene_bp.route('/gene-classifications/add', methods=['POST'])
@login_required
def add_classification():
    classification = GeneClassification(
        category_id=request.form.get('category_id'),
        category_name=request.form.get('category_name'),
        parent_category=request.form.get('parent_category', ''),
        description=request.form.get('description'),
        gene_count=request.form.get('gene_count', 0, type=int)
    )
    db.session.add(classification)
    db.session.commit()
    flash('基因分类添加成功', 'success')
    return redirect(url_for('gene.gene_classifications'))


# ==================== 文化基因检索管理 ====================
@gene_bp.route('/gene-search')
@login_required
def gene_search():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    gene_type = request.args.get('gene_type', '')
    search = request.args.get('search', '')
    
    query = CulturalGene.query
    if gene_type:
        query = query.filter_by(gene_type=gene_type)
    if search:
        query = query.filter(
            (CulturalGene.gene_name.contains(search)) |
            (CulturalGene.origin.contains(search))
        )
    
    pagination = query.order_by(CulturalGene.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    types = [t[0] for t in db.session.query(CulturalGene.gene_type).distinct().all()]
    
    return render_with_theme('gene_system/gene_search.html',
                           genes=pagination.items,
                           pagination=pagination,
                           types=types,
                           current_type=gene_type,
                           search=search)


@gene_bp.route('/gene-search/add', methods=['POST'])
@login_required
def add_gene():
    gene = CulturalGene(
        gene_id=request.form.get('gene_id'),
        gene_name=request.form.get('gene_name'),
        gene_type=request.form.get('gene_type'),
        origin=request.form.get('origin'),
        cultural_meaning=request.form.get('cultural_meaning'),
        confidence=request.form.get('confidence', 0.0, type=float),
        status=request.form.get('status', '待审核')
    )
    db.session.add(gene)
    db.session.commit()
    flash('文化基因添加成功', 'success')
    return redirect(url_for('gene.gene_search'))


# ==================== 文化基因分析报告管理 ====================
@gene_bp.route('/gene-reports')
@login_required
def gene_reports():
    return render_with_theme('gene_system/gene_reports.html')


# ==================== 手工艺品采集管理 ====================
@gene_bp.route('/collections')
@login_required
def collections():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    
    query = HandicraftCollection.query
    if search:
        query = query.filter(
            (HandicraftCollection.item_name.contains(search)) |
            (HandicraftCollection.category.contains(search))
        )
    
    pagination = query.order_by(HandicraftCollection.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('gene_system/collections.html',
                           collections=pagination.items,
                           pagination=pagination,
                           search=search)


@gene_bp.route('/collections/add', methods=['POST'])
@login_required
def add_collection():
    collection = HandicraftCollection(
        collection_id=request.form.get('collection_id'),
        item_name=request.form.get('item_name'),
        collector=request.form.get('collector'),
        collection_date=request.form.get('collection_date'),
        origin=request.form.get('origin'),
        category=request.form.get('category'),
        description=request.form.get('description'),
        status=request.form.get('status', '已采集')
    )
    db.session.add(collection)
    db.session.commit()
    flash('采集记录添加成功', 'success')
    return redirect(url_for('gene.collections'))


# ==================== 非遗传承人访谈管理 ====================
@gene_bp.route('/interviews')
@login_required
def interviews():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = HeritageInterview.query.order_by(HeritageInterview.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('gene_system/interviews.html',
                           interviews=pagination.items,
                           pagination=pagination)


@gene_bp.route('/interviews/add', methods=['POST'])
@login_required
def add_interview():
    interview = HeritageInterview(
        interview_id=request.form.get('interview_id'),
        interviewee=request.form.get('interviewee'),
        interviewer=request.form.get('interviewer'),
        interview_date=request.form.get('interview_date'),
        topic=request.form.get('topic'),
        content_summary=request.form.get('content_summary'),
        status=request.form.get('status', '已完成')
    )
    db.session.add(interview)
    db.session.commit()
    flash('访谈记录添加成功', 'success')
    return redirect(url_for('gene.interviews'))


# ==================== 文化传承教学管理 ====================
@gene_bp.route('/teaching')
@login_required
def teaching():
    designs = CulturalDesign.query.filter_by(status='已发布').all()
    return render_with_theme('gene_system/teaching.html', designs=designs)


# ==================== 系统效能监控 ====================
@gene_bp.route('/system-monitor')
@login_required
def system_monitor():
    return render_with_theme('gene_system/system_monitor.html')


# ==================== 基因审核流程管理 ====================
@gene_bp.route('/gene-review')
@login_required
def gene_review():
    pending_genes = CulturalGene.query.filter_by(status='待审核').all()
    pending_features = GeneFeature.query.filter_by(status='待审核').all()
    return render_with_theme('gene_system/gene_review.html',
                           pending_genes=pending_genes,
                           pending_features=pending_features)

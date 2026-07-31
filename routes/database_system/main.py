from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required
from models import db, Artisan, TrainingProgram, Artwork, Pattern
from models import CraftCategory, HeritageProject, Exhibition, CulturalInstitution
import csv
import io
import os
from urllib.parse import quote
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

database_bp = Blueprint('database', __name__)

SYSTEM_NAME = '民族手工艺数据库系统'
THEME_COLOR = '#E09456'
THEME_COLOR_LIGHT = '#F5C79A'


def render_with_theme(template, **kwargs):
    return render_template(template,
                         system_name=SYSTEM_NAME,
                         theme_color=THEME_COLOR,
                         theme_color_light=THEME_COLOR_LIGHT,
                         system_type='database',
                         **kwargs)


# ==================== 首页 ====================
@database_bp.route('/')
@login_required
def index():
    artisan_count = Artisan.query.count()
    artwork_count = Artwork.query.count()
    training_count = TrainingProgram.query.count()
    pattern_count = Pattern.query.count()
    
    stats = {
        'artisan_count': artisan_count,
        'artwork_count': artwork_count,
        'training_count': training_count,
        'pattern_count': pattern_count,
        'category_count': CraftCategory.query.count(),
        'project_count': HeritageProject.query.count(),
        'exhibition_count': Exhibition.query.count(),
        'institution_count': CulturalInstitution.query.count(),
    }
    
    recent_artisans = Artisan.query.order_by(Artisan.created_at.desc()).limit(3).all()
    recent_trainings = TrainingProgram.query.order_by(TrainingProgram.created_at.desc()).limit(3).all()
    
    return render_with_theme('database_system/index.html',
                           stats=stats,
                           recent_artisans=recent_artisans,
                           recent_trainings=recent_trainings)


# ==================== 传承人档案管理 ====================
@database_bp.route('/artisans')
@login_required
def artisans():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    
    query = Artisan.query
    if search:
        query = query.filter(
            (Artisan.name.contains(search)) |
            (Artisan.skill_type.contains(search)) |
            (Artisan.artisan_id.contains(search))
        )
    
    pagination = query.order_by(Artisan.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('database_system/artisans.html',
                           artisans=pagination.items,
                           pagination=pagination,
                           search=search)


@database_bp.route('/artisans/add', methods=['POST'])
@login_required
def add_artisan():
    artisan = Artisan(
        artisan_id=request.form.get('artisan_id'),
        name=request.form.get('name'),
        gender=request.form.get('gender'),
        ethnic_group=request.form.get('ethnic_group'),
        birth_date=request.form.get('birth_date'),
        skill_type=request.form.get('skill_type'),
        heritage_level=request.form.get('heritage_level'),
        representative_works=request.form.get('representative_works'),
        contact=request.form.get('contact'),
        location=request.form.get('location')
    )
    db.session.add(artisan)
    db.session.commit()
    flash('传承人添加成功', 'success')
    return redirect(url_for('database.artisans'))


@database_bp.route('/artisans/<int:id>/edit', methods=['POST'])
@login_required
def edit_artisan(id):
    artisan = Artisan.query.get_or_404(id)
    artisan.name = request.form.get('name')
    artisan.gender = request.form.get('gender')
    artisan.ethnic_group = request.form.get('ethnic_group')
    artisan.birth_date = request.form.get('birth_date')
    artisan.skill_type = request.form.get('skill_type')
    artisan.heritage_level = request.form.get('heritage_level')
    artisan.representative_works = request.form.get('representative_works')
    artisan.contact = request.form.get('contact')
    artisan.location = request.form.get('location')
    db.session.commit()
    flash('传承人信息更新成功', 'success')
    return redirect(url_for('database.artisans'))


@database_bp.route('/artisans/<int:id>/delete')
@login_required
def delete_artisan(id):
    artisan = Artisan.query.get_or_404(id)
    db.session.delete(artisan)
    db.session.commit()
    flash('传承人已删除', 'success')
    return redirect(url_for('database.artisans'))


# ==================== 技艺培训管理 ====================
@database_bp.route('/trainings')
@login_required
def trainings():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    
    query = TrainingProgram.query
    if search:
        query = query.filter(
            (TrainingProgram.title.contains(search)) |
            (TrainingProgram.instructor.contains(search))
        )
    
    pagination = query.order_by(TrainingProgram.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('database_system/trainings.html',
                           trainings=pagination.items,
                           pagination=pagination,
                           search=search)


@database_bp.route('/trainings/add', methods=['POST'])
@login_required
def add_training():
    training = TrainingProgram(
        program_id=request.form.get('program_id'),
        title=request.form.get('title'),
        instructor=request.form.get('instructor'),
        training_date=request.form.get('training_date'),
        location=request.form.get('location'),
        participants=request.form.get('participants', 0, type=int),
        duration=request.form.get('duration'),
        content=request.form.get('content'),
        assessment_method=request.form.get('assessment_method'),
        status=request.form.get('status', '未开始')
    )
    db.session.add(training)
    db.session.commit()
    flash('培训项目添加成功', 'success')
    return redirect(url_for('database.trainings'))


@database_bp.route('/trainings/<int:id>/edit', methods=['POST'])
@login_required
def edit_training(id):
    training = TrainingProgram.query.get_or_404(id)
    training.title = request.form.get('title')
    training.instructor = request.form.get('instructor')
    training.training_date = request.form.get('training_date')
    training.location = request.form.get('location')
    training.participants = request.form.get('participants', 0, type=int)
    training.duration = request.form.get('duration')
    training.content = request.form.get('content')
    training.assessment_method = request.form.get('assessment_method')
    training.status = request.form.get('status')
    db.session.commit()
    flash('培训项目更新成功', 'success')
    return redirect(url_for('database.trainings'))


# ==================== 手工艺作品管理 ====================
@database_bp.route('/artworks')
@login_required
def artworks():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    
    query = Artwork.query
    if search:
        query = query.filter(
            (Artwork.title.contains(search)) |
            (Artwork.artisan.contains(search)) |
            (Artwork.technique.contains(search))
        )
    
    pagination = query.order_by(Artwork.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('database_system/artworks.html',
                           artworks=pagination.items,
                           pagination=pagination,
                           search=search)


@database_bp.route('/artworks/add', methods=['POST'])
@login_required
def add_artwork():
    artwork = Artwork(
        artwork_id=request.form.get('artwork_id'),
        title=request.form.get('title'),
        artisan=request.form.get('artisan'),
        material=request.form.get('material'),
        technique=request.form.get('technique'),
        pattern_type=request.form.get('pattern_type'),
        cultural_value=request.form.get('cultural_value'),
        description=request.form.get('description'),
        status=request.form.get('status', '已归档')
    )
    db.session.add(artwork)
    db.session.commit()
    flash('作品添加成功', 'success')
    return redirect(url_for('database.artworks'))


# ==================== 纹样智能检索 ====================
@database_bp.route('/patterns')
@login_required
def patterns():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Pattern.query
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(
            (Pattern.name.contains(search)) |
            (Pattern.origin.contains(search))
        )
    
    pagination = query.order_by(Pattern.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    categories = [c[0] for c in db.session.query(Pattern.category).distinct().all()]
    
    return render_with_theme('database_system/patterns.html',
                           patterns=pagination.items,
                           pagination=pagination,
                           categories=categories,
                           current_category=category,
                           search=search)


# 新增纹样
@database_bp.route('/patterns/add', methods=['POST'])
@login_required
def add_pattern():
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 用纹样ID前缀避免重名
            pattern_id = request.form.get('pattern_id', 'pattern')
            ext = filename.rsplit('.', 1)[1].lower()
            save_name = f"pattern_{pattern_id}_{int(os.times()[4])}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, save_name))
            image_path = save_name
    
    pattern = Pattern(
        pattern_id=request.form.get('pattern_id'),
        name=request.form.get('name'),
        origin=request.form.get('origin'),
        category=request.form.get('category'),
        cultural_meaning=request.form.get('cultural_meaning'),
        color_scheme=request.form.get('color_scheme'),
        description=request.form.get('description'),
        image_path=image_path
    )
    db.session.add(pattern)
    db.session.commit()
    flash('纹样添加成功', 'success')
    return redirect(url_for('database.patterns'))


# 编辑纹样
@database_bp.route('/patterns/<int:id>/edit', methods=['POST'])
@login_required
def edit_pattern(id):
    pattern = Pattern.query.get_or_404(id)
    pattern.name = request.form.get('name')
    pattern.origin = request.form.get('origin')
    pattern.category = request.form.get('category')
    pattern.cultural_meaning = request.form.get('cultural_meaning')
    pattern.color_scheme = request.form.get('color_scheme')
    pattern.description = request.form.get('description')
    
    # 处理图片上传
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            # 删除旧图片
            if pattern.image_path:
                old_path = os.path.join(UPLOAD_FOLDER, pattern.image_path)
                if os.path.exists(old_path):
                    os.remove(old_path)
            # 保存新图片
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            save_name = f"pattern_{pattern.pattern_id}_{int(os.times()[4])}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, save_name))
            pattern.image_path = save_name
    
    db.session.commit()
    flash('纹样更新成功', 'success')
    return redirect(url_for('database.patterns'))


# 批量上传图片
@database_bp.route('/patterns/batch-upload', methods=['POST'])
@login_required
def batch_upload_images():
    files = request.files.getlist('images')
    success_count = 0
    skip_count = 0
    results = []
    
    for file in files:
        if not file or not file.filename:
            continue
        if not allowed_file(file.filename):
            skip_count += 1
            results.append(f"{file.filename} - 格式不支持")
            continue
        
        # 从原始文件名提取编号（去掉扩展名）
        original_filename = file.filename
        name_without_ext = os.path.splitext(original_filename)[0]
        ext = original_filename.rsplit('.', 1)[1].lower()
        
        # 安全的保存文件名
        safe_name = secure_filename(original_filename)
        
        # 匹配策略1：精确匹配纹样编号
        pattern = Pattern.query.filter_by(pattern_id=name_without_ext).first()
        
        # 匹配策略2：精确匹配纹样名称
        if not pattern:
            pattern = Pattern.query.filter_by(name=name_without_ext).first()
        
        # 匹配策略3：模糊匹配纹样名称（包含关系）
        if not pattern:
            pattern = Pattern.query.filter(Pattern.name.like(f'%{name_without_ext}%')).first()
        
        if not pattern:
            skip_count += 1
            results.append(f"{original_filename} - 未找到匹配的纹样")
            continue
        
        # 删除旧图片
        if pattern.image_path:
            old_path = os.path.join(UPLOAD_FOLDER, pattern.image_path)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # 保存新图片
        save_name = f"pattern_{pattern.pattern_id}_{int(os.times()[4])}_{success_count}.{ext}"
        file.save(os.path.join(UPLOAD_FOLDER, save_name))
        pattern.image_path = save_name
        success_count += 1
        results.append(f"{original_filename} → {pattern.name} ({pattern.pattern_id}) ✓")
    
    db.session.commit()
    result_msg = f'批量上传完成：成功 {success_count} 张，跳过 {skip_count} 张'
    if skip_count > 0:
        result_msg += '\n跳过原因：' + '; '.join([r for r in results if '✓' not in r][:5])
        if skip_count > 5:
            result_msg += f' ...等{skip_count}条'
    flash(result_msg, 'success')
    return redirect(url_for('database.patterns'))


# 删除纹样
@database_bp.route('/patterns/<int:id>/delete')
@login_required
def delete_pattern(id):
    pattern = Pattern.query.get_or_404(id)
    db.session.delete(pattern)
    db.session.commit()
    flash('纹样已删除', 'success')
    return redirect(url_for('database.patterns'))


# 下载导入模板
@database_bp.route('/patterns/template')
@login_required
def download_pattern_template():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['纹样编号', '纹样名称', '来源民族/地区', '纹样类别', '文化寓意', '配色方案', '详细描述'])
    writer.writerow(['PAT001', '云纹', '汉族', '自然纹样', '吉祥如意，步步高升', '蓝白相间', '传统云纹，常用于服饰、器物装饰'])
    writer.writerow(['PAT002', '缠枝纹', '多民族', '植物纹样', '生生不息，连绵不绝', '红绿金', '藤蔓缠绕，花卉点缀'])
    
    response = make_response(output.getvalue())
    response.headers["Content-type"] = "text/csv"
    filename = quote("纹样导入模板.csv")
    response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{filename}"
    return response


# 批量导入纹样
@database_bp.route('/patterns/import', methods=['POST'])
@login_required
def import_patterns():
    if 'file' not in request.files:
        flash('请选择要导入的CSV文件', 'error')
        return redirect(url_for('database.patterns'))
    
    file = request.files['file']
    if file.filename == '':
        flash('未选择文件', 'error')
        return redirect(url_for('database.patterns'))
    
    if not file.filename.endswith('.csv'):
        flash('仅支持CSV格式文件', 'error')
        return redirect(url_for('database.patterns'))
    
    try:
        # 读取文件原始字节
        file_bytes = file.stream.read()
        
        # 尝试多种编码格式
        content = None
        encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'big5']
        for enc in encodings:
            try:
                content = file_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            flash('导入失败：文件编码不支持，请保存为UTF-8或GBK编码的CSV文件', 'error')
            return redirect(url_for('database.patterns'))
        
        stream = io.StringIO(content)
        reader = csv.reader(stream)
        next(reader)  # 跳过表头
        
        success_count = 0
        skip_count = 0
        
        for row in reader:
            if len(row) < 2 or not row[1].strip():
                skip_count += 1
                continue
            
            # 检查编号是否已存在
            existing = Pattern.query.filter_by(pattern_id=row[0].strip()).first()
            if existing:
                skip_count += 1
                continue
            
            pattern = Pattern(
                pattern_id=row[0].strip() if len(row) > 0 else '',
                name=row[1].strip() if len(row) > 1 else '',
                origin=row[2].strip() if len(row) > 2 else '',
                category=row[3].strip() if len(row) > 3 else '',
                cultural_meaning=row[4].strip() if len(row) > 4 else '',
                color_scheme=row[5].strip() if len(row) > 5 else '',
                description=row[6].strip() if len(row) > 6 else ''
            )
            db.session.add(pattern)
            success_count += 1
        
        db.session.commit()
        flash(f'批量导入完成：成功 {success_count} 条，跳过 {skip_count} 条', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'导入失败：{str(e)}', 'error')
    
    return redirect(url_for('database.patterns'))


# 导出纹样
@database_bp.route('/patterns/export')
@login_required
def export_patterns():
    patterns = Pattern.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['纹样编号', '纹样名称', '来源民族/地区', '纹样类别', '文化寓意', '配色方案', '详细描述'])
    
    for p in patterns:
        writer.writerow([
            p.pattern_id, p.name, p.origin, p.category,
            p.cultural_meaning, p.color_scheme, p.description
        ])
    
    response = make_response(output.getvalue())
    response.headers["Content-type"] = "text/csv"
    filename = quote("纹样数据库.csv")
    response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{filename}"
    return response


# ==================== 元素融合设计 ====================
@database_bp.route('/fusion')
@login_required
def fusion():
    patterns = Pattern.query.all()
    return render_with_theme('database_system/fusion.html', patterns=patterns)


# ==================== 工艺品类分析 ====================
@database_bp.route('/category-analysis')
@login_required
def category_analysis():
    categories = CraftCategory.query.all()
    return render_with_theme('database_system/category_analysis.html', categories=categories)


# ==================== 工艺品类统计管理 ====================
@database_bp.route('/category-stats')
@login_required
def category_stats():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = CraftCategory.query.order_by(CraftCategory.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('database_system/category_stats.html',
                           categories=pagination.items,
                           pagination=pagination)


# ==================== 非遗传承分析 ====================
@database_bp.route('/heritage-analysis')
@login_required
def heritage_analysis():
    artisans = Artisan.query.all()
    trainings = TrainingProgram.query.all()
    return render_with_theme('database_system/heritage_analysis.html',
                           artisans=artisans,
                           trainings=trainings)


# ==================== 传承项目申报管理 ====================
@database_bp.route('/projects')
@login_required
def projects():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = HeritageProject.query.order_by(HeritageProject.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('database_system/projects.html',
                           projects=pagination.items,
                           pagination=pagination)


@database_bp.route('/projects/add', methods=['POST'])
@login_required
def add_project():
    project = HeritageProject(
        project_id=request.form.get('project_id'),
        project_name=request.form.get('project_name'),
        applicant=request.form.get('applicant'),
        project_type=request.form.get('project_type'),
        apply_date=request.form.get('apply_date'),
        status=request.form.get('status', '审核中'),
        description=request.form.get('description')
    )
    db.session.add(project)
    db.session.commit()
    flash('项目申报成功', 'success')
    return redirect(url_for('database.projects'))


# ==================== 展览活动管理 ====================
@database_bp.route('/exhibitions')
@login_required
def exhibitions():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = Exhibition.query.order_by(Exhibition.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('database_system/exhibitions.html',
                           exhibitions=pagination.items,
                           pagination=pagination)


@database_bp.route('/exhibitions/add', methods=['POST'])
@login_required
def add_exhibition():
    exhibition = Exhibition(
        exhibition_id=request.form.get('exhibition_id'),
        name=request.form.get('name'),
        location=request.form.get('location'),
        start_date=request.form.get('start_date'),
        end_date=request.form.get('end_date'),
        organizer=request.form.get('organizer'),
        status=request.form.get('status', '筹备中')
    )
    db.session.add(exhibition)
    db.session.commit()
    flash('展览活动添加成功', 'success')
    return redirect(url_for('database.exhibitions'))


# ==================== 国际合作管理 ====================
@database_bp.route('/international')
@login_required
def international():
    return render_with_theme('database_system/international.html')


# ==================== 文化机构管理 ====================
@database_bp.route('/institutions')
@login_required
def institutions():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = CulturalInstitution.query.order_by(CulturalInstitution.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_with_theme('database_system/institutions.html',
                           institutions=pagination.items,
                           pagination=pagination)


@database_bp.route('/institutions/add', methods=['POST'])
@login_required
def add_institution():
    institution = CulturalInstitution(
        institution_id=request.form.get('institution_id'),
        name=request.form.get('name'),
        type=request.form.get('type'),
        location=request.form.get('location'),
        contact=request.form.get('contact'),
        level=request.form.get('level')
    )
    db.session.add(institution)
    db.session.commit()
    flash('文化机构添加成功', 'success')
    return redirect(url_for('database.institutions'))


# ==================== 技法传承图谱 ====================
@database_bp.route('/heritage-graph')
@login_required
def heritage_graph():
    artisans = Artisan.query.all()
    return render_with_theme('database_system/heritage_graph.html', artisans=artisans)


# ==================== 数据备份管理 ====================
@database_bp.route('/backup')
@login_required
def backup():
    return render_with_theme('database_system/backup.html')

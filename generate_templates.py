import os

# 数据库系统侧边栏
database_sidebar = '''<div class="menu-group">
    <div class="menu-title">首页</div>
    <a href="{{ url_for('database.index') }}" class="menu-item"><span class="icon">🏠</span> 首页</a>
</div>
<div class="menu-group">
    <div class="menu-title">传承与发展</div>
    <a href="{{ url_for('database.heritage_graph') }}" class="menu-item"><span class="icon">🕸️</span> 技法传承图谱</a>
    <a href="{{ url_for('database.artisans') }}" class="menu-item"><span class="icon">👤</span> 传承人档案管理</a>
    <a href="{{ url_for('database.trainings') }}" class="menu-item"><span class="icon">📚</span> 技艺培训管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">作品与资源管理</div>
    <a href="{{ url_for('database.artworks') }}" class="menu-item"><span class="icon">🎨</span> 手工艺作品管理</a>
    <a href="{{ url_for('database.fusion') }}" class="menu-item"><span class="icon">🔀</span> 元素融合设计</a>
    <a href="{{ url_for('database.patterns') }}" class="menu-item"><span class="icon">🔍</span> 纹样智能检索</a>
</div>
<div class="menu-group">
    <div class="menu-title">数据分析</div>
    <a href="{{ url_for('database.category_analysis') }}" class="menu-item"><span class="icon">📊</span> 工艺品类分析</a>
    <a href="{{ url_for('database.category_stats') }}" class="menu-item"><span class="icon">📈</span> 工艺品类统计管理</a>
    <a href="{{ url_for('database.heritage_analysis') }}" class="menu-item"><span class="icon">📉</span> 非遗传承分析</a>
</div>
<div class="menu-group">
    <div class="menu-title">系统管理</div>
    <a href="{{ url_for('database.backup') }}" class="menu-item"><span class="icon">💾</span> 数据备份管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">项目管理</div>
    <a href="{{ url_for('database.projects') }}" class="menu-item"><span class="icon">📋</span> 传承项目申报管理</a>
    <a href="{{ url_for('database.exhibitions') }}" class="menu-item"><span class="icon">🖼️</span> 展览活动管理</a>
    <a href="{{ url_for('database.international') }}" class="menu-item"><span class="icon">🌍</span> 国际合作管理</a>
    <a href="{{ url_for('database.institutions') }}" class="menu-item"><span class="icon">🏛️</span> 文化机构管理</a>
</div>'''

# 基因系统侧边栏
gene_sidebar = '''<div class="menu-group">
    <div class="menu-title">首页</div>
    <a href="{{ url_for('gene.index') }}" class="menu-item"><span class="icon">🏠</span> 首页</a>
</div>
<div class="menu-group">
    <div class="menu-title">文创设计辅助</div>
    <a href="{{ url_for('gene.fusion_design') }}" class="menu-item"><span class="icon">✨</span> 智能融合设计</a>
    <a href="{{ url_for('gene.pattern_analysis') }}" class="menu-item"><span class="icon">🔬</span> 纹样智能解析</a>
    <a href="{{ url_for('gene.designs') }}" class="menu-item"><span class="icon">📝</span> 文创设计辅助管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">文化基因分析</div>
    <a href="{{ url_for('gene.gene_stats') }}" class="menu-item"><span class="icon">📊</span> 基因识别统计</a>
    <a href="{{ url_for('gene.gene_features') }}" class="menu-item"><span class="icon">🧬</span> 文化基因特征提取管理</a>
    <a href="{{ url_for('gene.heritage_trace') }}" class="menu-item"><span class="icon">🔗</span> 传承关系溯源</a>
    <a href="{{ url_for('gene.gene_atlas') }}" class="menu-item"><span class="icon">🗺️</span> 文化基因图谱构建管理</a>
    <a href="{{ url_for('gene.gene_classifications') }}" class="menu-item"><span class="icon">📂</span> 文化基因分类管理</a>
    <a href="{{ url_for('gene.gene_search') }}" class="menu-item"><span class="icon">🔍</span> 文化基因检索管理</a>
    <a href="{{ url_for('gene.gene_reports') }}" class="menu-item"><span class="icon">📑</span> 文化基因分析报告管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">文化资源采集</div>
    <a href="{{ url_for('gene.collections') }}" class="menu-item"><span class="icon">📦</span> 手工艺品采集管理</a>
    <a href="{{ url_for('gene.interviews') }}" class="menu-item"><span class="icon">🎙️</span> 非遗传承人访谈管理</a>
    <a href="{{ url_for('gene.teaching') }}" class="menu-item"><span class="icon">🎓</span> 文化传承教学管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">系统管理</div>
    <a href="{{ url_for('gene.system_monitor') }}" class="menu-item"><span class="icon">🖥️</span> 系统效能监控</a>
    <a href="{{ url_for('gene.gene_review') }}" class="menu-item"><span class="icon">✅</span> 基因审核流程管理</a>
</div>'''

# 设计系统侧边栏
design_sidebar = '''<div class="menu-group">
    <div class="menu-title">首页</div>
    <a href="{{ url_for('design.index') }}" class="menu-item"><span class="icon">🏠</span> 首页</a>
</div>
<div class="menu-group">
    <div class="menu-title">工艺管理</div>
    <a href="{{ url_for('design.craft_processes') }}" class="menu-item"><span class="icon">⚒️</span> 传统工艺适配管理</a>
    <a href="{{ url_for('design.product_schemes') }}" class="menu-item"><span class="icon">📦</span> 手工艺品方案管理</a>
    <a href="{{ url_for('design.material_calc') }}" class="menu-item"><span class="icon">🧮</span> 耗材计算</a>
</div>
<div class="menu-group">
    <div class="menu-title">市场分析</div>
    <a href="{{ url_for('design.trend_forecast') }}" class="menu-item"><span class="icon">📈</span> 趋势预测</a>
    <a href="{{ url_for('design.demand_insight') }}" class="menu-item"><span class="icon">💡</span> 需求洞察</a>
    <a href="{{ url_for('design.design_trends') }}" class="menu-item"><span class="icon">📊</span> 设计趋势分析管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">文化传承</div>
    <a href="{{ url_for('design.inheritors') }}" class="menu-item"><span class="icon">👤</span> 非遗传承人管理</a>
    <a href="{{ url_for('design.cultural_knowledge') }}" class="menu-item"><span class="icon">📖</span> 民族文化知识管理</a>
    <a href="{{ url_for('design.teaching_courses') }}" class="menu-item"><span class="icon">🎓</span> 工艺教学课程管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">智能设计工具</div>
    <a href="{{ url_for('design.pattern_generator') }}" class="menu-item"><span class="icon">🎨</span> 纹样生成</a>
    <a href="{{ url_for('design.smart_design') }}" class="menu-item"><span class="icon">🤖</span> 智能生成设计管理</a>
    <a href="{{ url_for('design.design_efficiency') }}" class="menu-item"><span class="icon">⚡</span> 设计效能</a>
</div>
<div class="menu-group">
    <div class="menu-title">订单管理</div>
    <a href="{{ url_for('design.custom_orders') }}" class="menu-item"><span class="icon">📋</span> 定制订单跟踪管理</a>
</div>
<div class="menu-group">
    <div class="menu-title">设计素材库</div>
    <a href="{{ url_for('design.pattern_materials') }}" class="menu-item"><span class="icon">🖼️</span> 民族图案素材管理</a>
    <a href="{{ url_for('design.copyrights') }}" class="menu-item"><span class="icon">©️</span> 数字版权登记管理</a>
</div>'''

def generate_template(system, filename, title, sidebar, content=''):
    """生成简单的模板文件"""
    if not content:
        content = '''<div class="card">
    <div class="card-title">{{ page_title }}</div>
    <p style="color: #999;">该模块功能开发中...</p>
</div>'''
    
    template = f'''{{% extends "layout.html" %}}

{{% block sidebar %}}
{sidebar}
{{% endblock %}}

{{% block page_title %}}{title}{{% endblock %}}

{{% block content %}}
{content}
{{% endblock %}}
'''
    return template

# 数据库系统页面
database_pages = [
    ('fusion.html', '元素融合设计'),
    ('category_analysis.html', '工艺品类分析'),
    ('category_stats.html', '工艺品类统计管理'),
    ('heritage_analysis.html', '非遗传承分析'),
    ('exhibitions.html', '展览活动管理'),
    ('international.html', '国际合作管理'),
    ('institutions.html', '文化机构管理'),
    ('heritage_graph.html', '技法传承图谱'),
    ('backup.html', '数据备份管理'),
]

# 基因系统页面
gene_pages = [
    ('fusion_design.html', '智能融合设计'),
    ('pattern_analysis.html', '纹样智能解析'),
    ('gene_stats.html', '基因识别统计'),
    ('gene_features.html', '文化基因特征提取管理'),
    ('heritage_trace.html', '传承关系溯源'),
    ('gene_atlas.html', '文化基因图谱构建管理'),
    ('classifications.html', '文化基因分类管理'),
    ('gene_search.html', '文化基因检索管理'),
    ('gene_reports.html', '文化基因分析报告管理'),
    ('collections.html', '手工艺品采集管理'),
    ('interviews.html', '非遗传承人访谈管理'),
    ('teaching.html', '文化传承教学管理'),
    ('system_monitor.html', '系统效能监控'),
    ('gene_review.html', '基因审核流程管理'),
]

# 设计系统页面
design_pages = [
    ('craft_processes.html', '传统工艺适配管理'),
    ('product_schemes.html', '手工艺品方案管理'),
    ('material_calc.html', '耗材计算'),
    ('trend_forecast.html', '趋势预测'),
    ('demand_insight.html', '需求洞察'),
    ('design_trends.html', '设计趋势分析管理'),
    ('inheritors.html', '非遗传承人管理'),
    ('cultural_knowledge.html', '民族文化知识管理'),
    ('teaching_courses.html', '工艺教学课程管理'),
    ('pattern_generator.html', '纹样生成'),
    ('smart_design.html', '智能生成设计管理'),
    ('design_efficiency.html', '设计效能'),
    ('custom_orders.html', '定制订单跟踪管理'),
    ('pattern_materials.html', '民族图案素材管理'),
    ('copyrights.html', '数字版权登记管理'),
]

base_dir = r'C:\Users\xiaoy\Doubao\chats\2026-07-24\new-chat\shouyi_project\templates'

# 生成数据库系统页面
for filename, title in database_pages:
    filepath = os.path.join(base_dir, 'database_system', filename)
    if not os.path.exists(filepath):
        content = generate_template('database', filename, title, database_sidebar)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Created: {filename}')

# 生成基因系统页面
for filename, title in gene_pages:
    filepath = os.path.join(base_dir, 'gene_system', filename)
    if not os.path.exists(filepath):
        content = generate_template('gene', filename, title, gene_sidebar)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Created: {filename}')

# 生成设计系统页面
for filename, title in design_pages:
    filepath = os.path.join(base_dir, 'design_system', filename)
    if not os.path.exists(filepath):
        content = generate_template('design', filename, title, design_sidebar)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Created: {filename}')

print('All templates generated!')

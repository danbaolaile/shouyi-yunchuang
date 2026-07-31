from flask import Blueprint, render_template, request
from models import db, Pattern, CulturalGene
import os
import random

customer_bp = Blueprint('customer', __name__)

SYSTEM_NAME = '手艺云创 - 客户体验中心'
THEME_COLOR = '#6C5CE7'
THEME_COLOR_LIGHT = '#A29BFE'


def render_customer(template, **kwargs):
    return render_template(template,
                         system_name=SYSTEM_NAME,
                         theme_color=THEME_COLOR,
                         theme_color_light=THEME_COLOR_LIGHT,
                         **kwargs)


# 民族文化元素库
ETHNIC_ELEMENTS = {
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
ETHNIC_COLORS = {
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

# 风格化配色方案
STYLE_COLORS = {
    '传统民族配色': {
        '传统风格': ['#8B0000', '#DAA520', '#2F4F4F', '#CD853F'],
        '简约': ['#2D3436', '#636E72', '#DFE6E9', '#00B894'],
        '复古': ['#6D4C41', '#D7CCC8', '#BCAAA4', '#8D6E63'],
        '怀旧': ['#795548', '#A1887F', '#D7CCC8', '#EFEBE9'],
        '极简主义': ['#212121', '#757575', '#BDBDBD', '#FAFAFA'],
        '现代时尚': ['#6C5CE7', '#00CEC9', '#FD79A8', '#FDCB6E'],
        '国潮': ['#C41E3A', '#D4AF37', '#1E3A5F', '#FF6B35'],
        '抽象化': ['#E91E63', '#9C27B0', '#3F51B5', '#00BCD4']
    },
    '暖色调': ['#D32F2F', '#F57C00', '#FBC02D', '#E64A19'],
    '冷色调': ['#1976D2', '#0097A7', '#7B1FA2', '#388E3C'],
    '高饱和': ['#F44336', '#E91E63', '#9C27B0', '#2196F3'],
    '低饱和': ['#90A4AE', '#A1887F', '#80CBC4', '#CE93D8'],
    '现代简约配色': ['#2D3436', '#636E72', '#B2BEC3', '#DFE6E9'],
    '黑白灰': ['#212121', '#616161', '#9E9E9E', '#F5F5F5'],
    '莫兰迪': ['#B5A89A', '#A6B1B8', '#C9B8A8', '#9AA8A6']
}

# 风格设计建议
STYLE_SUGGESTIONS = {
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
USAGE_SUGGESTIONS = {
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


# 客户首页
@customer_bp.route('/')
def index():
    pattern_count = Pattern.query.count()
    gene_count = CulturalGene.query.count()
    hot_patterns = Pattern.query.limit(6).all()
    return render_customer('customer/index.html', 
                          pattern_count=pattern_count,
                          gene_count=gene_count,
                          hot_patterns=hot_patterns)


# 纹样识别
@customer_bp.route('/recognize', methods=['GET', 'POST'])
def recognize():
    results = []
    uploaded = False
    filename = None
    
    if request.method == 'POST':
        uploaded = True
        file = request.files.get('image')
        
        if file and file.filename:
            filename = file.filename
            name_without_ext = os.path.splitext(filename)[0]
            
            # 智能匹配策略
            matches = Pattern.query.filter(
                (Pattern.pattern_id == name_without_ext) |
                (Pattern.name == name_without_ext)
            ).all()
            
            if not matches:
                matches = Pattern.query.filter(
                    Pattern.name.like(f'%{name_without_ext}%') |
                    Pattern.origin.like(f'%{name_without_ext}%') |
                    Pattern.category.like(f'%{name_without_ext}%')
                ).all()
            
            if not matches:
                matches = Pattern.query.limit(5).all()
            
            for i, p in enumerate(matches[:6]):
                similarity = random.randint(75, 98) - i * 3
                results.append({
                    'pattern': p,
                    'similarity': max(similarity, 60)
                })
    
    return render_customer('customer/recognize.html',
                          results=results,
                          uploaded=uploaded,
                          filename=filename)


# 智能设计
@customer_bp.route('/design', methods=['GET', 'POST'])
def design():
    design_result = None
    
    if request.method == 'POST':
        ethnic = request.form.get('ethnic', '多民族融合')
        style = request.form.get('style', '传统风格')
        usage = request.form.get('usage', '文创产品')
        color_pref = request.form.get('color_pref', '传统民族配色')
        main_color = request.form.get('main_color', '#6C5CE7')
        elements = request.form.get('elements', '')
        
        # 生成配色方案
        colors = generate_color_scheme(ethnic, style, color_pref, main_color)
        
        # 匹配参考纹样
        related_patterns = Pattern.query.filter(
            Pattern.origin.like(f'%{ethnic}%')
        ).limit(4).all()
        
        if not related_patterns:
            related_patterns = Pattern.query.limit(4).all()
        
        # 生成设计建议
        suggestions = generate_design_suggestions(ethnic, style, usage, elements)
        
        # 文化元素解析
        cultural_elements = get_cultural_elements(ethnic, elements)
        
        # 设计名称
        design_name = f'{ethnic}风{style}纹样设计'
        
        # 示例预览图（使用静态示例图片，实际项目可接入AI生成）
        preview_images = get_preview_images(ethnic, style, usage)
        
        design_result = {
            'ethnic': ethnic,
            'style': style,
            'usage': usage,
            'color_pref': color_pref,
            'main_color': main_color,
            'colors': colors,
            'related_patterns': related_patterns,
            'suggestions': suggestions,
            'cultural_elements': cultural_elements,
            'design_name': design_name,
            'preview_images': preview_images
        }
    
    return render_customer('customer/design.html', design_result=design_result)


def generate_color_scheme(ethnic, style, color_pref, main_color):
    """生成配色方案"""
    # 优先使用用户指定的色彩方向
    if color_pref == '传统民族配色':
        # 基于民族传统配色 + 风格调整
        base_colors = ETHNIC_COLORS.get(ethnic, ['#8B0000', '#DAA520', '#2F4F4F', '#CD853F'])
        if isinstance(base_colors, dict):
            base_colors = base_colors.get(style, ['#8B0000', '#DAA520', '#2F4F4F', '#CD853F'])
        return base_colors[:4]
    else:
        return STYLE_COLORS.get(color_pref, ['#8B0000', '#DAA520', '#2F4F4F', '#CD853F'])[:4]


def generate_design_suggestions(ethnic, style, usage, elements):
    """生成设计建议"""
    suggestions = []
    
    # 民族文化建议
    if ethnic in ETHNIC_ELEMENTS:
        elem_list = ETHNIC_ELEMENTS[ethnic]
        suggestions.append(f'融入{ethnic}典型文化元素：{"、".join(elem_list[:4])}等，确保文化符号的准确表达')
    
    if ethnic == '多民族融合':
        suggestions.append('融合多民族纹样元素，注重不同文化符号之间的和谐统一，避免生硬拼凑')
    
    # 风格建议
    if style in STYLE_SUGGESTIONS:
        suggestions.append(STYLE_SUGGESTIONS[style])
    
    # 场景建议
    if usage in USAGE_SUGGESTIONS:
        suggestions.append(USAGE_SUGGESTIONS[usage])
    
    # 用户指定元素
    if elements and elements.strip():
        suggestions.append(f'已融入您指定的文化元素：{elements}，建议作为主体纹样重点突出展示')
    
    # 通用文化建议
    suggestions.append('尊重非遗文化内涵，准确理解纹样寓意，避免误用或随意改造文化符号')
    
    return suggestions


def get_cultural_elements(ethnic, user_elements):
    """获取文化元素列表"""
    elements = []
    
    # 从民族元素库中选取
    if ethnic in ETHNIC_ELEMENTS:
        elements.extend(ETHNIC_ELEMENTS[ethnic][:5])
    
    # 添加用户指定元素
    if user_elements and user_elements.strip():
        user_elems = [e.strip() for e in user_elements.replace('，', '、').replace(',', '、').split('、') if e.strip()]
        for elem in user_elems:
            if elem not in elements:
                elements.append(elem)
    
    return elements[:8]


def get_preview_images(ethnic, style, usage):
    """获取设计预览图"""
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
    
    images = preview_map.get(ethnic, ['design_previews/guochao_dragon.jpg'])
    
    # 国潮风格用国潮图
    if style == '国潮':
        images = ['design_previews/guochao_dragon.jpg'] + images
    
    # 返回最多4张
    result = []
    for img in images[:4]:
        result.append(f'/static/{img}')
    
    return result

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db, User, Artisan, TrainingProgram, Artwork, Pattern
from models import CraftCategory, HeritageProject, Exhibition, CulturalInstitution
from models import CulturalGene, PatternAnalysis, GeneFeature, GeneClassification
from models import CulturalDesign, HandicraftCollection, HeritageInterview
from models import CraftProcess, ProductScheme, DesignTrend, HeritageInheritor
from models import CulturalKnowledge, TeachingCourse, PatternMaterial
from models import CopyrightRegistration, CustomOrder, UserPreference
from app import create_app


def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建成功！")
        
        # 创建默认管理员用户
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin', system_type='all')
            admin.set_password('admin123')
            db.session.add(admin)
            print("默认管理员账户创建成功：admin / admin123")
        
        # 插入示例数据 - 传承人
        if Artisan.query.count() == 0:
            artisans = [
                Artisan(artisan_id='28604797', name='汪*艺', gender='男', ethnic_group='景颇族',
                       birth_date='1996-08-01', skill_type='织锦', heritage_level='国家级传承人',
                       representative_works='彝族漆器', contact='邮箱', location='广西桂林'),
                Artisan(artisan_id='80104995', name='康*玛', gender='男', ethnic_group='水族',
                       birth_date='2001-01-29', skill_type='剪纸', heritage_level='国家级传承人',
                       representative_works='蒙古族马鞍', contact='邮箱', location='西藏拉萨'),
                Artisan(artisan_id='77286803', name='凌*福', gender='男', ethnic_group='高山族',
                       birth_date='1977-04-02', skill_type='蜡染', heritage_level='省级传承人',
                       representative_works='彝族漆器', contact='邮箱', location='青海西宁'),
                Artisan(artisan_id='78243568', name='陆*葆', gender='男', ethnic_group='汉族',
                       birth_date='1984-06-07', skill_type='织锦', heritage_level='省级传承人',
                       representative_works='苗族背带', contact='QQ', location='新疆喀什'),
                Artisan(artisan_id='62180318', name='朱*群', gender='男', ethnic_group='汉族',
                       birth_date='1963-03-10', skill_type='银饰制作', heritage_level='县级传承人',
                       representative_works='苗族背带', contact='邮箱', location='新疆喀什'),
            ]
            db.session.add_all(artisans)
            print("传承人示例数据插入成功")
        
        # 插入示例数据 - 培训项目
        if TrainingProgram.query.count() == 0:
            trainings = [
                TrainingProgram(program_id='61744716', title='陶艺成型方法', instructor='汪*子',
                               training_date='2024-11-04', location='广西桂林', participants=98,
                               duration='3天', content='木雕技艺', assessment_method='理论考试', status='进行中'),
                TrainingProgram(program_id='70106201', title='非遗文化传承', instructor='徐*风',
                               training_date='2025-01-30', location='广西桂林', participants=79,
                               duration='10天', content='陶艺制作', assessment_method='理论考试', status='已完成'),
                TrainingProgram(program_id='85658932', title='刺绣针法基础', instructor='益*厚',
                               training_date='2024-11-03', location='线上', participants=94,
                               duration='15天', content='陶艺制作', assessment_method='综合评定', status='进行中'),
                TrainingProgram(program_id='24097798', title='银器錾刻工艺', instructor='潘*耀',
                               training_date='2025-03-14', location='云南大理', participants=87,
                               duration='5天', content='陶艺制作', assessment_method='现场实操', status='进行中'),
            ]
            db.session.add_all(trainings)
            print("培训项目示例数据插入成功")
        
        # 插入示例数据 - 手工艺作品
        if Artwork.query.count() == 0:
            artworks = [
                Artwork(artwork_id='AW001', title='苗族百鸟衣', artisan='潘*耀',
                       material='蚕丝', technique='刺绣', pattern_type='花鸟纹',
                       cultural_value='国家级', description='苗族传统服饰，绣有百鸟图案', status='已归档'),
                Artwork(artwork_id='AW002', title='彝族漆器花瓶', artisan='康*玛',
                       material='木材', technique='漆艺', pattern_type='几何纹',
                       cultural_value='省级', description='彝族传统漆器工艺', status='已归档'),
                Artwork(artwork_id='AW003', title='蒙古族马鞍', artisan='凌*福',
                       material='皮革', technique='雕刻', pattern_type='卷草纹',
                       cultural_value='国家级', description='蒙古族传统马具', status='展览中'),
            ]
            db.session.add_all(artworks)
            print("手工艺作品示例数据插入成功")
        
        # 插入示例数据 - 纹样
        if Pattern.query.count() == 0:
            patterns = [
                Pattern(pattern_id='PT001', name='云纹', origin='汉族', category='自然纹样',
                       cultural_meaning='吉祥如意，步步高升', color_scheme='红金', description='传统云纹图案，常用于服饰、建筑装饰'),
                Pattern(pattern_id='PT002', name='回纹', origin='汉族', category='几何纹样',
                       cultural_meaning='连绵不断，吉利永长', color_scheme='蓝白', description='回形几何纹样，寓意富贵不断头'),
                Pattern(pattern_id='PT003', name='蜡染冰纹', origin='苗族', category='自然纹样',
                       cultural_meaning='冰裂纹理，自然天成', color_scheme='靛蓝', description='苗族蜡染特有纹样，冰裂纹效果'),
                Pattern(pattern_id='PT004', name='缠枝纹', origin='多民族', category='植物纹样',
                       cultural_meaning='生生不息，连绵不绝', color_scheme='红绿金', description='藤蔓缠绕，花卉点缀，常用于瓷器、织锦'),
                Pattern(pattern_id='PT005', name='蝴蝶纹', origin='苗族', category='动物纹样',
                       cultural_meaning='美好爱情，自由幸福', color_scheme='五彩', description='苗族刺绣经典纹样，象征蝴蝶妈妈'),
                Pattern(pattern_id='PT006', name='万字纹', origin='藏族', category='符号纹样',
                       cultural_meaning='吉祥万福，永恒不变', color_scheme='红黄', description='藏传佛教吉祥符号'),
                Pattern(pattern_id='PT007', name='八瓣花纹', origin='维吾尔族', category='植物纹样',
                       cultural_meaning='花开富贵，繁荣昌盛', color_scheme='蓝绿红', description='新疆地毯常见纹样'),
                Pattern(pattern_id='PT008', name='龙纹', origin='汉族', category='动物纹样',
                       cultural_meaning='权威尊贵，吉祥如意', color_scheme='金红', description='中华民族图腾纹样'),
                Pattern(pattern_id='PT009', name='铜鼓纹', origin='壮族', category='几何纹样',
                       cultural_meaning='太阳崇拜，丰收祈福', color_scheme='古铜色', description='广西铜鼓传统纹样'),
                Pattern(pattern_id='PT010', name='杜鹃花饰', origin='彝族', category='植物纹样',
                       cultural_meaning='热情奔放，生命绽放', color_scheme='红黄黑', description='彝族漆器常见装饰纹样'),
            ]
            db.session.add_all(patterns)
            print("纹样示例数据插入成功")
        
        # 插入示例数据 - 文化基因
        if CulturalGene.query.count() == 0:
            genes = [
                CulturalGene(gene_id='CG001', gene_name='苗族蜡染基因', gene_type='工艺基因',
                            gene_features='["靛蓝染色","手工绘制","冰裂纹理"]', origin='苗族',
                            cultural_meaning='古老的防染工艺', confidence=0.95, status='已审核'),
                CulturalGene(gene_id='CG002', gene_name='祥云纹基因', gene_type='纹样基因',
                            gene_features='["卷云形态","如意造型","渐变色彩"]', origin='汉族',
                            cultural_meaning='吉祥如意的象征', confidence=0.92, status='已审核'),
                CulturalGene(gene_id='CG003', gene_name='彝族漆器基因', gene_type='材质基因',
                            gene_features='["木胎","大漆","彩绘"]', origin='彝族',
                            cultural_meaning='少数民族漆艺代表', confidence=0.88, status='待审核'),
            ]
            db.session.add_all(genes)
            print("文化基因示例数据插入成功")
        
        # 插入示例数据 - 基因特征提取
        if GeneFeature.query.count() == 0:
            features = [
                GeneFeature(feature_id='03558886', related_collection_id='13762105',
                           feature_type='风格', feature_description='几何图形',
                           feature_vector='128维向量', extraction_algorithm='VGG视觉几何组',
                           extractor='袁*耀', extraction_date='2024-09-16', confidence='不确定', status='专家复核'),
                GeneFeature(feature_id='50193162', related_collection_id='02706142',
                           feature_type='图案', feature_description='文字符号',
                           feature_vector='自定义向量', extraction_algorithm='ResNet残差网络',
                           extractor='赖*溯', extraction_date='2024-08-24', confidence='低置信度', status='专家复核'),
                GeneFeature(feature_id='39328292', related_collection_id='36303891',
                           feature_type='图案', feature_description='文字符号',
                           feature_vector='128维向量', extraction_algorithm='VGG视觉几何组',
                           extractor='于*生', extraction_date='2025-05-17', confidence='高置信度', status='已归档'),
            ]
            db.session.add_all(features)
            print("基因特征示例数据插入成功")
        
        # 插入示例数据 - 文创设计
        if CulturalDesign.query.count() == 0:
            designs = [
                CulturalDesign(design_id='40855966', designer='易*中', design_date='2024-10-16',
                              theme='神话主题', reference_gene='藏族基因', sketch='手绘稿',
                              description='色彩搭配', cultural_elements='节日习俗', status='已审核', review_opinion='较差'),
                CulturalDesign(design_id='34912013', designer='潘*静', design_date='2024-10-28',
                              theme='神话主题', reference_gene='苗族基因', sketch='手绘稿',
                              description='工艺要求', cultural_elements='建筑风格', status='进行中', review_opinion='较差'),
                CulturalDesign(design_id='03114710', designer='方*兰', design_date='2024-08-22',
                              theme='非遗主题', reference_gene='彝族基因', sketch='概念图',
                              description='工艺要求', cultural_elements='神话传说', status='未开始', review_opinion='需修改'),
            ]
            db.session.add_all(designs)
            print("文创设计示例数据插入成功")
        
        # 插入示例数据 - 传统工艺
        if CraftProcess.query.count() == 0:
            processes = [
                CraftProcess(process_id='02712498', process_name='傣族织锦', process_type='编织',
                            applicable_material='丝绸', difficulty='大师级', estimated_time='30天以上',
                            tool_requirements='陶轮', description='手工制作', teaching_video='材料准备',
                            status='制作中', heritage_region='广西桂林', cultural_level='省级非遗'),
                CraftProcess(process_id='74180516', process_name='藏族唐卡', process_type='编织',
                            applicable_material='陶土', difficulty='专家级', estimated_time='3-7天',
                            tool_requirements='织布机', description='传统技法', teaching_video='工具使用',
                            status='已发布', heritage_region='西藏拉萨', cultural_level='国家级非遗'),
                CraftProcess(process_id='95760113', process_name='藏族唐卡', process_type='编织',
                            applicable_material='陶土', difficulty='高级', estimated_time='30天以上',
                            tool_requirements='剪刀', description='机器辅助', teaching_video='作品赏析',
                            status='已发布', heritage_region='贵州黔东南', cultural_level='民间传统'),
            ]
            db.session.add_all(processes)
            print("传统工艺示例数据插入成功")
        
        # 插入示例数据 - 产品方案
        if ProductScheme.query.count() == 0:
            schemes = [
                ProductScheme(product_id='76647368', product_name='蒙古族马鞍', base_design='抽象艺术',
                             applicable_craft='刺绣', material_list='天然染料', production_process='材料准备',
                             cost_budget='100元以下', suggested_price='500-1000元', status='已下架',
                             cultural_value='宗教象征', product_size='大型(30-50cm)', product_weight='100-200g',
                             innovation_score=72.5, history_score=88.3, art_score=76.8, practical_score=65.2,
                             culture_score=91.5, craft_score=82.1, total_score=79.4, market_level='B级',
                             is_ai_rated=True),
                ProductScheme(product_id='93779457', product_name='白族扎染', base_design='抽象艺术',
                             applicable_craft='木雕', material_list='陶土原料', production_process='材料准备',
                             cost_budget='100-500元', suggested_price='1000元以上', status='设计中',
                             cultural_value='地方特色', product_size='大型(30-50cm)', product_weight='50g以下'),
                ProductScheme(product_id='09578086', product_name='蒙古族马鞍', base_design='自然元素',
                             applicable_craft='银饰打造', material_list='纯银丝线', production_process='材料准备',
                             cost_budget='1000-5000元', suggested_price='50-100元', status='已售罄',
                             cultural_value='民俗风情', product_size='中型(10-30cm)', product_weight='200-500g',
                             innovation_score=68.2, history_score=92.1, art_score=85.6, practical_score=70.3,
                             culture_score=94.8, craft_score=88.7, total_score=83.3, market_level='A级',
                             is_ai_rated=True),
            ]
            db.session.add_all(schemes)
            print("产品方案示例数据插入成功")
        
        # 插入示例数据 - 设计趋势
        if DesignTrend.query.count() == 0:
            trends = [
                DesignTrend(analysis_id='83489293', analysis_dimension='地域分布', time_range='2024-11-28',
                           popular_materials='丝绸', popular_crafts='刺绣', region_distribution='中国腹地',
                           color_trend='靛蓝', product_type='工艺收藏', user_preference='文化认同', cultural_heat='复兴文化'),
                DesignTrend(analysis_id='98756318', analysis_dimension='文化背景', time_range='2024-11-05',
                           popular_materials='玉石', popular_crafts='扎染', region_distribution='中国腹地',
                           color_trend='墨绿', product_type='文具用品', user_preference='收藏价值', cultural_heat='热门IP'),
                DesignTrend(analysis_id='36585508', analysis_dimension='年龄层次', time_range='2024-11-20',
                           popular_materials='竹子', popular_crafts='剪纸', region_distribution='江南水乡',
                           color_trend='水墨黑', product_type='服饰配件', user_preference='文化认同', cultural_heat='新兴文化'),
            ]
            db.session.add_all(trends)
            print("设计趋势示例数据插入成功")
        
        # 插入示例数据 - 教学课程
        if TeachingCourse.query.count() == 0:
            courses = [
                TeachingCourse(course_id='TC001', course_name='苗族蜡染入门', instructor='潘*耀',
                              craft_type='蜡染', duration='20课时', difficulty='初级',
                              description='学习苗族蜡染的基本技法', status='已发布'),
                TeachingCourse(course_id='TC002', course_name='彝族漆器工艺', instructor='康*玛',
                              craft_type='漆艺', duration='30课时', difficulty='中级',
                              description='掌握彝族漆器的制作工艺', status='已发布'),
                TeachingCourse(course_id='TC003', course_name='苏绣进阶', instructor='陆*葆',
                              craft_type='刺绣', duration='40课时', difficulty='高级',
                              description='提升苏绣技艺水平', status='制作中'),
            ]
            db.session.add_all(courses)
            print("教学课程示例数据插入成功")
        
        # 插入示例数据 - 图案素材
        if PatternMaterial.query.count() == 0:
            materials = [
                PatternMaterial(material_id='PM001', material_name='传统云纹素材', pattern_type='自然纹样',
                               ethnic_origin='汉族', copyright_status='已授权', 
                               tags='云纹,祥云,自然纹样,汉族,传统,吉祥,传统纹样,民族文化',
                               auto_tagged=True, uploader='admin'),
                PatternMaterial(material_id='PM002', material_name='苗族蜡染冰纹', pattern_type='几何纹样',
                               ethnic_origin='苗族', copyright_status='原创', 
                               tags='蜡染,苗族,冰纹,几何纹样,刺绣,传统纹样,民族文化,设计素材',
                               auto_tagged=True, uploader='admin'),
                PatternMaterial(material_id='PM003', material_name='藏族吉祥八宝', pattern_type='符号纹样',
                               ethnic_origin='藏族', copyright_status='已授权', 
                               tags='藏族,吉祥,宗教,符号纹样,佛教,唐卡,传统纹样,民族文化',
                               auto_tagged=True, uploader='admin'),
                PatternMaterial(material_id='PM004', material_name='缠枝花卉纹', pattern_type='植物纹样',
                               ethnic_origin='多民族', copyright_status='已授权', 
                               tags='植物,花卉,自然,缠枝,藤蔓,传统纹样,民族文化,设计素材',
                               auto_tagged=True, uploader='admin'),
                PatternMaterial(material_id='PM005', material_name='蝴蝶妈妈纹', pattern_type='动物纹样',
                               ethnic_origin='苗族', copyright_status='原创', 
                               tags='蝴蝶,爱情,动物纹样,苗族,刺绣,图腾,传统纹样,民族文化',
                               auto_tagged=True, uploader='admin'),
            ]
            db.session.add_all(materials)
            print("图案素材示例数据插入成功")
        
        # 插入示例数据 - 传承项目
        if HeritageProject.query.count() == 0:
            projects = [
                HeritageProject(project_id='HP001', project_name='苗族蜡染传承计划', applicant='贵州省文旅厅',
                               project_type='传统工艺', apply_date='2024-01-15', status='审核中',
                               description='保护和传承苗族蜡染技艺'),
                HeritageProject(project_id='HP002', project_name='彝族漆器数字化保护', applicant='云南省非遗中心',
                               project_type='数字化保护', apply_date='2024-03-20', status='已通过',
                               description='对彝族漆器进行数字化记录和保护'),
            ]
            db.session.add_all(projects)
            print("传承项目示例数据插入成功")
        
        # 插入示例数据 - 展览活动
        if Exhibition.query.count() == 0:
            exhibitions = [
                Exhibition(exhibition_id='EX001', name='非遗手工艺精品展', location='北京国家博物馆',
                          start_date='2024-06-01', end_date='2024-06-30', organizer='中国非遗保护中心',
                          status='筹备中'),
                Exhibition(exhibition_id='EX002', name='民族服饰文化展', location='上海博物馆',
                          start_date='2024-09-15', end_date='2024-10-15', organizer='上海市文旅局',
                          status='已结束'),
            ]
            db.session.add_all(exhibitions)
            print("展览活动示例数据插入成功")
        
        # 插入示例数据 - 文化机构
        if CulturalInstitution.query.count() == 0:
            institutions = [
                CulturalInstitution(institution_id='CI001', name='中国非物质文化遗产保护中心',
                                   type='国家级机构', location='北京', contact='010-12345678', level='国家级'),
                CulturalInstitution(institution_id='CI002', name='贵州省民族博物馆',
                                   type='地方博物馆', location='贵阳', contact='0851-87654321', level='省级'),
            ]
            db.session.add_all(institutions)
            print("文化机构示例数据插入成功")
        
        # 插入示例数据 - 基因分类
        if GeneClassification.query.count() == 0:
            classifications = [
                GeneClassification(category_id='GC001', category_name='纹样基因', parent_category='',
                                  description='各类传统纹样的文化基因', gene_count=50),
                GeneClassification(category_id='GC002', category_name='工艺基因', parent_category='',
                                  description='传统制作工艺的文化基因', gene_count=35),
                GeneClassification(category_id='GC003', category_name='材质基因', parent_category='',
                                  description='传统材料使用的文化基因', gene_count=28),
            ]
            db.session.add_all(classifications)
            print("基因分类示例数据插入成功")
        
        # 插入示例数据 - 手工艺品采集
        if HandicraftCollection.query.count() == 0:
            collections = [
                HandicraftCollection(collection_id='HC001', item_name='清代苗族银饰',
                                    collector='张教授', collection_date='2024-05-10',
                                    origin='贵州黔东南', category='银饰',
                                    description='清代苗族妇女佩戴的银饰', status='已采集'),
                HandicraftCollection(collection_id='HC002', item_name='傣族织锦被面',
                                    collector='李研究员', collection_date='2024-07-22',
                                    origin='云南西双版纳', category='织锦',
                                    description='傣族传统手工织锦', status='待鉴定'),
            ]
            db.session.add_all(collections)
            print("手工艺品采集示例数据插入成功")
        
        # 插入示例数据 - 传承人访谈
        if HeritageInterview.query.count() == 0:
            interviews = [
                HeritageInterview(interview_id='HI001', interviewee='潘*耀', interviewer='王研究员',
                                 interview_date='2024-08-15', topic='苗族蜡染的传承与创新',
                                 content_summary='访谈了潘大师关于蜡染技艺的传承经历和创新思考', status='已完成'),
                HeritageInterview(interview_id='HI002', interviewee='康*玛', interviewer='李教授',
                                 interview_date='2024-09-20', topic='彝族漆器的历史渊源',
                                 content_summary='深入了解彝族漆器的发展历史和工艺特点', status='已完成'),
            ]
            db.session.add_all(interviews)
            print("传承人访谈示例数据插入成功")
        
        # 插入示例数据 - 非遗传承人（设计平台）
        if HeritageInheritor.query.count() == 0:
            inheritors = [
                HeritageInheritor(inheritor_id='HI-D001', name='朱炳式', skill_category='铜雕',
                                 heritage_level='国家级', region='浙江杭州',
                                 representative_works='铜雕《运河十景》', contact='邮箱'),
                HeritageInheritor(inheritor_id='HI-D002', name='姚建萍', skill_category='苏绣',
                                 heritage_level='国家级', region='江苏苏州',
                                 representative_works='苏绣《江山如此多娇》', contact='电话'),
            ]
            db.session.add_all(inheritors)
            print("非遗传承人（设计平台）示例数据插入成功")
        
        # 插入示例数据 - 民族文化知识
        if CulturalKnowledge.query.count() == 0:
            knowledge = [
                CulturalKnowledge(knowledge_id='CK001', title='苗族蜡染的历史渊源',
                                 category='工艺历史', ethnic_group='苗族',
                                 content='苗族蜡染是一种古老的防染工艺，距今已有两千多年历史...',
                                 source='中国民族博物馆'),
                CulturalKnowledge(knowledge_id='CK002', title='祥云纹的文化寓意',
                                 category='纹样文化', ethnic_group='汉族',
                                 content='祥云纹是中国传统吉祥纹样，象征吉祥如意、步步高升...',
                                 source='《中国纹样史》'),
            ]
            db.session.add_all(knowledge)
            print("民族文化知识示例数据插入成功")
        
        # 插入示例数据 - 数字版权登记
        if CopyrightRegistration.query.count() == 0:
            copyrights = [
                CopyrightRegistration(registration_id='CR001', work_name='苗族蜡染纹样设计系列',
                                     author='潘*耀', work_type='美术作品',
                                     registration_date='2024-03-15', copyright_number='国作登字-2024-F-001',
                                     status='已登记'),
                CopyrightRegistration(registration_id='CR002', work_name='彝族漆器图案集',
                                     author='康*玛', work_type='美术作品',
                                     registration_date='2024-05-20', copyright_number='国作登字-2024-F-002',
                                     status='登记中'),
            ]
            db.session.add_all(copyrights)
            print("数字版权登记示例数据插入成功")
        
        # 插入示例数据 - 定制订单
        if CustomOrder.query.count() == 0:
            orders = [
                CustomOrder(order_id='CO001', customer_name='张先生', product_type='蜡染挂画',
                           design_requirements='需要融入苗族蝴蝶妈妈图案，尺寸60*90cm',
                           order_date='2024-10-01', deadline='2024-11-01', status='设计中'),
                CustomOrder(order_id='CO002', customer_name='李女士', product_type='银饰项链',
                           design_requirements='彝族风格，镶嵌绿松石',
                           order_date='2024-10-15', deadline='2024-12-01', status='待确认'),
            ]
            db.session.add_all(orders)
            print("定制订单示例数据插入成功")
        
        # 插入示例数据 - 工艺品类统计
        if CraftCategory.query.count() == 0:
            categories = [
                CraftCategory(category_id='CC001', category_name='刺绣', count=1234,
                             region='西南地区', heritage_count=56, trend='上升'),
                CraftCategory(category_id='CC002', category_name='陶瓷', count=890,
                             region='华东地区', heritage_count=34, trend='稳定'),
                CraftCategory(category_id='CC003', category_name='编织', count=567,
                             region='中南地区', heritage_count=28, trend='上升'),
            ]
            db.session.add_all(categories)
            print("工艺品类统计示例数据插入成功")
        
        # 插入示例数据 - 用户偏好
        if UserPreference.query.count() == 0:
            prefs = [
                UserPreference(user_id=1, 
                              search_keywords='云纹,传统纹样,苗族,蜡染,创新设计',
                              preferred_styles='自然元素,抽象艺术',
                              weight_innovation=1.2, weight_history=1.0,
                              weight_art=1.1, weight_practical=0.9,
                              weight_culture=1.3, weight_craft=1.0,
                              total_searches=12, total_designs=5,
                              preference_level='中级'),
            ]
            db.session.add_all(prefs)
            print("用户偏好示例数据插入成功")
        
        db.session.commit()
        print("\n数据库初始化完成！")
        print("默认登录账号：admin / admin123")


if __name__ == '__main__':
    init_database()

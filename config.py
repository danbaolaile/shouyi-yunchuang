import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shouyi-yunchuang-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'shouyi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 系统配置
    SYSTEMS = {
        'database': {
            'name': '民族手工艺数据库系统',
            'theme_color': '#E09456',
            'theme_color_light': '#F5C79A',
            'description': '民族手工艺传承与保护综合信息管理平台'
        },
        'gene': {
            'name': '文化基因智能识别系统',
            'theme_color': '#0277BD',
            'theme_color_light': '#4FC3F7',
            'description': '非物质文化遗产保护与传承智能化平台'
        },
        'design': {
            'name': '民族手工艺品智能生成设计平台',
            'theme_color': '#26A69A',
            'theme_color_light': '#80CBC4',
            'description': '民族手工艺品设计与传承智能化系统'
        }
    }

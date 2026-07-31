from flask import Flask, redirect, url_for, send_from_directory
from flask_login import LoginManager, current_user
from config import Config
from models import db, User
import os

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录系统'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # 注册蓝图
    from routes.auth import auth_bp
    from routes.database_system.main import database_bp
    from routes.gene_system.main import gene_bp
    from routes.design_system.main import design_bp
    from routes.customer.main import customer_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(database_bp, url_prefix='/database')
    app.register_blueprint(gene_bp, url_prefix='/gene')
    app.register_blueprint(design_bp, url_prefix='/design')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    
    # 上传文件访问路由
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        uploads_dir = os.path.join(app.root_path, 'uploads')
        return send_from_directory(uploads_dir, filename)
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('database.index'))
        return redirect(url_for('auth.login'))
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

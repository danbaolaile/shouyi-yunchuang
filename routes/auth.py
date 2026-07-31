from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('database.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        system = request.form.get('system', 'database')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            
            if system == 'database':
                return redirect(next_page or url_for('database.index'))
            elif system == 'gene':
                return redirect(next_page or url_for('gene.index'))
            elif system == 'design':
                return redirect(next_page or url_for('design.index'))
            else:
                return redirect(next_page or url_for('database.index'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

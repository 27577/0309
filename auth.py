from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# 创建一个 Blueprint 对象
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 示例登录逻辑
        if username == "admin" and password == "password":
            session['username'] = username
            flash('You were successfully logged in', 'success')
            return redirect(url_for('index'))  # 修改为你的主页路由
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 这里添加注册逻辑
        flash('Registration is not implemented.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

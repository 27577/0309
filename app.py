from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from sqlalchemy import text  # 导入 text 函数
import subprocess
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKeyHere'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:9417@localhost/new_schema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
from models import *
# import models
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')  # 直接使用提交的密码
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user is None:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully. Please login.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.')
            
    return render_template('register.html')

# 登录逻辑调整为直接比较密码
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')  # 直接使用提交的密码进行比较
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('workbench'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/users')
def view_users():
    users = User.query.all()  # 获取所有用户
    return render_template('view_users.html', users=users)

@app.route('/verify-delete', methods=['GET', 'POST'])
def verify_delete():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '9417':
            # 密码正确，重定向到删除用户的页面
            return redirect(url_for('delete_users'))
        else:
            flash('Incorrect password. Please try again.')
            return redirect(url_for('verify_delete'))
    return render_template('verify_delete.html')


@app.route('/delete-users', methods=['GET', 'POST'])
def delete_users():
    
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f'User {username} has been deleted.')
        else:
            flash('User not found.')
        return redirect(url_for('delete_users'))
    return render_template('delete_users.html')


@app.route('/workbench')
def workbench():
    if 'username' in session:
        return render_template('workbench.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/customer_search', methods=['GET'])
def customer_search():
    # 渲染客户信息查询表单页面
    return render_template('customer_search.html')

@app.route('/customer_search_results', methods=['POST'])
def customer_search_results():
    customer_name = request.form.get('customerName')
    # 根据客户名称查询数据库
    customer = Customer.query.filter_by(c_name=customer_name).first()
    if customer:
        # 如果找到客户，渲染一个页面来显示客户信息
        return render_template('customer_details.html', customer=customer)
    else:
        # 如果没有找到客户，显示提示信息
        flash('没有找到该客户的信息')
        return redirect(url_for('customer_search'))

@app.route('/database-info')
def database_info():
    engine = db.get_engine()
    connection = engine.connect()
    
    # 确保 SQL 查询是以字符串的形式并使用 text 函数
    version_query = text("SELECT VERSION();")
    # 执行查询
    version_result = connection.execute(version_query).fetchone()
    
    # 获取数据库URL
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    
    buffer_query = text("SHOW VARIABLES LIKE 'innodb_buffer_pool_size';")
    buffer_result = connection.execute(buffer_query).fetchone()
    
    # 将结果转换为更易读的格式（例如，转换字节为MB）
    buffer_size_mb = int(buffer_result[1]) / 1024 / 1024 if buffer_result else "N/A"

  
        # 提取数据库连接信息
    db_info = {
        'database_url': db_url,
        'database_server_version': version_result[0],
        'database_buffer_size_mb': buffer_size_mb,
        
    }
    
    connection.close()
    
    return render_template('database_info.html', db_info=db_info)

@app.route('/change-database-info', methods=['GET', 'POST'])
def database_changeInfo():
    if request.method == 'POST':
        # 从表单获取连接时长并存储到 session
        session['connection_duration'] = request.form.get('connectionDuration')
        flash('数据库连接时长已更新。', 'success')
  
        return redirect(url_for('database_changeInfo'))
    
    # 从 session 获取连接时长以显示在表单上
    connection_duration = session.get('connection_duration', 1)
    return render_template('database_changeInfo.html', connection_duration=connection_duration)

@app.route('/data_gen', methods=['GET'])
def data_gen():
    # 显示命令输入表单
    return render_template('data_gen.html')
@app.route('/exe_gen', methods=['POST'])
def exe_gen():
    command_input = request.form['command']
    # 构建命令行命令
    dbgen_path = r"C:\Users\27577\Desktop\tools\教材\大三下\数据库\数据库系统原理课程设计-2-TPC电商数据管理系统\TPC-H\dbgen"
    command = f"dbgen.exe {command_input}"
    input_data = ('y\n'*8).encode('utf-8')
    try:
        # 执行命令
        subprocess.run(command, input=input_data,check=True, shell=True, cwd=dbgen_path)
        return "Command executed successfully."
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"
    
@app.route('/data_imp')
def data_imp():
    try:
        # 在新的cmd窗口中启动MySQL客户端，并尝试自动输入密码（注意：这可能不会按预期工作）
        command = 'cmd.exe /c start cmd.exe /k "mysql --local-infile=1 -u root -p9417 new_schema < load_data.txt"'
        subprocess.Popen(command, shell=True)
        return "Attempting to open MySQL client in a new terminal window..."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)



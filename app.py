from flask import Flask, render_template, request, redirect, url_for, flash, session,send_file, make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from sqlalchemy import text  # 导入 text 函数
import subprocess
import pandas as pd
import io
from io import BytesIO
import time
import os
from concurrent.futures import ThreadPoolExecutor,as_completed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKeyHere'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:9417@localhost/new_schema?local_infile=1'
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
            flash('注册成功')
            return redirect(url_for('login'))
        else:
            flash('该用户已存在')
            
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
            flash('账号或密码错误')
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
            flash('密码错误')
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
            flash(f'用户 {username} 已删除')
        else:
            flash('用户不存在')
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

def get_all_customers():
    return Customer.query.all()


@app.route('/all_customers')
def all_customers():
    # 假设有一个函数 get_all_customers 来获取所有客户信息
    customers = get_all_customers()
    # 为了演示，我们使用一个固定的客户列表
    # customers = [{'id': 1, 'name': '客户A'}, {'id': 2, 'name': '客户B'}]
    return render_template('all_customers.html', customers=customers)

@app.route('/customer_details/<customer_name>')
def customer_details(customer_name):
    # 使用 SQLAlchemy 查询特定名称的客户
    customer = Customer.query.filter_by(c_name=customer_name).first()
    
    # 如果没有找到客户，返回 404 错误
    
    
    return render_template('customer_details.html', customer=customer)

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
    dbgen_path = "dbgen"
    command = f"dbgen.exe {command_input}"
    try:
        # 执行命令
        subprocess.run(command,check=True, shell=True, cwd=dbgen_path)
        return "Command executed successfully."
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"
    
@app.route('/data_imp_all')
def data_imp_all():
    try:
        # 在新的cmd窗口中启动MySQL客户端，并尝试自动输入密码
        command = 'cmd.exe /c start cmd.exe /k "mysql --local-infile=1 -u root -p9417 new_schema < load_data.txt"'
        subprocess.Popen(command, shell=True)
        return "Attempting to open MySQL client in a new terminal window..."
    except Exception as e:
        return f"An error occurred: {e}"

def run_command(command):
    start_time = time.time()
    subprocess.run(command, shell=True, check=True)
    end_time = time.time()
    return end_time-start_time

@app.route('/concurrency_test_args',methods=['GET'])
def concurrency_test_args():
    return render_template('concurrency_test_args.html')

@app.route('/concurrency_test', methods=['GET', 'POST'])
def concurrency_test():
    concurrency_num = int(request.values.get('concurrency_num'))
    durations = []
    disql_path="mysql -u root -p9417 new_schema < queries"
    commands = [
    disql_path + "\\" + "d3.sql",
    disql_path + "\\" + "d4.sql",
    disql_path + "\\" + "d6.sql",
    disql_path + "\\" + "d9.sql",
    disql_path + "\\" + "d13.sql",
    ]
    start=time.time()
    with ThreadPoolExecutor(max_workers=concurrency_num) as executor:
    
        future_to_command = {executor.submit(run_command, cmd): cmd for cmd in commands}
        for future in as_completed(future_to_command):
            duration = future.result()
            durations.append(duration)
    # 计算平均延迟和吞吐量
    end= time.time()
    actual_time=end-start
    total_time = sum(durations)
    average_latency = actual_time / len(commands)
    throughput = len(commands) / actual_time
    
    # 将结果作为 JSON 返回
    results = {
        
        "average_latency": average_latency,
        "throughput": throughput,
        "total_execution_time": total_time,
        "actual_time":actual_time
    }

    return render_template('concurrency_test.html', results=results)

@app.route('/multi_user_args',methods=['GET'])
def multi_user_args():
    return render_template('multi_user_args.html')

@app.route('/multi_user', methods=['GET', 'POST'])
def multi_user():
    user_num = int(request.values.get('user_num'))
    query_num = int(request.values.get('query_num'))
    key_num = int(request.values.get('key_num'))
    iter_num= int(request.values.get('iter_num'))
    command = f"mysqlslap -uroot -p9417 --iterations={iter_num} --concurrency={user_num} --number-of-queries={query_num} --number-int-cols={key_num} --number-char-cols={key_num} --auto-generate-sql"
    
    # Execute the command and capture its output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    
    if process.returncode == 0:
        return render_template('multi_user.html', output=output.decode('utf-8'))
    else:
        return "error"


def split_file(original_file, line_count=50):
    with open(original_file, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()

    # 使用original_file的基础名称（不含扩展名）作为目录名的一部分
    base_name = os.path.splitext(os.path.basename(original_file))[0]
    output_folder = f'split/{base_name}_split'
    
    # 确保文件夹存在，用于存放分割后的文件
    os.makedirs(output_folder, exist_ok=True)

    file_index = 1
    for i in range(0, len(file_lines), line_count):
        part_file_path = os.path.join(output_folder, f'{file_index}.tbl')
        with open(part_file_path, 'w', encoding='utf-8') as file:
            file.writelines(file_lines[i:i+line_count])
        file_index += 1

    return file_index - 1  # 返回创建的文件数

@app.route('/data_split')
def data_split():
    path0='clean_data/'
    path_customer=os.path.join(path0,'clean_customer.tbl')
    path_lineitem=os.path.join(path0,'clean_lineitem.tbl')
    path_nation=os.path.join(path0,'clean_nation.tbl')
    path_orders=os.path.join(path0,'clean_orders.tbl')
    path_part=os.path.join(path0,'clean_part.tbl')
    path_partsupp=os.path.join(path0,'clean_partsupp.tbl')
    path_region=os.path.join(path0,'clean_region.tbl')
    path_supplier=os.path.join(path0,'clean_supplier.tbl')
   
    region_num=split_file(path_region)
    customer_num=split_file(path_customer)
    lineitem_num =split_file(path_lineitem)
    nation_num=split_file(path_nation)
    orders_num=split_file(path_orders)
    part_num=split_file(path_part)
    partsupp_num=split_file(path_partsupp)
    supplier_num=split_file(path_supplier)
    page_table={region_num,customer_num,lineitem_num,nation_num,orders_num,part_num,partsupp_num,supplier_num}
    return page_table

@app.route('/data_imp')
def data_imp():

    region_num=len(os.listdir("split\clean_region_split"))
    customer_num=len(os.listdir("split\clean_customer_split"))
    lineitem_num=len(os.listdir("split\clean_lineitem_split"))
    print(region_num)
    print(customer_num)
    print(lineitem_num)
    
    engine = db.get_engine()
    with engine.connect() as conn:
        # 使用 text() 封装 SQL 字符串
        conn.execute(text("""set global local_infile = 'ON';"""))
        region_folder_path = "split/clean_region_split"
        for i in range(1, region_num + 1):
            file_path = region_folder_path+ f'/{i}.tbl'
            
            # 构建SQL查询，动态插入文件路径
            region_sql_query = text(f"""
                LOAD DATA LOCAL INFILE '{file_path}'
                INTO TABLE REGION
                FIELDS TERMINATED BY '|' 
                LINES TERMINATED BY '\n'
                (R_REGIONKEY, R_NAME, R_COMMENT);
            """)
        customer_folder_path = "split/clean_customer_split"
        for i in range(1, customer_num + 1):
            file_path = customer_folder_path+ f'/{i}.tbl'
            
            # 构建SQL查询，动态插入文件路径
            customer_sql_query = text(f"""
                LOAD DATA LOCAL INFILE '{file_path}'
                INTO TABLE CUSTOMER
                FIELDS TERMINATED BY '|'
                LINES TERMINATED BY '\n'
                (C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL, C_MKTSEGMENT, C_COMMENT);


            """)
        # lineitem_folder_path = "split/clean_lineitem_split"
        # for i in range(1, lineitem_num + 1):
        #     file_path = lineitem_folder_path+ f'/{i}.tbl'
            
        #     # 构建SQL查询，动态插入文件路径
        #     lineitem_sql_query = text(f"""
        #         LOAD DATA LOCAL INFILE '{file_path}'
        #         INTO TABLE LINEITEM
        #         FIELDS TERMINATED BY '|'
        #         LINES TERMINATED BY '\n'
        #         (L_ORDERKEY, L_PARTKEY, L_SUPPKEY, L_LINENUMBER, L_QUANTITY, L_EXTENDEDPRICE, L_DISCOUNT, L_TAX, L_RETURNFLAG, L_LINESTATUS, L_SHIPDATE, L_COMMITDATE, L_RECEIPTDATE, L_SHIPINSTRUCT, L_SHIPMODE, L_COMMENT);


        #     """)
        
            
            # 执行SQL查询导入数据
            
            conn.execute(region_sql_query)
            conn.execute(customer_sql_query)
            # conn.execute(lineitem_sql_query)

    return("import success")

@app.route('/data_clean')
def data_clean():
    with open('clean.py', 'r') as file:
        exec(file.read(),globals())
    return ("clean success")
    


def get_tables():
    engine = db.get_engine()
    with engine.connect() as conn:
        # 使用 text() 封装 SQL 字符串
        result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
    return tables


@app.route('/show_tables')
def show_tables():
    tables = get_tables()
    return render_template('tables.html', tables=tables)

@app.route('/download_table/<table_name>')
def download_table(table_name):
    engine = db.get_engine()
    df = pd.read_sql_table(table_name, con=engine)

    # 使用 BytesIO 替代 StringIO
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name=f"{table_name}.csv", mimetype='text/csv')
@app.route('/order_priority',methods=['GET', 'POST'])
def order_priority():
    o_orderdate = request.values.get('o_orderdate')  
    if not o_orderdate:
        o_orderdate = '2016-07-01'
    engine = db.get_engine()
    with engine.connect() as conn:
        # 使用 text() 封装 SQL 字符串
        sql_query = text("""
            SELECT
                o_orderpriority,
                count(*) as order_count
            FROM
                orders
            WHERE
                o_orderdate >= :o_orderdate
                AND o_orderdate < date :o_orderdate + interval '3' month
                AND EXISTS (
                    SELECT
                        *
                    FROM
                        lineitem
                    WHERE
                        l_orderkey = o_orderkey
                        AND l_commitdate < l_receiptdate
                )
            GROUP BY
                o_orderpriority
            ORDER BY
                o_orderpriority;
        """)
        start_time = time.time()
        result = conn.execute(sql_query,{'o_orderdate': o_orderdate}).fetchall()
        end_time = time.time()
        execution_time=end_time-start_time
        
    return render_template('order_priority.html', results=result,execution_time=execution_time)

@app.route('/part_supplier')
def part_supplier():
    engine = db.get_engine()
    with engine.connect() as conn:
        sql_query = text("""
            select
                p_brand,
                p_type,
                p_size,
                count(distinct ps_suppkey) as supplier_cnt
            from
                partsupp,
                part
            where
                p_partkey = ps_partkey
                and p_brand <> 'Brand#45'
                and p_type not like 'MEDIUM POLISHED%'
                and p_size in (49, 14, 23, 45, 19, 3, 36, 9)
                and ps_suppkey not in (
                    select
                        s_suppkey
                    from
                        supplier
                    where
                        s_comment like '%Customer%Complaints%'
                )
            group by
                p_brand,
                p_type,
                p_size
            order by
                supplier_cnt desc,
                p_brand,
                p_type,
                p_size;

        """)
        start_time = time.time()
        result = conn.execute(sql_query).fetchall()
        end_time = time.time()
        execution_time=end_time-start_time
        
    return render_template('part_supplier_relation.html', results=result,execution_time=execution_time)

@app.route('/discount_salary' ,methods=['GET', 'POST'])
def discount_salary():
    p_brand = request.values.get('p_brand')  
    if not p_brand:
        p_brand = 'Brand#12'
    engine = db.get_engine()
    with engine.connect() as conn:
        sql_query = text("""
            select
                sum(l_extendedprice* (1 - l_discount)) as revenue
            from
                lineitem,
                part
            where
                (
                    p_partkey = l_partkey
                    and p_brand = :p_brand
                    and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
                    and l_quantity >= 1 and l_quantity <= 1 + 10
                    and p_size between 1 and 5
                    and l_shipmode in ('AIR', 'AIR REG')
                    and l_shipinstruct = 'DELIVER IN PERSON'
                )
                or
                (
                    p_partkey = l_partkey
                    and p_brand = 'Brand#23'
                    and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
                    and l_quantity >= 10 and l_quantity <= 10 + 10
                    and p_size between 1 and 10
                    and l_shipmode in ('AIR', 'AIR REG')
                    and l_shipinstruct = 'DELIVER IN PERSON'
                )
                or
                (
                    p_partkey = l_partkey
                    and p_brand = 'Brand#34'
                    and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
                    and l_quantity >= 20 and l_quantity <= 20 + 10
                    and p_size between 1 and 15
                    and l_shipmode in ('AIR', 'AIR REG')
                    and l_shipinstruct = 'DELIVER IN PERSON'
                );


        """)
        start_time = time.time()
        result = conn.execute(sql_query,{'p_brand': p_brand}).fetchall()
        end_time = time.time()
        execution_time=end_time-start_time
        
    return render_template('discount_salary.html', results=result,execution_time=execution_time)

@app.route('/little_order_args', methods=['GET'])
def little_order_args():
    # 渲染客户信息查询表单页面
    return render_template('little_order_args.html')

@app.route('/order_priority_args', methods=['GET'])
def order_priority_args():
    # 渲染客户信息查询表单页面
    return render_template('order_priority_args.html')

@app.route('/discount_salary_args', methods=['GET'])
def discount_salary_args():
    # 渲染客户信息查询表单页面
    return render_template('discount_salary_args.html')

@app.route('/little_order_salary', methods=['GET', 'POST'])
def little_order_salary():
    # Retrieve parameters from query string
    p_brand = request.values.get('p_brand')  # Default to 'Brand#23' if not specified
    p_container = request.values.get('p_container')  # Default to 'MED BOX' if not specified
    if not p_brand:
        p_brand = 'Brand#23'
    if not p_container:
        p_container = 'MED BOX'
 
    engine = db.get_engine()
    with engine.connect() as conn:
        # Prepare your SQL query using bound parameters
        sql_query = text("""
            select
                sum(l_extendedprice) / 7.0 as avg_yearly
            from
                lineitem,
                part
            where
                p_partkey = l_partkey
                and p_brand = :p_brand
                and p_container = :p_container
                and l_quantity < (
                    select
                        0.2 * avg(l_quantity)
                    from
                        lineitem
                    where
                        l_partkey = p_partkey
                );

        """)

        # Execute the query safely with parameters
        start_time = time.time()
        # result = conn.execute(sql_query,p_brand=p_brand, p_container=p_container).fetchall()
        result = conn.execute(sql_query, {'p_brand': p_brand, 'p_container': p_container}).fetchall()

        end_time = time.time()
        execution_time = end_time - start_time
        
    return render_template('little_order_salary.html', results=result,execution_time=execution_time)

@app.route('/repo_igni')
def repo_igni():
    engine = db.get_engine()
    with engine.connect() as conn:
        sql_query = text("""
            select
                ps_partkey,
                sum(ps_supplycost * ps_availqty) as value
            from
                partsupp,
                supplier,
                nation
            where
                ps_suppkey = s_suppkey
                and s_nationkey = n_nationkey
                and n_name = 'GERMANY'
            group by
                ps_partkey having
                    sum(ps_supplycost * ps_availqty) > (
                        select
                            sum(ps_supplycost * ps_availqty) * 0.0001000000
                        from
                            partsupp,
                            supplier,
                            nation
                        where
                            ps_suppkey = s_suppkey
                            and s_nationkey = n_nationkey
                            and n_name = 'GERMANY'
                    )
            order by
                value desc;

        """)
        start_time = time.time()
        result = conn.execute(sql_query).fetchall()
        end_time = time.time()
        execution_time=end_time-start_time
        
    return render_template('repo_igni.html', results=result,execution_time=execution_time)


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)



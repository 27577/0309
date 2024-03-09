# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    
    o_orderkey = db.Column(db.Integer, primary_key=True)
    o_custkey = db.Column(db.Integer,db.ForeignKey('customer.c_custkey'), nullable=False)
    o_orderstatus = db.Column(db.CHAR(1), nullable=False)
    o_totalprice = db.Column(db.Numeric(15, 2), nullable=False)
    o_orderdate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    o_orderpriority = db.Column(db.CHAR(15), nullable=False)
    o_clerk = db.Column(db.CHAR(15), nullable=False)
    o_shippriority = db.Column(db.Integer, nullable=False)
    o_comment = db.Column(db.String(79), nullable=False)

class Supplier(db.Model):
    __tablename__ = 'supplier'
    
    s_suppkey = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.CHAR(25), nullable=False)
    s_address = db.Column(db.String(40), nullable=False)
    s_nationkey = db.Column(db.Integer, db.ForeignKey('nation.n_nationkey'), nullable=False)
    s_phone = db.Column(db.CHAR(15), nullable=False)
    s_acctbal = db.Column(db.Numeric(15, 2), nullable=False)
    s_comment = db.Column(db.String(101), nullable=False)

class Region(db.Model):
    __tablename__ = 'region'
    
    r_regionkey = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.CHAR(25), nullable=False)
    r_comment = db.Column(db.String(152), nullable=False)

class Nation(db.Model):
    __tablename__ = 'nation'
    
    n_nationkey = db.Column(db.Integer, primary_key=True)
    n_name = db.Column(db.CHAR(25), nullable=False)
    n_regionkey = db.Column(db.Integer, db.ForeignKey('region.r_regionkey'), nullable=False)
    n_comment = db.Column(db.String(152), nullable=False)

class Part(db.Model):
    __tablename__ = 'part'
    
    p_partkey = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(55), nullable=False)
    p_mfgr = db.Column(db.CHAR(25), nullable=False)
    p_brand = db.Column(db.CHAR(10), nullable=False)
    p_type = db.Column(db.String(25), nullable=False)
    p_size = db.Column(db.Integer, nullable=False)
    p_container = db.Column(db.CHAR(10), nullable=False)
    p_retailprice = db.Column(db.Numeric(15, 2), nullable=False)
    p_comment = db.Column(db.String(23), nullable=False)

class PartSupp(db.Model):
    __tablename__ = 'partsupp'
    
    # 定义复合主键
    ps_partkey = db.Column(db.Integer, db.ForeignKey('part.p_partkey'), primary_key=True)
    ps_suppkey = db.Column(db.Integer, db.ForeignKey('supplier.s_suppkey'), primary_key=True)
    
    ps_availqty = db.Column(db.Integer, nullable=False)
    ps_supplycost = db.Column(db.Numeric(15, 2), nullable=False)
    ps_comment = db.Column(db.String(199), nullable=False)

class Customer(db.Model):
    __tablename__ = 'customer'
    c_custkey = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(25), primary_key=True)
    c_address = db.Column(db.String(40), nullable=False)
    c_nationkey = db.Column(db.Integer, db.ForeignKey('nation.n_nationkey'),nullable=False)
    c_phone = db.Column(db.String(15), nullable=False)
    c_acctbal = db.Column(db.Numeric(15, 2), nullable=False)
    c_mktsegment = db.Column(db.String(10), nullable=False)
    c_comment = db.Column(db.String(117), nullable=False)
    


class LineItem(db.Model):
    __tablename__ = 'lineitem'
    
    l_orderkey = db.Column(db.Integer, db.ForeignKey('order.o_orderkey'),primary_key=True)
    l_partkey = db.Column(db.Integer,db.ForeignKey('part.p_prtkey'),nullable=False)
    l_suppkey = db.Column(db.Integer,db.ForeignKey('supplier.s_suppkey'),nullable=False)
    l_linenumber = db.Column(db.Integer, primary_key=True)
    
    l_quantity = db.Column(db.Numeric(15, 2), nullable=False)
    l_extendedprice = db.Column(db.Numeric(15, 2), nullable=False)
    l_discount = db.Column(db.Numeric(15, 2), nullable=False)
    l_tax = db.Column(db.Numeric(15, 2), nullable=False)
    l_returnflag = db.Column(db.CHAR(1), nullable=False)
    l_linestatus = db.Column(db.CHAR(1), nullable=False)
    l_shipdate = db.Column(db.Date, nullable=False)
    l_commitdate = db.Column(db.Date, nullable=False)
    l_receiptdate = db.Column(db.Date, nullable=False)
    l_shipinstruct = db.Column(db.CHAR(25), nullable=False)
    l_shipmode = db.Column(db.CHAR(10), nullable=False)
    l_comment = db.Column(db.String(44), nullable=False)




    
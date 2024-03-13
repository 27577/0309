import datetime
import os
def validate_orders(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 10:  # Ensure there are exactly 9 fields
            return False
        
        # Validate each field according to the Order class definition
        o_orderkey = int(fields[0])
        o_custkey = int(fields[1])
        o_orderstatus = fields[2]
        o_totalprice = float(fields[3])
        o_orderdate = datetime.datetime.strptime(fields[4], '%Y-%m-%d').date()
        o_orderpriority = fields[5]
        o_clerk = fields[6]
        o_shippriority = int(fields[7])
        o_comment = fields[8]
        if fields[9]!='':
            return False
        # Add additional checks for value ranges if necessary
        if not o_orderstatus in ['F', 'O', 'P']:  # Example check
            return False

        # Further checks for other fields can be added here
        
        return True
    except ValueError:  # Catches conversion errors
        return False
    except IndexError:  # Catches wrong number of fields
        return False

def validate_supplier(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 8:  # Ensure there are exactly 7 fields
            return False
        if fields[7]!='':
            return False
        # Validate each field according to the Supplier class definition
        s_suppkey = int(fields[0])
        s_name = fields[1]
        if len(s_name) > 25:
            return False
        s_address = fields[2]
        if len(s_address) > 40:
            return False
        s_nationkey = int(fields[3])
        s_phone = fields[4]
        if len(s_phone) > 15:
            return False
        s_acctbal = float(fields[5])  # Assuming db.Numeric can be represented as float here
        s_comment = fields[6]
        if len(s_comment) > 101:
            return False
        
        # Add additional checks for value ranges or other constraints if necessary
        
        return True
    except ValueError:  # Catches conversion errors for int and float fields
        return False
    except IndexError:  # Catches wrong number of fields
        return False

def validate_region(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 4:  # Ensure there are exactly 3 fields
            return False
        if fields[3]!='':
            return False
        # Validate each field according to the Region class definition
        r_regionkey = int(fields[0])  # Convert and validate r_regionkey
        r_name = fields[1]
        if len(r_name) > 25:  # Validate length of r_name
            return False
        r_comment = fields[2]
        if len(r_comment) > 152:  # Validate length of r_comment
            return False
        
        return True
    except ValueError:  # Catches conversion errors for integer fields
        return False
    except IndexError:  # Catches wrong number of fields
        return False

def validate_nation(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 5:  # Ensure there are exactly 4 fields
            return False
        if fields[4]!='':
            return False
        # Validate each field according to the Nation class definition
        n_nationkey = int(fields[0])  # Convert and validate n_nationkey
        n_name = fields[1]
        if len(n_name) > 25:  # Validate length of n_name
            return False
        n_regionkey = int(fields[2])  # Convert and validate n_regionkey
        n_comment = fields[3]
        if len(n_comment) > 152:  # Validate length of n_comment
            return False
        
        # Add additional checks for value ranges or other constraints if necessary
        
        return True
    except ValueError:  # Catches conversion errors for integer fields
        return False
    except IndexError:  # Catches wrong number of fields
        return False

def validate_part(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 10:  # Ensure there are exactly 9 fields
            return False
        if fields[9]!='':
            return False
        # Validate each field according to the Part class definition
        p_partkey = int(fields[0])
        p_name = fields[1]
        if len(p_name) > 55:
            return False
        p_mfgr = fields[2]
        if len(p_mfgr) > 25:
            return False
        p_brand = fields[3]
        if len(p_brand) > 10:
            return False
        p_type = fields[4]
        if len(p_type) > 25:
            return False
        p_size = int(fields[5])
        p_container = fields[6]
        if len(p_container) > 10:
            return False
        p_retailprice = float(fields[7])  # Assuming db.Numeric can be represented as float here
        p_comment = fields[8]
        if len(p_comment) > 23:
            return False
        
        # Add additional checks for value ranges or other constraints if necessary
        
        return True
    except ValueError:  # Catches conversion errors for int and float fields
        return False
    except IndexError:  # Catches wrong number of fields
        return False

def validate_partsupp(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 6:  # Ensure there are exactly 5 fields
            return False
        if fields[5]!='':
            return False
        # Validate primary key fields (converted to int, checked for validity)
        ps_partkey = int(fields[0])
        ps_suppkey = int(fields[1])

        # Validate ps_availqty as integer
        ps_availqty = int(fields[2])

        # Validate ps_supplycost as numeric, converting to float for simplicity
        ps_supplycost = float(fields[3])

        # Validate length of ps_comment
        ps_comment = fields[4]
        if len(ps_comment) > 199:
            return False

        # Further validations can be added as needed (e.g., range checks)

        return True
    except ValueError:  # Catches conversion errors for int and float fields
        return False
    except IndexError:  # Catches wrong number of fields
        return False

def validate_customer(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 9:  # Ensure there are exactly 8 fields
            return False
        if fields[8]!='':
            return False
        # Validate each field according to the Customer class definition
        c_custkey = int(fields[0])
        c_name = fields[1]
        if len(c_name) > 25:
            return False
        c_address = fields[2]
        if len(c_address) > 40:
            return False
        c_nationkey = int(fields[3])
        c_phone = fields[4]
        if len(c_phone) > 15:
            return False
        c_acctbal = float(fields[5])  # Assuming db.Numeric can be represented as float here
        c_mktsegment = fields[6]
        if len(c_mktsegment) > 10:
            return False
        c_comment = fields[7]
        if len(c_comment) > 117:
            return False

        # Additional value range or constraint checks can be added here as needed

        return True
    except ValueError:  # Catches conversion errors for int and float fields
        return False
    except IndexError:  # Catches wrong number of fields
        return False


def validate_lineitem(line):
    try:
        fields = line.strip().split('|')
        if len(fields) != 17:  # Ensure there are exactly 16 fields
            return False
        if fields[16]!='':
            return False
        # Convert and validate numeric fields
        l_orderkey = int(fields[0])
        l_partkey = int(fields[1])
        l_suppkey = int(fields[2])
        l_linenumber = int(fields[3])
        l_quantity = float(fields[4])
        l_extendedprice = float(fields[5])
        l_discount = float(fields[6])
        l_tax = float(fields[7])

        # Validate char fields for correct length
        l_returnflag = fields[8]
        if len(l_returnflag) != 1:
            return False
        l_linestatus = fields[9]
        if len(l_linestatus) != 1:
            return False

        # Convert and validate date fields
        l_shipdate = datetime.datetime.strptime(fields[10], '%Y-%m-%d').date()
        l_commitdate = datetime.datetime.strptime(fields[11], '%Y-%m-%d').date()
        l_receiptdate = datetime.datetime.strptime(fields[12], '%Y-%m-%d').date()

        # Validate char fields for correct length
        l_shipinstruct = fields[13]
        if len(l_shipinstruct) > 25:
            return False
        l_shipmode = fields[14]
        if len(l_shipmode) > 10:
            return False
        l_comment = fields[15]
        if len(l_comment) > 44:
            return False

        # Additional checks for value ranges or constraints can be added here

        return True
    except ValueError:  # Catches conversion errors for int, float, and date fields
        return False
    except IndexError:  # Catches wrong number of fields
        return False



def clear(name,input_path, output_dir, output_filename, error_log_filename):
    output_path = os.path.join(output_dir, output_filename)
    error_log_path = os.path.join(output_dir, error_log_filename)

    with open(input_path, 'r') as infile, \
         open(output_path, 'w') as outfile, \
         open(error_log_path, 'w') as errorfile:
        
        line_number = 1
        for line in infile:
            if eval(f"validate_{name}(line)"):
                outfile.write(line)
            else:
                errorfile.write(f'{line_number}\n')
            line_number += 1


# 路径和文件名
path0 = 'dbgen/'
path_clean = 'clean_data/'

input_orders = os.path.join(path0, 'orders.tbl')
input_customer = os.path.join(path0, 'customer.tbl')
input_lineitem = os.path.join(path0, 'lineitem.tbl')
input_nation = os.path.join(path0, 'nation.tbl')
input_part = os.path.join(path0, 'part.tbl')
input_partsupp = os.path.join(path0, 'partsupp.tbl')
input_region = os.path.join(path0, 'region.tbl')
input_supplier = os.path.join(path0, 'supplier.tbl')

output_orders = 'clean_orders.tbl'
output_customer = 'clean_customer.tbl'
output_lineitem = 'clean_lineitem.tbl'
output_nation = 'clean_nation.tbl'
output_part = 'clean_part.tbl'
output_partsupp = 'clean_partsupp.tbl'
output_region = 'clean_region.tbl'
output_supplier = 'clean_supplier.tbl'

error_orders = 'invalid_oders.log'
error_customer = 'invalid_customer.log'
error_lineitem = 'invalid_lineitem.log'
error_nation = 'invalid_nation.log'
error_part = 'invalid_part.log'
error_partsupp = 'invalid_partsupp.log'
error_region = 'invalid_region.log'
error_supplier = 'invalid_supplier.log'

clear("orders",input_orders, path_clean, output_orders, error_orders)
clear("customer",input_customer, path_clean, output_customer, error_customer)
clear("lineitem",input_lineitem, path_clean, output_lineitem, error_lineitem)
clear("nation",input_nation, path_clean, output_nation, error_nation)
clear("part",input_part, path_clean, output_part, error_part)
clear("partsupp",input_partsupp, path_clean, output_partsupp, error_partsupp)
clear("region",input_region, path_clean, output_region, error_region)
clear("supplier",input_supplier, path_clean, output_supplier, error_supplier)


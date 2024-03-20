import pymysql
import pandas as pd


def live_db_conn():
    conn = pymysql.connect(host='host', 
                           user='user', 
                           password='password',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor, 
                           db = "database")
    return conn

def load_data():

    conn = live_db_conn()
    curs = conn.cursor()

    sql = """
    SELECT o.id as order_id, o.user_id as reviewer_name, o.store_id as live_store_id, o.status, op.product_id, op.updated_at, v.reserved_at
    FROM `order` o INNER JOIN order_product op on o.id = op.order_id
                INNER JOIN product p on op.product_id = p.id
                INNER JOIN voucher v on o.id = v.order_id
                INNER JOIN store s on o.store_id = s.id
                INNER JOIN store_contract sc on s.id = sc.store_id
    where p.status = 'normal' and p.sale_status = 'sale'
    and op.product_id not in (20007,20008,20009,20010,20011)
    and s.status = 'normal'
    and sc.status = 'normal'
    and o.status != 'partial_cancel'
    """
    curs.execute(sql)

    df = pd.DataFrame(curs.fetchall())

    curs.close()
    conn.close()

    df = df[['order_id', 'status','live_store_id', 'product_id','reviewer_name','updated_at', 'reserved_at']]
    df.dropna(subset='updated_at', inplace=True)

    return df

def tag_and_type(product_id_list):

    conn = live_db_conn()
    curs = conn.cursor()

    if len(product_id_list) > 1:
        sql = """
        SELECT p.store_id, p.id as product_id, group_concat(ptm.id separator ' ') as ptm_ids, group_concat(pt.type separator ' ') as tag_type
        FROM product p
        INNER JOIN product_tag pt
        INNER JOIN product_tag_master ptm
        on pt.product_id=p.id
        and pt.product_tag_master_id = ptm.id
        WHERE p.id in {}
        """.format(tuple(product_id_list))
    
    else:

        sql = """
        SELECT p.store_id, p.id as product_id, group_concat(ptm.id separator ' ') as ptm_ids, group_concat(pt.type separator ' ') as tag_type
        FROM product p
        INNER JOIN product_tag pt
        INNER JOIN product_tag_master ptm
        on pt.product_id=p.id
        and pt.product_tag_master_id = ptm.id
        WHERE p.id = {}
        """.format(product_id_list[0])

    curs.execute(sql)
    df = pd.DataFrame(curs.fetchall())

    curs.close()
    conn.close()
    
    return df

def get_store_location(x):

    conn = live_db_conn()
    curs = conn.cursor()

    sql = """
    SELECT * FROM store_location sl
    INNER JOIN location_master lm 
    on sl.location_master_id = lm.id
    where sl.store_id in {} 
    and lm.name2 != "" 
    and lm.name3 = ""
    """.format(x)
    curs.execute(sql)

    df = pd.DataFrame(curs.fetchall())

    curs.close()
    conn.close()

    return df

def rec_product_tag(product_list):

    conn = live_db_conn()
    curs = conn.cursor()

    if len(product_list) > 1:
        sql = """
        SELECT p.store_id as store_id, p.id as product_id, group_concat(ptm.id separator ' ') as ptm_ids, group_concat(pt.type separator ' ') as tag_type
        FROM product p
        INNER JOIN product_tag pt
        INNER JOIN product_tag_master ptm
        on pt.product_id=p.id
        and pt.product_tag_master_id = ptm.id
        WHERE p.id in {} and pt.type != 'option'
        group by p.id
        """.format(tuple(product_list))

    else:
        sql = """
        SELECT p.store_id as store_id, p.id as product_id, group_concat(ptm.id separator ' ') as ptm_ids, group_concat(pt.type separator ' ') as tag_type
        FROM product p
        INNER JOIN product_tag pt
        INNER JOIN product_tag_master ptm
        on pt.product_id=p.id
        and pt.product_tag_master_id = ptm.id
        WHERE p.id = {} and pt.type != 'option'
        group by p.id
        """.format(product_list[0])


    curs.execute(sql)
    df = pd.DataFrame(curs.fetchall())

    curs.close()
    conn.close()

    return df

def tag_groupby(x):

    conn = live_db_conn()
    curs = conn.cursor()

    sql = """
    SELECT product_id, group_concat(product_tag_master_id separator ',') as tag_set FROM product_tag
    WHERE product_id in {} and type != 'option'
    group by product_id
    """.format(tuple(x))
    curs.execute(sql)

    df = pd.DataFrame(curs.fetchall())

    curs.close()
    conn.close()

    return df

def get_tag(x):

    conn = live_db_conn()
    curs = conn.cursor()

    sql = """
    SELECT product_id, product_tag_master_id FROM product_tag
    WHERE product_id in {} and type != 'option'
    """.format(x)
    curs.execute(sql)

    df = pd.DataFrame(curs.fetchall())

    curs.close()
    conn.close()

    return df

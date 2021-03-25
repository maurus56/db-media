import MySQLdb
from settings.db import *
from tabulate import tabulate

import logging
from logging.config import dictConfig
from settings.logger import logging_config

dictConfig(logging_config)
logMyScrapper = logging.getLogger('db_actions')

####################################################################
################  Database  ########################################


def db_cursor():
    db = MySQLdb.connect(
        host="localhost", user=user, password=password, db=db_name)
    cur = db.cursor()
    return cur, db


def db_Get_Id(table, column, value, limit=''):
    query = f"SELECT {table}_id FROM {table} WHERE ({column} = '{value}') {limit}"
    a = db_Get_Data(query, fetchone=True)
    return a[0] if a else a


def db_Get_Val_by_Id(table, column, id):
    query = f"SELECT {column} FROM {table} WHERE ({table}_id = {id})"
    a = db_Get_Data(query, fetchone=True)
    return a[0] if a else a


def db_Get_Data(query='', fetchone=False):
    ''' 
        Main conection to db using query
        fetchall:\n
            returns ( (. ,), )
        fetchone:\n
            returns (. ,)
    '''
    if query:
        try:
            cur, db = db_cursor()

            cur.execute(query)
            data = None
            if fetchone:
                data = cur.fetchone()
            else:
                data = cur.fetchall()
            
            return data

        except MySQLdb.Error as e:
            print('Error:', e)

        finally:
            cur.close()
            db.close()


def db_Delete_Row(data: dict):
    '''Deletes row in table
        data {\n
            'table': table-name,
            'id': id of objec in db
        }
        Returns 1 if success
    '''
    if data['id']:
        try:
            cur, db = db_cursor()

            sql = f"DELETE FROM {data['table']} WHERE {data['table']}_id = {data['id']}"

            cur.execute(sql)
            db.commit()
            return 1

        except MySQLdb.Error as e:
            print('Error:', e)
            return 0

        finally:
            cur.close()
            db.close()


def db_Edit_Row(data: dict):
    ''' Edits row in table
        data {\n
            'table': table-name,
            'id': id of objec in db,
            'key': val...
        }
        Returns 1 if success
    '''

    try:
        cur, db = db_cursor()

        cur.execute(f"DESCRIBE {data['table']}")
        allowed_keys = set(row[0] for row in cur.fetchall())

        keys = allowed_keys.intersection(data)

        if len(keys) == 0:
            raise MySQLdb.Error

        values = list((f"{key}='{value}'" for key,
                       value in data.items() if key in allowed_keys))
        sql = f"UPDATE {data['table']} SET { ','.join(values)} WHERE ({data['table']}_id = {data['id']})"

        cur.execute(sql)
        db.commit()
        return 1

    except MySQLdb.Error as e:
        print('Error:', e)
        return 0

    finally:
        cur.close()
        db.close()


def db_Add_Row(data: dict):
    ''' Adds data to selected table
        data {\n
            'table': table-name,
            'key': val...
        }
        Returns 1 if success
    '''

    try:
        cur, db = db_cursor()

        cur.execute(f"DESCRIBE {data['table']}")
        allowed_keys = set(row[0] for row in cur.fetchall())

        keys = allowed_keys.intersection(data)

        if len(keys) == 0:
            raise MySQLdb.Error

        columns = ", ".join(keys)
        values_template = ", ".join(["%s"] * len(keys))

        sql = f"INSERT INTO {data['table']} ({columns}) VALUES ({values_template})"
        values = tuple(data[key] for key in keys)

        cur.execute(sql, values)
        db.commit()
        return 1

    except MySQLdb.Error as e:
        if e.args[0] == 1062: # DUPLICATE
            # print('Duplicate')
            pass
        else:
            print('Error:', e)
        return 0

    finally:
        cur.close()
        db.close()



#################################################################
####################    Utility    ##############################

def set_col_default(table, col, text=None):
    db_Get_Data(f"update {table} set {col} = {text if text else 'default'}", True)

def lower_note():
    a = db_Get_Data("select poi_id, note from poi where note != ''")
    data = {}
    data['table'] = 'poi'
    for i in a:
        data['id'] = i[0]
        data['note'] = i[1].lower()
        db_Edit_Row(data)
    print(db_Get_Data("select poi_id, note from poi where note != ''"))


def get_satistics_data(note: list, type_:str = None):
    
    def getter(where:str):
        like = "where note " + (f"like '%{note[0]}%'" if note[0] else "= ''" )
        query = f"select count(*) from poi {like} {where}"
        a = db_Get_Data(query, fetchone=True)
        return a[0] if a else a

    if type_ == "checked":
        return getter("and is_checked = 1")
    elif type_ == "mail":
        return getter("and poi_mail != '' and poi_phone = ''")
    elif type_ == "phone":
        return getter("and poi_phone != '' and poi_mail = ''")
    elif type_ == "both":
        return getter("and poi_phone != '' and poi_mail != ''")
    elif type_ == "followers":
        return getter("and got_followers = 1")
    elif type_ == 'contacts':
        return getter("and bool = 0 and is_business = 1 and poi_phone = '' and poi_mail = ''")

    else:
        data = []
        for i in note:
            like = "where note " + (f"like '%{i}%'" if i != 'none' else "= ''" )
            query = f"select count(*) from poi {like}"
            a = db_Get_Data(query, fetchone=True)
            a = a[0] if a else a
            data.append([i,
                get_satistics_data([i if i != 'none' else ''], type_="mail"), 
                get_satistics_data([i if i != 'none' else ''], type_="phone"),
                get_satistics_data([i if i != 'none' else ''], type_="both"),
                get_satistics_data([i if i != 'none' else ''], type_="checked"), 
                get_satistics_data([i if i != 'none' else ''], type_="followers"), 
                f"{get_satistics_data([i if i != 'none' else ''], type_='contacts')}/{a}"])
            data[-1].insert(4, data[-1][1] + data[-1][2] + data[-1][3])
        return data


def print_stats():
    a = db_Get_Data(
        "select count(case is_checked when 0 then 1 else null end) from user", fetchone=True)
    b = db_Get_Data("select count(*) from user", fetchone=True)
    e = db_Get_Data(
        "select count(case error when 1 then 1 else null end) from user", fetchone=True)
    print(
        f"\n USERS\n-------\nRemainig: {a[0]}\nDone: {b[0]-a[0]}/{b[0]}\nErrors: {e[0]}")

    a = db_Get_Data(
        "select count(*) from poi where bool = 0 and is_business = 1 and poi_phone = '' and poi_mail = ''", fetchone=True)
    b = db_Get_Data("select count(*) from poi", fetchone=True)
    print(f"\n  POI\n-------\nRemainig: {a[0]}\nDone: {b[0]-a[0]}/{b[0]}\n")

    k_words = ['dj', 'manage', 'music', 'dance',
               'bailar', 'choreogra', 'coreogra', 'prod', 'none']
    data = get_satistics_data(k_words)
    print(tabulate(data,
                   headers=('', 'mail/o', 'phone/o', 'both', 'total', 'checked', 'extracted', 'TOTAL'), tablefmt="orgtbl"))
    print('\n\n')


    ##################################################################
    #######################                 ##########################

if __name__ == '__main__':
    print_stats()
    # print(db_Get_Data("SELECT COUNT(*) FROM user", True)[0])
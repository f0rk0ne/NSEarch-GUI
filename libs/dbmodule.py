#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../libs")
sys.path.append("libs/")
from utils import *
import sqlite3 as lite
import re
import os
import i18n
import time

utils = Utils()
utils.check_config_file()
yaml_vars = utils.get_yaml_vars()

FAVDBNAME = "favorites.sqlite3"
dbname = yaml_vars["scriptdb"]
categories = yaml_vars["categories"]
file_path = yaml_vars["filePath"]
scripts_path = yaml_vars["scriptsPath"]
current_checksum = yaml_vars["checksum"]
hist_len = yaml_vars["histLen"]
lang = yaml_vars["lang"]
fallback = "es" if lang == "en" else "en"

i18n.load_path.append('i18n')
if lang in ["es", "en"]:    
    i18n.set('locale', lang)
    i18n.set(
        'fallback',
        fallback
    )
else:
    currentLocale = re.sub(r'\_.*', '', os.environ['LANG'])
    i18n.set(
        'locale',
        currentLocale
    )
    i18n.set(
        'fallback',
        'en' if currentLocale == "es" else 'es'
    )

lastresults = {}

RANKING_NORMAL = "setup.ranking_normal"
RANKING_GREAT = "setup.ranking_great"
RANKING_SUPER_GREAT = "setup.ranking_super_great"
UPDATE_APP_ERROR = "setup.updateapp_error"

def check_db():
    try:        
        if os.path.exists(dbname):
            utils.show_spinner(
                i18n.t("setup.checking_db_checksum")
            )
            if utils.is_db_checksum(current_checksum):                
                check_integrity()
                time.sleep(1)
            else:
                download_db()
        else:
            download_db()
        if os.path.exists(FAVDBNAME):
            check_fav_integrity()
        else:
            create_favdb()
    except Exception as e:
        utils.print_traceback(e)  

def check_integrity():
    try:
        utils.show_spinner(i18n.t("setup.checking_db"))
        db, cursor = get_connect()
        cursor.execute("PRAGMA integrity_check;")
        if cursor.fetchone()[0] == "ok":       
            cursor.execute("SELECT name from sqlite_master;")
            tables = [a[0] for a in cursor.fetchall()]
            tables_list = [
                "categories",                
                "script_category",
                "scripts",
                "sqlite_sequence"                
            ]            
            if sorted(tables) != sorted(tables_list):
                print("check_integrity")
                download_db()
        else:
            download_db()
    except Exception as e:
        utils.show_exception(e)
    finally:
        if db:
            db.close()

def check_fav_integrity():
    try:
        utils.show_spinner(i18n.t("setup.checking_favdb"))
        db, cursor = get_connect(True)
        cursor.execute("PRAGMA integrity_check;")        
        if cursor.fetchone()[0] == "ok":            
            cursor.execute("SELECT name from sqlite_master;")
            tables = [a[0] for a in cursor.fetchall()]
            tables_list = [
                "favorites",
                "sqlite_autoindex_favorites_1",
                "sqlite_sequence"
            ]
            if tables_list != tables:
                create_favdb()
        else:            
            create_favdb()
    except Exception as e: 
        utils.print_traceback(e)
    finally:
        if db:
            db.close()

def create_favdb():
    try:
        utils.show_spinner(i18n.t("setup.create_favdb"))
        db, cursor = get_connect(True)
        cursor.execute('DROP TABLE IF EXISTS "favorites";')
        cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS "favorites"(
                "id" INTEGER NOT NULL,
                "name" TEXT NOT NULL UNIQUE,
                "ranking" INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        ''')
        db.commit()
    except Exception as e:
        utils.print_traceback(e)
    finally:
        if db:
            db.close()

def download_db():
    utils.print(
        f"[{COLOR_2}]{i18n.t('setup.downloading')}[/{COLOR_2}]",
        True
    )
    if utils.is_con():
        if utils.download_db(
            i18n.t("setup.downloading"),
            i18n.t("setup.internet_error"),
        ):
            utils.print(
                f"[{BOLD_COLOR_2}]{i18n.t('setup.downloaded')}[/{BOLD_COLOR_2}]"
            )
    else:
        utils.print(
            i18n.t('setup.internet_error')
        )
        exit()

# get all scripts
def search_all():
    db = None
    try:
        db, cursor = __dbconnect()
        cursor.execute(
            "select id, replace(name,'.nse',''), author from scripts GROUP BY NAME ORDER BY NAME"
        )
        return __fetch_script(cursor.fetchall())
    except Exception as e:
        utils.print_traceback(e)
        utils.print("Error search_all %s:" % e.args[0])
    finally:
        if db:
            db.close()

# set script as a favorite
def create_favorite(**kwargs):
    if kwargs is not None:
        script = None
        ranking = None
        db = None
        try:
            if "name" in kwargs.keys() and "ranking" in kwargs.keys():
                script = kwargs["name"]
                ranking = get_ranking_index(kwargs["ranking"])
            elif "name" in kwargs.keys():
                script = kwargs["name"]
                ranking = 0
            else:
                utils.print(i18n.t("setup.bad_params"))
                return False
            db, cursor = __dbconnect(True)
            cursor.execute('''
            INSERT INTO favorites (name,ranking) values (?,?)
            ''', (script, ranking,))
            db.commit()
            if cursor.rowcount == 1:
                utils.print("[+] "+script+" "+i18n.t("setup.add_fav_ok"))
        except Exception as e:
            if "unique" in str(e).lower():
                utils.print("[-] " + i18n.t("setup.add_fav_error", script=script))
            else:
                utils.print_traceback(e)
        finally:
            if db:
                db.close()

# get script ranking index
def get_ranking_index(ranking):
    if ranking == i18n.t(RANKING_NORMAL):
        return 0
    elif ranking == i18n.t(RANKING_GREAT):
        return 1
    elif ranking == i18n.t(RANKING_SUPER_GREAT):
        return 2
    else:
        return 0

# get ranking text
def get_ranking_text(ranking):
    if ranking == 0:
        return i18n.t(RANKING_NORMAL)
    elif ranking == 1:
        return i18n.t(RANKING_GREAT)
    elif ranking == 2:
        return i18n.t(RANKING_SUPER_GREAT)
    else:
        return i18n.t(RANKING_NORMAL)

# update favorite row
def update_favorite(**kwargs):
    if kwargs is not None:
        db = None
        try:
            db, cursor = __dbconnect(True)
            if "name" in kwargs.keys() and "newname" in kwargs.keys()\
                    and "newranking" in kwargs.keys():
                script = kwargs["name"]
                newname = kwargs["newname"]
                newranking = get_ranking_index(kwargs["newranking"])
                cursor.execute('''
          UPDATE favorites SET name=?, ranking=? WHERE name=?
          ''', (newname, newranking, script,))
            elif "name" in kwargs.keys() and "newname" in kwargs.keys():
                script = kwargs["name"]
                newname = kwargs["newname"]
                cursor.execute('''
          UPDATE favorites SET name=? WHERE name=?
          ''', (newname, script,))
            elif "name" in kwargs.keys() and "newranking" in kwargs.keys():
                script = kwargs["name"]
                newranking = get_ranking_index(kwargs["newranking"])
                cursor.execute('''
          UPDATE favorites SET ranking=? WHERE name=?
          ''', (newranking, script,))
            else:
                utils.print(i18n.t("setup.bad_params"))
            db.commit()
            if cursor.rowcount == 1:
                utils.print("[+] "+script+" "+i18n.t("setup.update_fav_ok"))
        except Exception as e:
            utils.print("Error update_favorite %s:" % e.args[0])
            utils.print("[-] "+script+" "+i18n.t("setup.update_fav_error"))
            utils.print_traceback(e)
        finally:
            if db:
                db.close()

# delete script values
def delete_favorite(**kwargs):
    if kwargs is not None:
        db = None
        try:
            db, cursor = __dbconnect(True)
            if "name" in kwargs.keys():
                script = kwargs["name"]
                cursor.execute('''
                    DELETE FROM favorites WHERE name=?
                    ''',
                    (script,)
                )
                db.commit()
            if cursor.rowcount == 1:
                utils.print("[+] "+script+" "+i18n.t("setup.del_fav_ok"))
        except Exception as e:
            utils.print("[-] "+script+" "+i18n.t("setup.del_fav_error"))
            utils.print_traceback(e)
        finally:
            if db:
                db.close()

# Functions for all queries
def search_by_criterial(**kwargs):
    if kwargs is not None:
        db, cursor = __dbconnect()
        if "name" in kwargs.keys() and "category" in kwargs.keys()\
                and "author" in kwargs.keys():
            script = kwargs["name"]
            category = kwargs["category"]
            author = kwargs["author"]
            sql = get_search_statement(
                script=script,
                category=category,
                author=author
            )
        elif "name" in kwargs.keys() and "category" in kwargs.keys():
            script = kwargs["name"]
            category = kwargs["category"]
            sql = get_search_statement(
                script=script,
                category=category
            )
        elif "name" in kwargs.keys() and "author" in kwargs.keys():
            author = kwargs["author"]
            script = kwargs["name"]
            sql = "select id, replace(name,'.nse',''), author from scripts "
            sql += "where name like '%"+script+"%' "
            sql += "and author like '%"+author+"%';"
        elif "name" in kwargs.keys() or len(kwargs.keys()) == 0:
            script = kwargs["name"]
            sql = get_default_statement(script)
        elif "category" in kwargs.keys():
            category = kwargs["category"]
            sql = get_search_statement(
                category=category
            )
        elif "author" in kwargs.keys():
            author = kwargs["author"]
            sql = "select id, replace(name,'.nse',''), author from scripts where "
            sql += "author like '%"+author+"%'"
        cursor.execute(sql)
        result = __fetch_script(cursor.fetchall())
        db.close()
        return result

# get script search statement
def get_search_statement(script=None, category=None, author=None):
    sql = "select scripts.id, replace(scripts.name,'.nse',''), scripts.author "
    sql += "from scripts, categories, script_category "
    sql += f"where categories.name like '%{category}%' and "
    if script != None:
        sql += f"scripts.name like '%{script}%' and "
    if author != None:
        sql += f"scripts.author like '%{author}%' and "
    sql += "scripts.id=script_category.id_script and "
    sql += "categories.id=script_category.id_category;"
    return sql

# get default search statement
def get_default_statement(script):
    sql = "select id, replace(name,'.nse',''), author "
    sql += f"from scripts where name like '%{script}%'"
    return sql

# get favs scripts filter
def get_favorites(**kwargs):
    if kwargs is not None:
        sql = None
        db, cursor = __dbconnect(True)
        select_ = "select id, name, ranking from favorites "
        if "name" in kwargs.keys() and "ranking" in kwargs.keys():
            script = kwargs["name"]
            ranking = str(get_ranking_index(kwargs["ranking"]))
            sql = select_
            sql += f"where ranking like '%{ranking}%' "
            sql += f"and name like '%{script}%';"
        elif "name" in kwargs.keys():
            script = kwargs["name"]
            sql = select_
            sql += f"where name like '%{script}%';"
        elif "ranking" in kwargs.keys():
            ranking = str(get_ranking_index(kwargs["ranking"]))
            sql = select_
            sql += f"where ranking like '%{ranking}%';"
        else:
            sql = "select id, name, ranking from favorites;"
        cursor.execute(sql)
        result = __fetch_script(cursor.fetchall(), True)
        db.close()
        return result

# get categories
def get_categories():
    try:
        db, cursor = __dbconnect()
        cursor.execute('select * from categories;')
        return cursor.fetchall()
    except Exception as e:
        utils.print(i18n.t(UPDATE_APP_ERROR, error=e.args[0]))
        utils.print_traceback(e)

# get script by id
def get_script_by_id(script_id):
    try:
        db, cursor = __dbconnect()
        cursor.execute(
            'select replace(name, ".nse", "") from scripts where id=?;', [script_id])
        return cursor.fetchone()[0]
    except Exception as e:
        utils.print("Error get_script_by_id %s:" % e.args[0])
        utils.print_traceback(e)
    finally:
        db.close()

# get script by name
def get_script_by_name(script):
    try:
        db, cursor = get_connect()
        cursor.execute("SELECT * FROM scripts WHERE name=?;", [script])
        result = cursor.fetchone()
        if result == None:            
            return result
        categories = cursor.execute(
            """
            SELECT categories.name FROM categories INNER JOIN 
            script_category ON categories.id=script_category.id_category
            WHERE script_category.id_script=?
            """,
            [result[0]]
            )        
        categories_ = [ a[0] for a in categories.fetchall() ]
        return {
            "id" : result[0],
            "name" : result[1],
            "author" : result[2],
            "license" : result[3],
            "summary" : result[4],
            "categories": categories_,
            "args" : result[5],
            "requires" : result[6],
            "usage" : result[7]
        }
    except Exception as e:
        utils.print("Error get_script_by_name %s:" % e.args[0])
        utils.print_traceback(e)
    finally:
        db.close()

# get scrips in a category
def get_scripts_cat(**kwargs):
    try:
        db, cursor = __dbconnect()
        category = ''
        if 'id' in kwargs.keys():
            catid = kwargs['id']
            sql = 'select scripts.id, replace(scripts.name, ".nse", "") as script, categories.name '
            sql += 'from scripts INNER JOIN (script_category INNER JOIN categories ON '
            sql += 'script_category.id_category=categories.id) '
            sql += 'ON scripts.id=script_category.id_script '
            sql += 'WHERE script_category.id_category=?;'
            cursor.execute(
                sql, [catid]
            )
        elif 'name' in kwargs.keys():
            name = kwargs['name']
            sql = 'select scripts.id, replace(scripts.name, ".nse", "") as script, categories.name '
            sql += 'from scripts INNER JOIN (script_category INNER JOIN '
            sql += 'categories ON script_category.id_category=categories.id) '
            sql += 'ON scripts.id=script_category.id_script '
            sql += 'WHERE categories.name=?;'
            cursor.execute(
                sql, [name]
            )
        result = {}
        for a in cursor.fetchall():
            result.update({a[0]: a[1]})
            category = a[2]
        return (category, result)
    except Exception as e:
        utils.print(i18n.t(UPDATE_APP_ERROR, error=e.args[0]))
        utils.print_traceback(e)
    finally:
        db.close()

# get total scripts
def get_total_scripts():
    db, cursor = __dbconnect()
    cursor.execute("SELECT count(name) FROM scripts; ")
    data = cursor.fetchall()
    return data[0][0] if data != False else 0

# get favorites formmated
def get_fav_formmated():
    result = []
    for a in lastresults.keys():
        val = lastresults[a]
        result.append(
            {
                "name": val["name"],
                "ranking": get_ranking_text(val["ranking"]),
                "stars": utils.get_ranking(val["ranking"])
            }
        )
    return result

# get database rows for categories and sripts scheme
def get_data():
    try:
        db, cursor = __dbconnect()
        sql = "select categories.name, replace(scripts.name,'.nse','') "
        sql += "from scripts INNER JOIN (script_category INNER JOIN categories "
        sql += "ON script_category.id_category=categories.id ) ON "
        sql += "scripts.id = script_category.id_script "
        sql += "ORDER BY categories.name;"
        cursor.execute(sql)
        data = cursor.fetchall()
        result = dict()
        for cat, name in data:
            if cat in result.keys():
                result[cat].append(str(name))
            else:
                tmp = []
                tmp.append(str(name))
                result[cat] = tmp
        return result
    except Exception as e:
        utils.print("Error get_data %s:" % e.args[0])
        utils.print_traceback(e)
    finally:
        if db != None:
            db.close()


def get_scripts():
    scripts = []
    data = get_data()
    for a in data:
        for b in data[a]:
            if b not in scripts:
                scripts.append(b)
    return scripts

# get authors list
def get_author_data():
    try:
        db, cursor = __dbconnect()
        cursor.execute(
            'SELECT replace(name,".nse",""), author from scripts;'
        )
        data = cursor.fetchall()
        result = dict()
        for name, author in data:
            result[name] = str(
                re.sub(
                    r'[\"\{\}\<\>\-\=\@\(\)\;\]]',
                    '',
                    author
                )
            )
        return result
    except Exception as e:
        utils.print("Error get_author_data %s:" % e.args[0])
        utils.print_traceback(e)
    finally:
        if db != None:
            db.close()

# Connection to the databases from gui
def get_connect(favdb=False):
    return __dbconnect(favdb)

# Connection to the databases
def __dbconnect(favdb=False):
    if favdb:
        db = lite.connect(FAVDBNAME)
    else:
        db = lite.connect(f"file:{dbname}?mode=ro", uri=True)
    db.text_factory = str
    db.row_factory = lite.Row
    return (db, db.cursor())

# private function to fetch all results into a dict
def __fetch_script(fetchall, total=False):
    fetchlist = {}
    if total:
        for row in fetchall:
            fetchlist.update({row[0]: {"name": row[1], "ranking": row[2]}})
    else:
        for row in fetchall:
            fetchlist.update({row[0]: {"name": row[1], "author": row[2]}})
    return fetchlist

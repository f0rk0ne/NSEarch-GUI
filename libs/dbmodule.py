import i18n
import os
import sys
import hashlib
import re
import shutil
import yaml
import sqlite3 as lite
from libs.utils import Utils

conf_file = 'config.yaml'
utils = Utils()
utils.check_config_file(conf_file)

stream = open(conf_file, 'r+')
item = yaml.safe_load(stream)

dbname = item["config"]["scriptdb"]
categories = item["config"]["categories"]
file_path = item["config"]["filePath"]
file_backup = item["config"]["fileBackup"]
scripts_path = item["config"]["scriptsPath"]
current_checksum = item["config"]["checksum"]
hist_len = item["config"]["histLen"]
lang = item["config"]["lang"]
i18n.load_path.append('i18n')  
if lang == "es" or lang == "en":
  i18n.set(
    'locale', lang
  )
  i18n.set(
    'fallback',
    'en' if lang == "es" else 'es'
  )
else:
  currentLocale = re.sub(r'\_.*','', os.environ['LANG'] )
  i18n.set(
      'locale', currentLocale
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

def init_setup():  
  utils.spinnerText = f'{i18n.t("setup.create_db")} {dbname}'
  db = None
  try:
    db, cursor = __dbconnect()    
    # Create Script Table    
    cursor.execute('''
      create table if not exists scripts(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        author TEXT NULL
    )''')
    utils.show_spinner(i18n.t("setup.create_script_table")) 
    # Create Categories Table
    cursor.execute('''
      create table if not exists categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL
    )''')
    utils.show_spinner(i18n.t("setup.create_category_table")) 
    # Create Script/Category Table
    cursor.execute('''
      create table if not exists script_category(
        id_category INTEGER NOT NULL,
        id_script INETGER NOT NULL
    )''')
    utils.show_spinner(i18n.t("setup.create_category_script_table"))
    utils.show_spinner(i18n.t("setup.upload_categories")) 
    for category in categories:
      cursor.execute(
        '''INSERT INTO categories (name) VALUES (?)'''
        ,(category,)
      )
    # Create Favorite Table
    utils.show_spinner(i18n.t("setup.create_favorites_table")) 
    cursor.execute('''
      create table if not exists favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL UNIQUE,
        ranking INTEGER NOT NULL
    )''')   
    db.commit()
    set_data()
    create_backup()
    stream.close
  except Exception as e:
    utils.print_traceback(e)
    print(e)
    utils.print("Error init_setup %s:" % e.args[0])    
    sys.exit(1)
  finally:
    if db:
      db.close()

#create file backups
def create_backup():
  utils.show_spinner("\n"+i18n.t("setup.create_backup"))
  shutil.copy2(file_path, file_backup)
  if os.path.isfile(file_backup):
    utils.show_spinner(i18n.t("setup.create_backup_ok"))
  else:
    utils.show_spinner(i18n.t("setup.create_backup_error"))

#insert data into the tables
def set_data():  
  script_file = open(file_path,'r')  
  for line in script_file:
    line = line.replace(
      'Entry { filename = "',
      ""
    ).replace(
        '", categories = { "',
        ',"'
    ).replace(
        '", } }',
        '"'
    ).replace(
        '", "',
        '","'
    )
    for i, j in enumerate(categories):
      line = line.replace('"'+j+'"',str(i+1))
    newarray = line.split(",")
    for key,value in enumerate(newarray):      
      if value == newarray[0]:
        author = None
        lastrowid = None
        current_script = open(scripts_path+value,'r')
        author = get_author_from_file(current_script)                
        lastrowid = insert_script(value,author)
        current_script.close()
      else:        
        insert_script_category(lastrowid,value)  
  script_file.close()

# get author from file
def get_author_from_file(current_script):
  for line in current_script.readlines():
    if line.startswith("author"):
      return line.replace(
          "author = ",
          ""
      ).replace(
          "author     = ",
          ""
      ).replace(
          '"',
          ',"'
      ).replace(
          '[[',
          ""
      ).replace(
          ',"',
          ""
      ).replace(
          '{',
          ""
      ).replace(
          '}',
          ""
      ).replace(
          "author =",     
          "Brandon Enright <bmenrigh@ucsd.edu>, Duane Wessels <wessels@dns-oarc.net>, "
      ).strip()

#update app if the db exists
def update_app():  
  utils.show_spinner(i18n.t("setup.checking_db")+" "+dbname)  
  db = None
  try:
    db,cursor = __dbconnect()
    # Create Favorite Table
    cursor.execute('''
      create table if not exists favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL UNIQUE,
        ranking TEXT NOT NULL
    )''')
    new_hash = hashlib.sha256(open(file_path,'rb').read()).hexdigest()
    if new_hash == current_checksum:
      utils.show_spinner(i18n.t("setup.db_is_update")+" "+dbname)         
    else:      
      utils.create_config_file()
      utils.show_spinner(i18n.t("setup.update_db"))
      cursor.executescript('''
        DROP TABLE IF EXISTS scripts;
        DELETE FROM SQLITE_SEQUENCE WHERE name='scripts';
        DROP TABLE IF EXISTS categories;
        DELETE FROM SQLITE_SEQUENCE WHERE name='categories';
        DROP TABLE IF EXISTS script_category;
        DELETE FROM SQLITE_SEQUENCE WHERE name='script_category';
        ''')
      db.commit()
      db.close()      
      init_setup()      
  except Exception as e:
    utils.print_traceback(e)
    utils.print(i18n.t(UPDATE_APP_ERROR, error=e.args[0]))    
  finally:
    if db:
      db.close()

# Insert each Script and Author
def insert_script(script,author):
  db = None
  try:    
    utils.show_spinner(f'{i18n.t("setup.insert_script")} {script}')
    db, cursor = __dbconnect()
    cursor.execute('''
    Insert into scripts (name,author) values (?,?)
    ''',(script,author,))
    db.commit()
    return cursor.lastrowid
  except Exception as e:
    if db:
      db.rollback()
    utils.print("Error insert_script %s:" % e.args[0])
    utils.print_traceback(e)
  finally:
    if db:
      db.close()

#Insert the scripts_id and categories_id
def insert_script_category(scriptid, categoryid):
  db = None
  try:    
    db, cursor = __dbconnect()
    cursor.execute('''
      INSERT INTO script_category (id_category,id_script) VALUES (?,?)
      ''',
      (categoryid,scriptid,)
    )
    db.commit()
    if cursor.rowcount == 1:
      sys.stdout.flush()      
  except Exception as e:
     if db:
      db.rollback()
      utils.print("Error insert_script_category %s:" % e.args[0])
  finally:
    if db:
      db.close()

#get all scripts
def search_all():
  db = None
  try:
    db, cursor = __dbconnect()    
    cursor.execute(
      "select id, name, author from scripts GROUP BY NAME ORDER BY NAME"
    )
    return __fetch_script(cursor.fetchall())
  except Exception as e:
    utils.print_traceback(e)
    utils.print("Error search_all %s:" % e.args[0])
  finally:
    if db:
      db.close()

#set script as a favorite
def create_favorite(**kwargs):
  if kwargs is not None:
    script= None
    ranking= None
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
      db, cursor = __dbconnect()      
      cursor.execute('''
        Insert into favorites (name,ranking) values (?,?)
        ''',(script,ranking,))
      db.commit()
      if cursor.rowcount == 1:
        utils.print("[+] "+script+" "+i18n.t("setup.add_fav_ok"))
    except Exception as e:      
      utils.print("[-] "+script+" "+i18n.t("setup.add_fav_error"))
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

#update favorite row
def update_favorite(**kwargs):
  if kwargs is not None:    
    db = None
    try:
      db, cursor = __dbconnect()      
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

#delete script values
def delete_favorite(**kwargs):
  if kwargs is not None:
    db = None
    try:
      db, cursor = __dbconnect()      
      if "name" in kwargs.keys():
        script = kwargs["name"]
        cursor.execute('''
          DELETE FROM favorites WHERE name=?
          ''',(script,))
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
        script = script,
        category = category,
        author = author
      )      
    elif "name" in kwargs.keys() and "category" in kwargs.keys():
      script = kwargs["name"]
      category = kwargs["category"]
      sql = get_search_statement(
        script = script,
        category = category
      )      
    elif "name" in kwargs.keys() and "author" in kwargs.keys():
      author = kwargs["author"]
      script = kwargs["name"]
      sql = "select id, name, author from scripts "
      sql += "where name like '%"+script+"%' "
      sql += "and author like '%"+author+"%';"
    elif "name" in kwargs.keys() or len(kwargs.keys()) == 0:
      script = kwargs["name"]      
      sql= get_default_statement(script)
    elif "category" in kwargs.keys():
      category = kwargs["category"]
      sql = get_search_statement(
        category = category
      )      
    elif "author" in kwargs.keys():
      author = kwargs["author"]
      sql = "select id, name, author from scripts where " 
      sql += "author like '%"+author+"%'"    
    cursor.execute(sql)
    result = __fetch_script(cursor.fetchall())
    db.close()
    return result

# get script search statement
def get_search_statement(script = None, category = None, author = None):
  sql = "select scripts.id, scripts.name, scripts.author "
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
  return "select id, name, author " +\
          f"from scripts where name like '%{script}%'"

# get favs scripts filter
def get_favorites(**kwargs):
  if kwargs is not None:    
    sql=None
    db, cursor = __dbconnect()
    select_ = "select id, name, ranking from favorites "
    if "name" in kwargs.keys() and "ranking" in kwargs.keys():
      script = kwargs["name"]
      ranking =  str(get_ranking_index(kwargs["ranking"]))
      sql = select_
      sql += f"where ranking like '%{ranking}%' "
      sql += f"and name like '%{script}%';"
    elif "name" in kwargs.keys():
      script = kwargs["name"]
      sql = select_
      sql += f"where name like '%{script}%';"
    elif "ranking" in kwargs.keys():      
      ranking =  str(get_ranking_index(kwargs["ranking"]))      
      sql = select_
      sql += f"where ranking like '%{ranking}%';"      
    else:
      sql = "select id, name, ranking from favorites;"
    cursor.execute(sql)
    result = __fetch_script(cursor.fetchall(),True)
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

#get script by id
def get_script_by_id(script_id):
  try:
    db,cursor = __dbconnect()
    cursor.execute('select name from scripts where id=?;',[script_id])
    return cursor.fetchone()[0]
  except Exception as e:
    utils.print("Error get_script_by_id %s:" % e.args[0])
    utils.print_traceback(e)
  finally:    
    db.close()

#get scrips in a category
def get_scripts_cat(**kwargs):
  try:    
    db, cursor = __dbconnect()
    category = ''
    if 'id' in kwargs.keys():      
      catid = kwargs['id']      
      sql = 'select scripts.id, scripts.name as script, categories.name ' 
      sql += 'from scripts INNER JOIN (script_category INNER JOIN categories ON ' 
      sql += 'script_category.id_category=categories.id) '
      sql += 'ON scripts.id=script_category.id_script '
      sql += 'WHERE script_category.id_category=?;'
      cursor.execute(
        sql, [catid]
      )
    elif 'name' in kwargs.keys():
      name = kwargs['name']
      sql = 'select scripts.id, scripts.name as script, categories.name '
      sql += 'from scripts INNER JOIN (script_category INNER JOIN '
      sql += 'categories ON script_category.id_category=categories.id) '
      sql += 'ON scripts.id=script_category.id_script '
      sql += 'WHERE categories.name=?;'
      cursor.execute(
        sql, [name]
      )    
    result = {}
    for a in cursor.fetchall():
      result.update({a[0]: a[1] })
      category = a[2]    
    return (category, result)    
  except Exception as e:    
    utils.print(i18n.t(UPDATE_APP_ERROR, error=e.args[0]))
    utils.print_traceback(e)
  finally:
    db.close()

#get total scripts
def get_total_scripts():
  db, cursor = __dbconnect()
  cursor.execute("SELECT count(name) FROM scripts; ")
  data = cursor.fetchall()
  return data[0][0] if data != False else 0

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
        result[ cat ].append(str(name))
      else:
        tmp = []
        tmp.append(str(name))
        result[ cat ] = tmp
    return result
  except Exception as e:
    utils.print("Error get_data %s:" % e.args[0])
    utils.print_traceback(e)
  finally:
    if db != None:
      db.close()

# get authors list
def get_author_data():
  try:
    db, cursor = __dbconnect()
    cursor.execute(
      'SELECT replace(name,".nse",""), author from scripts;'
    )
    data = cursor.fetchall()
    result = dict()
    for name,author in data:
      result[ name ] = str(
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
def get_connect():
  return __dbconnect()

# Connection to the databases
def __dbconnect():
  db = lite.connect(dbname)
  db.text_factory = str
  db.row_factory = lite.Row
  return (db, db.cursor())

# private function to fetch all results into a dic
def __fetch_script(fetchall,total=False):
  fetchlist = {};
  if total:
    for row in fetchall:
      fetchlist.update({row[0]:{"name":row[1], "ranking":row[2]}})
  else:
    for row in fetchall:
      fetchlist.update({row[0]:{"name":row[1], "author":row[2]}})
  return fetchlist

import pymysql, os, json,unicodedata
import pandas, math
import numpy as np

# do validation and checks before insert
def validate_string(val):
   if val != None:
        if type(val) is int:
            #for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val


# connect to MySQL
con = pymysql.connect(host = 'localhost',user = 'root',passwd = '123456',db = '')
cursor = con.cursor()

cursor.execute("Drop database if exists receipes")
cursor.execute("Create database receipes")
cursor.execute("Use receipes")



# read EightPortion json files
print("Reading the EightPortion json files")
raw_json = pandas.read_json('json/parsed_recipes.json',)
modifiedjson = pandas.DataFrame(raw_json, columns=['id', 'instructions','ingredients_parsed', 'title'])
modifiedjson['id']=modifiedjson.index+1

# For receipe titles
print("Creating table for receipe_title ...")
cursor.execute("Drop Table if exists receipe_title")
cursor.execute("Create table receipe_title (recipe_id INT, title VARCHAR(200), primary key(recipe_id))")

for x in range(0, len(modifiedjson)):
  # print(modifiedjson['id'][x], modifiedjson['title'][x])
  # encodedUnicode = json.dumps(modifiedjson['title'][x], ensure_ascii=False)
  cursor.execute("INSERT INTO receipe_title (recipe_id, title) VALUES (%s,%s)", (int(modifiedjson['id'][x]), unicodedata.normalize('NFKD', modifiedjson['title'][x]).encode('ascii', 'ignore')))

print("Created table receipe_title ...\n")

# For ingredients
print("Creating table for receipe_ingre ...")
cursor.execute("Drop Table if exists receipe_ingre")
cursor.execute("Create table receipe_ingre (id INT AUTO_INCREMENT NOT NULL, recipe_id int,measure VARCHAR(50), ingredients TEXT, PRIMARY KEY(id), FOREIGN KEY (recipe_id) REFERENCES receipe_title (recipe_id) )")

for x in range(0, len(modifiedjson)):
  for y in modifiedjson['ingredients_parsed'][x]:
    # print(modifiedjson['id'][x],y['measure'],y['name'])
    cursor.execute("INSERT INTO receipe_ingre (recipe_id, measure, ingredients) VALUES (%s,%s, %s)", (int(modifiedjson['id'][x]),y['measure'],unicodedata.normalize('NFKD', y['name']).encode('ascii', 'ignore')))
print("Created table receipe_ingre ...\n")

# For Instructions
print("Creating table for receipe_instru ...")
cursor.execute("Drop Table if exists receipe_instru")
cursor.execute("Create table receipe_instru (id INT AUTO_INCREMENT NOT NULL, recipe_id int, instruc TEXT, Primary key(id), FOREIGN KEY (recipe_id) REFERENCES receipe_title (recipe_id))")

for x in range(0, len(modifiedjson)):
  cursor.execute("INSERT INTO receipe_instru (recipe_id, instruc) VALUES (%s,%s)", (int(modifiedjson['id'][x]), unicodedata.normalize('NFKD', modifiedjson['instructions'][x]).encode('ascii', 'ignore')))

print("Created table receipe_instru ...")

con.commit()
con.close()
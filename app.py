from flask import Flask, render_template, url_for, request
from flaskext.mysql import MySQL
from flask_paginate import Pagination, get_page_args
from itertools import combinations 


app= Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pwd'
app.config['MYSQL_DATABASE_DB'] = 'receipes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()

def getdatafromdb(ingredients):
    if len(ingredients)<2:
        ingredients.append('0')
    for x in ingredients:
        x.replace("'","")
    print("ingredients= ",ingredients)
    ingre=[]
    for x in ingredients:
        ingre.append(x.replace("'",""))
    result = []
    query =[]
    for times in range(len(ingre),1,-1):
        comb = combinations(ingre, times) 
        # Print the obtained combinations 
        for i in list(comb): 
            subquery= []
            for elem in range(0, len(i)):
                if elem != len(i)-1: 
                    subquery.append("SELECT recipe_id  FROM receipe_ingre WHERE ingredients LIKE '"  +i[elem]+ "' INTERSECT")
                else: 
                    subquery.append("SELECT recipe_id  FROM receipe_ingre WHERE ingredients LIKE '" +i[elem] +"' ")
            if subquery not in query:
                query.append(subquery)

    anotherquery=[] 
    for x in query:
        sendquery = " ".join(x)
        anotherquery.append((sendquery))

    a ="select RT.recipe_id, RT.title, GROUP_CONCAT(ingredients,  ' ') FROM receipe_title RT JOIN receipe_ingre RI ON RT.recipe_id=RI.recipe_id WHERE RT.recipe_id IN( Select Distinct(recipe_id) from ("
    for x in range(len(anotherquery)):
        if x != len(anotherquery)-1:
            a = a + "(" + anotherquery[x] + ")" + " UNION ALL "
        else:
            a = a + "(" + anotherquery[x] + ")) as a" + ") GROUP BY RT.recipe_id;  "

    cursor.execute(a)
    data = cursor.fetchall() 
    
    if len(data)==0:
        for ingre in ingredients:
            cursor.callproc('getrecipelist', [ingre])
            data = cursor.fetchall() 
            for x in data:
                result.append(x)
    else:
        for x in data:
            result.append(x)

    
    return result

@app.route('/', methods=['GET','POST'])
def index():
    # query= "SELECT * from newbuys;"
    # cursor.execute(query)
    search = False
    pagination = Pagination()
    if request.method == "POST":
        multiselect = request.form.getlist('mymultiselect')
        data = getdatafromdb(multiselect)
        cursor.callproc('getingredients')
        ingredients = cursor.fetchall() 
      
        page, per_page, offset = get_page_args()
        pagination = Pagination( p=page,
                                pp=10,
                                total=len(data),
                                record_name="data",
                                format_total=True,
                                format_number=True,
                                page_parameter="p",
                                per_page_parameter="pp",)
        return render_template('index.html', result=data, tasks=ingredients, selected= multiselect,pagination=pagination)
    else:
        cursor.callproc('getingredients')
        ingredients = cursor.fetchall() 
        return render_template('index.html', tasks=ingredients, pagination=pagination) # No need to specify the folder, it knows to look inside templates folder.

    return render_template('index.html', tasks=ingredients, pagination=pagination)
# selectedingre=[]


@app.route('/getrecipe')
def getrecipe():
    my_var = request.args.get('my_var', None)
    # print("my_var is ", my_var)
    cursor.callproc('getrecipeasperid', [my_var])
    result =cursor.fetchall() 
    # print(result)
    return render_template('getrecipe.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)




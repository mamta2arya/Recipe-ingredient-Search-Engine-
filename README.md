# Recipe-ingredient-Search-Engine-
1. Identified system requirements and designed a relational database schema that met the constraints and gave the list of recipes for given ingredients.
2. 45000 recipes were scrapped from foodnetwork.com using Python to populate the database. MySQL was used to query the designed database. 
3. An Interface was created using Flask.  Data mining using the Apriori algorithm is performed to get the nature of ingredients used in the recipes such as frequently used ingredients, dairy, and meat. 

To Run the code -

[X] Installing virtualenv
pip3 install virtualenv

[X] To check whether virtualenv exists and its version
virtualenv --version

[X] Creating virtual environment in directory
cd flaskproj
virtualenv env
# virtualenv env: Creates env folder

[X] Start Windows Subsystem for Linux (WSL) by typing-
WSL

[X] Activate the virtualenv
source env/Scripts/activate

Inside virtualenv:

[X] Install flask_MYsql-
pip3 install pymysql

[X] To run the code: python3 main.py

This code reads the parsed JSON and creates the database and the following tables:
receipe_title
receipe_instru
receipe_ingre

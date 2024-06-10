import sqlite3

con = sqlite3.connect('python.db')


cur = con.cursor()


sql = '''DROP TABLE IF EXISTS pyversions;'''

cur.execute(sql)

sql = '''CREATE TABLE pyversions (
    branch TEXT PRIMARY KEY,
    released_at_year INTEGER,
    released_at_month INTEGER,
    release_manager TEXT
);'''

cur.execute(sql)

sql = 'INSERT INTO pyversions VALUES ("2.6", 2008, 10, "Barry Warsaw")'

cur.execute(sql)

con.commit()

# es necesario escapar las comillas para que en el argumento pase como cadena 
branch = '"3.9.1"'
release_year = 2020
release_month = 10
release_manager = '"Lukasz Langa"'

sql = f'INSERT INTO pyversions VALUES ({branch},{release_year},{release_month},{release_manager})'

cur.execute(sql)
con.commit()

# cuando se utilizan placeholders no hace falta escapar la comilla del texto
branch = "3.9.2"
release_year = 2020
release_month = 10
release_manager = 'Lukasz Langa'

sql = f'INSERT INTO pyversions VALUES (?,?,?,?)'

# las variables se pasan como una tupla
cur.execute(sql, (branch, release_year, release_month, release_manager))
con.commit()

branch = "3.9.3"
release_year = 2020
release_month = 10
release_manager = 'Lukasz Langa'

sql = 'INSERT INTO pyversions VALUES (:branch, :year, :month, :manager)'

cur.execute(sql, dict(year=2020, month=10, branch="3.9.3", manager="Lukasz Langa"))
con.commit()

# esto lee una linea, la convierte en lista y luego la agrega a la bd
# una linea a la vez
'''
with open('pyversions.csv') as f:
    f.readline()
    for line in f:
        values = line.strip().split(',')
        sql = f'INSERT INTO pyversions VALUES (?,?,?,?)'
        cur.execute(sql, values)
    con.commit()
'''
with open('pyversions.csv') as f:
    values = [line.strip().split(',') for line in f.readlines()[1:]]
    print(type(values))
    print(values)
    sql = f'INSERT INTO pyversions VALUES (?,?,?,?)'
    cur.executemany(sql, values)
    con.commit()

# realizamos la consulta y el resultado se almacena en un cursor
sql = 'SELECT * FROM pyversions'

# barremos el cursor
for row in cur.execute(sql):
    print(row)
    
    

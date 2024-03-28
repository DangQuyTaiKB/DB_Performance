# import psycopg2

# def get_database_size():
#     conn = psycopg2.connect(
#         dbname="data",
#         user="postgres",
#         password="example",
#         host="localhost",
#         port="5432" 
#     )
#     cur = conn.cursor()
#     cur.execute("SELECT pg_size_pretty(pg_database_size('data'));")
#     size = cur.fetchone()
#     cur.close()
#     conn.close()
#     return size

# print(get_database_size())


# # SELECT pg_size_pretty(pg_database_size('your_database_name'));


import psycopg2
connection = psycopg2.connect(
    dbname='data',
    user='postgres',
    password='example',
    host='localhost',
    port=5432
)
with con.cursor(name='custom_cursor') as cursor:
     cursor.itersize = 1000 # chunk size
     query = 'SELECT * FROM mytable;'
     cursor.execute(query)
     for row in cursor:
         print(row)
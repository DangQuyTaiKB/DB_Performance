# SELECT
#     database_name,
#     sum(estimated_storage_bytes)/(1024*1024) AS size_in_mb
# FROM
#     crdb_internal.tables
# GROUP BY
#     database_name;

# import psycopg2

# def get_database_size():
#     conn = psycopg2.connect(
#         dbname="mycrdb",
#         user="root",
#         password="your_password",
#         host="localhost",
#         port="26257"  # Default port for CockroachDB
#     )
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT
#             database_name,
#             sum(estimated_storage_bytes)/(1024*1024) AS size_in_mb
#         FROM
#             crdb_internal.tables
#         WHERE
#             database_name = 'your_database_name'
#         GROUP BY
#             database_name;
#     """)
#     size = cur.fetchone()
#     cur.close()
#     conn.close()
#     return size

# print(get_database_size())



# import psycopg2

# def get_database_size():
#     conn = psycopg2.connect(
#         dbname="mycrdb",
#         user="root",
#         password="",
#         host="localhost",
#         port="26257"  # Default port for CockroachDB
#     )
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT
#             'mycrdb' AS database_name,
#             sum(total_bytes)/(1024*1024) AS size_in_mb
#         FROM
#             crdb_internal.table_statistics;
#     """)
#     size = cur.fetchone()
#     cur.close()
#     conn.close()
#     return size

# print(get_database_size())


# import psycopg2

# def get_database_size():
#     conn = psycopg2.connect(
#         dbname="mycrdb",
#         user="root",
#         password="",
#         host="localhost",
#         port="26257"  # Default port for CockroachDB
#     )
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT
#             table_name,
#             ROUND((data_bytes + index_bytes + system_bytes)/(1024*1024), 2) AS size_in_mb
#         FROM
#             crdb_internal.tables
#         WHERE
#             database_name = 'mycrdb';
#     """)
#     sizes = cur.fetchall()
#     total_size = sum(size for _, size in sizes)
#     cur.close()
#     conn.close()
#     return total_size

# print(get_database_size())

import psycopg2

def get_database_size():
    conn = psycopg2.connect(
        dbname="mycrdb",
        user="root",
        password="",
        host="localhost",
        port="26257"  # Default port for CockroachDB
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT
            name,
            ROUND((data_bytes + index_bytes + system_bytes)/(1024*1024), 2) AS size_in_mb
        FROM
            crdb_internal.tables
        WHERE
            database_name = 'mycrdb';
    """)
    sizes = cur.fetchall()
    total_size = sum(size for _, size in sizes)
    cur.close()
    conn.close()
    return total_size

print(get_database_size())
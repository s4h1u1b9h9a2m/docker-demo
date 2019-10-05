from flask import Flask, jsonify
app = Flask(__name__)
from psycopg2 import pool
import pandas as pd

import os
postgres_host = 'db'
postgres_port = '5432'
postgres_user = 'postgres'
postgres_password = 'postgres'

driver = pool.ThreadedConnectionPool(2, 40,
    host=postgres_host, 
    port=postgres_port,
    user=postgres_user, 
    password=postgres_password
)

@app.route('/', methods=['GET'])
def health():
    conn = None
    output = output = jsonify({ 
        "status": 'Failed'
    })
    try:
        query = """
            select table_name from information_schema.tables;
        """
        conn = driver.getconn()
        df = pd.read_sql_query(query, con = conn)
        output = jsonify({ 
            "status": 'Success',
            "message": len(df)
        })
    except (Exception) as error :
        print(error)
        pass
    finally:
        if conn != None:
            driver.putconn(conn)
    return output
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
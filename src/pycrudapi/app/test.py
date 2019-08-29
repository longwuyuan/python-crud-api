# app.py
# Implements crud api
#
import flask
import flask_uuid
import psycopg2
from flask import Flask, request, jsonify
from flask_uuid import FlaskUUID
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
FlaskUUID(app)

# Healthcheck
@app.route('/')
def index():
    return jsonify({'message': 'ok'}), 200

try:
    pgdb_conn_pool = psycopg2.pool.ThreadedConnectionPool(1, 20, host="postgres0", user="dbuser0", password="pwd0*", database="titanicdb")

    if (pgdb_conn_pool):
        print("passengerlist - pgdb connected")

    # GET all
    @app.route('/passengerlist', methods=['GET'])
    def get_passengerlist():
#        conn = psycopg2.connect(host='postgres0', user='dbuser0', password='pwd0*', dbname='titanicdb')
        conn = pgdb_conn_pool.getconn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM titanic")
        resp = cur.fetchall()
        cur.close()
    #    conn.close()
        pgdb_conn_pool.putconn(conn)
        return jsonify(resp)
finally:
    print("closed")
#    pgdb_conn_pool.closeall()

if __name__ == '__main__':
    app.run(debug=True)
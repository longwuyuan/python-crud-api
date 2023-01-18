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
@app.route('/hello')
def index():
    return jsonify({'message': 'ok'}), 201

@app.route('/zero')
def zero():
    return jsonify({'0'}), 201

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

    # POST
    @app.route('/postpassenger', methods=['POST'])
    def post_passenger():
        req_data = request.get_json()
        _survived = req_data['survived']
        _passengerClass = req_data['passengerClass']
        _name = req_data['name']
        _sex = req_data['sex']
        _age = req_data['age']
        _siblingsOrSpousesAboard = req_data['siblingsOrSpousesAboard']
        _parentsOrChildrenAboard = req_data['parentsOrChildrenAboard']
        _fare = req_data['fare']
        query = 'INSERT INTO titanic(survived, "passengerClass", name, sex, age, "siblingsOrSpousesAboard", "parentsOrChildrenAboard", fare) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        post_data = (_survived, _passengerClass, _name, _sex, _age,
                    _siblingsOrSpousesAboard, _parentsOrChildrenAboard, _fare)
    #    conn = psycopg2.connect(host='postgres0', user='dbuser0', password='pwd0*', dbname='titanicdb')
        conn = pgdb_conn_pool.getconn()
        cur = conn.cursor()
        cur.execute(query, post_data)
        conn.commit()
        cur.close()
        query = "SELECT * FROM titanic WHERE name = " + "'" + _name + "'"
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        resp = cur.fetchall()
        cur.close()
    #    conn.close()
        pgdb_conn_pool.putconn(conn)
        return jsonify(resp)

    # GET
    @app.route('/getpassenger/<uuid:id>', methods=['GET'])
    def get_passenger(id):
        #    conn = psycopg2.connect(host='postgres0', user='dbuser0', password='pwd0*', dbname='titanicdb')
        conn = pgdb_conn_pool.getconn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM titanic where uuid::text = " + "'" + str(id) + "'"
        cur.execute(query)
        resp = cur.fetchone()
        cur.close()
    #    conn.close()
        pgdb_conn_pool.putconn(conn)
        return jsonify(resp)

    # DELETE
    @app.route('/deletepassenger/<uuid:id>', methods=['DELETE'])
    def delete_passenger(id):
        #    conn = psycopg2.connect(host='postgres0', user='dbuser0', password='pwd0*', dbname='titanicdb')
        conn = pgdb_conn_pool.getconn()
        cur = conn.cursor()
        query = "DELETE FROM titanic WHERE uuid::text = " + "'" + str(id) + "'"
        cur.execute(query)
        resp = conn.commit()
        cur.close()
    #    conn.close()
        pgdb_conn_pool.putconn(conn)
        return jsonify(resp)

    # PUT
    @app.route('/putpassenger/<uuid:id>', methods=['PUT'])
    def put_passenger(id):
        req_data = request.get_json()
        _survived = req_data['survived']
        _passengerClass = req_data['passengerClass']
        _name = req_data['name']
        _sex = req_data['sex']
        _age = req_data['age']
        _siblingsOrSpousesAboard = req_data['siblingsOrSpousesAboard']
        _parentsOrChildrenAboard = req_data['parentsOrChildrenAboard']
        _fare = req_data['fare']
        query = 'UPDATE titanic SET survived = %s, "passengerClass" = %s, name = %s, sex = %s, age = %s, "siblingsOrSpousesAboard" = %s, "parentsOrChildrenAboard" = %s, fare = %s WHERE uuid::text = ' + \
            "'" + str(id) + "'"
        put_data = (_survived, _passengerClass, _name, _sex, _age,
                    _siblingsOrSpousesAboard, _parentsOrChildrenAboard, _fare)
    #    conn = psycopg2.connect(host='postgres0', user='dbuser0', password='pwd0*', dbname='titanicdb')
        conn = pgdb_conn_pool.getconn()
        cur = conn.cursor()
        cur.execute(query, put_data)
        resp = conn.commit()
        cur.close()
    #    conn.close()
        pgdb_conn_pool.putconn(conn)
        return jsonify(resp)

finally:
    print("closing all")
#    if (pgdb_conn_pool):
#        pgdb_conn_pool.closeall()

if __name__ == '__main__':
    app.run(debug=True)

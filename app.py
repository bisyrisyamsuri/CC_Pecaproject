from unittest import result
from flask import Flask, request
from flask_mysqldb import MySQL
from flask import jsonify
import yaml

# access image with url /static/file_name.jpg
app = Flask(__name__, static_folder='gambar')

db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/jenis', methods=['GET'])
def jenis():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM tb_hewan")
    if result > 0:
        jenis = cur.fetchall()
        return jsonify({'data': jenis}, 200)
 
@app.route('/jenis/<jenis_id>', methods=['GET'])
def jenis_by_id(jenis_id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM tb_hewan where id = %s", jenis_id)
    if result > 0:
        jenis = cur.fetchone()
        return jsonify({'data': jenis}, 200)

@app.route('/profil', methods=['GET'])
def profil():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM register")
    if result > 0:
        jenis = cur.fetchall()
        return jsonify({'data': jenis}, 200)

@app.route('/register', methods=['POST'])
def register():
        user = request.form
        name = user['name']
        email = user['email']
        password = user['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO register(name, email, password) VALUES(%s, %s, %s)",(name, email, password))
        mysql.connection.commit()
        cur.close()
        return jsonify({'data': user}, 200)

if __name__ == '__main__':
    app.run(debug=True)
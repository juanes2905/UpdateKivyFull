from flask import Flask, jsonify, request
import json
import logging
import pymssql
import os

app = Flask(__name__)

def cargarSetting():
    settings_file = 'C:/Gobernador/ServiciosJuan/settings/Settings.json'
    default_settings = {
        "DATABASE": {
            "server": "127.0.0.1",
            "user": "user",
            "password": "User123",
            "database": "CI_ControlAccessDb"
        }
    }

    if not os.path.exists(settings_file):
        try:
            with open(settings_file, 'w') as f:
                json.dump(default_settings, f, indent=4)
                logging.info(f"WARNING: Creación del archivo exitosa {default_settings}")
            return default_settings['DATABASE']
        except Exception as e:
            logging.error(f"DATABASE: Error al crear el archivo de configuración {str(e)}")
            raise RuntimeError(f'Error al crear el archivo de configuración: {str(e)}')
    
    try:
        with open(settings_file) as f:
            settings = json.load(f)
            logging.info(f"SETTINGS: {str(settings)}")
        return settings['DATABASE']
    except Exception as e:
        raise RuntimeError(f'Error al cargar la configuración de la base de datos: {str(e)}')



def connectDB():
    settings = cargarSetting()
    conn = pymssql.connect(server=settings['server'], user=settings['user'], password=settings['password'], database=settings['database'])
    cursor = conn.cursor(as_dict=True)
    return (conn, cursor)

@app.route('/query', methods=['GET'])
def buscaAqui():
    query = request.args.get('query')
    if not query:
        logging.error("DATABASE: Eror sin consulta")
        return jsonify({'ERROR': 'Sin consulta '}), 400
    
    try:
        conn, cursor = connectDB()
        # cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        logging.info("DATABASE: Conexion a la base de datos exitosa")
        conn.close()
        return jsonify({'result': rows})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/login', methods=['POST'])
def login():
    logging.info("ENTRE A LA FUNCION LOGIN DE MI SERVICIO")
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        logging.error("SEARCH: Error no se puede ingresar sin validación previa")
        return jsonify({'error': 'Falta correo electrónico o contraseña'}), 400
    
    try:
        conn, cursor = connectDB()
        query = "SELECT Email, StoredPassword FROM Tb_Users WHERE Email = %s AND StoredPassword = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        #print("ESTA ES SU CONSULTA: " + user)
        conn.close()
        
        if user:
            logging.info(f"DATABASE: {user}")
            return jsonify({'success': True, 'email': user['Email'], 'password': user['StoredPassword']})
        else:
            return jsonify({'error': 'Correo electrónico o contraseña incorrectos'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/verUsers', methods=['GET'])
def listar_usuarios():
    try:
        conn, cursor = connectDB()
        query = "SELECT UserName, Email, StoredPassword, IsActive  FROM Tb_Users"
        cursor.execute(query)
        usuarios = cursor.fetchall()
        conn.close()
        return jsonify({'usuarios': usuarios})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
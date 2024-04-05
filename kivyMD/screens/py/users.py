import logging
import requests
from kivymd.toast import toast


def verUsers(self):
    try:
        response = requests.get('http://127.0.0.1:8000/verUsers')
        if response.status_code == 200:
            users = response.json().get('USUARIOS', [])
            for user in users:
                print(user)  # Aquí puedes hacer lo que quieras con los datos de usuario
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
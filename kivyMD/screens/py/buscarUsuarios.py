import logging
import requests
from kivymd.toast import toast

def buscarUsuario(self):
    buscar = self.Data.ids.busUsers.text
    if buscar:
        try:
            url = 'http://localhost:8000/buscarUsuarios'
            data = {'busUsers': buscar}
            logging.info(f"REQUEST: {data}")
            response = requests.post(url, data=data)

            if response.status_code == 200:
                usuario = response.json()
                if usuario.get('success', False):
                    self.Data.ids.usuario.text = usuario.get('UserName', '')
                    self.Data.ids.busEmail.text = usuario.get('email', '')
                    self.Data.ids.busPassword.text = usuario.get('password', '')
                    self.screen_manager.current = "data"
                else:
                    self.Data.ids.usuario.text = "Usuario no encontrado"
                    self.Data.ids.busEmail.text = ""
                    self.Data.ids.busPassword.text = ""
            else:
                logging.error("RESPONSE: USUARIO NO ENCONTRADO")
                toast("USUARIO NO ENCONTRADO")
                self.Data.ids.usuario.text = ""
                self.Data.ids.busEmail.text = ""
                self.Data.ids.busPassword.text = ""
        except Exception as error:
            logging.error(f"Error de conexión: {error}")
            toast("Error de conexión al servidor")

def btnHabilit(self):
    pass
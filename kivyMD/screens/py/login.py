import logging
import requests
from kivymd.toast import toast

def login(self):
    email = self.Login.ids.validaInp.text
    password = self.Login.ids.inpPass.text

    if email and password:
        try:
            url = 'http://localhost:8000/login'
            data = {'email': email, 'password': password}
            logging.info(f"RESPONSE: {data}")
            response = requests.post(url, data=data)
                
            if response.status_code == 200:
                json_response = response.json()                
                if json_response.get('success'):
                    self.screen_manager.current = "newview"
                    self.principal.ids.top_app_bar.right_action_items=[["logout", lambda x: self.confirm_logout()]]
                    logging.info("VIEW: INGRESANDO A LA VISTA")
                    logging.info("-----------------------------------------------------")
                else:
                    toast("Correo electrónico o contraseña incorrectos")
            else:
                toast("Correo electrónico o contraseña incorrectos")
        except Exception as e:
            logging.error(f"Error de conexión: {e}")
            toast("Error de conexión al servidor")
    else:
        toast("Debe ingresar correo electrónico y contraseña")


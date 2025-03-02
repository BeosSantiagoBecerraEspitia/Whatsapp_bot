import time
import spacy
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")
whatsapp_sesion = os.getenv("Chrome_user_rute")


# Configurar Chrome con sesión iniciada
chrome_options = Options()
#chrome_options.add_argument(f"--user-data-dir={whatsapp_sesion}")  
chrome_options.add_argument("profile-directory=Default")

# Iniciar el navegador
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")

input("Escanea el código QR si es necesario y presiona Enter para continuar...")

# Buscar el chat por nombre
contacto = "Pago Hamburguesa"
search_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
)
search_box.send_keys(contacto)
time.sleep(2)
search_box.send_keys(Keys.ENTER)
time.sleep(2)

# Función para leer el último mensaje del chat
def leer_ultimo_mensaje():
    mensajes = driver.find_elements(By.CSS_SELECTOR, "div._amjv div._akbu")

    if mensajes:
        return mensajes[-1].text  # Obtener el último mensaje
    return None

# Función para analizar el mensaje con SpaCy
def analizar_mensaje_spacy(ultimo_mensaje):
    doc = nlp(ultimo_mensaje)
    
    # Extraer entidades nombradas (como nombres, lugares, fechas)
    entidades = [ent.text for ent in doc.ents]

    # Detectar si es una pregunta
    if "?" in ultimo_mensaje:
        return "Parece que tienes una pregunta. ¿Puedes dar más detalles?"

    # Identificar si se menciona una ubicación
    for ent in doc.ents:
        if ent.label_ == "LOC":
            return f"Veo que mencionaste un lugar: {ent.text}. ¿Quieres más información sobre ello?"

    return "No estoy seguro de cómo responder a eso, pero dime más detalles."

# Función para enviar mensajes a WhatsApp
def enviar_mensaje(texto):
    chat_box = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
    )
    chat_box[1].send_keys(texto)
    chat_box[1].send_keys(Keys.ENTER)

# Bucle para leer mensajes y responder con IA
while True:
    ultimo_mensaje = leer_ultimo_mensaje()
    print("el ultimo mensaje es", ultimo_mensaje,"----fin-----")

    ultimo_mensaje_recibido = ultimo_mensaje

    if ultimo_mensaje:
        print(f"Mensaje recibido: {ultimo_mensaje}")

        # Analizar mensaje con SpaCy
        respuesta = analizar_mensaje_spacy(ultimo_mensaje)
        print(f"Respuesta generada: {respuesta}")
        
        
        if "message-out" in ultimo_mensaje.get_attribute("class"):
            print("el ultimo mensaje fue enviado por el bot")

        if ultimo_mensaje_recibido==respuesta:
          print("La respuesta es la misma que la última enviada. No se reenvía.")
        else:
            # Enviar la respuesta al chat
            enviar_mensaje(respuesta)

        

    time.sleep(5)  # Esperar antes de revisar de nuevo

# Cerrar el navegador al salir del bucle
driver.quit()


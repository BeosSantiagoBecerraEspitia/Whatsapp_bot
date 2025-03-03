#here im gonna fake some conversations 

import time
import spacy
import os


#charge the model
nlp = spacy.load("es_core_news_sm")



ultimo_mensaje="hola en que ciudad atienden?"

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

respuesta =analizar_mensaje_spacy(ultimo_mensaje)

print(respuesta)
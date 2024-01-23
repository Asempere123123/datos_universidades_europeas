import requests
from bs4 import BeautifulSoup
import sqlite3

from data.all_categories import processed_categories

conn = sqlite3.connect("data/universidades.db")
cur = conn.cursor()

def add_entry_to_database(url, categoria):
    print("https://edurank.org" + url)
    response = requests.get("https://edurank.org" + url)
    filtrado_por = categoria

    datos_texto = response.text
    soup = BeautifulSoup(datos_texto, 'html.parser')

    target_classes = ["block-cont", "pt-4", "mb-4"]
    target_divs = soup.find_all('div', class_=target_classes)

    clases_ubicacion = ["uni-card__geo", "text-center"]
    clases_rango = ["uni-card__rank"]
    clases_datos_especificos = ["col-6", "mb-2", "col-md-auto", "mb-md-0"]
    for div in target_divs:
        ubicacion = div.find("div", class_=clases_ubicacion)
        if not ubicacion:
            continue

        name = div.find("h2")
        if not name:
            continue

        ubicacion = ubicacion.find("span")
        posiciones = div.find_all("div", class_=clases_rango)

        posicion_local = posiciones[0].find("span")
        posicion_global = posiciones[1].find("span")

        datos_nombre = name.text.split(". ")
        posicion_europa = datos_nombre[0]
        nombre = datos_nombre[1]
        
        tasa_aceptacion = None
        cantidad_matriculados = None

        datos_especificos = div.find_all("div", class_=clases_datos_especificos)
        for dato in datos_especificos:
            dato_titulo = dato.find("dt")
            dato_valor = dato.find("dd")

            if dato_titulo is None:
                continue

            if dato_titulo.text == "Acceptance Rate":
                tasa_aceptacion = dato_valor.text
            elif dato_titulo.text == "Enrollment":
                cantidad_matriculados = dato_valor.text

        data = (nombre, ubicacion.text, posicion_local.text, posicion_global.text, posicion_europa, tasa_aceptacion, cantidad_matriculados, filtrado_por)
        try:
            cur.execute("INSERT OR IGNORE INTO universidades (nombre, ubicacion, posicion_local, posicion_global, posicion_europa, tasa_acceptacion, cantidad_matriculados, filtrado_por) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", data)
        except:
            print("No se ha podido añadir la siguiente universidad:")
            print(data)

    conn.commit()

for categorie in processed_categories:
    add_entry_to_database(categorie[1], categorie[0])
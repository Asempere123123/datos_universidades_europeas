import requests
from bs4 import BeautifulSoup

response = requests.get("https://edurank.org/engineering/eu/")

datos_texto = response.text
soup = BeautifulSoup(datos_texto, 'html.parser')

target_classes = ["block-cont", "pt-4", "mb-4"]
target_divs = soup.find_all('div', class_=target_classes)

c=0
clases_ubicacion = ["uni-card__geo", "text-center"]
for div in target_divs:
    ubicacion = div.find("div", class_=clases_ubicacion)
    if not ubicacion:
        continue

    name = div.find("h2")
    if not name:
        continue

    print(name.text)
    print(ubicacion)
    c+=1

print(c)
import mysql.connector
import requests
import time

API_KEY = "AIzaSyDCn1rHkWdu9U1CDKBpebsvhG49KpPnXrk"

def ligar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="parque",
        password="parque123",
        database="parque_db"
    )

def inserir_parque(nome, localizacao, latitude, longitude, capacidade):
    ligacao = ligar_bd()
    cursor = ligacao.cursor()
    cursor.execute("SELECT * FROM parques WHERE nome=%s AND localizacao=%s", (nome, localizacao))
    if not cursor.fetchone():
        sql = "INSERT INTO parques (nome, localizacao, latitude, longitude, capacidade) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome, localizacao, latitude, longitude, capacidade)
        cursor.execute(sql, valores)
        ligacao.commit()
        print(f"Inserido: {nome} | {localizacao} | {latitude}, {longitude}")
    else:
        print(f"Já existe: {nome} | {localizacao}")
    ligacao.close()

def buscar_parques(cidade):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=parking+in+{cidade}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for item in data.get("results", []):
            nome = item.get("name")
            localizacao = item.get("formatted_address")
            lat = item["geometry"]["location"]["lat"]
            lng = item["geometry"]["location"]["lng"]
            capacidade = 0
            inserir_parque(nome, localizacao, lat, lng, capacidade)
    else:
        print(f"Erro ao buscar parques em {cidade}: {response.status_code}")

cidades = ["Lisboa","Porto","Coimbra","Braga","Faro","Aveiro","Viseu","Leiria","Évora","Setúbal"]

while True:
    for cidade in cidades:
        buscar_parques(cidade)
        time.sleep(2)

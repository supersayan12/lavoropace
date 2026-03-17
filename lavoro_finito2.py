import streamlit as st
import folium
import requests
import polyline
from streamlit_folium import st_folium
from PIL import Image
import os

st.set_page_config(page_title="Monumenti della Memoria", layout="wide")

# ----------------------------
# DATI MONUMENTI
# ----------------------------

coordinate_monumenti = {
    "Monumento ai Partigiani": [9.6699656270115,45.69479467330056],
    "Monumento ai Caduti in Cielo": [9.592063561703863,45.524091321195705],
    "Monumento ai Cinque Martiri": [9.518603225152182,45.52352438953796],
    "Binario 21": [9.208378942342174,45.48826595076151],
    "Monumento alla Resistenza": [9.594868821115409,45.52317780483042]
}

start = [9.592146713429965,45.523298931107114]

descrizioni = {

"Monumento ai Partigiani":
"Realizzato da Giacomo Manzù e inaugurato nel 1977 a Bergamo in Piazza Matteotti. "
"Questo monumento celebra la Resistenza e gli uomini e le donne che si opposero "
"al nazifascismo per restituire all’Italia libertà e dignità.",

"Monumento ai Caduti in Cielo":
"Il Monumento ai Caduti in Cielo ricorda gli aviatori militari morti durante missioni "
"di guerra e di servizio. È stato realizzato dall’Associazione Arma Aeronautica "
"nel secondo dopoguerra (anni ’50). Il monumento si trova a Treviglio.",

"Monumento ai Cinque Martiri":
"Questo monumento, voluto dal Comune e dall’ANPI di Cassano d’Adda, commemora "
"i cinque partigiani fucilati il 31 marzo 1945 in rappresaglia dai nazifascisti. "
"È simbolo di memoria e resistenza.",

"Binario 21":
"Dal Binario 21 della Stazione Centrale di Milano, tra il 1943 e il 1945, "
"partirono treni carichi di ebrei, oppositori politici e partigiani diretti "
"ai campi di sterminio. Oggi è il Memoriale della Shoah.",

"Monumento alla Resistenza":
"Il Monumento alla Resistenza di Treviglio è dedicato ai partigiani e ai cittadini "
"che si opposero al nazifascismo durante la Seconda guerra mondiale. "
"È un simbolo di libertà e democrazia."
}

# ----------------------------
# SIDEBAR MENU
# ----------------------------

st.sidebar.title("Menu")

pagina = st.sidebar.radio(
    "Vai a:",
    ["Home", "Lista Monumenti"]
)

# ----------------------------
# HOME
# ----------------------------

if pagina == "Home":

    st.title("MONUMENTI DELLA MEMORIA")

    st.write("""
Questo progetto racconta alcuni dei principali monumenti
legati alla Resistenza, alla guerra e alla memoria storica.

Ogni luogo è accompagnato da una mappa interattiva
per comprenderne il valore storico e culturale.
""")

    if os.path.exists("vittoriano-altare-della-patria.png"):
        image = Image.open("vittoriano-altare-della-patria.png")
        st.image(image, width=400)

# ----------------------------
# LISTA MONUMENTI
# ----------------------------

if pagina == "Lista Monumenti":

    monumento = st.selectbox(
        "Seleziona un monumento",
        list(coordinate_monumenti.keys())
    )

    st.header(monumento)

    st.write(descrizioni[monumento])

    # ----------------------------
    # IMMAGINE
    # ----------------------------

    nome_file = monumento.lower().replace(" ", "_") + ".png"

    if os.path.exists(nome_file):
        image = Image.open(nome_file)
        st.image(image, width=500)

    # ----------------------------
    # MAPPA
    # ----------------------------

    end = coordinate_monumenti[monumento]
    route_coords = []

    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[0]},{start[1]};{end[0]},{end[1]}?overview=full&geometries=polyline"
        response = requests.get(url, timeout=5).json()
        route_coords = polyline.decode(response['routes'][0]['geometry'])
    except:
        pass

    if route_coords:

        mappa = folium.Map(location=route_coords[0], zoom_start=13)

        folium.PolyLine(
            route_coords,
            color="blue",
            weight=5
        ).add_to(mappa)

        folium.Marker(route_coords[0], popup="Partenza").add_to(mappa)
        folium.Marker(route_coords[-1], popup="Arrivo").add_to(mappa)

    else:

        mappa = folium.Map(location=end, zoom_start=13)
        folium.Marker(end, popup=monumento).add_to(mappa)
        
    st_folium(mappa, width=900)
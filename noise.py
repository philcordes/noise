import streamlit as st
import numpy as np

st.set_page_config(page_title="Kuma Schallausbreitungsrechner", layout="centered")

# Kopfzeile mit Logo
col_logo, col_title = st.columns([5, 1])
with col_title:
    st.image("https://www.bayern-innovativ.de/fileadmin/map/bilder/bayern-innovativ/messe/kundenlogos/kumandra-ryve500px.jpg", width=300)

st.title("\U0001F50A Schallausbreitungs-berechnung nach vereinfachter Methode")


st.markdown("""
Dieses Tool berechnet den **Schalldruckpegel** an einem Immissionsort basierend auf:
- dem Schalldruckpegel in 1 m Entfernung *(oder optional Schallleistungspegel)*,
- dem Abstand zur Quelle,
- optionalen Dämpfungen durch Boden, Luft oder Hindernisse.
""")

# Eingaben
col1, col2 = st.columns(2)

with col1:
    eingabe_typ = st.radio("Welche Art Pegel liegt vor?", ["Schalldruckpegel @1 m (Lp)", "Schallleistungspegel (Lw)"])
    if eingabe_typ == "Schalldruckpegel @1 m (Lp)":
        Lp_1m = st.number_input("Schalldruckpegel in 1 m [dB(A)]", min_value=40.0, max_value=130.0, value=80.0)
    else:
        Lw = st.number_input("Schallleistungspegel [dB(A)]", min_value=40.0, max_value=150.0, value=91.0)

with col2:
    distance = st.number_input("Abstand zum Immissionsort [m]", min_value=1.0, max_value=1000.0, value=50.0)
    abschirmung = st.slider("Abschätzung Abschirmung durch Hindernisse [dB]", min_value=0, max_value=25, value=0)
    bodenwirkung = st.slider("Boden-/Bodenabsorption [dB]", min_value=-5, max_value=5, value=0)
    luftdampfung = st.slider("Luftabsorption (nur für große Distanzen) [dB]", min_value=0, max_value=5, value=0)

# Umrechnung Lp@1m zu Lw falls erforderlich
if eingabe_typ == "Schalldruckpegel @1 m (Lp)":
    Lw = Lp_1m + 8  # konservativ: Halbraum

# Geometrische Ausbreitung
A_div = 20 * np.log10(distance) + 11

# Gesamtdämpfung
A_total = A_div + luftdampfung + bodenwirkung + abschirmung

# Immissionspegel berechnen
Lp_immission = Lw - A_total

# Ausgabe
st.subheader("\U0001F4C8 Ergebnis")
st.markdown(f"**Schallleistungspegel (Lw):** {Lw:.1f} dB(A)")
st.markdown(f"**Geometrische Dämpfung (A_div):** {A_div:.1f} dB")
st.markdown(f"**Gesamtdämpfung (A_total):** {A_total:.1f} dB")
st.markdown(f"**Schalldruckpegel am Immissionsort (Lp):** \n\n### {Lp_immission:.1f} dB(A)")

st.caption("Berechnung basierend auf vereinfachter Formel nach DIN EN ISO 9613-2 / VDI 2571")

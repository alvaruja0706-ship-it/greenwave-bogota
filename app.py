import streamlit as st
import pandas as pd
import pydeck as pdk
import random

# Configuración inicial de la página
st.set_page_config(
    page_title="GreenWave - Red Semafórica Inteligente",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 GreenWave: Sistema Inteligente de Red Semafórica y SITP")
st.markdown("""
*Plataforma de gestión de tráfico urbano en tiempo real basada en modelado espacial y semaforización adaptativa.*
""")

# Catálogo real de intersecciones críticas en Bogotá (WGS84 / EPSG:4326)
INTERSECCIONES_BOGOTA = [
    {"id": 1, "nombre": "Calle 26 con Av. Caracas", "lat": 4.6097, "lon": -74.0817, "corredor": "Troncal Eje Ambiental / Caracas"},
    {"id": 2, "nombre": "Calle 45 con NQS", "lat": 4.6280, "lon": -74.0650, "corredor": "Troncal NQS"},
    {"id": 3, "nombre": "Calle 72 con Carrera 11", "lat": 4.6580, "lon": -74.0560, "corredor": "Corredor Zona Rosa / Chapinero"},
    {"id": 4, "nombre": "Calle 100 con Autopista Norte", "lat": 4.6750, "lon": -74.0480, "corredor": "Troncal Autonorte"},
    {"id": 5, "nombre": "Avenida Jiménez con Carrera Séptima", "lat": 4.6010, "lon": -74.0720, "corredor": "Centro Histórico"}
]

# Generar datos dinámicos simulando telemetría en vivo
red_actualizada = []
for nodo in INTERSECCIONES_BOGOTA:
    pasajeros_bus = random.randint(30, 85)
    densidad = random.choice(["Fluida", "Moderada", "Saturada / Hora Pico"])
    
    if pasajeros_bus > 60 or densidad == "Saturada / Hora Pico":
        tiempo_verde = 60
        estado = "Prioridad SITP Activa (Verde extendido)"
        tipo_color = "verde"
    else:
        tiempo_verde = 30
        estado = "Ciclo Normal Sincronizado"
        tipo_color = "rojo"
        
    red_actualizada.append({
        "id": nodo["id"],
        "interseccion": nodo["nombre"],
        "corredor": nodo["corredor"],
        "lat": nodo["lat"],
        "lon": nodo["lon"],
        "pasajeros_bus": pasajeros_bus,
        "densidad_trafico": densidad,
        "tiempo_verde_asignado": tiempo_verde,
        "estado_semaforo": estado,
        "tipo_color": tipo_color
    })

df_nodos = pd.DataFrame(red_actualizada)

# Asignar colores y radios para el mapa
df_nodos['color'] = df_nodos['tipo_color'].apply(
    lambda x: [0, 255, 128, 200] if x == 'verde' else [255, 75, 75, 180]
)
df_nodos['radio'] = df_nodos['tipo_color'].apply(
    lambda x: 200 if x == 'verde' else 120
)

# --- PANEL DE MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📍 Nodos Monitoreados", value=len(df_nodos), delta="Bogotá D.C.")
with col2:
    promedio_pasajeros = int(df_nodos['pasajeros_bus'].mean())
    st.metric(label="🚌 Ocupación Promedio SITP", value=f"{promedio_pasajeros} pas.", delta="En tiempo real")
with col3:
    nodos_prioridad = len(df_nodos[df_nodos['tipo_color'] == 'verde'])
    st.metric(label="🚦 Semáforos en Prioridad", value=f"{nodos_prioridad} activos", delta="Adaptativos")
with col4:
    st.metric(label="🔄 Estado del Sistema", value="Operativo", delta="Cloud Ready")

st.markdown("---")

# --- MAPA Y TABLA ---
col_mapa, col_info = st.columns([2, 1])

with col_mapa:
    st.subheader("🗺️ Visualización Espacial de la Red Semafórica")
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        df_nodos,
        get_position='[lon, lat]',
        get_color='color',
        get_radius='radio',
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=4.6350,
        longitude=-74.0650,
        zoom=11.5,
        pitch=30,
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text": "Intersección: {interseccion}\nCorredor: {corredor}\nPasajeros Bus: {pasajeros_bus}\nEstado: {estado_semaforo}\nVerde Asignado: {tiempo_verde_asignado} seg"
        }
    )
    st.pydeck_chart(r)

with col_info:
    st.subheader("📊 Estado de Nodos en Vivo")
    resumen_tabla = df_nodos[['interseccion', 'tiempo_verde_asignado', 'densidad_trafico']]
    resumen_tabla.columns = ['Intersección', 'Verde (s)', 'Densidad']
    st.dataframe(resumen_tabla, hide_index=True, use_container_width=True)

# --- DOCUMENTACIÓN TÉCNICA ---
with st.expander("📌 Documentación Técnica del Prototipo (Para Exposición)"):
    st.markdown("""
    * **Arquitectura:** Aplicación web monolítica optimizada para despliegue en la nube mediante Streamlit Cloud.
    * **Modelo Ge espacial:** Ubicaciones reales basadas en el sistema de coordenadas de Bogotá (`EPSG:4326`).
    * **Algoritmo de Control:** Reglas heurísticas dinámicas para priorizar pasos de buses del SITP según saturación de vía.
    """)
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

# Creamos un fragmento que se actualiza automáticamente cada 3 segundos
@st.fragment(run_every=3)
def mostrar_panel_en_vivo():
    # Red extendida de intersecciones críticas en Bogotá (WGS84 / EPSG:4326)
    INTERSECCIONES_BOGOTA = [
        {"id": 1, "nombre": "Calle 26 con Av. Caracas", "lat": 4.6097, "lon": -74.0817, "corredor": "Troncal Eje Ambiental / Caracas"},
        {"id": 2, "nombre": "Calle 45 con NQS", "lat": 4.6280, "lon": -74.0650, "corredor": "Troncal NQS"},
        {"id": 3, "nombre": "Calle 72 con Carrera 11", "lat": 4.6580, "lon": -74.0560, "corredor": "Corredor Zona Rosa / Chapinero"},
        {"id": 4, "nombre": "Calle 100 con Autopista Norte", "lat": 4.6750, "lon": -74.0480, "corredor": "Troncal Autonorte"},
        {"id": 5, "nombre": "Avenida Jiménez con Carrera Séptima", "lat": 4.6010, "lon": -74.0720, "corredor": "Centro Histórico"},
        {"id": 6, "nombre": "Calle 80 con Av. Ciudad de Cali", "lat": 4.7100, "lon": -74.1100, "corredor": "Corredor Occidente / Calle 80"},
        {"id": 7, "nombre": "Av. Boyacá con Calle 127", "lat": 4.7050, "lon": -74.0600, "corredor": "Av. Boyacá (Suba)"},
        {"id": 8, "nombre": "Calle 13 con Carrera 68", "lat": 4.6400, "lon": -74.1150, "corredor": "Zona Industrial / Calle 13"},
        {"id": 9, "nombre": "Av. 1 de Mayo con Carrera 68", "lat": 4.6000, "lon": -74.1300, "corredor": "Corredor Sur"},
        {"id": 10, "nombre": "Autopista Norte con Calle 170", "lat": 4.7400, "lon": -74.0430, "corredor": "Troncal Autonorte Norte"},
        {"id": 11, "nombre": "Carrera Séptima con Calle 100", "lat": 4.6850, "lon": -74.0440, "corredor": "Corredor Norte / 7ma"},
        {"id": 12, "nombre": "Autopista Sur con Bosa", "lat": 4.5800, "lon": -74.1800, "corredor": "Troncal Autopista Sur"}
    ]

    # Generar datos dinámicos simulando telemetría en vivo
    red_actualizada = []
    for nodo in INTERSECCIONES_BOGOTA:
        pasajeros_bus = random.randint(25, 90)
        densidad = random.choice(["Fluida", "Moderada", "Saturada / Hora Pico"])
        
        if pasajeros_bus > 60 or densidad == "Saturada / Hora Pico":
            tiempo_verde = 60
            estado = "Prioridad SITP Activa"
            tipo_color = "verde"
        else:
            tiempo_verde = 30
            estado = "Ciclo Normal"
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
        lambda x: 220 if x == 'verde' else 140
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
        st.metric(label="🔄 Estado del Sistema", value="Operativo", delta="Sincronizado")

    st.markdown("---")

    # --- MAPA INTERACTIVO Y TABLA ---
    col_mapa, col_info = st.columns([2, 1])
    
    with col_mapa:
        st.subheader("🗺️ Mapa Interactivo de Tráfico en Vivo")
        
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
            zoom=11.2,
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
        st.subheader("📊 Estado de Nodos")
        resumen_tabla = df_nodos[['interseccion', 'tiempo_verde_asignado', 'densidad_trafico']]
        resumen_tabla.columns = ['Intersección', 'Verde (s)', 'Densidad']
        st.dataframe(resumen_tabla, hide_index=True, use_container_width=True)

# Ejecutamos el panel dinámico
mostrar_panel_en_vivo()

# --- PANEL INFORMATIVO LIMPIO ---
with st.expander("📌 Panel de Control y Resumen Técnico"):
    st.markdown("""
    * **Módulo Geespacial:** Visualización de nodos estratégicos distribuidos por las principales troncales de Bogotá.
    * **Automatización:** Reglas de control dinámico que recalculan los tiempos de verde según la saturación de pasajeros en los buses del SITP.
    """)

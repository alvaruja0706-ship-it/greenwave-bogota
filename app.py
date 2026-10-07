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

st.title("🚦 GreenWave: Sistema Inteligente de Gestión de Tráfico y Semaforización")
st.markdown("""
*Plataforma de control de tráfico urbano para mitigar la congestión vehicular (carros, motos y SITP) en Bogotá D.C mediante semaforización adaptativa.*
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

    # Simulación de telemetría de tráfico mixto (Carros, Motos y Buses)
    red_actualizada = []
    for nodo in INTERSECCIONES_BOGOTA:
        carros = random.randint(120, 350)
        motos = random.randint(80, 280)
        buses_sitp = random.randint(15, 45)
        
        # Nivel de saturación total del nodo
        carga_total = carros + (motos * 0.7) + (buses_sitp * 1.5)
        
        if carga_total > 350:
            estado_trafico = "Trancón Crítico (Saturado)"
            tiempo_verde = 65
            estado_semaforo = "Ciclo Extendido por Saturación"
            tipo_color = "verde" # Verde prioritario para evacuar la vía
        elif carga_total > 250:
            estado_trafico = "Tráfico Moderado"
            tiempo_verde = 45
            estado_semaforo = "Ciclo Dinámico Ajustado"
            tipo_color = "amarillo"
        else:
            estado_trafico = "Flujo Fluido"
            tiempo_verde = 30
            estado_semaforo = "Ciclo Normal Sincronizado"
            tipo_color = "rojo" # Ciclo estándar
            
        red_actualizada.append({
            "id": nodo["id"],
            "interseccion": nodo["nombre"],
            "corredor": nodo["corredor"],
            "lat": nodo["lat"],
            "lon": nodo["lon"],
            "carros": carros,
            "motos": motos,
            "buses": buses_sitp,
            "estado_trafico": estado_trafico,
            "tiempo_verde_asignado": tiempo_verde,
            "estado_semaforo": estado_semaforo,
            "tipo_color": tipo_color
        })

    df_nodos = pd.DataFrame(red_actualizada)

    # Asignar colores profesionales en el mapa según el estado del semáforo/tráfico
    def asignar_color(tipo):
        if tipo == 'verde':
            return [0, 220, 100, 210]     # Verde (Prioridad/Evacuación)
        elif tipo == 'amarillo':
            return [255, 180, 0, 210]   # Amarillo (Precaución/Moderado)
        else:
            return [235, 60, 60, 200]     # Rojo (Normal/Estándar)

    df_nodos['color'] = df_nodos['tipo_color'].apply(asignar_color)
    df_nodos['radio'] = df_nodos['tipo_color'].apply(lambda x: 240 if x == 'verde' else (180 if x == 'amarillo' else 140))

    # --- PANEL DE MÉTRICAS GLOBALES ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📍 Nodos Semafóricos", value=len(df_nodos), delta="Red Urbana Bogotá")
    with col2:
        total_vehiculos = int((df_nodos['carros'] + df_nodos['motos'] + df_nodos['buses']).mean())
        st.metric(label="🚗 Flujo Promedio de Vehículos", value=f"{total_vehiculos} un.", delta="Carros, Motos y Buses")
    with col3:
        nodos_prioridad = len(df_nodos[df_nodos['tipo_color'] == 'verde'])
        st.metric(label="🚦 Semáforos en Modo Alivio", value=f"{nodos_prioridad} activos", delta="Mitigando Trancón")
    with col4:
        st.metric(label="⚡ Sistema Adaptativo", value="Operativo", delta="En Tiempo Real")

    st.markdown("---")

    # --- MAPA INTERACTIVO Y TABLA DE ESTADO ---
    col_mapa, col_info = st.columns([2, 1])
    
    with col_mapa:
        st.subheader("🗺️ Mapa Interactivo de la Red Semafórica y Tráfico Mixto")
        
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
            pitch=35,
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "text": "Intersección: {interseccion}\nCorredor: {corredor}\nCarros: {carros} | Motos: {motos} | Buses: {buses}\nEstado Vía: {estado_trafico}\nAcción Semáforo: {estado_semaforo}\nTiempo Verde: {tiempo_verde_asignado}s"
            }
        )
        st.pydeck_chart(r)

    with col_info:
        st.subheader("📊 Monitoreo de Nodos")
        resumen_tabla = df_nodos[['interseccion', 'tiempo_verde_asignado', 'estado_trafico']]
        resumen_tabla.columns = ['Intersección', 'Verde(s)', 'Estado del Tráfico']
        st.dataframe(resumen_tabla, hide_index=True, use_container_width=True)

# Ejecutamos el panel dinámico
mostrar_panel_en_vivo()

# --- PANEL DE CONTROL TÉCNICO ---
with st.expander("📌 Resumen del Problema y Solución Propuesta"):
    st.markdown("""
    * **Problemática:** La congestión vehicular en Bogotá generada por el alto volumen simultáneo de vehículos particulares (carros), motocicletas y flotas de transporte público (SITP), agravada por una deficiente sincronización estática de los semáforos tradicionales.
    * **Solución (GreenWave):** Un sistema de semaforización adaptativa que analiza la densidad del tráfico mixto en tiempo real y reconfigura los ciclos de verde de forma inteligente para evitar trancones y mejorar la fluidez vial.
    """)

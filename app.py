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
*Plataforma de control adaptativo para mitigar la congestión vehicular (carros, motos y SITP) en las principales vías de Bogotá D.C.*
""")

# Creamos un fragmento que se actualiza automáticamente cada 3 segundos
@st.fragment(run_every=3)
def mostrar_panel_en_vivo():
    # Red de intersecciones críticas reales en Bogotá (WGS84 / EPSG:4326)
    INTERSECCIONES_BOGOTA = [
        {"id": 1, "nombre": "Calle 26 con Av. Caracas", "corredor": "Troncal Eje Ambiental / Caracas", "lat": 4.6097, "lon": -74.0817},
        {"id": 2, "nombre": "Calle 45 con NQS", "corredor": "Troncal NQS", "lat": 4.6280, "lon": -74.0650},
        {"id": 3, "nombre": "Calle 72 con Carrera 11", "corredor": "Corredor Zona Rosa / Chapinero", "lat": 4.6580, "lon": -74.0560},
        {"id": 4, "nombre": "Calle 100 con Autopista Norte", "corredor": "Troncal Autonorte", "lat": 4.6750, "lon": -74.0480},
        {"id": 5, "nombre": "Avenida Jiménez con Carrera 7ma", "corredor": "Centro Histórico", "lat": 4.6010, "lon": -74.0720},
        {"id": 6, "nombre": "Calle 80 con Av. Ciudad de Cali", "corredor": "Corredor Occidente / Calle 80", "lat": 4.7100, "lon": -74.1100},
        {"id": 7, "nombre": "Av. Boyacá con Calle 127", "corredor": "Av. Boyacá (Suba)", "lat": 4.7050, "lon": -74.0600},
        {"id": 8, "nombre": "Calle 13 con Carrera 68", "corredor": "Zona Industrial / Calle 13", "lat": 4.6400, "lon": -74.1150},
        {"id": 9, "nombre": "Av. 1 de Mayo con Carrera 68", "corredor": "Corredor Sur", "lat": 4.6000, "lon": -74.1300},
        {"id": 10, "nombre": "Autopista Norte con Calle 170", "corredor": "Troncal Autonorte Norte", "lat": 4.7400, "lon": -74.0430},
        {"id": 11, "nombre": "Carrera 7ma con Calle 100", "corredor": "Corredor Norte / 7ma", "lat": 4.6850, "lon": -74.0440},
        {"id": 12, "nombre": "Autopista Sur con Bosa", "corredor": "Troncal Autopista Sur", "lat": 4.5800, "lon": -74.1800}
    ]

    # Simulación coherente del tráfico mixto en tiempo real
    red_actualizada = []
    for nodo in INTERSECCIONES_BOGOTA:
        # Generación estocástica coherente de vehículos
        carros = random.randint(110, 310)
        motos = random.randint(80, 240)
        buses_sitp = random.randint(10, 38)
        
        # Cálculo de carga total ponderada para el tráfico
        carga_total = carros + (motos * 0.7) + (buses_sitp * 1.5)
        
        if carga_total > 320:
            estado_trafico = "🔴 Trancón Crítico (Saturado)"
            tiempo_verde = 65
            accion_sistema = "Ciclo Extendido (Prioridad de Evacuación)"
            color_halo = [255, 59, 48, 220]     # Rojo intenso
        elif carga_total > 210:
            estado_trafico = "🟡 Tráfico Moderado"
            tiempo_verde = 45
            accion_sistema = "Ciclo Dinámico Ajustado"
            color_halo = [255, 204, 0, 220]     # Amarillo
        else:
            estado_trafico = "🟢 Flujo Fluido"
            tiempo_verde = 30
            accion_sistema = "Ciclo Estándar Sincronizado"
            color_halo = [52, 199, 89, 220]     # Verde
            
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
            "tiempo_verde": tiempo_verde,
            "accion_sistema": accion_sistema,
            "icono": "🚦",
            "color_halo": color_halo
        })

    df_nodos = pd.DataFrame(red_actualizada)

    # --- MÉTRICAS SUPERIORES ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📍 Nodos Semafóricos", value=len(df_nodos), delta="Bogotá D.C.")
    with col2:
        promedio_total = int((df_nodos['carros'] + df_nodos['motos'] + df_nodos['buses']).mean())
        st.metric(label="🚗 Parque Automotor Promedio", value=f"{promedio_total} un.", delta="Carros, Motos y Buses")
    with col3:
        nodos_criticos = len(df_nodos[df_nodos['tiempo_verde'] == 65])
        st.metric(label="🚨 Nodos Mitigando Trancón", value=f"{nodos_criticos} activos", delta="Adaptativos")
    with col4:
        st.metric(label="⚡ Sistema Inteligente", value="Operativo", delta="Actualización en Vivo")

    st.markdown("---")

    # --- MAPA Y PANEL LATERAL ---
    col_mapa, col_panel = st.columns([2, 1])
    
    with col_mapa:
        st.subheader("🗺️ Mapa Interactivo: Red de Semáforos Inteligentes")
        st.markdown("*(Pasa el cursor sobre cualquier **🚦** para ver el reporte detallado del tráfico)*")

        # Capa 1: Halo circular de fondo (indica el estado de saturación del semáforo)
        layer_halo = pdk.Layer(
            'ScatterplotLayer',
            df_nodos,
            get_position='[lon, lat]',
            get_color='color_halo',
            get_radius=280,
            pickable=True,
            auto_highlight=True,
        )

        # Capa 2: Íconos de semáforo reales (emojis 🚦) en cada intersección
        layer_iconos = pdk.Layer(
            'TextLayer',
            df_nodos,
            get_position='[lon, lat]',
            get_text='icono',
            get_size=24,
            get_color=[255, 255, 255, 255],
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=4.6350,
            longitude=-74.0650,
            zoom=11.2,
            pitch=35,
        )

        r = pdk.Deck(
            layers=[layer_halo, layer_iconos],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>Intersección:</b> {interseccion}<br/>"
                        "<b>Corredor Vial:</b> {corredor}<br/>"
                        "----------------------------------<br/>"
                        "🚗 <b>Carros Particulares:</b> {carros} un.<br/>"
                        "🏍️ <b>Motocicletas:</b> {motos} un.<br/>"
                        "🚌 <b>Buses SITP:</b> {buses} un.<br/>"
                        "----------------------------------<br/>"
                        "📊 <b>Estado de la Vía:</b> {estado_trafico}<br/>"
                        "⚙️ <b>Acción del Semáforo:</b> {accion_sistema}<br/>"
                        "⏱️ <b>Ciclo Verde Asignado:</b> {tiempo_verde} segundos",
                "style": {
                    "backgroundColor": "#181818",
                    "color": "#ffffff",
                    "font-family": "sans-serif",
                    "padding": "14px",
                    "border-radius": "8px",
                    "border": "1px solid #444"
                }
            }
        )
        st.pydeck_chart(r)

    with col_panel:
        st.subheader("🔍 Inspector de Semáforos en Vivo")
        
        # Selector para consultar al detalle cualquier intersección
        nodos_lista = df_nodos['interseccion'].tolist()
        nodo_elegido = st.selectbox("Seleccione un semáforo de la red:", nodos_lista)
        
        datos_nodo = df_nodos[df_nodos['interseccion'] == nodo_elegido].iloc[0]
        
        st.markdown(f"""
        ### 🚦 {datos_nodo['interseccion']}
        * **Corredor:** {datos_nodo['corredor']}
        * **Estado del Tráfico:** {datos_nodo['estado_trafico']}
        
        ---
        **Conteo Aproximado en Tiempo Real:**
        * 🚗 **Carros:** `{datos_nodo['carros']}` vehículos
        * 🏍️ **Motos:** `{datos_nodo['motos']}` motocicletas
        * 🚌 **Buses SITP:** `{datos_nodo['buses']}` unidades
        
        ---
        **Respuesta del Sistema Adaptativo:**
        * ⚙️ **Acción:** {datos_nodo['accion_sistema']}
        * ⏱️ **Tiempo Verde:** **{datos_nodo['tiempo_verde']} segundos**
        """)

# Ejecutamos la aplicación
mostrar_panel_en_vivo()

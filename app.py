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
*Control adaptativo de tráfico urbano para mitigar embotellamientos por vehículos particulares, motocicletas y flotas del SITP en Bogotá D.C.*
""")

# Creamos un fragmento que se actualiza automáticamente cada 3 segundos
@st.fragment(run_every=3)
def mostrar_panel_en_vivo():
    # Red de intersecciones críticas en Bogotá (WGS84 / EPSG:4326)
    INTERSECCIONES_BOGOTA = [
        {"id": 1, "nombre": "🚦 Semáforo T-01: Calle 26 con Av. Caracas", "lat": 4.6097, "lon": -74.0817, "corredor": "Troncal Eje Ambiental / Caracas"},
        {"id": 2, "nombre": "🚦 Semáforo T-02: Calle 45 con NQS", "lat": 4.6280, "lon": -74.0650, "corredor": "Troncal NQS"},
        {"id": 3, "nombre": "🚦 Semáforo T-03: Calle 72 con Carrera 11", "lat": 4.6580, "lon": -74.0560, "corredor": "Corredor Zona Rosa / Chapinero"},
        {"id": 4, "nombre": "🚦 Semáforo T-04: Calle 100 con Autopista Norte", "lat": 4.6750, "lon": -74.0480, "corredor": "Troncal Autonorte"},
        {"id": 5, "nombre": "🚦 Semáforo T-05: Avenida Jiménez con Carrera 7ma", "lat": 4.6010, "lon": -74.0720, "corredor": "Centro Histórico"},
        {"id": 6, "nombre": "🚦 Semáforo T-06: Calle 80 con Av. Ciudad de Cali", "lat": 4.7100, "lon": -74.1100, "corredor": "Corredor Occidente / Calle 80"},
        {"id": 7, "nombre": "🚦 Semáforo T-07: Av. Boyacá con Calle 127", "lat": 4.7050, "lon": -74.0600, "corredor": "Av. Boyacá (Suba)"},
        {"id": 8, "nombre": "🚦 Semáforo T-08: Calle 13 con Carrera 68", "lat": 4.6400, "lon": -74.1150, "corredor": "Zona Industrial / Calle 13"},
        {"id": 9, "nombre": "🚦 Semáforo T-09: Av. 1 de Mayo con Carrera 68", "lat": 4.6000, "lon": -74.1300, "corredor": "Corredor Sur"},
        {"id": 10, "nombre": "🚦 Semáforo T-10: Autopista Norte con Calle 170", "lat": 4.7400, "lon": -74.0430, "corredor": "Troncal Autonorte Norte"},
        {"id": 11, "nombre": "🚦 Semáforo T-11: Carrera 7ma con Calle 100", "lat": 4.6850, "lon": -74.0440, "corredor": "Corredor Norte / 7ma"},
        {"id": 12, "nombre": "🚦 Semáforo T-12: Autopista Sur con Bosa", "lat": 4.5800, "lon": -74.1800, "corredor": "Troncal Autopista Sur"}
    ]

    # Simulación en tiempo real del tráfico mixto (Carros, Motos y Buses)
    red_actualizada = []
    for nodo in INTERSECCIONES_BOGOTA:
        carros = random.randint(100, 320)
        motos = random.randint(70, 250)
        buses_sitp = random.randint(12, 40)
        
        carga_total = carros + (motos * 0.7) + (buses_sitp * 1.5)
        
        if carga_total > 330:
            estado_trafico = "🔴 Trancón Crítico (Saturado)"
            tiempo_verde = 65
            accion_sistema = "Ciclo Extendido para Evacuar Flujo"
            color_rgb = [255, 69, 58, 240]      # Rojo intenso brillante
            radio_nodo = 320
        elif carga_total > 220:
            estado_trafico = "🟡 Tráfico Moderado (Precaución)"
            tiempo_verde = 45
            accion_sistema = "Ciclo Dinámico Ajustado"
            color_rgb = [255, 204, 0, 240]     # Amarillo brillante
            radio_nodo = 260
        else:
            estado_trafico = "🟢 Flujo Fluido (Óptimo)"
            tiempo_verde = 30
            accion_sistema = "Ciclo Estándar Sincronizado"
            color_rgb = [52, 199, 89, 240]     # Verde brillante
            radio_nodo = 220
            
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
            "color": color_rgb,
            "radio": radio_nodo
        })

    df_nodos = pd.DataFrame(red_actualizada)

    # --- MÉTRICAS SUPERIORES ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📍 Nodos Semafóricos", value=len(df_nodos), delta="Red Activa Bogotá")
    with col2:
        promedio_autos = int((df_nodos['carros'] + df_nodos['motos'] + df_nodos['buses']).mean())
        st.metric(label="🚗 Parque Automotor Promedio", value=f"{promedio_autos} un.", delta="Carros, Motos y SITP")
    with col3:
        nodos_criticos = len(df_nodos[df_nodos['tiempo_verde'] == 65])
        st.metric(label="🚨 Nodos en Mitigación de Trancón", value=f"{nodos_criticos} activos", delta="Prioridad Adaptativa")
    with col4:
        st.metric(label="⚡ Estado del Algoritmo", value="En Línea", delta="Tiempo Real (3s)")

    st.markdown("---")

    # --- MAPA Y DETALLE INTERACTIVO ---
    col_mapa, col_panel = st.columns([2, 1])
    
    with col_mapa:
        st.subheader("🗺️ Mapa Geoespacial: Red de Semáforos Inteligentes")
        st.markdown("*(Pasa el cursor o haz clic en cualquier nodo para ver el reporte detallado del semáforo y el tráfico)*")

        # Capa PyDeck con nodos destacados estilo semáforo físico
        layer = pdk.Layer(
            'ScatterplotLayer',
            df_nodos,
            get_position='[lon, lat]',
            get_color='color',
            get_radius='radio',
            pickable=True,
            auto_highlight=True,
            stroked=True,
            get_line_color=[255, 255, 255, 255],
            get_line_width=30,
        )

        view_state = pdk.ViewState(
            latitude=4.6350,
            longitude=-74.0650,
            zoom=11.2,
            pitch=40,
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>{interseccion}</b><br/>"
                        "<b>Corredor:</b> {corredor}<br/>"
                        "----------------------------------<br/>"
                        "🚗 <b>Carros:</b> {carros} un.<br/>"
                        "🏍️ <b>Motos:</b> {motos} un.<br/>"
                        "🚌 <b>Buses SITP:</b> {buses} un.<br/>"
                        "----------------------------------<br/>"
                        "📊 <b>Estado Vía:</b> {estado_trafico}<br/>"
                        "⚙️ <b>Acción del Semáforo:</b> {accion_sistema}<br/>"
                        "⏱️ <b>Tiempo de Verde:</b> {tiempo_verde} segundos",
                "style": {
                    "backgroundColor": "#1E1E1E",
                    "color": "white",
                    "font-family": "sans-serif",
                    "padding": "12px",
                    "border-radius": "8px"
                }
            }
        )
        st.pydeck_chart(r)

    with col_panel:
        st.subheader("🔍 Inspector de Semáforos")
        
        # Selector desplegable para consultar un semáforo específico al instante
        nombres_nodos = df_nodos['interseccion'].tolist()
        nodo_seleccionado = st.selectbox("Selecciona un nodo semafórico:", nombres_nodos)
        
        # Filtramos la información del nodo elegido
        info_nodo = df_nodos[df_nodos['interseccion'] == nodo_seleccionado].iloc[0]
        
        st.markdown(f"""
        ### {info_nodo['interseccion']}
        * **Ubicación / Corredor:** {info_nodo['corredor']}
        * **Estado del Tráfico:** {info_nodo['estado_trafico']}
        
        ---
        **Conteo Vehicular Actual:**
        * 🚗 **Carros Particulares:** `{info_nodo['carros']}` unidades
        * 🏍️ **Motocicletas:** `{info_nodo['motos']}` unidades
        * 🚌 **Buses SITP:** `{info_nodo['buses']}` unidades
        
        ---
        **Respuesta del Sistema Inteligente:**
        * ⚙️ **Acción:** {info_nodo['accion_sistema']}
        * ⏱️ **Tiempo de Ciclo Verde Asignado:** **{info_nodo['tiempo_verde']} segundos**
        """)

# Ejecutamos el panel interactivo en tiempo real
mostrar_panel_en_vivo()

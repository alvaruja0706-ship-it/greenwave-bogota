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

# Estilos CSS y HTML personalizados para un diseño de nivel profesional
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #a0aec0;
        text-align: center;
        margin-bottom: 25px;
    }
    .card-container {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        border: 1px solid #4a4a6a;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        color: #ffffff;
    }
    .badge-critical {
        background-color: #ff3b30;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .badge-moderate {
        background-color: #ffcc00;
        color: #1a1a1a;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .badge-fluid {
        background-color: #34c759;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .metric-box {
        background: #161622;
        border-left: 5px solid #00d2ff;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título con HTML
st.markdown('<p class="main-title">🚦 GreenWave: Sistema Inteligente de Gestión de Tráfico</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plataforma adaptativa de control semafórico para optimizar el flujo de vehículos particulares, motocicletas y buses del SITP en Bogotá D.C.</p>', unsafe_allow_html=True)

# Fragmento en tiempo real (actualización cada 3 segundos)
@st.fragment(run_every=3)
def mostrar_panel_en_vivo():
    # Intersecciones críticas reales de Bogotá
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

    # Simulación estocástica coherente
    red_actualizada = []
    for nodo in INTERSECCIONES_BOGOTA:
        carros = random.randint(110, 310)
        motos = random.randint(80, 240)
        buses_sitp = random.randint(10, 38)
        
        carga_total = carros + (motos * 0.7) + (buses_sitp * 1.5)
        
        if carga_total > 320:
            estado_trafico = "Trancón Crítico (Saturado)"
            badge_html = '<span class="badge-critical">🔴 Saturado</span>'
            tiempo_verde = 65
            accion_sistema = "Ciclo Extendido (Prioridad de Evacuación)"
            color_nodo = [255, 59, 48, 240]
        elif carga_total > 210:
            estado_trafico = "Tráfico Moderado"
            badge_html = '<span class="badge-moderate">🟡 Moderado</span>'
            tiempo_verde = 45
            accion_sistema = "Ciclo Dinámico Ajustado"
            color_nodo = [255, 204, 0, 240]
        else:
            estado_trafico = "Flujo Fluido"
            badge_html = '<span class="badge-fluid">🟢 Fluido</span>'
            tiempo_verde = 30
            accion_sistema = "Ciclo Estándar Sincronizado"
            color_nodo = [52, 199, 89, 240]
            
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
            "badge_html": badge_html,
            "tiempo_verde": tiempo_verde,
            "accion_sistema": accion_sistema,
            "color": color_nodo
        })

    df_nodos = pd.DataFrame(red_actualizada)

    # --- MÉTRICAS SUPERIORES ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📍 Nodos Activos", value=len(df_nodos), delta="Bogotá D.C.")
    with col2:
        promedio_total = int((df_nodos['carros'] + df_nodos['motos'] + df_nodos['buses']).mean())
        st.metric(label="🚗 Parque Automotor", value=f"{promedio_total} un.", delta="Promedio por vía")
    with col3:
        nodos_criticos = len(df_nodos[df_nodos['tiempo_verde'] == 65])
        st.metric(label="🚨 Mitigando Trancón", value=f"{nodos_criticos} activos", delta="Prioridad alta")
    with col4:
        st.metric(label="⚡ Algoritmo Adaptativo", value="En Línea", delta="Tiempo Real (3s)")

    st.markdown("---")

    # --- MAPA Y PANEL LATERAL CON HTML ---
    col_mapa, col_panel = st.columns([1.6, 1])
    
    with col_mapa:
        st.subheader("🗺️ Mapa Geoespacial de la Red")
        st.markdown("<p style='color: #a0aec0; font-size: 0.9rem;'>Los puntos reflejan el estado del semáforo en tiempo real. Pasa el cursor o selecciona la intersección en el panel derecho.</p>", unsafe_allow_html=True)

        # Capa PyDeck con anillos brillantes
        layer = pdk.Layer(
            'ScatterplotLayer',
            df_nodos,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=320,
            pickable=True,
            auto_highlight=True,
            stroked=True,
            get_line_color=[255, 255, 255, 255],
            get_line_width=40,
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
                "text": "Intersección: {interseccion}\nCorredor: {corredor}\nCarros: {carros} | Motos: {motos} | Buses: {buses}\nEstado: {estado_trafico}\nVerde Asignado: {tiempo_verde}s"
            }
        )
        st.pydeck_chart(r)

    with col_panel:
        st.subheader("🔍 Inspector Detallado de Semáforo")
        
        nodos_lista = df_nodos['interseccion'].tolist()
        nodo_elegido = st.selectbox("Seleccione un semáforo de la red:", nodos_lista)
        
        datos_nodo = df_nodos[df_nodos['interseccion'] == nodo_elegido].iloc[0]
        
        # Tarjeta HTML personalizada súper limpia y profesional
        st.markdown(f"""
        <div class="card-container">
            <h3 style="margin-top: 0; color: #00d2ff; font-size: 1.25rem;">🚦 {datos_nodo['interseccion']}</h3>
            <p style="color: #cbd5e0; margin-bottom: 8px;"><b>Corredor Vial:</b> {datos_nodo['corredor']}</p>
            <div style="margin: 12px 0;"><b>Estado del Tráfico:</b> {datos_nodo['badge_html']}</div>
            
            <hr style="border-color: #4a4a6a; margin: 12px 0;">
            
            <p style="margin-bottom: 6px; font-weight: bold; color: #e2e8f0;">Conteo Vehicular en Tiempo Real:</p>
            <div class="metric-box">
                🚗 <b>Carros Particulares:</b> <code>{datos_nodo['carros']}</code> unidades<br>
                🏍️ <b>Motocicletas:</b> <code>{datos_nodo['motos']}</code> unidades<br>
                🚌 <b>Buses SITP:</b> <code>{datos_nodo['buses']}</code> unidades
            </div>
            
            <p style="margin-top: 12px; margin-bottom: 6px; font-weight: bold; color: #e2e8f0;">Respuesta del Sistema Inteligente:</p>
            <div style="background: #161622; padding: 10px; border-radius: 8px; border-left: 5px solid #ffcc00;">
                ⚙️ <b>Acción:</b> {datos_nodo['accion_sistema']}<br>
                ⏱️ <b>Tiempo de Verde:</b> <span style="color: #00d2ff; font-size: 1.1rem; font-weight: bold;">{datos_nodo['tiempo_verde']} segundos</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Ejecutamos la aplicación
mostrar_panel_en_vivo()

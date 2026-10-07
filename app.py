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

st.title("🚦 GreenWave: Sistema Inteligente de Gestión de Tráfico")
st.markdown("Plataforma adaptativa de control semafórico para optimizar el flujo vehicular (carros, motos y SITP) en Bogotá D.C.")

# Fragmento en tiempo real (actualización automática cada 3 segundos)
@st.fragment(run_every=3)
def mostrar_panel_en_vivo():
    # Red de intersecciones críticas en Bogotá
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

    # Simulación estocástica coherente en tiempo real
    red_actualizada = []
    for nodo in INTERSECCIONES_BOGOTA:
        carros = random.randint(110, 310)
        motos = random.randint(80, 240)
        buses_sitp = random.randint(10, 38)
        
        carga_total = carros + (motos * 0.7) + (buses_sitp * 1.5)
        
        if carga_total > 320:
            estado_trafico = "🔴 Saturado (Trancón Crítico)"
            tiempo_verde = 65
            accion_sistema = "Ciclo Extendido (Prioridad de Evacuación)"
            color_nodo = [255, 59, 48, 240]
        elif carga_total > 210:
            estado_trafico = "🟡 Moderado (Precaución)"
            tiempo_verde = 45
            accion_sistema = "Ciclo Dinámico Ajustado"
            color_nodo = [255, 204, 0, 240]
        else:
            estado_trafico = "🟢 Fluido (Óptimo)"
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
            "tiempo_verde": tiempo_verde,
            "accion_sistema": accion_sistema,
            "color": color_nodo
        })

    df_nodos = pd.DataFrame(red_actualizada)

    # --- MÉTRICAS SUPERIORES ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📍 Nodos Activos", value=len(df_nodos))
    with col2:
        promedio_total = int((df_nodos['carros'] + df_nodos['motos'] + df_nodos['buses']).mean())
        st.metric(label="🚗 Parque Automotor Prom.", value=f"{promedio_total} un.")
    with col3:
        nodos_criticos = len(df_nodos[df_nodos['tiempo_verde'] == 65])
        st.metric(label="🚨 Mitigando Trancón", value=f"{nodos_criticos} nodos")
    with col4:
        st.metric(label="⚡ Sistema Inteligente", value="En Línea")

    st.markdown("---")

    # --- MAPA Y PANEL LATERAL ---
    col_mapa, col_panel = st.columns([1.5, 1])
    
    with col_mapa:
        st.subheader("🗺️ Mapa de Semaforización en Vivo")
        st.caption("Los puntos muestran el estado actual de cada intersección en Bogotá.")

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
        st.subheader("🔍 Inspector de Intersecciones")
        
        nodos_lista = df_nodos['interseccion'].tolist()
        nodo_elegido = st.selectbox("Seleccione un semáforo:", nodos_lista)
        
        datos_nodo = df_nodos[df_nodos['interseccion'] == nodo_elegido].iloc[0]
        
        # Panel estructurado limpio y profesional con componentes nativos
        with st.container(border=True):
            st.markdown(f"### 🚦 {datos_nodo['interseccion']}")
            st.markdown(f"**Corredor:** {datos_nodo['corredor']}")
            st.markdown(f"**Estado:** {datos_nodo['estado_trafico']}")
            
            st.divider()
            
            st.markdown("**Conteo Vehicular en Tiempo Real:**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("🚗 Carros", f"{datos_nodo['carros']}")
            with col_b:
                st.metric("🏍️ Motos", f"{datos_nodo['motos']}")
            with col_c:
                st.metric("🚌 SITP", f"{datos_nodo['buses']}")
                
            st.divider()
            
            st.markdown("**Respuesta del Sistema Adaptativo:**")
            st.info(f"⚙️ **Acción:** {datos_nodo['accion_sistema']}\n\n⏱️ **Tiempo Verde Asignado:** **{datos_nodo['tiempo_verde']} segundos**")

# Ejecución principal
mostrar_panel_en_vivo()

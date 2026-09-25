import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página de la aplicación
st.set_page_config(page_title="Copiloto Financiero AI", page_icon="🧠", layout="wide")

st.title("🧠 Copiloto Financiero: Simulador de Apalancamiento")
st.markdown("### Transforma decisiones complejas en alertas visuales inmediatas.")
st.write("---")

# DISEÑO DE LA INTERFAZ: DOS COLUMNAS (CONTROLES A LA IZQUIERDA, RESULTADOS A LA DERECHA)
col_controles, col_resultados = st.columns(2)

with col_controles:
    st.header("📊 Datos de tu Empresa")
    ventas = st.number_input("Ventas Anuales Proyectadas ($ USD)", min_value=10000, value=200000, step=10000)
    costos_variables = st.number_input("Costos Variables ($ USD)", min_value=0, value=80000, step=5000)
    costos_fijos = st.number_input("Costos Fijos Operativos ($ USD)", min_value=0, value=40000, step=5000)
    
    st.header("💸 Simular Estrategia de Deuda")
    monto_deuda = st.slider("Monto del Nuevo Crédito ($ USD)", min_value=0, max_value=500000, value=100000, step=10000)
    tasa_interes = st.slider("Tasa de Interés Anual (%)", min_value=1.0, max_value=30.0, value=10.0, step=0.5)
    
    capital_propio = 200000  # Capital base de ejemplo aportado por accionistas

# MOTOR DE CÁLCULO FINANCIERO
utilidad_operativa = ventas - costos_variables - costos_fijos
intereses_anuales = monto_deuda * (tasa_interes / 100)
utilidad_antes_impuestos = utilidad_operativa - intereses_anuales

# Simulación de impuestos (30%)
impuestos = max(0.0, utilidad_antes_impuestos * 0.30)
utilidad_neta = utilidad_antes_impuestos - impuestos

# Ratios Clave
activos_totales = capital_propio + monto_deuda
roa = (utilidad_operativa / activos_totales) * 100 if activos_totales > 0 else 0.0
roe = (utilidad_neta / capital_propio) * 100 if capital_propio > 0 else 0.0
icr = (utilidad_operativa / intereses_anuales) if intereses_anuales > 0 else float('inf')

# DESPLIEGUE DE RESULTADOS Y ALERTAS VISUALES (COLUMNA DERECHA)
with col_resultados:
    st.header("🎯 Semáforo de Decisión Estratégica")
    
    # Alerta 1: Arbitraje de Capital (Apalancamiento Positivo vs Negativo)
    costo_deuda_pct = tasa_interes
    if monto_deuda > 0:
        if roa > costo_deuda_pct:
            st.success(f"🟢 **APALANCAMIENTO POSITIVO:** Tu rendimiento operativo ({roa:.2f}%) supera el costo del crédito ({costo_deuda_pct:.2f}%). ¡Esta deuda multiplicará tus ganancias!")
        else:
            st.error(f"🔴 **APALANCAMIENTO NEGATIVO:** Tu rendimiento ({roa:.2f}%) es menor al costo de la deuda ({costo_deuda_pct:.2f}%). Tomar este crédito destruirá tu patrimonio.")
    else:
        st.info("💡 Incrementa el slider del crédito para simular el impacto de la deuda.")

    # Alerta 2: Capacidad de Pago (Cobertura de Intereses)
    if monto_deuda > 0:
        if icr >= 3.0:
            st.success(f"🟢 **SALUD FINANCIERA:** Tu cobertura de intereses es de {icr:.2f}x. Tienes suficiente utilidad para pagar al banco cómodamente.")
        elif 1.5 <= icr < 3.0:
            st.warning(f"🟡 **ZONA DE ESTRÉS:** Cobertura de intereses en {icr:.2f}x. Estás en un nivel ajustado; variaciones en las ventas te pondrán en peligro.")
        else:
            st.error(f"🔴 **RIESGO DE QUIEBRA:** Cobertura crítica de {icr:.2f}x. Tus utilidades operativas apenas cubren (o no alcanzan a cubrir) los intereses.")

    # Tarjetas Métricas
    st.write("---")
    st.subheader("📈 Rendimiento del Accionista (ROE)")
    sin_deuda_roe = ((utilidad_operativa * 0.7) / capital_propio * 100)
    st.metric(label="Retorno sobre el Capital Propio simulado", value=f"{roe:.2f}%", 
              delta=f"{(roe - sin_deuda_roe):.2f}% vs Sin Deuda")

    # Gráfico de barras simple para contrastar la estructura de costos
    st.write("---")
    st.subheader("📊 Distribución del Flujo de Efectivo")
    datos_grafico = pd.DataFrame({
        "Concepto": ["Utilidad Neta", "Impuestos", "Intereses al Banco", "Costos Operativos"],
        "Monto ($)": [max(0.0, utilidad_neta), impuestos, intereses_anuales, (costos_variables + costos_fijos)]
    })
    st.bar_chart(data=datos_grafico, x="Concepto", y="Monto ($)")

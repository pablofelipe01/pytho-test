"""Examen-práctica autónomo de Python para alumnos."""
import streamlit as st

from components.code_editor import code_editor
from exercises import EXERCISES, NIVELES, por_id, por_nivel
from grader import grade


st.set_page_config(
    page_title="Práctica de Python",
    page_icon="🐍",
    layout="wide",
)


# ------------------------------------------------------------
# Estado de sesión
# ------------------------------------------------------------
if "resueltos" not in st.session_state:
    st.session_state.resueltos = set()  # ids de ejercicios resueltos
if "celebrados" not in st.session_state:
    st.session_state.celebrados = set()  # para que los globos solo salgan una vez
if "ejercicio_id" not in st.session_state:
    st.session_state.ejercicio_id = 1
if "editor_nonce" not in st.session_state:
    # Permite forzar el remontaje del editor (botón "Reiniciar")
    st.session_state.editor_nonce = {}


# ------------------------------------------------------------
# Banner superior
# ------------------------------------------------------------
st.markdown(
    "### 🐍 Práctica de Python — Modo libre, sin tiempo. "
    "Lo único bloqueado es **pegar código** en el editor."
)

resueltos_n = len(st.session_state.resueltos)
total_n = len(EXERCISES)
st.progress(resueltos_n / total_n, text=f"Has resuelto {resueltos_n}/{total_n} ejercicios")


with st.expander("ℹ️ Cómo funciona la app", expanded=False):
    st.markdown(
        """
- **Práctica libre**: no hay cronómetro, puedes intentar cada ejercicio las veces que quieras.
- **Pegar bloqueado**: el editor de código deshabilita pegar, arrastrar, Ctrl/Cmd+V y clic derecho.
  Sirve como fricción educativa; un usuario muy avanzado podría saltarlo desde la consola del navegador.
- **Calificación automática**: cada ejercicio se ejecuta contra varios casos de prueba.
  Verás cuáles pasaron y cuáles fallaron.
- **Sin guardado**: cuando termines, manda al profe un **pantallazo** de tus resultados.
- En la barra lateral aparece un ✅ junto a los ejercicios que ya resolviste durante la sesión.
        """
    )


# ------------------------------------------------------------
# Sidebar: navegación por niveles
# ------------------------------------------------------------
with st.sidebar:
    st.header("📚 Navegación")
    nivel_sel = st.radio(
        "Nivel",
        NIVELES,
        index=NIVELES.index(por_id(st.session_state.ejercicio_id)["nivel"]),
        key="nivel_radio",
    )

    ejs_nivel = por_nivel(nivel_sel)
    opciones = []
    for e in ejs_nivel:
        marca = "✅ " if e["id"] in st.session_state.resueltos else ""
        opciones.append((e["id"], f"{marca}{e['id']:>2}. {e['titulo']}"))

    ids = [eid for eid, _ in opciones]
    labels = [lbl for _, lbl in opciones]

    # Si el ejercicio actual no está en este nivel, ir al primero del nivel
    if st.session_state.ejercicio_id not in ids:
        st.session_state.ejercicio_id = ids[0]

    idx_actual = ids.index(st.session_state.ejercicio_id)
    elegido = st.radio(
        "Ejercicio",
        options=range(len(ids)),
        format_func=lambda i: labels[i],
        index=idx_actual,
        key=f"ej_radio_{nivel_sel}",
    )
    st.session_state.ejercicio_id = ids[elegido]

    st.divider()
    st.caption(
        f"Resueltos en este nivel: "
        f"{sum(1 for e in ejs_nivel if e['id'] in st.session_state.resueltos)}/{len(ejs_nivel)}"
    )


# ------------------------------------------------------------
# Zona principal: ejercicio actual
# ------------------------------------------------------------
ej = por_id(st.session_state.ejercicio_id)

st.markdown(f"## Ejercicio {ej['id']} — {ej['titulo']}")
st.caption(f"Nivel: **{ej['nivel']}**")

st.info(ej["enunciado"])

col_firma, col_ejemplo = st.columns([1, 1])
with col_firma:
    st.markdown("**Firma esperada:**")
    st.code(ej["firma"], language="python")
with col_ejemplo:
    st.markdown("**Ejemplo:**")
    st.code(ej["ejemplo"], language="python")

with st.expander("💡 Pistas (haz clic para ver)", expanded=False):
    for i, p in enumerate(ej["pistas"], 1):
        st.markdown(f"**Pista {i}.** {p}")

with st.expander("📋 Detalle del ejemplo", expanded=False):
    st.markdown(
        f"- **Modo de calificación:** `{ej['mode']}`\n"
        f"- **Número de tests ocultos:** {len(ej['tests'])}"
    )

st.markdown("### 📝 Tu código")

# Botón para reiniciar (cambia la key del editor → se remonta vacío)
col_a, col_b = st.columns([6, 1])
with col_b:
    if st.button("🔄 Reiniciar", key=f"reset_{ej['id']}"):
        st.session_state.editor_nonce[ej["id"]] = (
            st.session_state.editor_nonce.get(ej["id"], 0) + 1
        )
        st.rerun()

nonce = st.session_state.editor_nonce.get(ej["id"], 0)
editor_key = f"editor_{ej['id']}_{nonce}"

# Plantilla inicial: la firma esperada como punto de partida
plantilla = f"{ej['firma']}\n    # Escribe aquí tu solución\n    pass\n"

codigo = code_editor(
    key=editor_key,
    default=plantilla,
    height=320,
    placeholder=f"{ej['firma']}\n    ...",
)

# ------------------------------------------------------------
# Evaluación
# ------------------------------------------------------------
if codigo:
    with st.spinner("Ejecutando tus tests…"):
        resultados = grade(
            student_code=codigo,
            function_name=ej["function_name"],
            test_cases=ej["tests"],
            mode=ej["mode"],
            timeout=5,
        )

    # Si el grader devolvió un único error global (definición / timeout), mostrarlo
    if len(resultados) == 1 and len(ej["tests"]) > 1 and resultados[0].get("error") and not resultados[0]["pass"]:
        # Heurística: si el error menciona definir el código o timeout, es global
        err = resultados[0]["error"] or ""
        if "Error al definir" in err or "Tiempo agotado" in err or "Error de ejecución" in err:
            st.error(f"❌ {err}")
            st.stop()

    pasados = sum(1 for r in resultados if r["pass"])
    total = len(resultados)

    # Cabecera de resumen
    if pasados == total:
        st.success(f"✅ ¡Ejercicio resuelto! Pasaste los {pasados}/{total} tests.")
        if ej["id"] not in st.session_state.celebrados:
            st.balloons()
            st.session_state.celebrados.add(ej["id"])
        st.session_state.resueltos.add(ej["id"])
    elif pasados == 0:
        st.error(f"❌ Pasaste 0/{total} tests. Revisa la tabla y vuelve a intentarlo.")
    else:
        st.warning(f"⚠️ Pasaste {pasados}/{total} tests. Casi, sigue iterando.")

    # Tabla detallada
    filas = []
    for i, r in enumerate(resultados, 1):
        filas.append({
            "#": i,
            "Resultado": "✅" if r["pass"] else "❌",
            "Tu salida": r.get("got", "") or "—",
            "Esperado": r.get("expected", "") or "—",
            "Error": r.get("error") or "",
        })
    st.markdown("#### Detalle por test")
    st.dataframe(filas, use_container_width=True, hide_index=True)


# ------------------------------------------------------------
# Pie
# ------------------------------------------------------------
st.divider()
st.caption(
    "Cuando termines todos los ejercicios que puedas, toma una **captura de pantalla** "
    "de tu progreso (la barra superior) y envíasela al profe."
)

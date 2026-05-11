"""Modo Contrarreloj: 25 desafíos rápidos de Python con timer de 2 minutos.

Si el alumno no envía la respuesta correcta antes de los 2 minutos, la
pantalla "explota" (animación tipo cristal roto / temblor / flash rojo) y
el desafío cuenta como fallado.
"""
import subprocess
import sys
import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from components.code_editor import code_editor
from speed_challenges import SPEED_CHALLENGES, TIME_LIMIT_SECONDS


st.set_page_config(
    page_title="Contrarreloj — Python",
    page_icon="⚡",
    layout="wide",
)


# ------------------------------------------------------------
# Estado de sesión
# ------------------------------------------------------------
PLANTILLA = "# Escribe tu código aquí (usa print)\n"


def _init_state():
    defaults = {
        "sc_state": "idle",              # idle | playing | exploded | done
        "sc_idx": 0,                      # índice del desafío actual
        "sc_score": 0,
        "sc_start_ts": None,              # timestamp de inicio del desafío actual
        "sc_editor_nonce": 0,             # para reiniciar el editor entre desafíos
        "sc_results": [],                 # historial: [{id, passed, reason}]
        "sc_last_feedback": None,         # último intento fallido (para mostrar)
        "sc_last_submitted_code": PLANTILLA,  # último código evaluado (para detectar nuevos envíos)
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def _start_game():
    st.session_state.sc_state = "playing"
    st.session_state.sc_idx = 0
    st.session_state.sc_score = 0
    st.session_state.sc_start_ts = time.time()
    st.session_state.sc_editor_nonce += 1
    st.session_state.sc_results = []
    st.session_state.sc_last_feedback = None
    st.session_state.sc_last_submitted_code = PLANTILLA


def _next_challenge(passed: bool, reason: str = ""):
    """Avanza al siguiente desafío (o termina si era el último)."""
    ch = SPEED_CHALLENGES[st.session_state.sc_idx]
    st.session_state.sc_results.append({
        "id": ch["id"],
        "enunciado": ch["enunciado"].splitlines()[0][:80],
        "passed": passed,
        "reason": reason,
    })
    if passed:
        st.session_state.sc_score += 1

    st.session_state.sc_idx += 1
    st.session_state.sc_last_feedback = None
    st.session_state.sc_editor_nonce += 1
    st.session_state.sc_last_submitted_code = PLANTILLA

    if st.session_state.sc_idx >= len(SPEED_CHALLENGES):
        st.session_state.sc_state = "done"
        st.session_state.sc_start_ts = None
    else:
        st.session_state.sc_state = "playing"
        st.session_state.sc_start_ts = time.time()


def _run_code(code: str, timeout: int = 4):
    """Ejecuta el código en un subprocess y devuelve (stdout, error)."""
    if not code or not code.strip():
        return "", "Editor vacío. Escribe algo de código."
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "", f"Tiempo agotado ({timeout}s). ¿Bucle infinito?"
    except Exception as e:  # noqa: BLE001
        return "", f"{type(e).__name__}: {e}"

    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        # Cortamos para que la UI no se llene
        return "", err.splitlines()[-1][:300] if err else "Error desconocido"
    return proc.stdout, None


def _check_answer(code: str, expected: str):
    """Comprueba si la salida del código coincide con la esperada."""
    stdout, err = _run_code(code)
    if err:
        return False, f"Error: {err}", stdout
    got = (stdout or "").strip()
    exp = expected.strip()
    if got == exp:
        return True, "¡Correcto!", got
    return False, f"Salida obtenida: {got!r} — Se esperaba: {exp!r}", got


# ------------------------------------------------------------
# Estilos globales (CSS) — usados por las pantallas
# ------------------------------------------------------------
COMMON_CSS = """
<style>
@keyframes pulse-time {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
.sc-timer {
    font-family: 'Courier New', monospace;
    font-size: 4.5rem;
    font-weight: 900;
    text-align: center;
    letter-spacing: 0.1em;
    padding: 0.6rem 0;
    border-radius: 14px;
    margin-bottom: 0.5rem;
}
.sc-timer.green  { color: #0a7d2c; background: #e8f8ee; }
.sc-timer.orange { color: #b35900; background: #fff1e0; }
.sc-timer.red    {
    color: #ffffff; background: #c30000;
    animation: pulse-time 0.6s ease-in-out infinite;
}
.sc-pill {
    display: inline-block; padding: 0.2rem 0.7rem;
    background: #eee; border-radius: 999px; font-weight: 600;
    margin-right: 0.4rem; font-size: 0.95rem;
}
</style>
"""

EXPLOSION_HTML = """
<style>
@keyframes shake {
    0%, 100% { transform: translate(0, 0) rotate(0); }
    10%      { transform: translate(-8px, -10px) rotate(-2deg); }
    20%      { transform: translate(10px, 8px) rotate(2deg); }
    30%      { transform: translate(-12px, 6px) rotate(-3deg); }
    40%      { transform: translate(12px, -8px) rotate(3deg); }
    50%      { transform: translate(-10px, 12px) rotate(-2deg); }
    60%      { transform: translate(10px, -12px) rotate(2deg); }
    70%      { transform: translate(-6px, 8px) rotate(-1deg); }
    80%      { transform: translate(6px, -6px) rotate(1deg); }
    90%      { transform: translate(-4px, 4px) rotate(0); }
}
@keyframes flash-bg {
    0%, 100% { background: #ffe1e1; }
    50%      { background: #ff2a2a; }
}
@keyframes zoom-boom {
    0%   { transform: scale(0.3) rotate(-15deg); opacity: 0; }
    40%  { transform: scale(1.3) rotate(5deg);   opacity: 1; }
    70%  { transform: scale(0.95) rotate(-2deg); }
    100% { transform: scale(1.05) rotate(0);     opacity: 1; }
}
.sc-explosion {
    position: relative;
    border-radius: 16px;
    padding: 2.4rem 1.2rem;
    text-align: center;
    overflow: hidden;
    animation: shake 0.45s ease-in-out 4, flash-bg 0.4s ease-in-out 6;
    background: #ffe1e1;
    border: 6px dashed #c30000;
    box-shadow: 0 0 60px rgba(195, 0, 0, 0.6) inset;
}
.sc-explosion .boom {
    font-size: 5.5rem;
    font-weight: 900;
    color: #b00000;
    text-shadow: 0 0 18px #ffe600, 0 0 8px #ff8800;
    animation: zoom-boom 0.7s ease-out;
    margin: 0;
}
.sc-explosion .subtitle {
    font-size: 1.6rem;
    font-weight: 700;
    color: #5a0000;
    margin: 0.4rem 0 0.2rem;
}
.sc-explosion .cracks {
    position: absolute; inset: 0; pointer-events: none;
    background:
      linear-gradient(120deg, transparent 48%, #5a0000 49%, transparent 50%) 0 0/55% 55% no-repeat,
      linear-gradient(60deg,  transparent 48%, #5a0000 49%, transparent 50%) 100% 0/55% 55% no-repeat,
      linear-gradient(20deg,  transparent 48%, #5a0000 49%, transparent 50%) 30% 100%/45% 55% no-repeat,
      linear-gradient(160deg, transparent 48%, #5a0000 49%, transparent 50%) 80% 80%/45% 45% no-repeat;
    opacity: 0.45;
}
</style>

<div class="sc-explosion">
  <div class="cracks"></div>
  <p class="boom">💥 BOOM 💥</p>
  <p class="subtitle">¡La pantalla ha EXPLOTADO!</p>
  <p style="font-size: 1.2rem; color:#5a0000; margin:0;">
    Se te acabaron los 2 minutos. Este desafío cuenta como fallado.
  </p>
</div>
"""


# ============================================================
# PANTALLAS
# ============================================================
st.markdown(COMMON_CSS, unsafe_allow_html=True)

state = st.session_state.sc_state


# ------------------------------------------------------------
# Pantalla 1: idle (inicio)
# ------------------------------------------------------------
if state == "idle":
    st.markdown("# ⚡ Contrarreloj — Python")
    st.markdown(
        "### 25 desafíos · 2 minutos cada uno · una sola oportunidad por bloque"
    )
    st.warning(
        "🔥 **Reglas**\n\n"
        "- Tienes **2 minutos** para resolver cada desafío.\n"
        "- Escribe código Python que **imprima** (con `print`) lo que se pide.\n"
        "- Si la salida coincide con lo esperado, ganas 1 punto y pasas al siguiente.\n"
        "- Puedes intentarlo varias veces dentro de los 2 minutos.\n"
        "- Si se acaba el tiempo... **💥 la pantalla EXPLOTA 💥** y el desafío se pierde.\n"
        "- Puedes saltar un desafío si te trabas (cuenta como fallo).\n"
    )
    st.info(
        "💡 **Ejemplo:** si te piden imprimir `15`, puedes escribir `print(7 + 8)` o `print(15)`. "
        "Si es una pregunta tipo test con opciones a/b/c, imprime la letra correcta: `print(\"b\")`."
    )

    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_b:
        if st.button("🚀 EMPEZAR", use_container_width=True, type="primary"):
            _start_game()
            st.rerun()


# ------------------------------------------------------------
# Pantalla 2: playing (en curso)
# ------------------------------------------------------------
elif state == "playing":
    # Auto-refresh cada segundo para que el timer baje en pantalla
    st_autorefresh(interval=1000, key=f"sc_tick_{st.session_state.sc_idx}")

    start_ts = st.session_state.sc_start_ts or time.time()
    elapsed = time.time() - start_ts
    remaining = max(0.0, TIME_LIMIT_SECONDS - elapsed)

    # ¿Se acabó el tiempo? → cambiar a estado explotado
    if remaining <= 0:
        st.session_state.sc_state = "exploded"
        st.rerun()

    ch = SPEED_CHALLENGES[st.session_state.sc_idx]

    # --- Cabecera: timer + progreso ---
    mm = int(remaining // 60)
    ss = int(remaining % 60)
    if remaining < 20:
        color = "red"
    elif remaining < 60:
        color = "orange"
    else:
        color = "green"

    st.markdown(
        f'<div class="sc-timer {color}">⏱️ {mm:02d}:{ss:02d}</div>',
        unsafe_allow_html=True,
    )
    st.progress(
        remaining / TIME_LIMIT_SECONDS,
        text=(
            f"Desafío {st.session_state.sc_idx + 1}/{len(SPEED_CHALLENGES)} · "
            f"Puntos: {st.session_state.sc_score} · "
            f"Quedan {int(remaining)} s"
        ),
    )

    # --- Enunciado ---
    st.markdown(f"### 🎯 Desafío {ch['id']}")
    st.info(ch["enunciado"])

    # --- Editor (pulsa "▶ Ejecutar y calificar" dentro del editor para enviar) ---
    codigo = code_editor(
        key=f"sc_editor_{ch['id']}_{st.session_state.sc_editor_nonce}",
        default=PLANTILLA,
        height=200,
        placeholder="print(...)",
    )

    # --- Botones auxiliares (saltar / pista) ---
    col1, col2 = st.columns([1, 1])
    with col1:
        saltar = st.button("⏭️ Saltar este desafío", use_container_width=True)
    with col2:
        with st.popover("💡 Ver pista", use_container_width=True):
            st.code(ch["pista"], language="python")

    if saltar:
        _next_challenge(False, "Saltado")
        st.rerun()

    # --- Detectar nuevo envío del editor ---
    # El editor solo manda valor cuando el alumno toca su botón interno
    # "▶ Ejecutar y calificar". Para distinguirlo del auto-refresh comparamos
    # contra el último código evaluado.
    is_new_submission = (
        codigo is not None
        and codigo != st.session_state.sc_last_submitted_code
    )

    if is_new_submission:
        st.session_state.sc_last_submitted_code = codigo
        # Re-comprobamos el tiempo justo antes de aceptar
        if time.time() - start_ts > TIME_LIMIT_SECONDS:
            st.session_state.sc_state = "exploded"
            st.rerun()
        passed, msg, _got = _check_answer(codigo, ch["expected"])
        if passed:
            st.success(f"✅ {msg} +1 punto")
            _next_challenge(True, "Correcto")
            time.sleep(0.6)
            st.rerun()
        else:
            st.session_state.sc_last_feedback = msg
            st.error(f"❌ {msg}")
    elif st.session_state.sc_last_feedback:
        # Mantener el feedback del último intento entre ticks del auto-refresh
        st.warning(f"Último intento: {st.session_state.sc_last_feedback}")


# ------------------------------------------------------------
# Pantalla 3: exploded (se acabó el tiempo)
# ------------------------------------------------------------
elif state == "exploded":
    st.markdown(EXPLOSION_HTML, unsafe_allow_html=True)

    ch = SPEED_CHALLENGES[st.session_state.sc_idx]
    st.markdown("---")
    st.markdown(f"#### Desafío {ch['id']}")
    st.info(ch["enunciado"])
    st.markdown("**Solución de ejemplo:**")
    st.code(ch["pista"], language="python")

    is_last = st.session_state.sc_idx + 1 >= len(SPEED_CHALLENGES)
    label = "Ver resumen final" if is_last else "Siguiente desafío →"
    if st.button(label, type="primary"):
        _next_challenge(False, "Tiempo agotado 💥")
        st.rerun()


# ------------------------------------------------------------
# Pantalla 4: done (resumen final)
# ------------------------------------------------------------
elif state == "done":
    score = st.session_state.sc_score
    total = len(SPEED_CHALLENGES)
    pct = score / total

    st.markdown("# 🏁 ¡Fin del contrarreloj!")
    if pct >= 0.9:
        st.success(f"🏆 ¡Increíble! Puntuación: **{score}/{total}** ({pct:.0%})")
        st.balloons()
    elif pct >= 0.6:
        st.success(f"🥈 Buen trabajo. Puntuación: **{score}/{total}** ({pct:.0%})")
    elif pct >= 0.3:
        st.warning(f"📚 A seguir practicando. Puntuación: **{score}/{total}** ({pct:.0%})")
    else:
        st.error(f"💥 Esta ronda fue dura. Puntuación: **{score}/{total}** ({pct:.0%})")

    st.markdown("### 📋 Detalle por desafío")
    filas = []
    for i, r in enumerate(st.session_state.sc_results, 1):
        filas.append({
            "#": i,
            "ID": r["id"],
            "Resultado": "✅" if r["passed"] else "❌",
            "Motivo": r["reason"],
            "Enunciado": r["enunciado"],
        })
    st.dataframe(filas, use_container_width=True, hide_index=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("🔁 Volver a jugar", use_container_width=True, type="primary"):
            _start_game()
            st.rerun()
    with col_b:
        if st.button("🏠 Pantalla inicial", use_container_width=True):
            st.session_state.sc_state = "idle"
            st.rerun()

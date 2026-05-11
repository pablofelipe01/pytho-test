"""Modo Contrarreloj: 25 desafíos rápidos de Python con timer de 2 minutos.

Cronómetro en JavaScript puro (no hay autorefresh del servidor).
Evaluación in-process con exec() + redirect_stdout (rápida y sin
depender de subprocess).

- CORRECTO → animación verde + +1 punto + avanza al siguiente desafío.
- INCORRECTO → mini-explosión (shake + flash rojo) + sigue intentando.
- TIEMPO AGOTADO (>120s) → pantalla de explosión grande + se cuenta como fallo.
"""
import contextlib
import io
import time

import streamlit as st
import streamlit.components.v1 as components

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
        "sc_state": "idle",                   # idle | playing | exploded | done
        "sc_idx": 0,
        "sc_score": 0,
        "sc_start_ts": None,
        "sc_editor_nonce": 0,
        "sc_results": [],
        "sc_last_feedback": None,             # str | None (mensaje de error a mostrar)
        "sc_last_submitted_code": PLANTILLA,
        "sc_just_passed": False,              # flag para animación de éxito
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
    st.session_state.sc_just_passed = False


def _next_challenge(passed: bool, reason: str = ""):
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
    st.session_state.sc_just_passed = passed

    if st.session_state.sc_idx >= len(SPEED_CHALLENGES):
        st.session_state.sc_state = "done"
        st.session_state.sc_start_ts = None
    else:
        st.session_state.sc_state = "playing"
        st.session_state.sc_start_ts = time.time()


def _run_code(code: str):
    """Ejecuta el código in-process y captura stdout.

    No usa subprocess; más rápido y compatible con cualquier deploy.
    Riesgo aceptable para ejercicios pequeños — los alumnos solo escriben
    código simple tipo print.
    """
    if not code or not code.strip():
        return "", "Editor vacío. Escribe algo de código."

    buf = io.StringIO()
    try:
        compiled = compile(code, "<student>", "exec")
        with contextlib.redirect_stdout(buf):
            exec(compiled, {"__name__": "__main__"})
    except SyntaxError as e:
        return "", f"SyntaxError línea {e.lineno}: {e.msg}"
    except Exception as e:  # noqa: BLE001
        return "", f"{type(e).__name__}: {e}"

    return buf.getvalue(), None


def _check_answer(code: str, expected: str):
    stdout, err = _run_code(code)
    if err:
        return False, err, stdout or ""
    got = (stdout or "").strip()
    exp = expected.strip()
    if got == exp:
        return True, "¡Correcto!", got
    if not got:
        return False, f"No imprimiste nada. Esperado: {exp!r}", got
    return False, f"Tu salida: {got!r} — Esperado: {exp!r}", got


# ------------------------------------------------------------
# Componentes visuales
# ------------------------------------------------------------
def _render_js_timer(remaining_seconds: float):
    """Cuenta atrás 100% JavaScript, sin refrescos del servidor."""
    ms = max(0, int(remaining_seconds * 1000))
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
  html,body{{margin:0;padding:0;background:transparent;
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}}
  .sc-timer{{font-family:'Courier New',monospace;font-size:4.5rem;font-weight:900;
            text-align:center;letter-spacing:.1em;padding:.6rem 0;border-radius:14px;
            margin:0 8px;transition:background .3s,color .3s;}}
  .sc-timer.green {{color:#0a7d2c;background:#e8f8ee;}}
  .sc-timer.orange{{color:#b35900;background:#fff1e0;}}
  .sc-timer.red   {{color:#fff;background:#c30000;animation:pulse .6s infinite;}}
  .sc-timer.boom  {{color:#fff;background:#5a0000;animation:shake .35s infinite;}}
  @keyframes pulse{{0%,100%{{transform:scale(1);}}50%{{transform:scale(1.05);}}}}
  @keyframes shake{{0%,100%{{transform:translate(0,0);}}25%{{transform:translate(-8px,-3px);}}
                    50%{{transform:translate(8px,3px);}}75%{{transform:translate(-3px,7px);}}}}
</style></head><body>
<div id="t" class="sc-timer green">⏱️ 02:00</div>
<script>
  const REMAIN={ms}; const EXPIRES=Date.now()+REMAIN;
  const el=document.getElementById('t');
  function tick(){{
    const ms=Math.max(0,EXPIRES-Date.now());
    const sec=Math.ceil(ms/1000);
    const mm=Math.floor(sec/60), ss=sec%60;
    let cls='green';
    if(ms<=0) cls='boom';
    else if(sec<=20) cls='red';
    else if(sec<=60) cls='orange';
    el.className='sc-timer '+cls;
    el.textContent=ms<=0?'💥 ¡TIEMPO! 💥'
      :'⏱️ '+String(mm).padStart(2,'0')+':'+String(ss).padStart(2,'0');
    if(ms>0) requestAnimationFrame(tick);
  }}
  tick();
</script></body></html>"""
    components.html(html, height=130)


WRONG_FLASH_CSS = """
<style>
@keyframes sc-shake-h {
  0%,100% { transform: translateX(0); }
  10%,50%,90% { transform: translateX(-12px); }
  30%,70% { transform: translateX(12px); }
}
@keyframes sc-flash-red {
  0%   { background:#ff5252; box-shadow:0 0 60px rgba(255,0,0,.6) inset; }
  100% { background:#ffe1e1; box-shadow:0 0 0 rgba(255,0,0,0)   inset; }
}
.sc-wrong {
  border-radius: 14px;
  padding: 1rem 1.4rem;
  background: #ffe1e1;
  border: 4px dashed #c30000;
  margin-bottom: 0.6rem;
  animation: sc-shake-h 0.55s ease-in-out 2, sc-flash-red 0.9s ease-out;
}
.sc-wrong h2 {
  margin: 0 0 0.3rem; color: #c30000; font-size: 1.8rem; font-weight: 900;
}
.sc-wrong p { margin: 0; color: #5a0000; font-family: 'Courier New', monospace; }
.sc-wrong .retry { color:#5a0000; margin-top:.3rem; font-style:italic; font-family:inherit; }
</style>
"""

CORRECT_FLASH_CSS = """
<style>
@keyframes sc-pop {
  0%   { transform: scale(0.5) rotate(-8deg); opacity: 0; }
  60%  { transform: scale(1.15) rotate(3deg); opacity: 1; }
  100% { transform: scale(1) rotate(0); }
}
.sc-correct {
  border-radius: 14px;
  padding: 1rem 1.4rem;
  background: #e8f8ee;
  border: 4px solid #0a7d2c;
  margin-bottom: 0.6rem;
  text-align: center;
  animation: sc-pop 0.5s ease-out;
}
.sc-correct h2 {
  margin: 0; color: #0a7d2c; font-size: 2rem; font-weight: 900;
}
</style>
"""

EXPLOSION_HTML = """
<style>
@keyframes shake {
    0%,100% { transform: translate(0,0) rotate(0); }
    10% { transform: translate(-8px,-10px) rotate(-2deg); }
    20% { transform: translate(10px,8px) rotate(2deg); }
    30% { transform: translate(-12px,6px) rotate(-3deg); }
    40% { transform: translate(12px,-8px) rotate(3deg); }
    50% { transform: translate(-10px,12px) rotate(-2deg); }
    60% { transform: translate(10px,-12px) rotate(2deg); }
    70% { transform: translate(-6px,8px) rotate(-1deg); }
    80% { transform: translate(6px,-6px) rotate(1deg); }
    90% { transform: translate(-4px,4px) rotate(0); }
}
@keyframes flash-bg { 0%,100% { background:#ffe1e1; } 50% { background:#ff2a2a; } }
@keyframes zoom-boom {
    0%   { transform: scale(0.3) rotate(-15deg); opacity:0; }
    40%  { transform: scale(1.3) rotate(5deg);   opacity:1; }
    100% { transform: scale(1.05) rotate(0);     opacity:1; }
}
.sc-explosion {
    position:relative; border-radius:16px; padding:2.4rem 1.2rem; text-align:center;
    overflow:hidden;
    animation: shake .45s ease-in-out 4, flash-bg .4s ease-in-out 6;
    background:#ffe1e1; border:6px dashed #c30000;
    box-shadow: 0 0 60px rgba(195,0,0,.6) inset;
}
.sc-explosion .boom {
    font-size:5.5rem; font-weight:900; color:#b00000;
    text-shadow: 0 0 18px #ffe600, 0 0 8px #ff8800;
    animation: zoom-boom .7s ease-out; margin:0;
}
.sc-explosion .subtitle { font-size:1.6rem; font-weight:700; color:#5a0000; margin:.4rem 0 .2rem; }
</style>
<div class="sc-explosion">
  <p class="boom">💥 BOOM 💥</p>
  <p class="subtitle">¡La pantalla ha EXPLOTADO!</p>
  <p style="font-size:1.2rem;color:#5a0000;margin:0;">
    Se te acabaron los 2 minutos. Este desafío cuenta como fallado.
  </p>
</div>
"""


# ============================================================
# PANTALLAS
# ============================================================
state = st.session_state.sc_state


# ---------- Pantalla 1: idle ----------
if state == "idle":
    st.markdown("# ⚡ Contrarreloj — Python")
    st.markdown("### 25 desafíos · 2 minutos cada uno")
    st.warning(
        "🔥 **Reglas**\n\n"
        "- Tienes **2 minutos** para resolver cada desafío.\n"
        "- Escribe código Python que **imprima** (con `print`) lo que se pide.\n"
        "- Pulsa **▶ Ejecutar y calificar** (botón rojo del editor) para enviar.\n"
        "- ✅ Si aciertas → +1 punto y avanza automáticamente.\n"
        "- 💥 Si fallas → mini-explosión y puedes volver a intentarlo (dentro del tiempo).\n"
        "- ⏱️ Si se acaba el tiempo → la pantalla EXPLOTA y el desafío se pierde."
    )
    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        if st.button("🚀 EMPEZAR", use_container_width=True, type="primary"):
            _start_game()
            st.rerun()


# ---------- Pantalla 2: playing ----------
elif state == "playing":
    ch = SPEED_CHALLENGES[st.session_state.sc_idx]
    start_ts = st.session_state.sc_start_ts or time.time()
    elapsed = time.time() - start_ts
    remaining = max(0.0, TIME_LIMIT_SECONDS - elapsed)

    # === 1) BANDA DE FEEDBACK ARRIBA (siempre visible) ===
    feedback_slot = st.empty()
    if st.session_state.sc_just_passed:
        # Acabamos de avanzar: mostrar celebración del desafío anterior
        with feedback_slot.container():
            st.markdown(
                CORRECT_FLASH_CSS
                + '<div class="sc-correct"><h2>🎉 ¡CORRECTO! +1 punto. Siguiente desafío…</h2></div>',
                unsafe_allow_html=True,
            )
        st.session_state.sc_just_passed = False  # one-shot
    elif st.session_state.sc_last_feedback:
        with feedback_slot.container():
            st.markdown(
                WRONG_FLASH_CSS
                + f'<div class="sc-wrong"><h2>💥 ¡INCORRECTO!</h2>'
                + f'<p>{st.session_state.sc_last_feedback}</p>'
                + f'<p class="retry">↻ Edita tu código y vuelve a pulsar el botón rojo.</p></div>',
                unsafe_allow_html=True,
            )

    # === 2) TIMER ===
    _render_js_timer(remaining)

    st.progress(
        remaining / TIME_LIMIT_SECONDS,
        text=(
            f"Desafío {st.session_state.sc_idx + 1}/{len(SPEED_CHALLENGES)} · "
            f"Puntos: {st.session_state.sc_score}"
        ),
    )

    # === 3) ENUNCIADO ===
    st.markdown(f"### 🎯 Desafío {ch['id']}")
    st.info(ch["enunciado"])

    # === 4) EDITOR ===
    codigo = code_editor(
        key=f"sc_editor_{ch['id']}_{st.session_state.sc_editor_nonce}",
        default=PLANTILLA,
        height=200,
        placeholder="print(...)",
    )

    # === 5) BOTONES AUXILIARES ===
    col1, col2 = st.columns([1, 1])
    with col1:
        saltar = st.button("⏭️ Saltar este desafío", use_container_width=True)
    with col2:
        with st.expander("💡 Ver pista", expanded=False):
            st.code(ch["pista"], language="python")

    if saltar:
        _next_challenge(False, "Saltado")
        st.rerun()

    # === 6) DETECTAR NUEVO ENVÍO ===
    is_new_submission = (
        codigo is not None
        and codigo != st.session_state.sc_last_submitted_code
    )

    if is_new_submission:
        st.session_state.sc_last_submitted_code = codigo

        if time.time() - start_ts > TIME_LIMIT_SECONDS:
            st.session_state.sc_state = "exploded"
            st.rerun()

        passed, msg, _got = _check_answer(codigo, ch["expected"])

        if passed:
            st.toast("🎉 ¡CORRECTO! +1 punto", icon="🎉")
            _next_challenge(True, "Correcto")
            st.rerun()
        else:
            st.session_state.sc_last_feedback = msg
            st.toast("💥 ¡Falló! Sigue intentando", icon="💥")
            st.rerun()


# ---------- Pantalla 3: exploded (tiempo agotado) ----------
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


# ---------- Pantalla 4: done ----------
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

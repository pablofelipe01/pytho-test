import os
import streamlit.components.v1 as components

_parent_dir = os.path.dirname(os.path.abspath(__file__))
_build_dir = os.path.join(_parent_dir, "frontend")
_component_func = components.declare_component("code_editor", path=_build_dir)


def code_editor(key=None, default="", height=320, placeholder="Escribe tu código aquí..."):
    """Editor de código que bloquea pegar/arrastrar/Ctrl+V."""
    return _component_func(
        key=key,
        default=default,
        height=height,
        placeholder=placeholder,
    )

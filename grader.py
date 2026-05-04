"""Motor de calificación: ejecuta código del alumno en un subprocess aislado."""
import subprocess
import sys
import json
import textwrap


def grade(student_code: str, function_name, test_cases: list, mode: str = "function", timeout: int = 5):
    """
    Ejecuta el código del alumno contra una lista de casos de prueba.

    Parámetros:
        student_code: el código tal cual lo escribió el alumno.
        function_name: nombre de la función/clase a probar (puede ser None si mode='custom').
        test_cases: lista de dicts. Cada uno con:
            - "args": lista de argumentos posicionales (modo 'function')
            - "kwargs": opcional, dict de kwargs
            - "expected": valor esperado
            - "custom": expresión Python a evaluar (modo 'custom')
        mode: "function" (llamar function_name(*args)) o "custom" (eval de test["custom"]).
        timeout: segundos antes de matar el proceso.

    Devuelve:
        Lista de dicts: {"pass": bool, "got": str, "expected": str, "error": str|None}.
    """
    # Empaquetamos los datos como un único JSON y dejamos que el subprocess
    # lo decodifique en tiempo de ejecución. Así evitamos el problema de que
    # `true`/`false`/`null` (literales JSON) no son sintaxis Python válida.
    payload = json.dumps({
        "student_code": student_code,
        "tests": test_cases,
        "fn_name": function_name,
        "mode": mode,
    })

    wrapper = textwrap.dedent(f"""
        import json, sys, traceback

        _PAYLOAD = {json.dumps(payload)}
        _data = json.loads(_PAYLOAD)
        STUDENT_CODE = _data["student_code"]
        TESTS = _data["tests"]
        FN_NAME = _data["fn_name"]
        MODE = _data["mode"]

        results = []
        ns = {{}}
        try:
            exec(STUDENT_CODE, ns)
        except Exception as e:
            results.append({{
                "pass": False,
                "got": "",
                "expected": "",
                "error": f"Error al definir el código: {{type(e).__name__}}: {{e}}"
            }})
            print(json.dumps(results))
            sys.exit(0)

        for t in TESTS:
            try:
                if MODE == "custom":
                    result = eval(t["custom"], ns)
                    expected = t["expected"]
                    ok = result == expected
                    results.append({{
                        "pass": bool(ok),
                        "got": repr(result),
                        "expected": repr(expected),
                        "error": None,
                    }})
                else:
                    if FN_NAME not in ns:
                        results.append({{
                            "pass": False,
                            "got": "",
                            "expected": repr(t["expected"]),
                            "error": f"No se encontró la función '{{FN_NAME}}'",
                        }})
                        continue
                    fn = ns[FN_NAME]
                    args = t.get("args", [])
                    kwargs = t.get("kwargs", {{}})
                    result = fn(*args, **kwargs)
                    expected = t["expected"]
                    ok = result == expected
                    results.append({{
                        "pass": bool(ok),
                        "got": repr(result),
                        "expected": repr(expected),
                        "error": None,
                    }})
            except Exception as e:
                results.append({{
                    "pass": False,
                    "got": "",
                    "expected": repr(t.get("expected", "")),
                    "error": f"{{type(e).__name__}}: {{e}}",
                }})

        print(json.dumps(results))
    """)

    try:
        proc = subprocess.run(
            [sys.executable, "-c", wrapper],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return [{
            "pass": False,
            "got": "",
            "expected": "",
            "error": f"Tiempo agotado ({timeout}s). ¿Tienes un bucle infinito?",
        }]

    out = (proc.stdout or "").strip()
    if not out:
        return [{
            "pass": False,
            "got": "",
            "expected": "",
            "error": f"Error de ejecución:\n{proc.stderr.strip()[:500]}",
        }]
    try:
        return json.loads(out.splitlines()[-1])
    except Exception:
        return [{
            "pass": False,
            "got": "",
            "expected": "",
            "error": f"Salida inesperada:\n{out[:500]}",
        }]

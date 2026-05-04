# Práctica de Python — Streamlit

App de práctica autónoma de Python para alumnos. 30 ejercicios en 3 niveles
(básico, intermedio, intermedio-superior). Cada ejercicio se califica
ejecutando el código del alumno contra casos de prueba ocultos.

El editor de código integrado **bloquea pegar, arrastrar, Ctrl/Cmd+V,
Ctrl/Cmd+Shift+V y el menú contextual** para que el alumno tenga que
escribir el código a mano.

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

La app abrirá en `http://localhost:8501`.

## Despliegue en Streamlit Community Cloud

1. Sube este repositorio a GitHub (público o con la cuenta conectada).
2. Entra en https://share.streamlit.io y haz clic en **New app**.
3. Selecciona el repo, la rama (`main`) y el archivo `streamlit_app.py`.
4. Pulsa **Deploy**. Streamlit Cloud instalará `requirements.txt`
   automáticamente.
5. Comparte el link público con tus alumnos.

## Estructura del proyecto

```
python_practica/
├── streamlit_app.py             # entrypoint de la app
├── requirements.txt             # dependencias (solo streamlit)
├── README.md                    # este archivo
├── exercises.py                 # los 30 ejercicios
├── grader.py                    # ejecuta código en subprocess con timeout
└── components/
    └── code_editor/
        ├── __init__.py          # wrapper de declare_component
        └── frontend/
            └── index.html       # textarea con bloqueo de pegado
```

## Cómo lo usan los alumnos

1. Abren el link público.
2. Escogen nivel y ejercicio en la barra lateral.
3. Leen el enunciado, ven la firma esperada y, si quieren, las pistas.
4. Escriben su código en el editor (no pueden pegar).
5. Pulsan **▶ Ejecutar y calificar** y ven la tabla de tests.
6. Cuando terminan, mandan un pantallazo del progreso al profe.

## Notas

- No hay login ni persistencia de resultados. El progreso vive solo en la
  sesión del navegador del alumno.
- El bloqueo del pegado es de buena fe: un usuario muy avanzado podría
  saltarlo desde la consola del navegador. Sirve como fricción educativa.
- El motor de calificación lanza el código en un subprocess con timeout
  de 5 segundos para evitar bucles infinitos.

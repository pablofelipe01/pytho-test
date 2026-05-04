"""Definición de los 30 ejercicios del examen-práctica."""

EXERCISES = [
    # ============================================================
    # NIVEL BÁSICO (1-10)
    # ============================================================
    {
        "id": 1,
        "nivel": "Básico",
        "titulo": "Saludo personalizado",
        "enunciado": (
            "María acaba de abrir su cafetería y quiere que cada vez que entre un cliente, "
            "su pantalla muestre un saludo personalizado. Escribe una función que reciba "
            "el nombre del cliente y devuelva el texto `Hola, <nombre>!`."
        ),
        "pistas": [
            "Usa el operador `+` para concatenar strings, o un f-string como `f\"Hola, {nombre}!\"`."
        ],
        "ejemplo": 'saludar("Ana") → "Hola, Ana!"',
        "firma": "def saludar(nombre):",
        "function_name": "saludar",
        "mode": "function",
        "tests": [
            {"args": ["Ana"], "expected": "Hola, Ana!"},
            {"args": ["Luis"], "expected": "Hola, Luis!"},
            {"args": [""], "expected": "Hola, !"},
        ],
    },
    {
        "id": 2,
        "nivel": "Básico",
        "titulo": "Suma de dos números",
        "enunciado": (
            "Pedro tiene un puesto de frutas y necesita un programa que sume el precio "
            "de dos productos. Escribe una función que reciba dos números y devuelva su suma."
        ),
        "pistas": ["El operador para sumar es `+`."],
        "ejemplo": "sumar(2, 3) → 5",
        "firma": "def sumar(a, b):",
        "function_name": "sumar",
        "mode": "function",
        "tests": [
            {"args": [2, 3], "expected": 5},
            {"args": [-1, 1], "expected": 0},
            {"args": [100, 200], "expected": 300},
        ],
    },
    {
        "id": 3,
        "nivel": "Básico",
        "titulo": "Conversión de temperatura",
        "enunciado": (
            "Carmen viaja a Estados Unidos y todas las temperaturas están en Fahrenheit. "
            "Escribe una función que convierta grados Celsius a Fahrenheit. "
            "Fórmula: `F = C * 9/5 + 32`."
        ),
        "pistas": [
            "Recuerda el orden de operaciones: multiplicación antes que suma.",
            "En Python `9/5` da `1.8` (división normal), `9//5` daría `1` (división entera). Usa `/`.",
        ],
        "ejemplo": "celsius_a_fahrenheit(0) → 32.0",
        "firma": "def celsius_a_fahrenheit(c):",
        "function_name": "celsius_a_fahrenheit",
        "mode": "function",
        "tests": [
            {"args": [0], "expected": 32.0},
            {"args": [100], "expected": 212.0},
            {"args": [-40], "expected": -40.0},
        ],
    },
    {
        "id": 4,
        "nivel": "Básico",
        "titulo": "Par o impar",
        "enunciado": (
            "Juan está aprendiendo matemáticas y necesita un programa que le diga si "
            "un número es par. Escribe una función que devuelva `True` si el número es "
            "par y `False` si es impar."
        ),
        "pistas": ["El operador `%` da el resto de una división. Si `n % 2 == 0`, es par."],
        "ejemplo": "es_par(4) → True",
        "firma": "def es_par(n):",
        "function_name": "es_par",
        "mode": "function",
        "tests": [
            {"args": [4], "expected": True},
            {"args": [7], "expected": False},
            {"args": [0], "expected": True},
            {"args": [-3], "expected": False},
        ],
    },
    {
        "id": 5,
        "nivel": "Básico",
        "titulo": "El más caro",
        "enunciado": (
            "En una tienda, Sofía debe encontrar cuál de tres productos es el más caro. "
            "Escribe una función que reciba tres precios y devuelva el mayor."
        ),
        "pistas": ["Puedes usar `if` con varias comparaciones, o la función `max(a, b, c)`."],
        "ejemplo": "mayor(10, 25, 18) → 25",
        "firma": "def mayor(a, b, c):",
        "function_name": "mayor",
        "mode": "function",
        "tests": [
            {"args": [1, 2, 3], "expected": 3},
            {"args": [5, 2, 4], "expected": 5},
            {"args": [10, 10, 5], "expected": 10},
            {"args": [-1, -5, -2], "expected": -1},
        ],
    },
    {
        "id": 6,
        "nivel": "Básico",
        "titulo": "Tabla de multiplicar",
        "enunciado": (
            "Una maestra de primaria quiere imprimir la tabla de multiplicar de un número "
            "del 1 al 10. Escribe una función que reciba un número y devuelva una **lista** "
            "con los resultados de multiplicarlo por 1, 2, 3… hasta 10."
        ),
        "pistas": [
            "Usa un bucle `for i in range(1, 11):` y agrega `n*i` a una lista.",
            "Inicia con `resultado = []` y al final `return resultado`.",
        ],
        "ejemplo": "tabla(2) → [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]",
        "firma": "def tabla(n):",
        "function_name": "tabla",
        "mode": "function",
        "tests": [
            {"args": [2], "expected": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]},
            {"args": [5], "expected": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]},
            {"args": [1], "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        ],
    },
    {
        "id": 7,
        "nivel": "Básico",
        "titulo": "Calculadora de propinas",
        "enunciado": (
            "En el restaurante de Sofía, los clientes dejan una propina del 15% sobre el "
            "total de la cuenta. Escribe una función que reciba el total y devuelva la propina."
        ),
        "pistas": ["El 15% es 0.15 en decimal. Multiplica el total por 0.15."],
        "ejemplo": "propina(100) → 15.0",
        "firma": "def propina(total):",
        "function_name": "propina",
        "mode": "function",
        "tests": [
            {"args": [100], "expected": 15.0},
            {"args": [50], "expected": 7.5},
            {"args": [0], "expected": 0.0},
            {"args": [200], "expected": 30.0},
        ],
    },
    {
        "id": 8,
        "nivel": "Básico",
        "titulo": "¿Es vocal?",
        "enunciado": (
            "Un programa educativo para niños necesita saber si una letra es vocal. "
            "Escribe una función que reciba una sola letra y devuelva `True` si es vocal "
            "(a, e, i, o, u) sin importar si está en mayúscula o minúscula."
        ),
        "pistas": [
            "Convierte la letra a minúsculas con `.lower()`.",
            "Puedes usar `letra in \"aeiou\"` para verificar.",
        ],
        "ejemplo": 'es_vocal("A") → True',
        "firma": "def es_vocal(letra):",
        "function_name": "es_vocal",
        "mode": "function",
        "tests": [
            {"args": ["a"], "expected": True},
            {"args": ["E"], "expected": True},
            {"args": ["b"], "expected": False},
            {"args": ["Z"], "expected": False},
            {"args": ["i"], "expected": True},
        ],
    },
    {
        "id": 9,
        "nivel": "Básico",
        "titulo": "Cuenta regresiva",
        "enunciado": (
            "Un cohete espacial necesita una cuenta regresiva. Escribe una función que "
            "reciba un número N y devuelva una lista con los números desde N hasta 0 "
            "(incluido el 0)."
        ),
        "pistas": [
            "Usa `range(n, -1, -1)` para ir de n a 0 hacia abajo.",
            "Convierte a lista con `list(...)`.",
        ],
        "ejemplo": "cuenta_regresiva(3) → [3, 2, 1, 0]",
        "firma": "def cuenta_regresiva(n):",
        "function_name": "cuenta_regresiva",
        "mode": "function",
        "tests": [
            {"args": [3], "expected": [3, 2, 1, 0]},
            {"args": [5], "expected": [5, 4, 3, 2, 1, 0]},
            {"args": [0], "expected": [0]},
        ],
    },
    {
        "id": 10,
        "nivel": "Básico",
        "titulo": "Promedio de notas",
        "enunciado": (
            "El profesor Ramírez quiere calcular el promedio de las tres notas de cada "
            "alumno. Escribe una función que reciba tres notas y devuelva su promedio."
        ),
        "pistas": ["Suma las tres notas y divide por 3."],
        "ejemplo": "promedio(10, 8, 9) → 9.0",
        "firma": "def promedio(n1, n2, n3):",
        "function_name": "promedio",
        "mode": "function",
        "tests": [
            {"args": [10, 10, 10], "expected": 10.0},
            {"args": [5, 7, 3], "expected": 5.0},
            {"args": [0, 0, 0], "expected": 0.0},
            {"args": [10, 8, 9], "expected": 9.0},
        ],
    },
    # ============================================================
    # NIVEL INTERMEDIO (11-20)
    # ============================================================
    {
        "id": 11,
        "nivel": "Intermedio",
        "titulo": "Factorial",
        "enunciado": (
            "Para una clase de matemáticas necesitamos calcular el factorial de un número. "
            "El factorial de N es 1 × 2 × 3 × … × N. El factorial de 0 es 1 por definición."
        ),
        "pistas": [
            "Usa un bucle `for i in range(1, n+1)` multiplicando un acumulador.",
            "Empieza con `resultado = 1`.",
        ],
        "ejemplo": "factorial(5) → 120",
        "firma": "def factorial(n):",
        "function_name": "factorial",
        "mode": "function",
        "tests": [
            {"args": [0], "expected": 1},
            {"args": [1], "expected": 1},
            {"args": [5], "expected": 120},
            {"args": [6], "expected": 720},
            {"args": [10], "expected": 3628800},
        ],
    },
    {
        "id": 12,
        "nivel": "Intermedio",
        "titulo": "Pares hasta N",
        "enunciado": (
            "Genera una lista con todos los números pares desde 0 hasta N "
            "(incluido si N es par)."
        ),
        "pistas": ["`range(0, n+1, 2)` te da exactamente los pares."],
        "ejemplo": "pares_hasta(10) → [0, 2, 4, 6, 8, 10]",
        "firma": "def pares_hasta(n):",
        "function_name": "pares_hasta",
        "mode": "function",
        "tests": [
            {"args": [10], "expected": [0, 2, 4, 6, 8, 10]},
            {"args": [5], "expected": [0, 2, 4]},
            {"args": [0], "expected": [0]},
            {"args": [1], "expected": [0]},
        ],
    },
    {
        "id": 13,
        "nivel": "Intermedio",
        "titulo": "Contar vocales",
        "enunciado": (
            "Cuenta cuántas vocales (a, e, i, o, u) tiene una palabra. "
            "No distingue entre mayúsculas y minúsculas."
        ),
        "pistas": [
            "Recorre cada letra con `for letra in palabra:`.",
            "Usa `.lower()` para normalizar.",
        ],
        "ejemplo": 'contar_vocales("Hola") → 2',
        "firma": "def contar_vocales(palabra):",
        "function_name": "contar_vocales",
        "mode": "function",
        "tests": [
            {"args": ["hola"], "expected": 2},
            {"args": ["Python"], "expected": 1},
            {"args": ["aeiou"], "expected": 5},
            {"args": ["BCD"], "expected": 0},
            {"args": [""], "expected": 0},
        ],
    },
    {
        "id": 14,
        "nivel": "Intermedio",
        "titulo": "Invertir cadena",
        "enunciado": "Escribe una función que invierta una cadena de texto.",
        "pistas": [
            "El truco más corto: `texto[::-1]`.",
            "También puedes recorrer la cadena al revés con un bucle.",
        ],
        "ejemplo": 'invertir("hola") → "aloh"',
        "firma": "def invertir(texto):",
        "function_name": "invertir",
        "mode": "function",
        "tests": [
            {"args": ["hola"], "expected": "aloh"},
            {"args": ["python"], "expected": "nohtyp"},
            {"args": [""], "expected": ""},
            {"args": ["a"], "expected": "a"},
        ],
    },
    {
        "id": 15,
        "nivel": "Intermedio",
        "titulo": "Máximo sin max()",
        "enunciado": (
            "Encuentra el máximo de una lista **sin usar la función `max()`**. "
            "Asume que la lista no está vacía."
        ),
        "pistas": [
            "Empieza asumiendo que el primer elemento es el mayor.",
            "Recorre el resto y actualiza si encuentras uno más grande.",
        ],
        "ejemplo": "maximo([3, 1, 7, 2]) → 7",
        "firma": "def maximo(lista):",
        "function_name": "maximo",
        "mode": "function",
        "tests": [
            {"args": [[1, 2, 3]], "expected": 3},
            {"args": [[10, 5, 7, 2]], "expected": 10},
            {"args": [[-5, -2, -10]], "expected": -2},
            {"args": [[42]], "expected": 42},
        ],
    },
    {
        "id": 16,
        "nivel": "Intermedio",
        "titulo": "Total del inventario",
        "enunciado": (
            "Una tienda tiene su inventario en un diccionario `{producto: cantidad}`. "
            "Escribe una función que devuelva el total de unidades sumando todas las cantidades."
        ),
        "pistas": [
            "`dict.values()` te da los valores.",
            "`sum(...)` los suma.",
        ],
        "ejemplo": 'total_inventario({"manzana": 5, "pera": 3}) → 8',
        "firma": "def total_inventario(inv):",
        "function_name": "total_inventario",
        "mode": "function",
        "tests": [
            {"args": [{"a": 5, "b": 3}], "expected": 8},
            {"args": [{}], "expected": 0},
            {"args": [{"x": 10}], "expected": 10},
            {"args": [{"a": 1, "b": 1, "c": 1, "d": 1}], "expected": 4},
        ],
    },
    {
        "id": 17,
        "nivel": "Intermedio",
        "titulo": "Palíndromo",
        "enunciado": (
            "Verifica si una palabra es palíndromo (se lee igual al derecho y al revés). "
            "Ignora mayúsculas/minúsculas. No te preocupes por espacios."
        ),
        "pistas": ["Convierte a minúsculas y compara con su versión invertida (`palabra[::-1]`)."],
        "ejemplo": 'es_palindromo("Reconocer") → True',
        "firma": "def es_palindromo(palabra):",
        "function_name": "es_palindromo",
        "mode": "function",
        "tests": [
            {"args": ["ana"], "expected": True},
            {"args": ["oso"], "expected": True},
            {"args": ["hola"], "expected": False},
            {"args": ["Reconocer"], "expected": True},
            {"args": [""], "expected": True},
        ],
    },
    {
        "id": 18,
        "nivel": "Intermedio",
        "titulo": "Eliminar duplicados conservando orden",
        "enunciado": (
            "Elimina los elementos duplicados de una lista, **conservando el orden** "
            "en que aparecieron por primera vez."
        ),
        "pistas": [
            "Recorre la lista y agrega cada elemento a una nueva lista solo si no estaba ya.",
            "Usar `set()` directamente NO conserva el orden.",
        ],
        "ejemplo": "sin_duplicados([1, 2, 2, 3, 1, 4]) → [1, 2, 3, 4]",
        "firma": "def sin_duplicados(lista):",
        "function_name": "sin_duplicados",
        "mode": "function",
        "tests": [
            {"args": [[1, 2, 2, 3, 1]], "expected": [1, 2, 3]},
            {"args": [[]], "expected": []},
            {"args": [[1, 1, 1]], "expected": [1]},
            {"args": [["a", "b", "a", "c"]], "expected": ["a", "b", "c"]},
        ],
    },
    {
        "id": 19,
        "nivel": "Intermedio",
        "titulo": "Suma de pares en lista",
        "enunciado": "Suma todos los números **pares** de una lista de enteros.",
        "pistas": ["Recorre la lista y suma solo si `x % 2 == 0`."],
        "ejemplo": "suma_pares([1, 2, 3, 4, 5, 6]) → 12",
        "firma": "def suma_pares(lista):",
        "function_name": "suma_pares",
        "mode": "function",
        "tests": [
            {"args": [[1, 2, 3, 4, 5, 6]], "expected": 12},
            {"args": [[1, 3, 5]], "expected": 0},
            {"args": [[]], "expected": 0},
            {"args": [[2, 4, 6]], "expected": 12},
        ],
    },
    {
        "id": 20,
        "nivel": "Intermedio",
        "titulo": "Precio con descuento (parámetro por defecto)",
        "enunciado": (
            "Una tienda aplica un descuento del 10% por defecto, pero a veces aplica otro "
            "porcentaje. Escribe una función que reciba el precio y opcionalmente el "
            "descuento (en porcentaje), y devuelva el precio final. Si no se pasa el "
            "descuento, debe usar 10."
        ),
        "pistas": [
            "Define el parámetro con valor por defecto: `def precio_final(precio, descuento=10):`.",
            "Precio final = precio × (1 - descuento/100).",
        ],
        "ejemplo": "precio_final(100) → 90.0; precio_final(100, 25) → 75.0",
        "firma": "def precio_final(precio, descuento=10):",
        "function_name": "precio_final",
        "mode": "function",
        "tests": [
            {"args": [100], "expected": 90.0},
            {"args": [100, 25], "expected": 75.0},
            {"args": [50], "expected": 45.0},
            {"args": [200, 50], "expected": 100.0},
        ],
    },
    # ============================================================
    # NIVEL INTERMEDIO-SUPERIOR (21-30)
    # ============================================================
    {
        "id": 21,
        "nivel": "Intermedio-superior",
        "titulo": "Cuadrados de los pares (list comprehension)",
        "enunciado": (
            "Dada una lista de números, devuelve una nueva lista con los **cuadrados** "
            "de los números **pares**. Resuélvelo usando una list comprehension en una "
            "sola línea."
        ),
        "pistas": ["Sintaxis: `[expresion for x in lista if condicion]`."],
        "ejemplo": "cuadrados_pares([1,2,3,4,5]) → [4, 16]",
        "firma": "def cuadrados_pares(lista):",
        "function_name": "cuadrados_pares",
        "mode": "function",
        "tests": [
            {"args": [[1, 2, 3, 4, 5]], "expected": [4, 16]},
            {"args": [[]], "expected": []},
            {"args": [[1, 3, 5]], "expected": []},
            {"args": [[2, 4, 6]], "expected": [4, 16, 36]},
        ],
    },
    {
        "id": 22,
        "nivel": "Intermedio-superior",
        "titulo": "Clase Estudiante",
        "enunciado": (
            "Crea una clase `Estudiante` con dos atributos: `nombre` (str) y `notas` "
            "(lista de números). Debe tener un método `promedio()` que devuelve el "
            "promedio de sus notas. Si la lista está vacía, devuelve 0."
        ),
        "pistas": [
            "Define `__init__(self, nombre, notas)`.",
            "En `promedio`, maneja el caso de lista vacía con un `if`.",
        ],
        "ejemplo": 'Estudiante("Ana", [8, 9, 10]).promedio() → 9.0',
        "firma": "class Estudiante:",
        "function_name": None,
        "mode": "custom",
        "tests": [
            {"custom": "Estudiante('Ana', [8,9,10]).promedio()", "expected": 9.0},
            {"custom": "Estudiante('Luis', [10,10]).promedio()", "expected": 10.0},
            {"custom": "Estudiante('X', []).promedio()", "expected": 0},
            {"custom": "Estudiante('Y', [5,7]).nombre", "expected": "Y"},
        ],
    },
    {
        "id": 23,
        "nivel": "Intermedio-superior",
        "titulo": "División segura",
        "enunciado": (
            "Escribe una función que divida dos números, pero que maneje el caso de "
            "división por cero usando `try/except`. Si hay error, debe devolver `None`."
        ),
        "pistas": ["Sintaxis: `try: ... except ZeroDivisionError: return None`."],
        "ejemplo": "dividir(10, 0) → None",
        "firma": "def dividir(a, b):",
        "function_name": "dividir",
        "mode": "function",
        "tests": [
            {"args": [10, 2], "expected": 5.0},
            {"args": [10, 0], "expected": None},
            {"args": [0, 5], "expected": 0.0},
            {"args": [-6, 2], "expected": -3.0},
        ],
    },
    {
        "id": 24,
        "nivel": "Intermedio-superior",
        "titulo": "Ordenar por longitud (lambda)",
        "enunciado": (
            "Ordena una lista de strings por su longitud (de menor a mayor). "
            "Usa la función `sorted` con una `lambda`."
        ),
        "pistas": ["`sorted(lista, key=lambda s: len(s))`."],
        "ejemplo": 'ordenar_por_largo(["aaa", "b", "cc"]) → ["b", "cc", "aaa"]',
        "firma": "def ordenar_por_largo(lista):",
        "function_name": "ordenar_por_largo",
        "mode": "function",
        "tests": [
            {"args": [["aaa", "b", "cc"]], "expected": ["b", "cc", "aaa"]},
            {"args": [[]], "expected": []},
            {"args": [["hola", "hi"]], "expected": ["hi", "hola"]},
        ],
    },
    {
        "id": 25,
        "nivel": "Intermedio-superior",
        "titulo": "Frecuencia de letras",
        "enunciado": (
            "Devuelve un diccionario con la frecuencia de cada letra de una palabra "
            "(cuántas veces aparece cada una). Distingue mayúsculas de minúsculas."
        ),
        "pistas": [
            "Recorre la palabra y usa `dict.get(letra, 0) + 1`.",
            "También puedes usar `collections.Counter`, pero practica el bucle.",
        ],
        "ejemplo": 'frecuencias("aabbc") → {"a": 2, "b": 2, "c": 1}',
        "firma": "def frecuencias(palabra):",
        "function_name": "frecuencias",
        "mode": "function",
        "tests": [
            {"args": ["aabbc"], "expected": {"a": 2, "b": 2, "c": 1}},
            {"args": [""], "expected": {}},
            {"args": ["abc"], "expected": {"a": 1, "b": 1, "c": 1}},
        ],
    },
    {
        "id": 26,
        "nivel": "Intermedio-superior",
        "titulo": "Herencia: Animal y Perro",
        "enunciado": (
            "Crea una clase `Animal` con un método `hablar()` que devuelve `\"...\"`. "
            "Crea una clase `Perro` que **herede** de `Animal` y sobreescriba `hablar()` "
            "para devolver `\"Guau\"`."
        ),
        "pistas": ["Sintaxis de herencia: `class Perro(Animal):`."],
        "ejemplo": 'Perro().hablar() → "Guau"',
        "firma": "class Animal:\n    ...\nclass Perro(Animal):",
        "function_name": None,
        "mode": "custom",
        "tests": [
            {"custom": "Animal().hablar()", "expected": "..."},
            {"custom": "Perro().hablar()", "expected": "Guau"},
            {"custom": "isinstance(Perro(), Animal)", "expected": True},
        ],
    },
    {
        "id": 27,
        "nivel": "Intermedio-superior",
        "titulo": "Generador de Fibonacci",
        "enunciado": (
            "Implementa un **generador** que produzca los primeros N números de "
            "Fibonacci (empezando por 0, 1, 1, 2, 3…)."
        ),
        "pistas": [
            "Usa `yield` dentro de un bucle.",
            "Lleva dos variables `a, b = 0, 1` y haz `a, b = b, a+b`.",
        ],
        "ejemplo": "list(fibonacci(5)) → [0, 1, 1, 2, 3]",
        "firma": "def fibonacci(n):",
        "function_name": None,
        "mode": "custom",
        "tests": [
            {"custom": "list(fibonacci(5))", "expected": [0, 1, 1, 2, 3]},
            {"custom": "list(fibonacci(0))", "expected": []},
            {"custom": "list(fibonacci(1))", "expected": [0]},
            {"custom": "list(fibonacci(8))", "expected": [0, 1, 1, 2, 3, 5, 8, 13]},
        ],
    },
    {
        "id": 28,
        "nivel": "Intermedio-superior",
        "titulo": "Suma de dígitos recursiva",
        "enunciado": (
            "Suma los dígitos de un número entero positivo usando **recursión** "
            "(sin bucles, sin convertir a string)."
        ),
        "pistas": [
            "Caso base: si `n < 10`, devuelve `n`.",
            "Caso recursivo: `n % 10 + suma_digitos(n // 10)`.",
        ],
        "ejemplo": "suma_digitos(123) → 6",
        "firma": "def suma_digitos(n):",
        "function_name": "suma_digitos",
        "mode": "function",
        "tests": [
            {"args": [0], "expected": 0},
            {"args": [5], "expected": 5},
            {"args": [123], "expected": 6},
            {"args": [9999], "expected": 36},
            {"args": [10], "expected": 1},
        ],
    },
    {
        "id": 29,
        "nivel": "Intermedio-superior",
        "titulo": "Decorador que duplica el resultado",
        "enunciado": (
            "Crea un decorador llamado `duplicar` que multiplique por 2 el resultado "
            "de la función decorada. Aplícalo a una función `obtener_valor()` que "
            "devuelve `5`. El resultado de llamarla debe ser `10`."
        ),
        "pistas": [
            "Un decorador es una función que recibe otra función y devuelve un wrapper.",
            "Plantilla:\n```\ndef duplicar(f):\n    def wrapper(*a, **kw):\n        return f(*a, **kw) * 2\n    return wrapper\n```",
            "Recuerda usar `@duplicar` encima de `obtener_valor`.",
        ],
        "ejemplo": "obtener_valor() → 10",
        "firma": "def duplicar(f):\n    ...\n@duplicar\ndef obtener_valor():",
        "function_name": None,
        "mode": "custom",
        "tests": [
            {"custom": "obtener_valor()", "expected": 10},
        ],
    },
    {
        "id": 30,
        "nivel": "Intermedio-superior",
        "titulo": "Clase Punto con __str__ y __eq__",
        "enunciado": (
            "Crea una clase `Punto` con atributos `x` e `y`. Implementa `__str__` para "
            "que devuelva la cadena `\"(x, y)\"` y `__eq__` para que dos puntos sean "
            "iguales si tienen el mismo `x` y el mismo `y`."
        ),
        "pistas": [
            "`__str__(self)` debe devolver un string.",
            "`__eq__(self, other)` compara `self.x == other.x and self.y == other.y`.",
        ],
        "ejemplo": "str(Punto(1,2)) → \"(1, 2)\"",
        "firma": "class Punto:",
        "function_name": None,
        "mode": "custom",
        "tests": [
            {"custom": "str(Punto(1,2))", "expected": "(1, 2)"},
            {"custom": "Punto(1,2) == Punto(1,2)", "expected": True},
            {"custom": "Punto(1,2) == Punto(3,4)", "expected": False},
            {"custom": "str(Punto(0,0))", "expected": "(0, 0)"},
        ],
    },
]


NIVELES = ["Básico", "Intermedio", "Intermedio-superior"]


def por_nivel(nivel: str):
    """Devuelve los ejercicios de un nivel concreto."""
    return [e for e in EXERCISES if e["nivel"] == nivel]


def por_id(eid: int):
    """Devuelve un ejercicio por su id."""
    for e in EXERCISES:
        if e["id"] == eid:
            return e
    return None

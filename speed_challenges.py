"""25 desafíos rápidos de Python para el modo Contrarreloj.

Cada desafío tiene un `expected` que es exactamente lo que el alumno debe
imprimir por la salida estándar (se compara con `.strip()` para tolerar
saltos de línea finales). Para preguntas de opción múltiple el alumno
imprime la letra correcta como texto, por ejemplo `print("a")`.
"""

SPEED_CHALLENGES = [
    {
        "id": 1,
        "tipo": "salida",
        "enunciado": "Imprime exactamente: Hola Mundo",
        "expected": "Hola Mundo",
        "pista": 'print("Hola Mundo")',
    },
    {
        "id": 2,
        "tipo": "salida",
        "enunciado": "Imprime el resultado de 7 + 8",
        "expected": "15",
        "pista": "print(7 + 8)",
    },
    {
        "id": 3,
        "tipo": "salida",
        "enunciado": 'Imprime cuántas letras tiene la palabra "python" (sin contar las comillas).',
        "expected": "6",
        "pista": 'print(len("python"))',
    },
    {
        "id": 4,
        "tipo": "salida",
        "enunciado": 'Imprime la palabra "PYTHON" toda en minúsculas.',
        "expected": "python",
        "pista": 'print("PYTHON".lower())',
    },
    {
        "id": 5,
        "tipo": "salida",
        "enunciado": "Imprime el resultado de 5 elevado al cuadrado.",
        "expected": "25",
        "pista": "print(5 ** 2)",
    },
    {
        "id": 6,
        "tipo": "salida",
        "enunciado": "Imprime la división ENTERA de 100 entre 7 (sin decimales).",
        "expected": "14",
        "pista": "print(100 // 7)",
    },
    {
        "id": 7,
        "tipo": "salida",
        "enunciado": "Imprime el resto (módulo) de dividir 23 entre 4.",
        "expected": "3",
        "pista": "print(23 % 4)",
    },
    {
        "id": 8,
        "tipo": "salida",
        "enunciado": 'Imprime "ABC" repetido 4 veces seguidas en la misma línea.',
        "expected": "ABCABCABCABC",
        "pista": 'print("ABC" * 4)',
    },
    {
        "id": 9,
        "tipo": "salida",
        "enunciado": "Imprime el PRIMER elemento de la lista [10, 20, 30].",
        "expected": "10",
        "pista": "print([10, 20, 30][0])",
    },
    {
        "id": 10,
        "tipo": "salida",
        "enunciado": "Imprime el ÚLTIMO elemento de la lista [10, 20, 30].",
        "expected": "30",
        "pista": "print([10, 20, 30][-1])",
    },
    {
        "id": 11,
        "tipo": "salida",
        "enunciado": "Imprime el resultado booleano de comparar si 5 es mayor que 3.",
        "expected": "True",
        "pista": "print(5 > 3)",
    },
    {
        "id": 12,
        "tipo": "salida",
        "enunciado": 'Imprime el resultado de comparar el entero 10 con el texto "10" usando ==',
        "expected": "False",
        "pista": 'print(10 == "10")',
    },
    {
        "id": 13,
        "tipo": "salida",
        "enunciado": "Imprime la longitud de la lista [1, 2, 3, 4, 5, 6, 7].",
        "expected": "7",
        "pista": "print(len([1, 2, 3, 4, 5, 6, 7]))",
    },
    {
        "id": 14,
        "tipo": "salida",
        "enunciado": "Imprime el VALOR MÁXIMO entre los números 15, 27 y 9.",
        "expected": "27",
        "pista": "print(max(15, 27, 9))",
    },
    {
        "id": 15,
        "tipo": "salida",
        "enunciado": "Imprime el VALOR MÍNIMO entre los números 8, 3 y 12.",
        "expected": "3",
        "pista": "print(min(8, 3, 12))",
    },
    {
        "id": 16,
        "tipo": "salida",
        "enunciado": "Imprime el resultado de 2 elevado a 10.",
        "expected": "1024",
        "pista": "print(2 ** 10)",
    },
    {
        "id": 17,
        "tipo": "salida",
        "enunciado": "Imprime la suma de los números del 1 al 10 (ambos incluidos).",
        "expected": "55",
        "pista": "print(sum(range(1, 11)))",
    },
    {
        "id": 18,
        "tipo": "salida",
        "enunciado": 'Imprime True si la cadena "py" aparece dentro de "python".',
        "expected": "True",
        "pista": 'print("py" in "python")',
    },
    {
        "id": 19,
        "tipo": "multiple",
        "enunciado": (
            "¿Qué función convierte un texto a número entero?\n\n"
            "a) int()\n"
            "b) str()\n"
            "c) float()\n\n"
            "Imprime SOLO la letra correcta como texto (por ejemplo: print(\"x\"))."
        ),
        "expected": "a",
        "pista": 'print("a")',
    },
    {
        "id": 20,
        "tipo": "multiple",
        "enunciado": (
            "¿Qué símbolo se usa para comentar una sola línea en Python?\n\n"
            "a) //\n"
            "b) #\n"
            "c) /*\n\n"
            "Imprime SOLO la letra correcta como texto."
        ),
        "expected": "b",
        "pista": 'print("b")',
    },
    {
        "id": 21,
        "tipo": "multiple",
        "enunciado": (
            "¿Cuál de estos NO es un tipo nativo de Python?\n\n"
            "a) int\n"
            "b) char\n"
            "c) list\n\n"
            "Imprime SOLO la letra correcta como texto."
        ),
        "expected": "b",
        "pista": 'print("b")',
    },
    {
        "id": 22,
        "tipo": "multiple",
        "enunciado": (
            "¿Qué palabra clave define una función en Python?\n\n"
            "a) function\n"
            "b) def\n"
            "c) func\n\n"
            "Imprime SOLO la letra correcta como texto."
        ),
        "expected": "b",
        "pista": 'print("b")',
    },
    {
        "id": 23,
        "tipo": "salida",
        "enunciado": 'Imprime "hola mundo" todo en MAYÚSCULAS.',
        "expected": "HOLA MUNDO",
        "pista": 'print("hola mundo".upper())',
    },
    {
        "id": 24,
        "tipo": "salida",
        "enunciado": 'Imprime la PRIMERA letra de la palabra "Python".',
        "expected": "P",
        "pista": 'print("Python"[0])',
    },
    {
        "id": 25,
        "tipo": "salida",
        "enunciado": 'Imprime la palabra "hola" escrita al revés.',
        "expected": "aloh",
        "pista": 'print("hola"[::-1])',
    },
]


TIME_LIMIT_SECONDS = 120  # 2 minutos por desafío

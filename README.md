# Generador Automático de Casos de Prueba - GLC

## Descripción
Este proyecto implementa un generador automático de casos de prueba para gramáticas libres de contexto (GLC), desarrollado como parte del Proyecto 02 de INFO1148.

## Características Principales

### 1. Generación de Casos de Prueba
- **Casos Válidos**: Generados mediante derivaciones aleatorias desde el símbolo inicial
- **Casos Inválidos**: Generados mediante mutaciones sintácticas de casos válidos
- **Casos Extremos**: Casos límite con profundidad máxima, mínima, expresiones largas y anidamiento profundo

### 2. Interfaz Gráfica
- Interfaz amigable construida con tkinter
- Panel de definición de gramática con carga desde archivo
- Configuración de parámetros de generación
- Visualización de resultados en pestañas separadas
- Filtrado de casos por tipo
- Barra de estado con información en tiempo real

### 3. Métricas y Estadísticas
- Total de casos generados
- Distribución por categorías (válidas, inválidas, extremas)
- Longitud promedio de expresiones
- Profundidad máxima alcanzada
- Conteo de operadores utilizados
- Tiempo de ejecución

### 4. Exportación
- Exportación completa a formato JSON
- Incluye casos de prueba y métricas
- Nombre de archivo automático con timestamp

## Requisitos
- Python 3.7 o superior
- Tkinter (incluido en Python por defecto)

## Estructura del Proyecto

```
miniproyecto2/
├── generator.py             # Módulo con las clases principales (GrammarParser, TestCaseGenerator)
├── interfaz.py              # Interfaz gráfica de usuario
├── test_functionality.py    # Script de pruebas
├── gramatica_ejemplo.txt    # Ejemplo de gramática
└── README.md                # Este archivo
```

## Uso

### Ejecución de la Interfaz Gráfica
```bash
python interfaz.py
```

### Ejecución de Pruebas
```bash
python test_functionality.py
```

### Pasos para generar casos de prueba:

1. **Ejecutar la aplicación**
   ```bash
   python interfaz.py
   ```

2. **Definir Gramática**
   - Escribe la gramática en el panel izquierdo
   - O carga un archivo de texto con el botón "📁 Cargar Archivo"
   - O usa el ejemplo predefinido con "📄 Ejemplo"
   
2. **Definir Gramática**
   - Escribe la gramática en el panel izquierdo
   - O carga un archivo de texto con el botón "📁 Cargar Archivo"
   - O usa el ejemplo predefinido con "📄 Ejemplo"
   
   Formato de la gramática:
   ```
   No-Terminal -> producción | producción
   ```
   
   Ejemplo:
   ```
   E -> E + T | E - T | T
   T -> T * F | T / F | F
   F -> ( E ) | num
   ```

3. **Configurar Parámetros**
   - Casos Válidos: Número de casos válidos a generar (1-100)
   - Casos Inválidos: Número de casos inválidos a generar (1-100)
   - Casos Extremos: Número de casos extremos a generar (1-100)
   - Profundidad Máxima: Profundidad máxima del árbol de derivación (1-15)
   - Longitud Máxima: Longitud máxima de las expresiones (10-500)

4. **Generar**
   - Clic en "🚀 GENERAR CASOS DE PRUEBA"
   - Espera a que se complete la generación
   - Revisa los resultados en las pestañas

5. **Ver Resultados**
   - Pestaña "📈 Métricas y Estadísticas": Resumen estadístico
   - Pestaña "📋 Casos de Prueba Generados": Lista detallada de casos
   - Usa el filtro para ver casos específicos por tipo

6. **Exportar**
   - Clic en "💾 Exportar a JSON"
   - Selecciona la ubicación y nombre del archivo
   - El archivo incluirá todos los casos y métricas

## Componentes Principales

### generator.py

#### GrammarParser
Clase que parsea y almacena las reglas de la gramática libre de contexto.

#### TestCaseGenerator
Clase que genera los casos de prueba:
- `generate_valid()`: Genera casos válidos mediante derivación
- `generate_invalid()`: Genera casos inválidos mediante mutación
- `generate_extreme()`: Genera casos extremos
- `calculate_metrics()`: Calcula estadísticas
- `export_json()`: Exporta resultados a JSON

### interfaz.py

#### Application
Clase de la interfaz gráfica que gestiona toda la interacción con el usuario.

## Tipos de Mutaciones para Casos Inválidos

1. **eliminar_operador**: Elimina un operador aleatorio
2. **duplicar_operador**: Duplica un operador aleatorio
3. **parentesis_desbalanceado**: Elimina un paréntesis
4. **operador_inicio**: Agrega operador al inicio
5. **operador_final**: Agrega operador al final
6. **eliminar_operando**: Elimina un operando
7. **espacios_incorrectos**: Elimina espacios

## Formato de Salida JSON

```json
{
  "test_cases": [
    {
      "id": 1,
      "type": "válida",
      "expression": "num + num * num",
      "depth": 3,
      "length": 17
    },
    {
      "id": 2,
      "type": "inválida",
      "expression": "num num + num",
      "mutation": "eliminar_operador",
      "length": 13
    }
  ],
  "metrics": {
    "total_cases": 20,
    "distribution": {
      "valid": "50.00%",
      "invalid": "25.00%",
      "extreme": "25.00%"
    },
    "avg_length": "22.50",
    "max_depth": 5,
    "operators": {
      "+": 15,
      "-": 8,
      "*": 12,
      "/": 5,
      "%": 3
    },
    "execution_time": "0.0234s",
    "generated_at": "2025-11-26T10:30:45.123456"
  }
}
```

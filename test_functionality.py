"""
Script de prueba rápida para verificar funcionalidad básica
sin interfaz gráfica
"""

import json
from datetime import datetime
from generator import GrammarParser, TestCaseGenerator

def test_basic_functionality():
    """Prueba la funcionalidad básica del generador"""
    
    print("=" * 80)
    print("PRUEBA DE FUNCIONALIDAD BÁSICA")
    print("=" * 80)
    
    # Definir gramática de prueba
    grammar_text = """E -> E + T | E - T | T
T -> T * F | T / F | T % F | F
F -> ( E ) | num"""
    
    print("\n1. Parseando gramática...")
    grammar = GrammarParser(grammar_text)
    print(f"   ✓ Símbolos no-terminales encontrados: {list(grammar.rules.keys())}")
    print(f"   ✓ Símbolo inicial: {grammar.get_start_symbol()}")
    
    print("\n2. Creando generador de casos de prueba...")
    generator = TestCaseGenerator(grammar)
    print("   ✓ Generador creado exitosamente")
    
    print("\n3. Generando casos de prueba...")
    print("   - 5 casos válidos")
    print("   - 3 casos inválidos")
    print("   - 2 casos extremos")
    
    generator.generate_all(
        valid_count=5,
        invalid_count=3,
        extreme_count=2,
        max_depth=4,
        max_length=50
    )
    
    print(f"   ✓ Total generado: {len(generator.test_cases)} casos")
    
    print("\n4. Mostrando ejemplos de casos generados:")
    print("   " + "-" * 76)
    
    for i, case in enumerate(generator.test_cases[:10], 1):
        print(f"\n   Caso #{i}:")
        print(f"   Tipo: {case['type'].upper()}")
        print(f"   Expresión: {case['expression']}")
        if 'mutation' in case:
            print(f"   Mutación: {case['mutation']}")
        if 'extreme_type' in case:
            print(f"   Tipo extremo: {case['extreme_type']}")
    
    print("\n" + "   " + "-" * 76)
    
    print("\n5. Métricas generadas:")
    print(f"   Total de casos: {generator.metrics['total_cases']}")
    print(f"   Distribución:")
    for tipo, porcentaje in generator.metrics['distribution'].items():
        print(f"     - {tipo}: {porcentaje}")
    print(f"   Longitud promedio: {generator.metrics['avg_length']} símbolos")
    print(f"   Profundidad máxima: {generator.metrics['max_depth']}")
    print(f"   Tiempo de ejecución: {generator.metrics['execution_time']}")
    
    print("\n6. Exportando a JSON...")
    output_file = "test_output.json"
    generator.export_json(output_file)
    print(f"   ✓ Exportado a: {output_file}")
    
    # Verificar el archivo exportado
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"   ✓ Archivo JSON válido con {len(data['test_cases'])} casos")
    
    print("\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS PASADAS EXITOSAMENTE")
    print("=" * 80)

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

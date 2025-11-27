import json
import random
import time
from datetime import datetime
from typing import Dict, List, Tuple


class GrammarParser:
    """Parser de gramáticas libres de contexto"""
    
    def __init__(self, grammar_text: str):
        self.rules = {}
        self.parse_grammar(grammar_text)
    
    def parse_grammar(self, grammar_text: str):
        """Parsea la gramática desde texto"""
        lines = [line.strip() for line in grammar_text.split('\n') if line.strip()]
        
        for line in lines:
            if '->' not in line:
                continue
            
            left, right = line.split('->', 1)
            left = left.strip()
            
            # Dividir por '|' para obtener las producciones
            productions = [prod.strip().split() for prod in right.split('|')]
            self.rules[left] = productions
    
    def get_start_symbol(self) -> str:
        """Obtiene el símbolo inicial (primer símbolo definido)"""
        return list(self.rules.keys())[0] if self.rules else None


class TestCaseGenerator:
    """Generador de casos de prueba"""
    
    def __init__(self, grammar: GrammarParser):
        self.grammar = grammar
        self.test_cases = []
        self.metrics = {}
        self.start_time = None
        self.end_time = None
    
    def generate_valid(self, symbol: str, depth: int, max_depth: int) -> str:
        """Genera una cadena válida mediante derivación"""
        if depth > max_depth:
            # Si alcanzamos profundidad máxima, intentar derivar a terminal
            if symbol not in self.grammar.rules:
                return symbol
            # Buscar producción que derive directamente a terminales
            for prod in self.grammar.rules[symbol]:
                if all(s not in self.grammar.rules for s in prod):
                    return ' '.join(prod)
            return ''
        
        # Si es terminal, retornarlo
        if symbol not in self.grammar.rules:
            return symbol
        
        # Elegir una producción al azar
        productions = self.grammar.rules[symbol]
        production = random.choice(productions)
        
        # Derivar cada símbolo de la producción
        result = []
        for sym in production:
            derived = self.generate_valid(sym, depth + 1, max_depth)
            if derived:
                result.append(derived)
        
        return ' '.join(result)
    
    def generate_invalid(self, valid_string: str) -> Tuple[str, str]:
        """Genera una cadena inválida mediante mutación sintáctica"""
        mutations = [
            ('eliminar_operador', lambda s: self._remove_operator(s)),
            ('duplicar_operador', lambda s: self._duplicate_operator(s)),
            ('parentesis_desbalanceado', lambda s: self._unbalanced_parenthesis(s)),
            ('operador_inicio', lambda s: '+ ' + s),
            ('operador_final', lambda s: s + ' *'),
            ('eliminar_operando', lambda s: self._remove_operand(s)),
            ('espacios_incorrectos', lambda s: s.replace(' ', '')),
        ]
        
        mutation_name, mutation_func = random.choice(mutations)
        try:
            invalid_string = mutation_func(valid_string)
            return invalid_string, mutation_name
        except:
            return valid_string + ' +', 'operador_final'
    
    def _remove_operator(self, s: str) -> str:
        """Elimina un operador aleatorio"""
        operators = ['+', '-', '*', '/', '%']
        for op in operators:
            if op in s:
                return s.replace(op, '', 1)
        return s
    
    def _duplicate_operator(self, s: str) -> str:
        """Duplica un operador aleatorio"""
        operators = ['+', '-', '*', '/', '%']
        for op in operators:
            if op in s:
                return s.replace(op, op + op, 1)
        return s
    
    def _unbalanced_parenthesis(self, s: str) -> str:
        """Desbalancea paréntesis"""
        if ')' in s:
            return s.replace(')', '', 1)
        elif '(' in s:
            return s.replace('(', '', 1)
        return '( ' + s
    
    def _remove_operand(self, s: str) -> str:
        """Elimina un operando"""
        tokens = s.split()
        if len(tokens) > 2:
            # Buscar un token que no sea operador
            for i, token in enumerate(tokens):
                if token not in ['+', '-', '*', '/', '%', '(', ')']:
                    tokens.pop(i)
                    return ' '.join(tokens)
        return s
    
    def generate_extreme(self, symbol: str, extreme_type: str, max_depth: int, max_length: int) -> str:
        """Genera casos extremos"""
        if extreme_type == 'max_depth':
            return self.generate_valid(symbol, 0, max_depth)
        elif extreme_type == 'min_depth':
            return self.generate_valid(symbol, 0, 1)
        elif extreme_type == 'long_expression':
            # Intentar generar expresión larga
            attempts = 0
            while attempts < 10:
                expr = self.generate_valid(symbol, 0, max_depth)
                if len(expr) >= max_length * 0.7:
                    return expr
                attempts += 1
            return expr
        elif extreme_type == 'nested_parenthesis':
            # Expresión con muchos paréntesis anidados
            return self.generate_valid(symbol, 0, max_depth)
        else:
            return self.generate_valid(symbol, 0, max_depth)
    
    def generate_all(self, valid_count: int, invalid_count: int, 
                    extreme_count: int, max_depth: int, max_length: int):
        """Genera todos los casos de prueba"""
        self.start_time = time.time()
        self.test_cases = []
        
        start_symbol = self.grammar.get_start_symbol()
        if not start_symbol:
            raise ValueError("Gramática vacía o inválida")
        
        # Generar casos válidos
        for i in range(valid_count):
            expr = self.generate_valid(start_symbol, 0, max_depth)
            self.test_cases.append({
                'id': len(self.test_cases) + 1,
                'type': 'válida',
                'expression': expr,
                'depth': random.randint(1, max_depth),
                'length': len(expr)
            })
        
        # Generar casos inválidos
        for i in range(invalid_count):
            valid_expr = self.generate_valid(start_symbol, 0, max_depth)
            invalid_expr, mutation_type = self.generate_invalid(valid_expr)
            self.test_cases.append({
                'id': len(self.test_cases) + 1,
                'type': 'inválida',
                'expression': invalid_expr,
                'mutation': mutation_type,
                'length': len(invalid_expr)
            })
        
        # Generar casos extremos
        extreme_types = ['max_depth', 'min_depth', 'long_expression', 'nested_parenthesis']
        for i in range(extreme_count):
            extreme_type = extreme_types[i % len(extreme_types)]
            expr = self.generate_extreme(start_symbol, extreme_type, max_depth, max_length)
            self.test_cases.append({
                'id': len(self.test_cases) + 1,
                'type': 'extrema',
                'expression': expr,
                'extreme_type': extreme_type,
                'length': len(expr)
            })
        
        self.end_time = time.time()
        self.calculate_metrics()
    
    def calculate_metrics(self):
        """Calcula métricas del proceso"""
        total_cases = len(self.test_cases)
        valid_cases = len([c for c in self.test_cases if c['type'] == 'válida'])
        invalid_cases = len([c for c in self.test_cases if c['type'] == 'inválida'])
        extreme_cases = len([c for c in self.test_cases if c['type'] == 'extrema'])
        
        avg_length = sum(c['length'] for c in self.test_cases) / total_cases if total_cases > 0 else 0
        
        # Contar operadores
        operators = {'+': 0, '-': 0, '*': 0, '/': 0, '%': 0}
        max_depth = 0
        
        for case in self.test_cases:
            expr = case['expression']
            for op in operators:
                operators[op] += expr.count(op)
            if 'depth' in case:
                max_depth = max(max_depth, case['depth'])
        
        execution_time = self.end_time - self.start_time if self.start_time and self.end_time else 0
        
        self.metrics = {
            'total_cases': total_cases,
            'distribution': {
                'valid': f"{(valid_cases / total_cases * 100):.2f}%" if total_cases > 0 else "0%",
                'invalid': f"{(invalid_cases / total_cases * 100):.2f}%" if total_cases > 0 else "0%",
                'extreme': f"{(extreme_cases / total_cases * 100):.2f}%" if total_cases > 0 else "0%"
            },
            'avg_length': f"{avg_length:.2f}",
            'max_depth': max_depth,
            'operators': operators,
            'execution_time': f"{execution_time:.4f}s",
            'generated_at': datetime.now().isoformat()
        }
    
    def export_json(self, filename: str):
        """Exporta resultados a JSON"""
        data = {
            'test_cases': self.test_cases,
            'metrics': self.metrics
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

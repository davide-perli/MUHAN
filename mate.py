#-----------------------------------------------------------------------------#
                                # Importuri #
#-----------------------------------------------------------------------------#
from arrow_string import *


#-----------------------------------------------------------------------------#
                                # Constante #
#-----------------------------------------------------------------------------#

DIGITS = '0123456789'



#-----------------------------------------------------------------------------#
                                # Erori custom #
#-----------------------------------------------------------------------------#

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def show_as_string(self):
        show = f'{self.error_name}: {self.details}\n'
        show += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        show += '\n\n' + arrow_string(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return show

class IllegalsInMyEquations(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Allah did not approve this character', details)

class InvalidStntaxError(Error):
    def __init__(self, pos_start, pos_end, details = ''):
        super().__init__(pos_start, pos_end, 'Wallahi what is this mess of an ecuation?', details)


#-----------------------------------------------------------------------------#
                            # Position #
#-----------------------------------------------------------------------------#

class Position:
		def __init__(self, idx, ln, col, fn, ftxt):
				self.idx = idx
				self.ln = ln
				self.col = col
				self.fn = fn
				self.ftxt = ftxt

		def advance(self, current_char=None):
				self.idx += 1
				self.col += 1

				if current_char == '\n':
						self.ln += 1
						self.col = 0

				return self

		def copy(self):
				return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#-----------------------------------------------------------------------------#
                    # Definire tipuri de date #
#-----------------------------------------------------------------------------#

INTEGER           = 'INTEGER'
FLOAT             = 'FLOAT'
PLUS              = 'PLUS'
MINUS             = 'MINUS'
MULTIPLICATION    = 'MULTIPLICATION'
DIVISION          = 'DIVISION'
POWER             = 'POWER'
SQUARE_ROOT       = 'SQUARE ROOT'
FACTORIAL         = 'FACTORIAL'
PROCENT           = 'PROCENT'          # !!!!!!!!! Atentie, asta scoate cat la suta reprezinta un numar dintr-un alt numar, nu restul, ca nu suntem fatalai
LOGARITHM         = 'LOGARITHM'
LEFT_PARENTHESiS  = 'LEFT PARENTHESIS'
RIGHT_PARENTHESiS = 'RIGHT PARENTHESIS'
EOF               = 'EOF'

class Data_Types:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        self.pos_start = pos_start.copy() if pos_start else None
        self.pos_end = pos_end.copy() if pos_end else None

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'






#-----------------------------------------------------------------------------#
            # Parcurgerea si spargerea textului de input #
#-----------------------------------------------------------------------------#

class Input_Read_And_Breakdown:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text               # cam un constructor de initializare
        self.position = Position(-1, 0, -1, fn, text)             # positia curenta in text
        self.current_character = None  # caracterul curent
        self.next_character()

    def next_character(self):
        self.position.advance(self.current_character)                                                                   
        self.current_character = self.text[self.position.idx] if self.position.idx < len(self.text) else None  # caracterul curent e caracterul la pozitia curenta in text, dar logic nu poate intrece lungimea textului

    def make_data_types(self):
        data_types_list = []

        while self.current_character != None: 
            if self.current_character in ' \t':
                self.next_character() 

            elif self.current_character in DIGITS:
                data_types_list.append(self.create_number())

            elif self.current_character == '+':       #identific adunarea
                data_types_list.append(Data_Types(PLUS, pos_start = self.position))
                self.next_character()

            elif self.current_character == '-':       #identific scaderea
                data_types_list.append(Data_Types(MINUS, pos_start = self.position))
                self.next_character()

            elif self.current_character == '*':       #identific inmultirea
                data_types_list.append(Data_Types(MULTIPLICATION, pos_start = self.position))
                self.next_character()

            elif self.current_character == '/':       #identific impartirea
                data_types_list.append(Data_Types(DIVISION, pos_start = self.position))
                self.next_character()

            elif self.current_character == '^':       #identific ridicarea la putere
                data_types_list.append(Data_Types(POWER, pos_start = self.position))
                self.next_character()

            elif self.current_character == '~':       #identific radicalul
                data_types_list.append(Data_Types(SQUARE_ROOT, pos_start = self.position))
                self.next_character()

            elif self.current_character == '!':       #identific factorialul
                data_types_list.append(Data_Types(FACTORIAL, pos_start = self.position))
                self.next_character()

            elif self.current_character == '%':             #identific procentul, cat  la suta reprezinta un numar dintr-un alt numar, NU REST
                data_types_list.append(Data_Types(PROCENT, pos_start = self.position))
                self.next_character()

            elif self.current_character == 'l' or self.current_character == 'L':       #identific logaritmul
                data_types_list.append(Data_Types(LOGARITHM, pos_start = self.position))
                self.next_character()

            elif self.current_character == ',':
                data_types_list.append(Data_Types(',', pos_start=self.position))
                self.next_character()


            elif self.current_character == '(':       #identific paranteza stanga
                data_types_list.append(Data_Types(LEFT_PARENTHESiS, pos_start = self.position))
                self.next_character()

            elif self.current_character == ')':       #identific paranteza dreapta
                data_types_list.append(Data_Types(RIGHT_PARENTHESiS, pos_start = self.position))
                self.next_character()

            else:
                character = self.current_character
                pos_start = self.position.copy()
                self.next_character()
                return [], IllegalsInMyEquations(pos_start, self.position.copy(), f"  :(  ! {character} !")

        data_types_list.append(Data_Types(EOF, pos_start = self.position))
        return data_types_list, None

    def create_number(self):
        number_string = ""
        dot_number = 0   # niciun 0, adica intreg, 1 zero adica float, mai multe eroare
        pos_start = self.position.copy()

        while self.current_character != None and self.current_character in DIGITS + '.':     # caracterul curent e cifra, nu None sau un punct
            
            if self.current_character == '.':
                if dot_number == 1: break    # nu poti avea mai  mult de un punct intr-un numar

                dot_number += 1
                number_string += '.'

            else:
                number_string += self.current_character
            self.next_character()

        if dot_number == 0:  # e intreg numarul
            return Data_Types(INTEGER, int(number_string), pos_start, self.position)

        else:               # e float numarul
            return Data_Types(FLOAT, float(number_string), pos_start, self.position)


#-----------------------------------------------------------------------------#
        # Noduri, ca na, ordinea operatiilor e pracric un arbore :( #
#-----------------------------------------------------------------------------#

class NrNoduri:
    def __init__(self, nr_data_types):
        self.nr_data_types = nr_data_types

    def __repr__(self):
        return f'{self.nr_data_types}'

class NodOperatoriBinari:
    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'



 #-----------------------------------------------------------------------------#
                            # Parser Result #
 #-----------------------------------------------------------------------------#   

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res
    
    def succes(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        self.error = error
        return self



#-----------------------------------------------------------------------------#
                            # Parser #
#-----------------------------------------------------------------------------#

class Parser:
    def __init__(self, data_types):
        self.data_types = data_types
        self.index_data_types = -1
        self.current_data_type = None
        self.advance()

    def advance(self):
        self.index_data_types += 1
        self.current_data_type = (
            self.data_types[self.index_data_types] if self.index_data_types < len(self.data_types) else None
        )

    def parse(self):
        res = self.expression()
        if not res.error and self.current_data_type.type != EOF:
            return res.failure(InvalidStntaxError(
                self.current_data_type.pos_start, self.current_data_type.pos_end,
                "Expected valid mathematical variables or EOF"
            ))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_data_type
        if tok.type == LOGARITHM:
            res.register(self.advance())  # Advance past 'l' or 'L'
            if self.current_data_type.type == LEFT_PARENTHESiS:
                res.register(self.advance())  # Advance past '('
                left_factor = res.register(self.factor())  # The number for which we want the log
                if res.error: return res
                
                if self.current_data_type.type == ',':
                    res.register(self.advance())  # Advance past ','
                    right_factor = res.register(self.factor())  # The base of the logarithm
                    if res.error: return res
                    
                    if self.current_data_type.type == RIGHT_PARENTHESiS:
                        res.register(self.advance())  # Advance past ')'
                        return res.succes(NodOperatoriBinari(left_factor, tok, right_factor))
                        
                return res.failure(InvalidStntaxError(tok.pos_start, tok.pos_end, "Expected base for logarithm"))

        if tok.type in (PLUS, MINUS):  # Handle unary operators
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.succes(NodOperatoriBinari(None, tok, factor))

        elif tok.type in (INTEGER, FLOAT): 
            res.register(self.advance())
            node = NrNoduri(tok)


            while self.current_data_type and self.current_data_type.type == FACTORIAL:
                op_tok = self.current_data_type
                res.register(self.advance())
                node = NodOperatoriBinari(node, op_tok, None)

            return res.succes(node)

        elif tok.type == LEFT_PARENTHESiS:  
            res.register(self.advance())
            expr = res.register(self.expression())
            if res.error: return res
            if self.current_data_type.type == RIGHT_PARENTHESiS:
                res.register(self.advance())
                return res.succes(expr)
            return res.failure(InvalidStntaxError(
                tok.pos_start, tok.pos_end, "Expected ')'"
            ))


        elif tok.type == SQUARE_ROOT:  # Handle square root
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.succes(NodOperatoriBinari(None, tok, factor))

        return res.failure(InvalidStntaxError(
            tok.pos_start, tok.pos_end, "Expected number, '(' or unary operator"
        ))


    def power(self):
        return self.bin_op(self.factor, [POWER])

    def term(self):
        return self.bin_op(self.power, [MULTIPLICATION, DIVISION])

    def percent(self):
        return self.bin_op(self.term, [PROCENT])

    def expression(self):
        return self.bin_op(self.percent, [PLUS, MINUS])

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_data_type and self.current_data_type.type in ops:
            op_tok = self.current_data_type
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = NodOperatoriBinari(left, op_tok, right)

        return res.succes(left)


#-----------------------------------------------------------------------------#
                            # Interpreter #
#-----------------------------------------------------------------------------#


class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NrNoduri(self, node):
        return node.nr_data_types.value

    def visit_NodOperatoriBinari(self, node):
        left = self.visit(node.left_node) if node.left_node else 0
        right = self.visit(node.right_node) if node.right_node else 0
        op_type = node.operator.type

        if op_type == PLUS:
            return left + right
        elif op_type == MINUS:
            return left - right
        elif op_type == MULTIPLICATION:
            return left * right
        elif op_type == DIVISION:
            if right == 0:
                raise Exception("Division by zero is illegal sentance: Oil up and throw to Diddy")
            return left / right
        elif op_type == POWER:
            return left ** right
        elif op_type == SQUARE_ROOT:
            if right < 0:
                raise Exception("Cannot take the square root of a negative number! Sentance: Oil up and throw to Diddy")
            return right ** 0.5
        elif op_type == FACTORIAL:
            if not isinstance(left, int) or left < 0:
                raise Exception("Factorial is only defined for non-negative integers! Sentance: Oil up and throw to Diddy")
            return self.factorial(left)
        elif op_type == PROCENT:
            if right == 0:
                raise Exception("Cannot calculate percentage with zero divisor! Sentance: Oil up and throw to Diddy")
            return (left / right) * 100
        elif op_type == LOGARITHM:
            return self.custom_logarithm(left, right)
        

        raise Exception(f'Unknown operator type: {op_type}')

    def factorial(self, n):
        if n == 0 or n == 1:
            return 1
        return n * self.factorial(n - 1)


    def custom_logarithm(self, value, base):
        if value <= 0:
            raise Exception("Logarithm argument must be greater than zero.")
        if base <= 0 or base == 1:
            raise Exception("Logarithm base must be greater than zero and not equal to one.")
        
        log_value = 0
        current_value = 1
        
  
        while current_value < value:
            current_value *= base
            log_value += 1
        
       
        if current_value > value:
            log_value -= (current_value - value) / current_value
        
        return log_value


#-----------------------------------------------------------------------------#
                            # Rulare #
#-----------------------------------------------------------------------------#


def run(fn,text):

    input_read_and_breakdown = Input_Read_And_Breakdown(fn, text)
    data_types, error = input_read_and_breakdown.make_data_types()

    if error: return None, error

    parser = Parser(data_types)
    ast = parser.parse()

    if ast.error: return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result,  None
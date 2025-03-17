from components.lexica import MyLexer
from components.memory import Memory
from sly import Parser
    # -------------------------------------------
    #   MyParser is a class that defines a syntax parser for evaluating arithmetic expressions.
    #   It uses the SLY library (Python's version of lex & yacc).

    #       - It supports basic arithmetic operations: addition (+), subtraction (-), multiplication (*), and division (/).
    #       - It follows standard operator precedence (multiplication/division before addition/subtraction).
    #       - It converts expressions into prefix and postfix notation.
    # -------------------------------------------
class MyParser(Parser):
    debugfile = 'parser.out'            # Debug file
    start = 'statement'                 # Starting rule (entry point for the parser)
    
    tokens = MyLexer.tokens             # Get the list of tokens from the lexer (MyLexer)
    precedence = (                      # Define operator precedence (higher values have lower precedence)
        ('left', "+", MINUS),           # Addition & Subtraction (lowest precedence)
        ('left', TIMES, DIVIDE),        # Multiplication & Division (higher precedence)
        ('right', UMINUS),              # Unary minus (-x) (highest precedence)
        )

    def __init__(self):
        # Initialize parser with a memory store for variable assignments.
        self.memory:Memory = Memory()   # Stores variable values

    @_('NAME ASSIGN expr')              # Rule: Assigning a value to a variable (e.g., x = 5 + 3)
    def statement(self, p):
        # Handles variable assignment (e.g., x = 5 + 3).
        var_name = p.NAME               
        value = p.expr
        self.memory.set(variable_name=var_name,value=value, data_type=type(value))
        # No return statement since this stores a variable in memory.

    @_('expr')                          # Rule: An expression by itself is a valid statement (e.g., "5 + 3")
    # S -> E
    def statement(self, p) -> int:      
        # ⭐️ Handles standalone expressions (e.g., "5 + 3").
        return p.expr

    # The example with literals
    @_('expr "+" expr')                 
    # E -> E + E
    def expr(self, p):
        # You can refer to the token 2 ways
        # Way1: using array
        # print(p[0], p[1], p[2])

        # Way2: using symbol name. 
        # Here, if you have more than one symbols with the same name
        # You have to indiciate the number at the end.

        # ⭐️ Handles addition (e.g., 5 + 3). 
        return p.expr0 + p.expr1

    # The example with normal token
    @_('expr MINUS expr')
    def expr(self, p):
        print(p[0], p[1], p[2])
        # ⭐️ Handles subtraction (e.g., 5 - 3).
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        # ⭐️ Handles multiplication (e.g., 5 * 3).
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        # ⭐️ Handles division (e.g., 6 / 3).
        return p.expr0 / p.expr1

    # https://sly.readthedocs.io/en/latest/sly.html#dealing-with-ambiguous-grammars
    # `%prec UMINUS` is the way to override the `precedence` of MINUS to UMINUS.
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        # ⭐️ Handles negative numbers (e.g., -5).
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        # ⭐️ Handles expressions inside parentheses (e.g., (5 + 3)).
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        # ⭐️ Handles integer numbers (e.g., 42).
        return int(p.NUMBER)

    # -------------------------------------------
    #  Prefix Notation Conversion (e.g., `+ 3 4` instead of `3 + 4`)
    # -------------------------------------------
    def infix_to_prefix(self, input_text):
        print(f"==== Prefix Notation")
        """
        Converts an infix expression into prefix notation.
        """
        try:
            print(f"🔹 Original Infix Expression: {input_text}")  # Debug
            
            # ✅ Step 1: Tokenize while keeping multi-digit numbers
            tokens = input_text.split()
            print(f"🔹 Tokenized Input: {tokens}")  # Debug
            
            # ✅ Step 2: Reverse token list and swap parentheses
            reversed_tokens = []
            for token in reversed(tokens):
                if token == '(':
                    reversed_tokens.append(')')
                elif token == ')':
                    reversed_tokens.append('(')
                else:
                    reversed_tokens.append(token)

            print(f"🔹 Reversed Tokens: {' '.join(reversed_tokens)}")  # Debug

            # ✅ Step 3: Convert reversed infix to postfix
            operator_stack = []
            prefix = []
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

            print(f"🔹 Converting to Postfix...")  # Debug

            for token in reversed_tokens:
                if token.isdigit():
                    prefix.append(token)  # Append numbers directly
                    print(f"✅ Added Number: {token} → Prefix (Postfix Order): {' '.join(prefix)}")
                elif token == ')':
                    operator_stack.append(token)
                    print(f"⚫️ Pushed ')': Stack: {operator_stack}")
                elif token == '(':
                    while operator_stack and operator_stack[-1] != ')':
                        popped = operator_stack.pop()
                        prefix.append(popped)
                        print(f"🔴 Popped Operator '{popped}' → Prefix (Postfix Order): {' '.join(prefix)}")
                    operator_stack.pop()  # Remove ')'
                    print(f"🧹 Removed ')': Stack: {operator_stack}")
                elif token in precedence:
                    while operator_stack and precedence.get(operator_stack[-1], 0) > precedence.get(token, 0):
                        popped = operator_stack.pop()
                        prefix.append(popped)
                        print(f"🔴 Popped Operator '{popped}' (Higher Precedence) → Prefix (Postfix Order): {' '.join(prefix)}")
                    operator_stack.append(token)
                    print(f"⚫️ Pushed Operator '{token}' → Stack: {operator_stack}")

            while operator_stack:
                popped = operator_stack.pop()
                prefix.append(popped)
                print(f"🔴 Popped Remaining '{popped}' → Prefix (Postfix Order): {' '.join(prefix)}")

            print(f"🔹 Postfix Before Reverse: {' '.join(prefix)}")  # Debug

            # ✅ Step 4: Reverse postfix result to get correct prefix
            prefix.reverse()
            final_prefix = ' '.join(prefix)
            
            print(f"✅ Final Prefix Expression: {final_prefix}\n")  # Debug
            
            return final_prefix

        except Exception as e:
            return f"ERROR: {e}"
    
    # -------------------------------------------
    # Postfix Notation Conversion (e.g., `3 4 +` instead of `3 + 4`)
    # -------------------------------------------
    def infix_to_postfix(self, expression):
        print(f"==== Prefix Notation")
        """
        Converts an infix expression into postfix notation.
        """

        def isOperator(c):
            return c in {"+", "-", "*", "/"}

        def precedence(op):
            if op in {'+', '-'}:
                return 1
            elif op in {'*', '/'}:
                return 2
            return 0

        stack = []
        postfix = []
        tokens = expression.split()

        print(f"🔹 Original Infix Expression: {expression}")
        print(f"🔹 Tokens: {tokens}")

        for token in tokens:
            if token.isdigit():  # If it's a number, add it to output
                postfix.append(token)
                print(f"✅ Added Number: {token} → Postfix: {' '.join(postfix)}")
            elif token == '(':  # Left Parenthesis: Push to stack
                stack.append(token)
                print(f"⚫️ Pushed '(': Stack: {stack}")
            elif token == ')':  # Right Parenthesis: Pop until '('
                while stack and stack[-1] != '(':
                    popped = stack.pop()
                    postfix.append(popped)
                    print(f"🔴 Popped Operator '{popped}' → Postfix: {' '.join(postfix)}")
                stack.pop()  # Remove '('
                print(f"🧹 Removed '(': Stack: {stack}")
            elif isOperator(token):  # If it's an operator
                while (stack and precedence(stack[-1]) >= precedence(token)):
                    popped = stack.pop()
                    postfix.append(popped)
                    print(f"🔴 Popped Operator '{popped}' (Higher Precedence) → Postfix: {' '.join(postfix)}")
                stack.append(token)
                print(f"⚫️ Pushed Operator '{token}' → Stack: {stack}")

        # Pop remaining operators
        while stack:
            popped = stack.pop()
            postfix.append(popped)
            print(f"🔴 Popped Remaining '{popped}' → Postfix: {' '.join(postfix)}")

        final_postfix = ' '.join(postfix)
        print(f"✅ Final Postfix Expression: {final_postfix}\n")

        return final_postfix
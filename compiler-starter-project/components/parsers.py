from components.lexica import MyLexer
from components.memory import Memory
from sly import Parser

class MyParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', "+", MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
        )

    def __init__(self):
        self.memory:Memory = Memory()

    @_('NAME ASSIGN expr')
    def statement(self, p):
        var_name = p.NAME
        value = p.expr
        self.memory.set(variable_name=var_name,value=value, data_type=type(value))
        # Note that I did not return anything

    @_('expr')
    # S -> E
    def statement(self, p) -> int:
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
        return p.expr0 + p.expr1

    # The example with normal token
    @_('expr MINUS expr')
    def expr(self, p):
        print(p[0], p[1], p[2])
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    # https://sly.readthedocs.io/en/latest/sly.html#dealing-with-ambiguous-grammars
    # `%prec UMINUS` is the way to override the `precedence` of MINUS to UMINUS.
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    def pre_fix_expr(self, input_text):
        tokens = input_text.split()
        prefix = []
        operator_stack = []
        precedence = {'+': 2, '-': 2, '*': 1, '/': 1}

        for token in reversed(list(tokens)):
            if token.isdigit():
                prefix.append(token)
            elif token in precedence:
                while (operator_stack and
                    precedence[token] <= precedence[operator_stack[-1]]):
                    prefix.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            prefix.append(operator_stack.pop())
        prefix.reverse()
        prefix_str = ' '.join(prefix)

        return prefix_str
    
    def post_fix_expr(self, expression):
        operator_stack = []
        postfix = []
        tokens = expression.split()
        precedence = {'+': 2, '-': 2, '*': 1, '/': 1}

        for token in tokens:
            if token.isdigit():
                postfix.append(token)
            else:
                while operator_stack and precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0):
                    postfix.append(operator_stack.pop())
                operator_stack.append(token)
        
        postfix.extend(reversed(operator_stack))
        postfix_str = ' '.join(postfix)

        return postfix_str
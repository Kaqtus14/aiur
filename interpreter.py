from lexer import TokenType


class Env:
    def __init__(self):
        self.symbols = {}

    def define(self, key, value, check=False):
        if check:
            if not key in self.symbols:
                raise SyntaxError(f"Undefined variable: {key}")
        self.symbols[key] = value

    def get(self, key):
        try:
            return self.symbols[key]
        except IndexError:
            raise SyntaxError(f"Undefined variable: {key}")


class Interpreter:
    def __init__(self):
        self.env = Env()

    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def execute(self, stmt):
        return stmt.accept(self)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expr)

    def visit_print_stmt(self, stmt):
        print(self.evaluate(stmt.expr))

    def visit_var_stmt(self, stmt):
        value = self.evaluate(stmt.initializer) if stmt is not None else None
        self.env.define(stmt.name.lexeme, value)

    def visit_literal(self, expr):
        return expr.value

    def visit_grouping(self, expr):
        return self.evaluate(expr.expr)

    def visit_variable(self, expr):
        return self.env.get(expr.name)

    def visit_assign(self, expr):
        value = self.evaluate(expr.value)
        self.env.define(expr.name, value, True)
        return value

    def visit_unary(self, expr):
        right = self.evaluate(expr.right)

        if expr.op.typ == TokenType.MINUS:
            self.check_number(right)
            return -right
        elif expr.op.typ == TokenType.BANG:
            return not right
        else:
            assert False

    def visit_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.op.typ == TokenType.PLUS:
            return left + right
        elif expr.op.typ == TokenType.MINUS:
            self.check_number(left, right)
            return left - right
        elif expr.op.typ == TokenType.STAR:
            self.check_number(left, right)
            return left * right
        elif expr.op.typ == TokenType.SLASH:
            self.check_number(left, right)
            return left / right
        elif expr.op.typ == TokenType.EQ:
            return left == right
        elif expr.op.typ == TokenType.NEQ:
            return left != right
        elif expr.op.typ == TokenType.GT:
            self.check_number(left, right)
            return left > right
        elif expr.op.typ == TokenType.GE:
            self.check_number(left, right)
            return left >= right
        elif expr.op.typ == TokenType.LT:
            self.check_number(left, right)
            return left < right
        elif expr.op.typ == TokenType.LE:
            self.check_number(left, right)
            return left <= right
        else:
            assert False

    @staticmethod
    def check_number(*vs):
        for v in vs:
            if type(v) != int and type(v) != float:
                raise RuntimeError(f"expected number, got {type(v)}")

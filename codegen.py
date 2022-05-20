import time
from dataclasses import dataclass
from typing import Any, Callable

from lexer import TokenType


class CodeGenerator:
    def __init__(self):
        self.out = ""

    def compile(self, statements):
        self.out = "#include \"lib.h\"\n\n"
        self.out += "int main() {\n"
        for stmt in statements:
            self.compile_stmt(stmt)
        self.out += "}"

        return self.out

    def compile_stmt(self, stmt):
        return stmt.accept(self)

    def compile_expr(self, expr):
        return expr.accept(self)

    def visit_expression_stmt(self, stmt):
        self.compile_expr(stmt.expr)

    def visit_print_stmt(self, stmt):
        self.emit("std::cout << ")
        self.compile_expr(stmt.expr)
        self.emit(" << std::endl;\n")

    def visit_if_stmt(self, stmt):
        assert False, "unimplemented"

    def visit_while_stmt(self, stmt):
        assert False, "unimplemented"

    def visit_function_stmt(self, stmt):
        assert False, "unimplemented"

    def visit_return_stmt(self, stmt):
        assert False, "unimplemented"

    def visit_var_stmt(self, stmt):
        assert False, "unimplemented"

    def visit_block_stmt(self, stmt):
        assert False, "unimplemented"

    def visit_literal(self, expr):
        if isinstance(expr.value, bool):
            self.emit("true" if expr.value else "false")
        elif isinstance(expr.value, (int, float)):
            self.emit(str(expr.value))
        elif isinstance(expr.value, str):
            self.emit(f"\"{expr.value}\"")
        else:
            raise RuntimeError(f"Unexpected literal type: {type(expr.value)}")

    def visit_grouping(self, expr):
        self.emit("(")
        self.compile_expr(expr.expr)
        self.emit(")")

    def visit_variable(self, expr):
        assert False, "unimplemented"

    def visit_assign(self, expr):
        assert False, "unimplemented"

    def visit_unary(self, expr):
        self.emit(expr.op.lexeme)
        self.compile_expr(expr.right)

    def visit_logical(self, expr):
        assert False, "unimplemented"

    def visit_call(self, expr):
        assert False, "unimplemented"

    def visit_binary(self, expr):
        self.emit("(")
        self.compile_expr(expr.left)
        self.emit(expr.op.lexeme)
        self.compile_expr(expr.right)
        self.emit(")")

    def compile_stmt_block(self, statements, env):
        assert False, "unimplemented"

    def emit(self, code):
        self.out += code

    def emitln(self, code):
        self.emit(code+"\n")

    @staticmethod
    def check_number(*vs):
        for v in vs:
            if type(v) != int and type(v) != float:
                raise RuntimeError(f"expected number, got {type(v)}")

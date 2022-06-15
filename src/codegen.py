import os
import re
import ctx


class CompileError(Exception):
    pass


class CodeGenerator:
    MOD_PATH = os.path.join(os.path.dirname(__file__), "..", "stdlib")

    def __init__(self, ctx):
        self.ctx = ctx
        self.out = ""
        self.mods = os.listdir(self.MOD_PATH)
        self.symbols = set()

    def compile(self, statements):
        for mod in self.mods:
            self.symbols.update(self.get_mod_symbols(mod))
            self.out += "#include \"%s\"\n" % mod
        self.out += "\n"

        for stmt in statements:
            self.compile_stmt(stmt)

        if "main" not in self.symbols:
            ctx.error("main function isn't defined", self.ctx)

        return self.out

    def compile_stmt(self, stmt):
        return stmt.accept(self)

    def compile_expr(self, expr):
        return expr.accept(self)

    def visit_expression_stmt(self, stmt):
        self.compile_expr(stmt.expr)
        self.emitln(";")

    def visit_if_stmt(self, stmt):
        self.emit("if (")
        self.compile_expr(stmt.condition)
        self.emit(")")
        self.compile_stmt(stmt.then_branch)

        if stmt.else_branch is not None:
            self.emitln()
            self.emit("else")
            self.compile_stmt(stmt.else_branch)
        self.emitln()

    def visit_while_stmt(self, stmt):
        self.emit("while (")
        self.compile_expr(stmt.condition)
        self.emit(")")
        self.compile_expr(stmt.body)

    def visit_for_stmt(self, stmt):
        self.emit("for (auto ")
        self.emit(stmt.variable.lexeme)
        self.symbols.add(stmt.variable.lexeme)
        self.emit(" : ")
        self.compile_expr(stmt.iterator)
        self.emit(") ")
        self.compile_expr(stmt.body)

    def visit_function_stmt(self, stmt):
        self.symbols.add(stmt.name.lexeme)

        if len(stmt.params) > 0:
            self.emit(f"template <")
            self.emit(
                ", ".join([f"typename T{i}" for i in range(len(stmt.params))]))
            self.emitln(">")

        self.emit("auto " if stmt.name.lexeme != "main" else "int ")
        self.emit(stmt.name.lexeme)

        self.symbols.update(param.lexeme for param in stmt.params)
        self.emit("(")
        self.emit(",".join(f"T{i} {param.lexeme}" for i,
                           param in enumerate(stmt.params)))
        self.emit(")")

        self.emitln("{")
        for s in stmt.body.statements:
            self.compile_stmt(s)
        self.emitln("}")

    def visit_return_stmt(self, stmt):
        self.emit("return")
        if stmt.value is not None:
            self.emit(" ")
            self.compile_expr(stmt.value)
        self.emitln(";")

    def visit_var_stmt(self, stmt):
        self.symbols.add(stmt.name.lexeme)

        self.emit("auto ")
        self.emit(stmt.name.lexeme)
        if stmt.initializer is not None:
            self.emit(" = ")
            self.compile_expr(stmt.initializer)
        self.emitln(";")

    def visit_block_stmt(self, stmt):
        self.emitln("{")
        for statement in stmt.statements:
            self.compile_stmt(statement)
        self.emit("}")

    def visit_defer_stmt(self, stmt):
        self.emit("ScopeGuard guard([]()")
        self.compile_stmt(stmt.block)
        self.emitln(");")

    def visit_literal(self, expr):
        if isinstance(expr.value, bool):
            self.emit("true" if expr.value else "false")
        elif isinstance(expr.value, (int, float)):
            self.emit(str(expr.value))
        elif isinstance(expr.value, str):
            self.emit(f"std::string(\"{expr.value}\")")
        else:
            assert False, "unreachable"

    def visit_grouping(self, expr):
        self.emit("(")
        self.compile_expr(expr.expr)
        self.emit(")")

    def visit_variable(self, expr):
        if not expr.name.lexeme in self.symbols:
            ctx.error(f"undefined variable: {expr.name.lexeme}", self.ctx, expr.name.pos)
        self.emit(expr.name.lexeme)

    def visit_assign(self, expr):
        if not expr.name.lexeme in self.symbols:
            ctx.error(f"undefined variable: {expr.name.lexeme}", self.ctx, expr.name.pos)

        self.emit("(")
        self.emit(expr.name.lexeme)
        self.emit(" = ")
        self.compile_expr(expr.value)
        self.emit(")")

    def visit_unary(self, expr):
        self.emit(expr.op.lexeme)
        self.compile_expr(expr.right)

    def visit_call(self, expr):
        function = expr.callee.name.lexeme

        if not function in self.symbols:
            ctx.error(f"undefined function: {function}", self.ctx, expr.callee.name.pos)

        self.emit(function)
        self.emit("(")
        if expr.arguments:
            for arg in expr.arguments:
                self.compile_expr(arg)
                self.emit(",")
            self.out = self.out[:-1]
        self.emit(")")

    def visit_binary(self, expr):
        self.emit("(")
        self.compile_expr(expr.left)
        self.emit(expr.op.lexeme)
        self.compile_expr(expr.right)
        self.emit(")")

    def emit(self, code):
        self.out += code

    def emitln(self, code=""):
        self.emit(code+"\n")

    def get_mod_symbols(self, mod):
        symbols = set()

        with open(os.path.join(self.MOD_PATH, mod)) as f:
            matches = re.finditer(
                r"\/\/(\s+)?export ([a-zA-Z0-9:_]+)", f.read(), re.MULTILINE)

            for match in matches:
                symbols.add(match.group(2))
        return symbols

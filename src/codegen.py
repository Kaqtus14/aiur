class CompileError(Exception):
    pass


class CodeGenerator:
    def __init__(self):
        self.out = ""
        self.symbols = set(["null",
                            "string::len", "string::repeat", "string::split", "string::join",
                            "num::range", "num::sqrt",
                            "fmt::write", "fmt::print", "fmt::to_string",
                            "net::connect", "net::send_str", "net::receive"])

    def compile(self, statements):
        self.out = "#include \"lib.h\"\n\n"

        for stmt in statements:
            self.compile_stmt(stmt)

        if "main" not in self.symbols:
            raise CompileError("main function isn't defined")

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
            self.emit("\nelse")
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
        self.emit(")")
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
        self.emit("{")
        for statement in stmt.statements:
            self.compile_stmt(statement)
        self.emit("}")

    def visit_literal(self, expr):
        if isinstance(expr.value, bool):
            self.emit("true" if expr.value else "false")
        elif isinstance(expr.value, (int, float)):
            self.emit(str(expr.value))
        elif isinstance(expr.value, str):
            self.emit(f"std::string(\"{expr.value}\")")
        else:
            raise CompileError(f"Unexpected literal type: {type(expr.value)}")

    def visit_grouping(self, expr):
        self.emit("(")
        self.compile_expr(expr.expr)
        self.emit(")")

    def visit_variable(self, expr):
        if not expr.name.lexeme in self.symbols:
            raise CompileError(f"Undefined variable: {expr.name.lexeme}")
        self.emit(expr.name.lexeme)

    def visit_assign(self, expr):
        if not expr.name.lexeme in self.symbols:
            raise CompileError(f"Undefined variable: {expr.name.lexeme}")

        self.emit(expr.name.lexeme)
        self.emit(" = ")
        self.compile_expr(expr.value)
        self.emitln(";")

    def visit_unary(self, expr):
        self.emit(expr.op.lexeme)
        self.compile_expr(expr.right)

    def visit_call(self, expr):
        function = expr.callee.name.lexeme

        if not function in self.symbols:
            raise CompileError(f"Undefined function: {function}")

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

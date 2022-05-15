from dataclasses import dataclass
from typing import Any

from lexer import Token


class Expr:
    pass


@dataclass
class BinaryExpr(Expr):
    left: Expr
    op: Token
    right: Expr

    def accept(self, acceptor):
        acceptor.visit_binary(self)


@dataclass
class GroupingExpr(Expr):
    expr: Expr

    def accept(self, acceptor):
        acceptor.visit_grouping(self)


@dataclass
class LiteralExpr(Expr):
    literal: Any

    def accept(self, acceptor):
        acceptor.visit_literal(self)


@dataclass
class UnaryExpr(Expr):
    op: Token
    right: Expr

    def accept(self, acceptor):
        acceptor.visit_unary(self)
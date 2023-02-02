from dataclasses import dataclass
from typing import List

from src.lexer import Token, TokenType
from src.parser import BinOpNode, BlockNode, FunctionNode, FunctionPrototypeNode, FunctionInvocNode, LangType, \
    LiteralNode, ReturnNode, VarNode

@dataclass
class LangExample:
    plaintext: str
    tokens: List[Token]
    syntax_tree: BlockNode = None
    ir_output: str = None


simple_assignment_example = LangExample(
    plaintext="x=5 \n x+1",
    tokens=[
        Token(TokenType.IDENTIFIER, "x"),
        Token(TokenType.OPERATOR,   "="),
        Token(TokenType.LITERAL_NUM, "5"),
        Token(TokenType.IDENTIFIER, "x"),
        Token(TokenType.OPERATOR,   "+"),
        Token(TokenType.LITERAL_NUM, "1"),
    ],
    syntax_tree=BlockNode([
        BinOpNode(Token(TokenType.OPERATOR, "="),
                  VarNode("x"),
                  LiteralNode("5", LangType.INT)),
        BinOpNode(Token(TokenType.OPERATOR, "+"),
                  VarNode("x"),
                  LiteralNode("1", LangType.INT)),
    ]),
)

simple_function_def_example = LangExample(
    plaintext="def x(a: Int) -> Void { \n a+1 \n return \n }",
    tokens = [
        Token(TokenType.KEYWORD,        "def"),
        Token(TokenType.IDENTIFIER,     "x"),
        Token(TokenType.OPEN_PARENS,    "("),
        Token(TokenType.IDENTIFIER,     "a"),
        Token(TokenType.TYPE_DEF,       ":"),
        Token(TokenType.TYPE_KEYWORD,   "Int"),
        Token(TokenType.CLOSE_PARENS,    ")"),
        Token(TokenType.OPERATOR,       "->"),
        Token(TokenType.TYPE_KEYWORD,   "Void"),
        Token(TokenType.OPEN_BRACE,     "{"),
        Token(TokenType.IDENTIFIER,     "a"),
        Token(TokenType.OPERATOR,       "+"),
        Token(TokenType.LITERAL_NUM,    "1"),
        Token(TokenType.KEYWORD,        "return"),
        Token(TokenType.CLOSE_BRACE,    "}"),
    ],
    syntax_tree=BlockNode([
            FunctionNode(
                prototype=FunctionPrototypeNode(
                    name="x",
                    args=[VarNode("a", LangType.INT)],
                    return_type=LangType.VOID
                ),
                body=BlockNode([
                    BinOpNode(Token(TokenType.OPERATOR, "+"), VarNode("a"), LiteralNode("1", LangType.INT)),
                    ReturnNode()
                ])
            )
    ])
)

singleline_comment_example = LangExample(
    plaintext="x # a singleline comment",
    tokens=[
        Token(TokenType.IDENTIFIER, "x"),
    ],
    syntax_tree=BlockNode([
        VarNode("x"),
    ])
)

simple_function_invoc_example = LangExample(
    plaintext="function(a,b)",
    tokens=[
        Token(TokenType.IDENTIFIER, "function"),
        Token(TokenType.OPEN_PARENS, "("),
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.SEPARATOR, ","),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.CLOSE_PARENS, ")"),
    ],
    syntax_tree=BlockNode([
        FunctionInvocNode(
            "function",
            [VarNode("a"), VarNode("b")])
    ])
)

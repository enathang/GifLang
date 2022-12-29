import argparse

import lexer as Lexer
import parser as Parser
import semantic_analyzer as Analyzer

argparser = argparse.ArgumentParser()
argparser.add_argument("-f", "--file")
args = argparser.parse_args()

def print_line(text):
  print(f"\n============{text}===========")

program_file_name = args.file
print_line("")
print(f"Welcome to my compiler! Retrieving source code from {program_file_name}")

tokens = Lexer.lex(program_file_name)
print_line("Tokens")
print(tokens)

print_line("AST")
ast_root = Parser.parse(tokens)
print(ast_root)

print_line("Semantic analysis")
analysis = Analyzer.verify_ast(ast_root, None)

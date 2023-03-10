import argparse

import lexer as Lexer
import parser as Parser
import semantics as Analyzer
import llvm_generator as Generator

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
analysis = Analyzer.verify_ast(ast_root)

print_line("Generate LLVM IR")
llvm_context = Generator.init(__file__)
Generator.generate_ir(ast_root, llvm_context)
print(llvm_context.module.functions)
Generator.generate_object_file(llvm_context.module)


from src import llvm_generator as Generator
from tst.program_examples import *


def test_undeclared_variable():
  assert True


def test_simple_assignment():
  syntax_tree = simple_assignment_example.syntax_tree

  # Setup block
  from llvmlite import ir
  from src.llvm_generator import generate_alloca

  context = Generator.init("A")

  x_addr = generate_alloca(".2", ir.IntType(32), context)
  context.builder.store(ir.Constant(ir.IntType(32), 5), x_addr)
  x = context.builder.load(x_addr, "x")
  context.builder.fadd(x, ir.Constant(ir.IntType(32), 1))

  expected_ir = context.entry_function

  test_context = Generator.init(__file__)
  Generator.generate_ir(syntax_tree, test_context)
  ir = test_context.entry_function

  assert expected_ir == ir, f"Expected: {expected_ir}, actual: {ir}"

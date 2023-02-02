from src import llvm_generator as Generator
from tst.program_examples import *

def test_simple_assignment():
  syntax_tree = simple_assignment_example.syntax_tree

  # Setup block
  from llvmlite import ir
  from src.llvm_generator import generate_alloca

  context = Generator.init("A")

  x_addr = generate_alloca(".2", ir.IntType(32), context)
  context.builder.store(ir.Constant(ir.IntType(32), 5), x_addr)
  x = context.builder.load(x_addr, "x")
  context.builder.add(x, ir.Constant(ir.IntType(32), 1), "addtmp")

  expected_ir = context.entry_function

  test_context = Generator.init(__file__)
  Generator.generate_ir(syntax_tree, test_context)
  ir = test_context.entry_function

  assert str(expected_ir) == str(ir), f"Expected: {expected_ir}, actual: {ir}"

def test_simple_function_def():
  syntax_tree = simple_function_def_example.syntax_tree

  from llvmlite import ir
  from src.llvm_generator import generate_alloca

  context = Generator.init("A")
  void_t = ir.VoidType()
  int_t = ir.IntType(32)
  func_type = ir.FunctionType(void_t, [])
  func = ir.Function(context.module, func_type, "function_name")
  func_entry_block = func.append_basic_block("entry")
  context.builder.position_at_start(func_entry_block)
  addr = context.builder.alloca(int_t, "a")
  sum = context.builder.add(context.builder.load(addr), ir.Constant(int_t, 1))
  context.builder.ret(sum)
  expected_ir = context.module.get_global("function_name")

  test_context = Generator.init(__file__)
  Generator.generate_ir(syntax_tree, test_context)
  ir = test_context.entry_function

  assert str(expected_ir) == str(ir)


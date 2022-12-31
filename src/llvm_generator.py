from lexer import TokenType

from llvmlite import ir
from llvmlite import binding as llvm


# Define types here
int = ir.IntType(32)
void = ir.VoidType()
print_func_type = ir.FunctionType(int, [])


# Define module
module = ir.Module(name=__file__)
named_values = {}


# Define entry function here
entry_function = ir.Function(module, print_func_type, "entry_function")
entry_block = entry_function.append_basic_block('entry')
builder = ir.IRBuilder(entry_block)


def optimize(llvm_ir):
  pass_manager_builder = llvm.create_pass_manager_builder()
  pass_manager_builder.opt_level = 2
  pass_manager = llvm.create_module_pass_manager()
  pass_manager_builder.populate(pass_manager)
  
  pass_manager.run(llvm_ir) # Optimize the LLVM IR
 
'''
def verify_function(llvm_ir):
  ir.Verifier.verifyFunction()
'''

def generate_object_file(llvm_ir):
  llvm.initialize_native_target()
  llvm.initialize_native_asmprinter()
  target = llvm.Target.from_default_triple()
  target_machine = target.create_target_machine()

  print(f"Target: {target}")
  print(f"Target machine: {target_machine}")

  llvm_mod = llvm.parse_assembly(str(llvm_ir)) # Not 100% sure what's happening here
  optimize(llvm_mod)
  object = target_machine.emit_object(llvm_mod)

  # Output object code to a file.
  object_filename = '../bin/output.o'
  with open(object_filename, 'wb') as obj_file:
    obj_file.write(object)
    print('Wrote ' + object_filename)


def generate_ir(node):
  if (node.token.type == TokenType.ASSIGNMENT):
    key = node.children[0].token.value
    value = node.children[1].token.value
    
    value_ir = ir.Constant(int, value)
 
    # Allocate memory for the variable, store it, and add the pointer to the values table
    alloca = builder.alloca(int)
    builder.store(value_ir, alloca)
    named_values[key] = alloca

  if (node.token.type == TokenType.LITERAL):
    cons = ir.Constant(context, int(node.token.value))
    print(cons)
    return cons

  if (node.token.type == TokenType.SCOPE):
    for child in node.children:
      generate_ir(child)
  
    builder.ret(int(0))

  return module

def generate_ir_top_level(node):
  llvm.initialize() # Not sure what this does...
  ir_module = generate_ir(node)
  # verify_function(entry_function)
  print(ir_module)
  generate_object_file(ir_module)
  
  return ir_module


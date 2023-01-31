from src.parser import BlockNode, BinOpNode, FunctionDefNode, FunctionInvocNode, ReturnNode, \
  VarNode, LiteralNode, LangType

from llvmlite import ir
from llvmlite import binding as llvm

# Define LLVM types here
int_t = ir.IntType(32)
char_t = ir.IntType(32)
bool_t = ir.IntType(1)
void_t = ir.VoidType()

void_func_type = ir.FunctionType(void_t, [])


class Context:
  def __init__(self, module_name):
    self.module = ir.Module(module_name)
    self.entry_function = ir.Function(self.module, void_func_type, "entry_function")
    self.entry_block = self.entry_function.append_basic_block('entry')
    self.builder = ir.IRBuilder(self.entry_block)
    self.named_values = {}


def optimize(llvm_ir):
  pass_manager_builder = llvm.create_pass_manager_builder()
  pass_manager_builder.opt_level = 2
  pass_manager = llvm.create_module_pass_manager()
  pass_manager_builder.populate(pass_manager)
  
  pass_manager.run(llvm_ir) # Optimize the LLVM IR
 

def verify_function(llvm_ir):
  ir.Verifier.verifyFunction()


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
  object_filename = '/Users/nathangifford/Desktop/compiler/bin/output.o'
  with open(object_filename, 'wb') as obj_file:
    obj_file.write(object)
    print('Wrote ' + object_filename)


def generate_alloca(name, type, context):
  current_block = context.builder.block

  context.builder.position_at_start(context.builder.block.function.entry_basic_block)
  addr = context.builder.alloca(type, None, name)
  context.builder.position_at_end(current_block)

  return addr


def generate_assignment_ir(node, context):
  key = node.left.value
  value = generate_ir(node.right, context)

  # Allocate memory for the variable, store it, and add the pointer to the values table
  if (not isinstance(value, FunctionDefNode) and not isinstance(value, list)):
    addr = context.builder.alloca(int_t)
    context.builder.store(value, addr)
    context.named_values[key] = addr


def generate_binop_ir(node, context):
  if (node.op.value == "="):
    return generate_assignment_ir(node, context)

  lhs = generate_ir(node.left, context)
  rhs = generate_ir(node.right, context)
  if (node.op.value == "+"):
    return context.builder.add(lhs, rhs, "addtmp")
  elif (node.op.value == "-"):
    return context.builder.sub(lhs, rhs, "subtmp")
  elif (node.op.value == "*"):
    return context.builder.mul(lhs, rhs, "subtmp")
  else:
    raise Exception(f"Unknown binary operation {node.op.value}")


def generate_block_ir(node, context):
  statements_ir = []
  for statement in node.statements:
      statement_ir = generate_ir(statement, context)
      statements_ir.append(statement_ir)

  return statements_ir


def generate_literal_ir(node: LiteralNode):
  type_map = {
    LangType.INT: int_t,
    LangType.CHAR: char_t,
    LangType.BOOL: bool_t
  }

  return ir.Constant(type_map[node.type], node.value)

def generate_var_ir(node: VarNode, context: Context):
  var_name = node.value
  var_addr = context.named_values.get(var_name)
  if (var_addr is None):
    raise Exception(f"Undeclared variable {var_name} used")

  return context.builder.load(var_addr, var_name)


def get_type_of_value(node, context):
  # If the value is a literal, grab it directly
  if (node.val.is_literal):
    return node.type

  # Otherwise, look up the type from the declaration
  return context.named_values[node.val.value.value].type


def generate_func_prototype_ir(node, context):
  if (node.name in context.module.globals):
    raise Exception(f"Function name {node.name} already declared")

  arg_types = []
  for arg in node.args:
    var_addr = generate_alloca(arg.value.value, int_t, context)
    context.named_values[arg.value.value] = var_addr
    arg_types.append(context.named_values[arg.value.value].type)

  ret_type = None
  for statement in node.body.statements:
    if (isinstance(statement, ReturnNode)):
      new_ret_type = get_type_of_value(statement, context)

      if (ret_type is None):
        ret_type = new_ret_type
      else:
        if (ret_type != new_ret_type):
          raise Exception(f"Mismatching return types for {node.name}: {ret_type} and {new_ret_type}")

  if (ret_type is None):
    raise Exception(f"Function {node.name} missing return")

  # Save current writing position
  current_block = context.entry_block

  # Create new function + block
  func_type = ir.FunctionType(ret_type, arg_types)
  func = ir.Function(context.module, func_type, node.name)
  func_entry_block = func.append_basic_block('entry')

  # Write to new function + block
  context.builder.position_at_start(func_entry_block)
  func_body_ir = generate_ir(node.body, context)

  # Reset builder position back to previous writing position
  context.builder.position_at_end(current_block)

  return func_body_ir


def generate_return_ir(node, context):
  if (node.val is None):
    context.builder.ret_void()
  else:
    context.builder.ret(node.val.value.value)


def generate_func_invoc_ir(node, context):
  called_func = context.module.get_global(node.name)
  if (called_func is None):
    raise Exception(f"Undeclared function {node.name}")

  args = [generate_ir(arg, context) for arg in node.args]

  return context.builder.call(called_func, args)


def generate_ir(node, context):
  if (isinstance(node, BlockNode)):
    return generate_block_ir(node, context)
  elif (isinstance(node, BinOpNode)):
    return generate_binop_ir(node, context)
  elif (isinstance(node, VarNode)):
    return generate_var_ir(node, context)
  elif (isinstance(node, LiteralNode)):
    return generate_literal_ir(node)
  elif (isinstance(node, FunctionDefNode)):
    return generate_func_prototype_ir(node, context)
  elif (isinstance(node, FunctionInvocNode)):
    return generate_func_invoc_ir(node, context)
  elif (isinstance(node, ReturnNode)):
    return generate_return_ir(node, context)
  else:
    raise Exception(f"Unknown node type {node}")


def init(module_name):
  context = Context(module_name)
  llvm.initialize()  # Not sure what this does...
  return context

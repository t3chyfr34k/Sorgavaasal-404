from lexer import tokenize
from parser import parse, FunctionNode, AssignNode, ReturnNode, BinOpNode, VarNode, NumNode

def eval_node(node, context):
    if isinstance(node, FunctionNode):
        for stmt in node.body:
            result = eval_node(stmt, context)
            if isinstance(result, ReturnNode):
                return eval_node(result.value, context)
    elif isinstance(node, AssignNode):
        context[node.varname] = eval_node(node.value, context)
    elif isinstance(node, ReturnNode):
        return node
    elif isinstance(node, BinOpNode):
        left = eval_node(node.left, context)
        right = eval_node(node.right, context)
        return left + right
    elif isinstance(node, VarNode):
        return context[node.name]
    elif isinstance(node, NumNode):
        return node.value

def run_code(code):
    tokens = tokenize(code)
    ast = parse(tokens)
    context = {}
    result = eval_node(ast, context)
    print(" Result Vandhutann:", result)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <file.sv404>")
    else:
        with open(sys.argv[1], "r") as f:
            code = f.read()
        run_code(code)

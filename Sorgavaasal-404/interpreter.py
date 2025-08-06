from lexer import lex
from parser import parse, NumberNode, StringNode, VarAssignNode, VarAccessNode, ReturnNode, FunctionDefNode, FunctionCallNode

class Environment:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def execute(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, VarAssignNode):
            val = self.execute(node.value)
            self.variables[node.name] = val
        elif isinstance(node, VarAccessNode):
            return self.variables.get(node.name, None)
        elif isinstance(node, ReturnNode):
            return self.execute(node.value)
        elif isinstance(node, FunctionDefNode):
            self.functions[node.name] = node.body
        elif isinstance(node, FunctionCallNode):
            body = self.functions.get(node.name)
            if not body:
                raise Exception(f"Function {node.name} not defined")
            for stmt in body:
                val = self.execute(stmt)
                if isinstance(stmt, ReturnNode):
                    return val
        else:
            raise Exception(f"Unknown node: {node}")

def run(source):
    tokens = lex(source)
    ast = parse(tokens)
    env = Environment()
    for node in ast:
        env.execute(node)

if __name__ == "__main__":
    sample = """
    kooptaVaran vaanga:
        irukku = 10
        Vandhutann irukku
    thirumbaVaa

    vaanga
    """
    run(sample)

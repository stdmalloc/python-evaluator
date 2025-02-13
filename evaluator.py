from parser import Literal, Op_Branch

#intend on adding more here w/ newer features

def main(parsed_expr):
    if not parsed_expr:
        return ''
    elif isinstance(parsed_expr, Literal):
        return parsed_expr
    elif isinstance(parsed_expr, Op_Branch):
        return parsed_expr.run()
    else:
        raise ValueError(
            f'issue at evaluating -> expr of invalid type, {type(parsed_expr)}, passed'
        )
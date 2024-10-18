from central import get_piece_type, check_if_piece_type, mop_info

#objects
class Op_Branch:
    def __init__(self, op_id, args):
        self.op_id = op_id
        self.eval_func = mop_info[op_id]['eval_func']
        self.args = args
    def __repr__(self):
        return f'op_branch(op_id={self.op_id})(args={self.args})'
    def run(self):
        for ind, arg in enumerate(self.args):
            if isinstance(arg, Op_Branch):
                self.args[ind] = arg.run()
            elif isinstance(arg, str):
                self.args[ind] = eval(arg)
        return self.eval_func(self.args)

#main function
def main(token_chain):
    #uses shunting yard to make an ast
    output, op_stack = [], []
    for ind, token in enumerate(token_chain):
        token_type = get_piece_type(token)

        #if num
        if token_type == 'num':
            output.append(token)

        #spltting subtraction into unary and binary
        elif token == '-':
            if token_chain[ind-1] == ')' or check_if_piece_type('num', token_chain[ind-1]):
                token = '-b'
            else:
                token = '-u'
            curr_prec = mop_info[token]['prec']
            while op_stack and op_stack[-1]!='(' and mop_info[op_stack[-1]]['prec']>curr_prec:
                num_args=mop_info[op_stack[-1]]['num_args']
                args = output[-num_args:]
                output = output[:-num_args]
                output.append(Op_Branch(op_stack[-1], args))
                op_stack.pop(-1)
            op_stack.append(token)

        #handling other math operations
        elif token_type == 'mop':
            curr_prec = mop_info[token]['prec']
            while op_stack and op_stack[-1]!='(' and mop_info[op_stack[-1]]['prec']>curr_prec:
                num_args=mop_info[op_stack[-1]]['num_args']
                args = output[-num_args:]
                output = output[:-num_args]
                output.append(Op_Branch(op_stack[-1], args))
                op_stack.pop(-1)
            op_stack.append(token)
        
        #left and right parenthesis handling
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack[-1] != '(':
                num_args=mop_info[op_stack[-1]]['num_args']
                args = output[-num_args:]
                output = output[:-num_args]
                output.append(Op_Branch(op_stack[-1], args))
                op_stack.pop(-1)
            op_stack.pop(-1)

        else:
            raise ValueError(f'invalid token: debug -> {token}')

    #push remaining operators to output
    while op_stack:
        num_args=mop_info[op_stack[-1]]['num_args']
        args = output[-num_args:]
        output = output[:-num_args]
        output.append(Op_Branch(op_stack[-1], args))
        op_stack.pop(-1)

    #output
    if output[1:]:
        raise ValueError(f'args needed does not match args given: debug -> {output, op_stack}')
    else:
        return output[0]
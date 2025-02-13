from central import get_piece_type, check_if_piece_type
from central import fnc_info, nop_info

#objects
class Literal:
    def __init__(self, val):
        #only real numbers so far
        if isinstance(val, str):
            if '.' in val:
                self.val=float(val)
            else:
                self.val=int(val)
        else:
            self.val = val
    def __repr__(self):
        return f'literal(val={self.val})'
class Op_Branch:
    def __init__(self, op_id, args):
        self.op_id = op_id
        self.args = args

        if check_if_piece_type('nop', op_id):
            self.eval_func = nop_info[op_id]['eval_func']
        else: #op_id is a function
            self.eval_func = fnc_info[op_id]['eval_func']
    def __repr__(self):
        return f'op_branch(op_id={self.op_id})(args={self.args})'
    def run(self):
        for ind, arg in enumerate(self.args):
            if isinstance(arg, Op_Branch):
                self.args[ind] = arg.run()
        return Literal(self.eval_func([i.val for i in self.args]))

#main function
def main(token_list):
    #uses shunting yard to make an ast

    if not token_list:
        return ''

    output, op_stack = [], []
    token_list_len = len(token_list)

    ind=0
    while True:
        if ind == token_list_len:
            break

        token = token_list[ind]
        token_type = get_piece_type(token)

        #if number
        if token_type=='num':
            output.append(Literal(token))

        #if function
        elif token_type=='fnc':
            op_stack.append(token)

        #if numerical operator
        elif token_type=='nop':
            #correct subtraction into unary and binary
            if token=='-':
                if ind==0:
                    #if theres no character before it
                    token = '-u'
                else:
                    #if theres a character before it
                    prev_piece_type = get_piece_type(token_list[ind-1])
                    if prev_piece_type in ('cpt', 'num'):
                        token = '-b'
                    elif prev_piece_type in ('opt', 'nop'):
                        token = '-u'
                    else:
                        raise SyntaxError(
                            f'issue at parsing -> invalid "{repr(token_list[ind-1])}" at token {ind-1}'
                        )
            
            #continue normally
            while True:
                #check conditions
                if not op_stack:
                    break
                if op_stack[-1]=='(':
                    break
                tok_prec = nop_info[token]['prec']
                opr_prec = nop_info[op_stack[-1]]['prec']
                if not (opr_prec > tok_prec or (opr_prec == tok_prec and nop_info[token]['assoc']=='l')):
                    break

                #form expr using top operation in op_stack
                num_args = nop_info[op_stack[-1]]['num_args']
                output, args = output[:-num_args], output[-num_args:]
                output.append(Op_Branch(op_stack[-1], args))

                #pop operation at top of op_stack
                op_stack = op_stack[:-1]

            #move token to op_stack
            op_stack.append(token)


        #if parenthesis
        elif token_type=='opt':
            #add to op_stack
            op_stack.append(token)
        elif token_type=='cpt':
            #dump operations from op_stack until '(' found
            #and discard both parenthesis

            while op_stack[-1] != '(':
                #form expr using top operation in op_stack
                num_args = nop_info[op_stack[-1]]['num_args']
                output, args = output[:-num_args], output[-num_args:]
                output.append(Op_Branch(op_stack[-1], args))

                #pop operation at top of op_stack
                op_stack = op_stack[:-1]
            
            #pop the opening parenthesis
            op_stack = op_stack[:-1]

            #adding function if exists
            if not op_stack:
                ind+=1
                continue
            if check_if_piece_type('fnc', op_stack[-1]):
                #form expr using top function in op_stack
                num_args = fnc_info[op_stack[-1]]['num_args']
                output, args = output[:-num_args], output[-num_args:]
                output.append(Op_Branch(op_stack[-1], args))
                
                #pop operation at top of op_stack
                op_stack = op_stack[:-1]

        #if comma
        elif token_type=='com':
            while op_stack[-1] != '(':
                #form expr using top operation in op_stack
                num_args = nop_info[op_stack[-1]]['num_args']
                output, args = output[:-num_args], output[-num_args:]
                output.append(Op_Branch(op_stack[-1], args))

                #pop operation at top of op_stack
                op_stack = op_stack[:-1]
            
        #invalid token
        else:
            raise ValueError(
                f'issue at parsing -> invalid "{token_list[ind]}" at token {ind}'
            )

        #increment ind
        ind+=1
    
    #clear op_stack + form exprs in output
    while op_stack:
        #form expr using top operation in op_stack
        num_args = nop_info[op_stack[-1]]['num_args']
        output, args = output[:-num_args], output[-num_args:]
        output.append(Op_Branch(op_stack[-1], args))

        #pop operation from top of op_stack
        op_stack = op_stack[:-1]

    #check that output was properly generated
    if len(output)>1:
        raise SyntaxError(f'issue at parsing -> missing operators')

    #return
    return output[0]
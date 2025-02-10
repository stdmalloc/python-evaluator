from central import get_piece_type, nop_info

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
        self.eval_func = nop_info[op_id]['eval_func']
        self.args = args
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
                            f'issue at parsing -> invalid {repr(token_list[ind-1])} at char {ind-1}'
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
        elif token=='(':
            #add to op_stack
            op_stack.append(token)
        elif token==')':
            #dump operations from op_stack until '(' found
            # + discard both parenthesis
            while op_stack[-1] != '(':
                #form expr using top operation in op_stack
                num_args = nop_info[op_stack[-1]]['num_args']
                output, args = output[:-num_args], output[-num_args:]
                output.append(Op_Branch(op_stack[-1], args))

                #pop operation at top of op_stack
                op_stack = op_stack[:-1]
            
            #pop the opening parenthesis
            op_stack = op_stack[:-1]

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
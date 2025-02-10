from string import whitespace

#notes here are for each section
#not for the whole file

'''
used in tokenizer

defines types of pieces (potential token)
also checks for + gets piece type of an input

fragment = symbol in a multisymbol operation
could be its own symbol; combined if in pair, ignored if not
ex: << = shift left; < = fragment
'''
def checkifnum(piece:str):
    try:
        float(piece)
        return True
    except:
        return False
piece_type_info = {
    'num': checkifnum, #number (int or float)
    'frg': lambda i: i in frg_list, #fragment
    'nop': lambda i: i in nop_list, #numerical operation
    'opt': lambda i: i == '(', #opening parenthesis
    'cpt': lambda i: i==')', #closing parenthesis
    'wsp': lambda i: i in whitespace, #whitespace
    'prd': lambda i: i == '.', #period
}
def get_piece_type(piece):
    for id, check_func in piece_type_info.items():
        if check_func(piece):
            return id
    return 'def' #default
def check_if_piece_type(target_type, piece):
    return piece_type_info[target_type](piece)

'''
used in parser

defines how to handle math operations

nop_list defines which symbols are used in the expression notation
nop_info defines the behaviors of the symbols
    note the minus sign split into -u and -b since it denotes two separate operations

high prec evaluates before lower prec

associativity defines what order operations of the same precedent evaluate in
'l' = left associative; 'r' = right associative
'''
frg_list = [
    #arithmetic
    '/',
    '*',
    #bitwise
    '<',
    '>',
]
nop_list = [
    #arithmetic
    '+',
    '-',
    '*',
    '/',
    '//',
    '**',
    '%',
    #bitwise
    '~',
    '|',
    '^',
    '&',
    '<<',
    '>>',
]
nop_info = {
    #arithmetic
    '+': {'prec':3, 'num_args':2, 'eval_func':lambda args:args[0]+args[1], 'assoc':'l'},
    '-u': {'prec':6, 'num_args':1, 'eval_func':lambda args:-args[0], 'assoc':'r'},
    '-b': {'prec':3, 'num_args':2, 'eval_func':lambda args:args[0]-args[1], 'assoc':'l'},
    '*': {'prec':4, 'num_args':2, 'eval_func':lambda args:args[0]*args[1], 'assoc':'l'},
    '/': {'prec':4, 'num_args':2, 'eval_func':lambda args:args[0]/args[1], 'assoc':'l'},
    '//': {'prec':4, 'num_args':2, 'eval_func':lambda args:args[0]//args[1], 'assoc':'l'},
    '**': {'prec':5, 'num_args':2, 'eval_func':lambda args:args[0]**args[1], 'assoc':'r'},
    '%': {'prec':4, 'num_args':2, 'eval_func':lambda args:args[0]%args[1], 'assoc':'l'},
    #bitwise
    '~': {'prec':1, 'num_args':1, 'eval_func':lambda args:~args[0], 'assoc':'r'},
    '|': {'prec':1, 'num_args':2, 'eval_func':lambda args:args[0]|args[1], 'assoc':'l'},
    '^': {'prec':1, 'num_args':2, 'eval_func':lambda args:args[0]^args[1], 'assoc':'l'},
    '&': {'prec':1, 'num_args':2, 'eval_func':lambda args:args[0]&args[1], 'assoc':'l'},
    '<<': {'prec':2, 'num_args':2, 'eval_func':lambda args:args[0]<<args[1], 'assoc':'l'},
    '>>': {'prec':2, 'num_args':2, 'eval_func':lambda args:args[0]>>args[1], 'assoc':'l'},
}
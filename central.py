from string import whitespace

'''
used in tokenizer

defines types of pieces (potential token)
also checks for + gets piece type of an input
'''
def checkifnum(piece):
    try:
        float(piece)
        return True
    except:
        return False
piece_type_info = {
    'num': checkifnum, #number (int or float)
    'mop': lambda i: i in mop_info.keys(), #math operation
    'pts': lambda i: i in ('(', ')'), #parentheses
    'wsp': lambda i: i in tuple(whitespace), #whitespace
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
'''
mop_info = {
    '+': {'prec': 2, 'num_args':2, 'eval_func': lambda args:args[0]+args[1]},
    '-u': {'prec': 3, 'num_args':1, 'eval_func': lambda args:-args[0]},
    '-b': {'prec': 2, 'num_args':2, 'eval_func': lambda args:args[0]+args[1]},
    '*': {'prec': 3, 'num_args':2, 'eval_func': lambda args:args[0]+args[1]},
    '/': {'prec': 3, 'num_args':2, 'eval_func': lambda args:args[0]+args[1]},
    '//': {'prec': 3, 'num_args':2, 'eval_func': lambda args:args[0]+args[1]},
    '**': {'prec': 4, 'num_args':2, 'eval_func': lambda args:args[0]+args[1]},
    '%': {'prec': 1, 'num_args':2, 'eval_func': lambda args:args[0]+args[1]},
}
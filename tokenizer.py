from central import get_piece_type, check_if_piece_type

#main function
def main(input_expr):
    
    output, cache = [], ''
    for ind, char in enumerate(input_expr):

        char_type = get_piece_type(char)

        #add cache to output as normal
        if char_type in ('nop', 'opt', 'cpt'):
            if cache:
                output.append(cache)
                cache = ''
            output.append(char)
        elif char_type == 'wsp':
            #special case for wsp
            if cache:
                output.append(cache)
                cache = ''
            #no append bc wsp ignored

        #putting together multisymbol operations
        elif char_type == 'frg':
            if cache:
                output.append(cache)
                cache = ''
            if output[-1]==char:
                output[-1]*=2
            else:
                output.append(char)

        #putting together floats
        elif char_type == 'prd':
            len_input = len(input_expr)
            if ind==0: #first char
                if not check_if_piece_type('num', input_expr[1]):
                    raise SyntaxError(
                        'issue at tokenizing -> invalid . at char 0'
                    )
                cache+='.'
            elif ind==len_input-1: #last char
                if not check_if_piece_type('num', input_expr[len_input-1]):
                    raise SyntaxError(
                        f'issue at tokenizing -> invalid . at char {len_input-1}'
                    )
                cache+='.'
            else: #any char in b/w
                if not check_if_piece_type('num', input_expr[ind-1]) and not check_if_piece_type('num', input_expr[ind+1]):
                    raise SyntaxError(
                        f'issue at tokenizing -> invalid . at char {ind}'
                    )
                else:
                    cache+='.'

        #otherwise char added to cache
        else:
            cache += char
    
    if cache:
        output.append(cache)

    #return
    return output
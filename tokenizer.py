from central import get_piece_type, check_if_piece_type

#main function
def main(input_expr):
    #handles groupings of one piece type
    output, cache = [], ''
    for char in input_expr:
        char_type = get_piece_type(char)
        if char_type in ('nop', 'frg', 'opt', 'cpt', 'prd'):
            if cache:
                output.append(cache)
                cache = ''
            output.append(char)
        elif char_type == 'wsp':
            if cache:
                output.append(cache)
                cache = ''
        else:
            cache += char
    if cache:
        output.append(cache)

    #handles groupings of multiple piece types
    #ind and while used so that ind can be shifted around as needed
    ind=0
    while True:
        if ind == len(output):
            break

        #puts together floats
        elif check_if_piece_type('prd', output[ind]):
            if ind==0:
                if check_if_piece_type('num', output[ind+1]):
                    output[ind] += output[ind+1]
                    output.pop(ind+1)
                else:
                    raise ValueError('issue at tokenizing -> invalid . at char #0')
            elif ind==len(output)-1:
                if check_if_piece_type('num', output[ind-1]):
                    output[ind-1] += '.'
                    output.pop(ind)
                else:
                    raise ValueError(f'issue at tokenizing -> invalid . at char #{ind}')
            else:
                num_bf_is_num = check_if_piece_type('num', output[ind-1])
                num_aft_is_num = check_if_piece_type('num', output[ind+1])
                if num_bf_is_num and num_aft_is_num:
                    output[ind-1] += '.' + output[ind+1]
                    output.pop(ind)
                    output.pop(ind) #since first pop shifts elements after leftwards one
                    ind -=2
                elif num_bf_is_num and not num_aft_is_num:
                    if check_if_piece_type('num', output[ind-1]):
                        output[ind-1] += '.'
                        output.pop(ind)
                elif not num_bf_is_num and num_aft_is_num:
                    if check_if_piece_type('num', output[ind+1]):
                        output[ind] += output[ind+1]
                        output.pop(ind+1)
                else:
                    raise ValueError(f'issue at tokenizing -> invalid . at char #{ind}')

        #puts together multisymbol operations
        elif output[ind] in ('/', '*', '<', '>'):
            if output[ind+1] == output[ind]:
                #since the only multisymbol operations are //, **, <<, and >>
                #-> which are two of the same symbol
                output[ind] *= 2
                output.pop(ind+1)

        #increment ind
        ind+=1

    #return
    return output
import shlex

def parse_args(str_args, mapping={'FUZZED_FILE': '%(input)s'}):
    '''
    Decompose args string, replace keywords with
    python string formatting tokens and recompose back
    to string.
    '''
    split = map(lambda x: x.strip(), shlex.split(str_args))
    new = []
    for i in split:
        if i in mapping:
            new.append(mapping[i])
            del mapping[i]
        else:
            new.append(i)

    return ' '.join(new)


